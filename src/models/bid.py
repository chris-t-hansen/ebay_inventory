"""
SQLAlchemy Model for Auction Bid Tracking.
"""

from sqlalchemy import Column, String, Numeric, DateTime, TIMESTAMP, func
from src.models.base import Base


class AuctionBid(Base):
    """Represents a physical bid made by a buyer on an auction-style listing."""

    __tablename__ = "auction_bids"

    bid_id = Column(String(50), primary_key=True, nullable=False)
    ebay_listing_id = Column(String(50), nullable=False)
    bidder_username = Column(String(100), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    bid_time = Column(DateTime, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    def __repr__(self) -> str:
        return f"<AuctionBid(bid_id='{self.bid_id}', listing='{self.ebay_listing_id}', bidder='{self.bidder_username}', amount={self.amount})>"
