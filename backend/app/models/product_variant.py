from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
    true,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.company import Company
    from app.models.product import Product


class ProductVariant(Base):
    __tablename__ = "product_variants"
    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "sku",
            name="uq_product_variants_company_sku",
        ),
        UniqueConstraint(
            "product_id",
            "color",
            "size",
            name="uq_product_variants_product_color_size",
        ),
        CheckConstraint(
            "cost_price >= 0",
            name="ck_product_variants_cost_price",
        ),
        CheckConstraint(
            "sale_price >= 0",
            name="ck_product_variants_sale_price",
        ),
        CheckConstraint(
            "minimum_stock >= 0",
            name="ck_product_variants_minimum_stock",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    color: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    size: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    cost_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    sale_price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    minimum_stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=true(),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    company: Mapped["Company"] = relationship(
        back_populates="product_variants",
    )

    product: Mapped["Product"] = relationship(
        back_populates="variants",
    )