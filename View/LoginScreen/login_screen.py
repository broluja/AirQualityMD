from kivymd.uix.screen import MDScreen

from View.Manager.user_manager import UserManager
from View.Manager.notification_manager import NotificationManager
from Controller.exceptions import DataBaseException


class LoginScreenView(MDScreen):
    """Screen used for logging in APP."""
    def __init__(self, **kwargs):
        super(LoginScreenView, self).__init__(**kwargs)
        self.user = UserManager()
        self.notification_manager = NotificationManager()

    def login(self, email: str, password: str) -> None:
        """
        Logging in using unique email and password.

        Args:
            email (str): String value representing user`s name.
            password (str): String value representing user`s password.

        Returns:
            None.
        """
        try:
            self.user.login_user(email, password)
        except DataBaseException as ex:
            ex.to_log()
            self.notification_manager.notify(ex.user_error_message)
        else:
            self.notification_manager.notify('Successfully logged IN.')
            self.manager.switch_screen('main')
