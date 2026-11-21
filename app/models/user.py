from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base_class import Base
from .base_mixins import BaseIDModelMixin
from .enums import UserRole, enum_column

if TYPE_CHECKING:
    from .activity_log import ActivityLog
    from .comment import Comment
    from .notifications import Notification
    from .task import Task
    from .team import TeamMember


class User(BaseIDModelMixin, Base):
    __tablename__ = 'users'

    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        enum_column(UserRole), default=UserRole.MEMBER
    )

    # relationships
    team_memberships: Mapped[list['TeamMember']] = relationship(back_populates='user')
    assigned_tasks: Mapped[list['Task']] = relationship(
        back_populates='assignee', foreign_keys='Task.assignee_id'
    )
    comments: Mapped[list['Comment']] = relationship(back_populates='author')
    notifications: Mapped[list['Notification']] = relationship(back_populates='user')
    activity_logs: Mapped[list['ActivityLog']] = relationship(back_populates='user')
