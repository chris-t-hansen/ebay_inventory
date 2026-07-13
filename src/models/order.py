"""
SQLAlchemy Model for Orders, Transactions, and Shipments.
"""

from sqlalchemy import Column, String, Numeric, DateTime, ForeignKey, TIMESTAMP, func, Boolean
from sqlalchemy.orm import relationship
from src.models.base import Base


class Order(Base):
    """Represents an eBay order, shipping status, tracking information, and buyer feedback state."""

    __tablename__ = "orders"

    order_id = Column(String(50), primary_key=True, nullable=False)
    sku = Column(String(50), ForeignKey("inventory_items.sku", ondelete="RESTRICT"), nullable=False)
    buyer_username = Column(String(100), nullable=True)
    sale_price = Column(Numeric(10, 2), nullable=False)
    shipping_cost = Column(Numeric(10, 2), default=0.00)
    carrier = Column(String(50), nullable=True)
    tracking_number = Column(String(100), nullable=True)
    shipping_status = Column(String(30), default="pending")            # pending, shipped, delivered, cancelled
    feedback_left = Column(Boolean, default=False)
    feedback_received = Column(Boolean, default=False)
    sold_at = Column(DateTime, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    item = relationship("InventoryItem", back_populates="orders")

    def __repr__(self) -> str:
        return f"<Order(id='{self.order_id}', sku='{self.sku}', status='{self.shipping_status}', sold_at={self.sold_at})>"
