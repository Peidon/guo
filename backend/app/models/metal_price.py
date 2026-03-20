from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class MetalPrice(Base):
    __tablename__ = "metal_prices"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Core Metadata
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    metal: Mapped[str] = mapped_column(String(10))
    currency: Mapped[str] = mapped_column(String(10))
    exchange: Mapped[str] = mapped_column(String(50))
    symbol: Mapped[str] = mapped_column(String(50))

    # Price Data (using Numeric for financial precision)
    prev_close_price: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    open_price: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    low_price: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    high_price: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    open_time: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    price: Mapped[Decimal] = mapped_column(Numeric(15, 4))

    # Change Data
    ch: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    chp: Mapped[Decimal] = mapped_column(Numeric(10, 4))

    # Market Depth
    ask: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    bid: Mapped[Decimal] = mapped_column(Numeric(15, 4))

    # Gram Breakdown
    price_gram_24k: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    price_gram_22k: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    price_gram_21k: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    price_gram_20k: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    price_gram_18k: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    price_gram_16k: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    price_gram_14k: Mapped[Decimal] = mapped_column(Numeric(15, 4))
    price_gram_10k: Mapped[Decimal] = mapped_column(Numeric(15, 4))