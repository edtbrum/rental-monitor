from sqlalchemy import select
from app.models.user import User

class UserRepository:

    def __init__(self, session):
        self.session = session

    def create(self, data):
        user = User(**data)
        self.session.add(user)
        return user
    
    def update(self, username, data):
        user = self.get_by_username(username)
        if not user:
            return None
        user.username = data['username']
        user.email = data['email']
        return user
    
    def get_by_username(self, username):
        query = select(User).filter_by(username=username)
        return self.session.execute(query).scalar_one_or_none()
    
    def delete(self, user):
        self.session.delete(user)
        return user