"""
Unit Tests for SQLAlchemy Models and Relational Integrity.
Verifies table mapping, cascade deletes, and constraints using SQLite in-memory database.
"""

from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.orm import Session
from src.models.item import InventoryItem, ItemPicture
from src.models.order import Order
from src.models.bid import AuctionBid


def test_inventory_item_creation(db_session: Session):
    """Verifies that an InventoryItem can be successfully created, saved, and queried."""
    item = InventoryItem(
        sku="TEST-SKU-1",
        title="Test Item Title",
        description="A great item for testing purposes.",
        price=Decimal("19.99"),
        quantity=5,
        weight_lbs=Decimal("1.25"),
        carrier="USPS",
        shipping_service="First Class",
        status="draft",
    )
    db_session.add(item)
    db_session.commit()

    # Query item back from database
    fetched = db_session.query(InventoryItem).filter_by(sku="TEST-SKU-1").first()
    assert fetched is not None
    assert fetched.title == "Test Item Title"
    assert fetched.price == Decimal("19.99")
    assert fetched.quantity == 5


def test_item_pictures_cascade_delete(db_session: Session):
    """Verifies that deleting an InventoryItem cascade-deletes all associated pictures."""
    item = InventoryItem(
        sku="TEST-SKU-2",
        title="Test Cascade Item",
        price=Decimal("9.99"),
    )
    pic = ItemPicture(sku="TEST-SKU-2", picture_url="http://example.com/pic.jpg", display_order=1)
    item.pictures.append(pic)

    db_session.add(item)
    db_session.commit()

    # Confirm record creation
    assert len(item.pictures) == 1
    pic_id = pic.id

    # Delete the primary item
    db_session.delete(item)
    db_session.commit()

    # Query for the picture; should be cascade deleted
    fetched_pic = db_session.query(ItemPicture).filter_by(id=pic_id).first()
    assert fetched_pic is None


def test_order_creation_and_relationship(db_session: Session):
    """Verifies that an Order can reference an InventoryItem SKU and traverse the relationship."""
    item = InventoryItem(
        sku="TEST-SKU-3",
        title="Test Order Item SKU",
        price=Decimal("150.00"),
    )
    db_session.add(item)
    db_session.commit()

    order = Order(
        order_id="EBAY-ORDER-1",
        sku="TEST-SKU-3",
        buyer_username="buyer_joe",
        sale_price=Decimal("145.00"),
        shipping_cost=Decimal("5.00"),
        carrier="UPS",
        tracking_number="1Z999AA10123456784",
        shipping_status="shipped",
        sold_at=datetime.now(timezone.utc),
    )
    db_session.add(order)
    db_session.commit()

    # Fetch and check order
    fetched_order = db_session.query(Order).filter_by(order_id="EBAY-ORDER-1").first()
    assert fetched_order is not None
    assert fetched_order.item.title == "Test Order Item SKU"
    assert fetched_order.buyer_username == "buyer_joe"


def test_bid_creation(db_session: Session):
    """Verifies that an AuctionBid is correctly mapped and saved."""
    bid = AuctionBid(
        bid_id="EBAY-BID-1",
        ebay_listing_id="LIST-12345",
        bidder_username="bidder_bob",
        amount=Decimal("10.50"),
        bid_time=datetime.now(timezone.utc),
    )
    db_session.add(bid)
    db_session.commit()

    fetched_bid = db_session.query(AuctionBid).filter_by(bid_id="EBAY-BID-1").first()
    assert fetched_bid is not None
    assert fetched_bid.amount == Decimal("10.50")
    assert fetched_bid.bidder_username == "bidder_bob"
