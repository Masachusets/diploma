from typing import List

from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Category
from src.ordering_goods.schemas import CategoryCreate


async def create_category(session: AsyncSession, category: CategoryCreate):
    stmt = insert(Category).values(**category.dict())
    await session.execute(stmt)
    await session.commit()

    return {"status": f"Category {category.name} created"}


async def create_categories_from_list(session: AsyncSession,
                                      categories: List[CategoryCreate],
                                      ):
    # user):
    category_list = []
    for category in categories:
        stmt = insert(Category).values(**category)
        await session.execute(stmt)
        try:
            await session.commit()
        except IntegrityError:
            continue
    for category in categories:
        query = select(Category).where(Category.id == category["id"])
        result = await session.execute(query)
        category_list.append(result.unique().scalar_one())
    return category_list
