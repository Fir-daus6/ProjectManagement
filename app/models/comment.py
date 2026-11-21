from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base_class import Base
from .base_mixins import BaseIDModelMixin

if TYPE_CHECKING:
    from .task import Task
    from .user import User


class Comment(BaseIDModelMixin, Base):
    __tablename__ = 'comments'

    task_id: Mapped[int] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE'), index=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # relationships
    task: Mapped['Task'] = relationship(back_populates='comments')
    author: Mapped['User'] = relationship(back_populates='comments')
