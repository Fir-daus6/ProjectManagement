import enum

from sqlalchemy import Enum as SAEnum


class UserRole(str, enum.Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    MEMBER = 'member'


class TaskStatus(str, enum.Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    REVIEW = 'review'
    DONE = 'done'


class TaskPriority(str, enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    URGENT = 'urgent'


class ProjectStatus(str, enum.Enum):
    PLANNING = 'planning'
    ACTIVE = 'active'
    ON_HOLD = 'on_hold'
    COMPLETED = 'completed'


def enum_column(enum_cls: type[enum.Enum], length: int = 20) -> SAEnum:
    """Store an enum as a VARCHAR holding its values, not a native MySQL ENUM."""
    return SAEnum(
        enum_cls,
        native_enum=False,
        length=length,
        values_callable=lambda e: [member.value for member in e],
        validate_strings=True,
    )
