import uuid as py_uuid
from datetime import datetime
from typing import Any, Optional

from sqlalchemy import Boolean, DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column


class BaseModelMixin:
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    delete_protection: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text('CURRENT_TIMESTAMP'),
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text('CURRENT_TIMESTAMP'),
        onupdate=text('CURRENT_TIMESTAMP'),
        index=True,
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

    def to_dict_with_relations(self) -> dict[str, Any]:
        result = self.to_dict()

        for rel in self.__mapper__.relationships:
            # only include relations that are already loaded (async-safe)
            if rel.key in self.__dict__:
                value = getattr(self, rel.key)

                if value is None:
                    result[rel.key] = None
                elif isinstance(value, list):
                    result[rel.key] = [
                        (
                            item.to_dict_with_relations()
                            if hasattr(item, 'to_dict_with_relations')
                            else (
                                item.to_dict()
                                if hasattr(item, 'to_dict')
                                else str(item)
                            )
                        )
                        for item in value
                    ]
                else:
                    result[rel.key] = (
                        value.to_dict_with_relations()
                        if hasattr(value, 'to_dict_with_relations')
                        else (
                            value.to_dict() if hasattr(value, 'to_dict') else str(value)
                        )
                    )

        return result


class SlugBaseModelMixin(BaseModelMixin):
    slug: Mapped[str] = mapped_column(
        String(255), index=True, unique=True, nullable=False
    )


class BaseIDModelMixin(BaseModelMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class BaseIDSlugModelMixin(BaseIDModelMixin, SlugBaseModelMixin):
    pass


class BaseUUIDModelMixin(BaseModelMixin):
    uuid: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(py_uuid.uuid4()),
        nullable=False,
    )


class BaseUUIDSlugModelMixin(BaseUUIDModelMixin, SlugBaseModelMixin):
    pass


class SoftDeleteMixin:
    soft_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    soft_deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
