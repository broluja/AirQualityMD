from kivymd.uix.screen import MDScreen

from View.Manager.user_manager import UserManager
from View.Manager.notification_manager import NotificationManager
from Controller.exceptions import DataBaseException


class RegisterScreenView(MDScreen):
    """Screen used for logging in game."""
    def __init__(self, **kwargs):
        super(RegisterScreenView, self).__init__(**kwargs)
        self.user = UserManager()
        self.notification_manager = NotificationManager()

    def register(self, email: str, password: str, password_confirmed: str) -> None:
        """
        Registering users. Emails are unique values, and you need one to register as user.
        Passwords are being hashed and stored to database.

        Args:
            email (str): String value representing user`s name.
            password (str): String value representing user`s password.
            password_confirmed (str): String value, repeated user`s password.

        Returns:
            None. User is transferred to Log-in screen.
        """
        try:
            self.user.register_user(email, password, password_confirmed)
        except DataBaseException as ex:
            ex.to_log()
            self.notification_manager.notify(ex.user_error_message)
        else:
            self.notification_manager.notify('Successfully registered. You can login now.')
            self.manager.switch_screen('login')
