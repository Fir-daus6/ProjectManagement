from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base_class import Base
from .base_mixins import BaseIDModelMixin
from .enums import TaskPriority, TaskStatus, enum_column

if TYPE_CHECKING:
    from .comment import Comment
    from .project import Project
    from .user import User


class Task(BaseIDModelMixin, Base):
    __tablename__ = 'tasks'

    project_id: Mapped[int] = mapped_column(
        ForeignKey('projects.id', ondelete='CASCADE'), index=True
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    assignee_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'), index=True
    )
    created_by: Mapped[int] = mapped_column(ForeignKey('users.id'))
    priority: Mapped[TaskPriority] = mapped_column(
        enum_column(TaskPriority), default=TaskPriority.MEDIUM
    )
    status: Mapped[TaskStatus] = mapped_column(
        enum_column(TaskStatus), default=TaskStatus.TODO, index=True
    )
    due_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, index=True)

    # relationships (two FKs point at users, so foreign_keys is required)
    project: Mapped['Project'] = relationship(back_populates='tasks')
    assignee: Mapped[Optional['User']] = relationship(
        back_populates='assigned_tasks', foreign_keys=[assignee_id]
    )
    creator: Mapped['User'] = relationship(foreign_keys=[created_by])
    comments: Mapped[list['Comment']] = relationship(
        back_populates='task',
        cascade='all, delete-orphan',
        passive_deletes=True,
    )


class TaskDependency(Base):
    __tablename__ = 'task_dependencies'

    task_id: Mapped[int] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE'), primary_key=True
    )
    depends_on_task_id: Mapped[int] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE'), primary_key=True
    )
