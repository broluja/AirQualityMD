"""Creating Model for 'user' table."""
import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID

from Model.database.settings import Base


class User(Base):
    """Model for data table 'users'."""
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String)
    hashed_password = Column(String)

    def to_dict(self) -> dict:
        return {'id': self.id, 'email': self.email}
