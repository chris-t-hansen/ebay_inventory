"""
SQLAlchemy Models for Inventory Items and Pictures.
"""

from sqlalchemy import Column, String, Integer, Numeric, DateTime, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from src.models.base import Base


class InventoryItem(Base):
    """Represents a physical inventory item and its eBay listing state."""
    
    __tablename__ = "inventory_items"

    sku = Column(String(50), primary_key=True, nullable=False)
    title = Column(String(80), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=1)
    weight_lbs = Column(Numeric(5, 2), nullable=True)
    carrier = Column(String(50), nullable=True)
    shipping_service = Column(String(100), nullable=True)
    scheduled_at = Column(DateTime, nullable=True)            # Planned publication date/time
    ebay_listing_id = Column(String(50), nullable=True)        # eBay Item ID (populated after publishing)
    status = Column(String(20), default="draft")              # draft, scheduled, active, sold, ended
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    pictures = relationship("ItemPicture", back_populates="item", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="item")

    def __repr__(self) -> str:
        return f"<InventoryItem(sku='{self.sku}', title='{self.title}', status='{self.status}', price={self.price})>"


class ItemPicture(Base):
    """Represents a photo or image asset associated with a specific SKU."""
    
    __tablename__ = "item_pictures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String(50), ForeignKey("inventory_items.sku", ondelete="CASCADE"), nullable=False)
    picture_url = Column(String(2048), nullable=False)
    display_order = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    item = relationship("InventoryItem", back_populates="pictures")

    def __repr__(self) -> str:
        return f"<ItemPicture(id={self.id}, sku='{self.sku}', order={self.display_order})>"
