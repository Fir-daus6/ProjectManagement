from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database.base_class import Base
from .base_mixins import BaseIDModelMixin

if TYPE_CHECKING:
    from .project import Project
    from .user import User


class Team(BaseIDModelMixin, Base):
    __tablename__ = 'teams'

    name: Mapped[str] = mapped_column(String(120), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey('users.id'))

    # relationships
    members: Mapped[list['TeamMember']] = relationship(
        back_populates='team', cascade='all, delete-orphan'
    )
    projects: Mapped[list['Project']] = relationship(back_populates='team')


class TeamMember(Base):
    __tablename__ = 'team_members'
    __table_args__ = (UniqueConstraint('team_id', 'user_id'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    team_id: Mapped[int] = mapped_column(
        ForeignKey('teams.id', ondelete='CASCADE'), index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), index=True
    )
    role_in_team: Mapped[str] = mapped_column(String(50), default='member')
    joined_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # relationships
    team: Mapped['Team'] = relationship(back_populates='members')
    user: Mapped['User'] = relationship(back_populates='team_memberships')
