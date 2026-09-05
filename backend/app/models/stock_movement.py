from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

if TYPE_CHECKING:
    pass


class StockMovement(Base):
    __tablename__ = "stock_movements"

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_stock_movements_quantity_positive",
        ),
        CheckConstraint(
            "movement_type IN ('ENTRY', 'EXIT')",
            name="ck_stock_movements_type",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    product_variant_id: Mapped[int] = mapped_column(
        ForeignKey("product_variants.id"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    movement_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )