from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base_class import Base
from .base_mixins import BaseIDModelMixin
from .enums import ProjectStatus, enum_column

if TYPE_CHECKING:
    from .task import Task
    from .team import Team
    from .user import User


class Project(BaseIDModelMixin, Base):
    __tablename__ = 'projects'

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    team_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('teams.id', ondelete='SET NULL'), index=True
    )
    status: Mapped[ProjectStatus] = mapped_column(
        enum_column(ProjectStatus), default=ProjectStatus.PLANNING
    )
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    deadline: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # relationships
    owner: Mapped['User'] = relationship(foreign_keys=[owner_id])
    team: Mapped[Optional['Team']] = relationship(back_populates='projects')
    tasks: Mapped[list['Task']] = relationship(
        back_populates='project', cascade='all, delete-orphan'
    )
