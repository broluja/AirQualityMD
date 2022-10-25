from email_validator import validate_email, EmailNotValidError

from Controller.exceptions import *
from Controller.utils import get_password_hash, verify_password
from Model.repository.user_repository import user_repository


class UserManager:
    """Database client for managing user`s registration, login, updating..."""
    def __init__(self):
        self.email = None
        self.password = None

    def register_user(self, email: str, password: str, password_confirmed: str) -> None:
        """
        Args:
            email (str): string value, user`s email.
            password (str): string value, user`s password.
            password_confirmed (str): string value, user`s password repeated.

        Returns:
            None.
        """
        try:
            valid = validate_email(email)
            email = valid.email
            if user_repository.get_user_by_email(email):
                raise EmailAlreadyInUseException('User with this email already exists.')
        except EmailNotValidError as e:
            raise LoginException(e.args[0], user_message=e.args[0]) from e

        if not password:
            raise LoginException(user_message='Please, enter and re-type your password.')

        if password != password_confirmed:
            raise PasswordsDoNotMatchException

        self.email = email
        self.password = password
        hashed_password = get_password_hash(password)
        user_repository.create({'email': email, 'hashed_password': hashed_password})

    def login_user(self, email: str, password: str) -> None:
        """
        Args:
            email (str): string value, user`s email.
            password (str): string value, user`s password.

        Returns:
            None.
        """
        if not email:
            raise LoginException(user_message='Please enter your email')
        if not password:
            raise LoginException(user_message='Please enter your password')
        user = user_repository.get_user_by_email(email)
        if not user:
            raise UserDoNotExistException
        if not verify_password(password, user.hashed_password):
            raise WrongPasswordException
        self.email = email
        self.password = password
