from app.extensions import db
from datetime import datetime, timezone

class Match(db.Model):
    __tablename__ = "matches"

    __table_args__ = (
        db.UniqueConstraint(
            "monitor_id",
            "property_id",
            name="uq_monitor_property_match"
        ),
        db.Index(
            "idx_match_notified_matched_at",
            "notified",
            "matched_at"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    monitor_id = db.Column(
        db.Integer,
        db.ForeignKey("monitors.id"),
        nullable=False,
        index=True
    )
    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False,
        index=True
    )
    matched_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True
    )
    notified = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Match {self.id}>"