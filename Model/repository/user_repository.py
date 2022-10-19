"""ORM model for 'user'."""
from typing import Optional

from Model.models.user_model import User
from Model.repository.base_repository import CRUDBase
from Controller.utils import verify_password, get_password_hash


class UserRepository(CRUDBase[User]):
    """ CRUD`s subclass for interaction with 'tasks' table """

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Args:
            email (str): string value, title of the task.

        Returns:
            list object.
        """
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_password(self, password: str) -> Optional[User]:
        """
        Args:
            password (str): string value, id of the task.

        Returns:
            task object.
        """
        hashed_password = get_password_hash(password)
        if verify_password(hashed_password=hashed_password, plain_password=password):
            return self.db.query(User).filter(User.hashed_password == hashed_password).first()


user_repository = UserRepository(User)
