from app.extensions import db
from sqlalchemy import CheckConstraint
import enum

class PropertyType(enum.Enum):
    APARTMENT = "apartment"
    HOUSE = "house"
    STUDIO = "studio"

class Monitor(db.Model):
    __tablename__ = "monitors"

    __table_args__ = (
        db.Index(
            "idx_monitor_location_type",
            "state",
            "city",
            "neighborhood",
            "property_type"
        ),
        CheckConstraint("max_price > 0", name="check_max_price_positive"),
        CheckConstraint("min_bedrooms >= 0", name="check_min_bedrooms_non_negative"),
        CheckConstraint("min_area >= 0", name="check_min_area_non_negative"),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey("users.id"), 
        nullable=False, 
        index=True
    )
    state = db.Column(db.String(2), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    neighborhood = db.Column(db.String(255), nullable=False)
    property_type = db.Column(
        db.Enum(PropertyType, name="property_type_enum"), 
        nullable=False
    )
    max_price = db.Column(db.Numeric(10,2), nullable=False)
    min_bedrooms = db.Column(db.Integer, nullable=False)
    min_area = db.Column(db.Integer, nullable=False)

    matches = db.relationship(
        "Match", 
        backref="monitor", 
        lazy="selectin", 
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Monitor {self.id}>"