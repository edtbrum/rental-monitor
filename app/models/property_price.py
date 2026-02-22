from app.extensions import db
from sqlalchemy import CheckConstraint
from datetime import datetime, timezone

class PropertyPrice(db.Model):
    __tablename__ = "property_prices"

    __table_args__ = (
        db.Index(
            "idx_property_price_property_created",
            "property_id",
            "created_at"
        ),
        CheckConstraint("price > 0", name="check_price_positive"),
    )

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False,
        index=True
    )
    price = db.Column(db.Numeric(10,2), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )

    def __repr__(self):
        return f"<PropertyPrice {self.id}>"