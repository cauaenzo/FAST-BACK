from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_username(self, username: str) -> User | None:
        result = await self._session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def find_by_id(self, user_id: int) -> User | None:
        result = await self._session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def find_all(self) -> list[User]:
        result = await self._session.execute(select(User).order_by(User.id))
        return list(result.scalars().all())

    async def save(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def delete(self, user_id: int) -> bool:
        result = await self._session.execute(delete(User).where(User.id == user_id))
        await self._session.commit()
        return result.rowcount > 0
