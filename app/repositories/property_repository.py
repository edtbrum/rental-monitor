from app.models.property import Property
from app import db

class PropertyRepository:

    @staticmethod
    def create(data):
        property = Property(**data)
        db.session.add(property)
        return property
    
    @staticmethod
    def get_all():
        return Property.query.all()
    
    @staticmethod
    def get_by_city(city):
        return Property.query.filter_by(city=city).all()
    
    @staticmethod
    def delete(property_id):
        property = db.session.get(Property, property_id)
        if not property:
            return None
        db.session.delete(property)
        return property
