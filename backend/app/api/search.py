from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, desc, func
from typing import List, Optional
from rapidfuzz import fuzz

from app.database.base import get_db
from app.models import Product, SearchLog
from app.schemas import ProductResponse
from app.config import get_settings

router = APIRouter(prefix="/api", tags=["search"])
settings = get_settings()


@router.get("/search", response_model=List[ProductResponse])
async def search_products(
    q: str = Query(..., min_length=2, description="Search query"),
    category: Optional[str] = Query(None),
    color: Optional[str] = Query(None),
    material: Optional[str] = Query(None),
    style: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    state: Optional[str] = Query(None),
    limit: int = Query(20, le=100),
    db: AsyncSession = Depends(get_db)
):
    """Search products with filters"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        # Build base query
        filters = [
            Product.is_active == True,
            Product.state == state_filter
        ]
        
        # Text search filters
        search_filters = []
        search_term = f"%{q}%"
        
        search_filters.append(Product.name.ilike(search_term))
        search_filters.append(Product.description.ilike(search_term))
        search_filters.append(Product.brand.ilike(search_term))
        search_filters.append(Product.category.ilike(search_term))
        
        filters.append(or_(*search_filters))
        
        # Apply additional filters
        if category:
            filters.append(Product.category == category)
        
        if color:
            filters.append(Product.color.ilike(f"%{color}%"))
        
        if material:
            filters.append(Product.material.ilike(f"%{material}%"))
        
        if style:
            filters.append(Product.style.ilike(f"%{style}%"))
        
        if min_price is not None:
            filters.append(Product.price >= min_price)
        
        if max_price is not None:
            filters.append(Product.price <= max_price)
        
        # Execute query
        query = select(Product).where(and_(*filters)).order_by(
            desc(Product.trend_score),
            desc(Product.popularity_score)
        ).limit(limit)
        
        result = await db.execute(query)
        products = result.scalars().all()
        
        # Log search
        await _log_search(db, q, category, state_filter, len(products))
        
        return [ProductResponse.model_validate(p) for p in products]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


@router.get("/search/autocomplete")
async def autocomplete(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, le=20),
    db: AsyncSession = Depends(get_db)
):
    """Autocomplete suggestions"""
    try:
        # Get product name suggestions
        query = select(Product.name).where(
            Product.is_active == True,
            Product.name.ilike(f"%{q}%")
        ).distinct().limit(limit)
        
        result = await db.execute(query)
        product_names = result.scalars().all()
        
        # Get category suggestions
        category_query = select(Product.category).where(
            Product.is_active == True,
            Product.category.ilike(f"%{q}%")
        ).distinct().limit(5)
        
        category_result = await db.execute(category_query)
        categories = category_result.scalars().all()
        
        suggestions = []
        
        # Add product names
        for name in product_names:
            suggestions.append({
                'text': name,
                'type': 'product',
                'category': None
            })
        
        # Add categories
        for cat in categories:
            suggestions.append({
                'text': cat,
                'type': 'category',
                'category': cat
            })
        
        return {
            'query': q,
            'suggestions': suggestions[:limit]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Autocomplete error: {str(e)}")


@router.get("/search/filters")
async def get_search_filters(
    state: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get available filter options"""
    try:
        state_filter = state or settings.DEFAULT_STATE
        
        # Get categories
        category_query = select(Product.category, func.count(Product.id).label('count')).where(
            Product.is_active == True,
            Product.state == state_filter,
            Product.category.isnot(None)
        ).group_by(Product.category).order_by(desc('count'))
        
        category_result = await db.execute(category_query)
        categories = [{'value': row.category, 'count': row.count} for row in category_result.all()]
        
        # Get colors
        color_query = select(Product.color, func.count(Product.id).label('count')).where(
            Product.is_active == True,
            Product.state == state_filter,
            Product.color.isnot(None)
        ).group_by(Product.color).order_by(desc('count')).limit(20)
        
        color_result = await db.execute(color_query)
        colors = [{'value': row.color, 'count': row.count} for row in color_result.all()]
        
        # Get materials
        material_query = select(Product.material, func.count(Product.id).label('count')).where(
            Product.is_active == True,
            Product.state == state_filter,
            Product.material.isnot(None)
        ).group_by(Product.material).order_by(desc('count')).limit(20)
        
        material_result = await db.execute(material_query)
        materials = [{'value': row.material, 'count': row.count} for row in material_result.all()]
        
        # Get styles
        style_query = select(Product.style, func.count(Product.id).label('count')).where(
            Product.is_active == True,
            Product.state == state_filter,
            Product.style.isnot(None)
        ).group_by(Product.style).order_by(desc('count')).limit(20)
        
        style_result = await db.execute(style_query)
        styles = [{'value': row.style, 'count': row.count} for row in style_result.all()]
        
        # Get price range
        price_query = select(
            func.min(Product.price).label('min_price'),
            func.max(Product.price).label('max_price')
        ).where(
            Product.is_active == True,
            Product.state == state_filter,
            Product.price.isnot(None)
        )
        
        price_result = await db.execute(price_query)
        price_row = price_result.one()
        
        return {
            'categories': categories,
            'colors': colors,
            'materials': materials,
            'styles': styles,
            'price_range': {
                'min': float(price_row.min_price) if price_row.min_price else 0,
                'max': float(price_row.max_price) if price_row.max_price else 10000
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching filters: {str(e)}")


async def _log_search(
    db: AsyncSession,
    query: str,
    category: Optional[str],
    state: str,
    results_count: int
):
    """Log search query for analytics"""
    try:
        search_log = SearchLog(
            query=query,
            category=category,
            state=state,
            results_count=results_count,
            filters={'category': category} if category else {}
        )
        db.add(search_log)
        await db.commit()
    except Exception as e:
        # Don't fail the request if logging fails
        pass
