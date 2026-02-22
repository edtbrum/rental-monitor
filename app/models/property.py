from app.extensions import db
from datetime import datetime, timezone
from .monitor import PropertyType

class Property(db.Model):
    __tablename__ = "properties"

    __table_args__ = (
        db.Index(
            "idx_property_location_type",
            "state",
            "city",
            "neighborhood",
            "property_type"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255), nullable=False, index=True)
    url = db.Column(db.String(1024), nullable=False, unique=True)
    title = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    neighborhood = db.Column(db.String(255), nullable=False)
    property_type = db.Column(
        db.Enum(PropertyType, name="property_type_enum"), 
        nullable=False
    )
    bedrooms = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Integer, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )

    property_prices = db.relationship(
        "PropertyPrice", 
        backref="property", 
        lazy="selectin", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Property {self.id}>"