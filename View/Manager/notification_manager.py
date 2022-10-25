from kivymd.toast import toast
from kivymd.app import MDApp


class NotificationManager(object):
    """Class for serving proper notifications."""
    def __init__(self):
        self.app = MDApp.get_running_app()

    def __str__(self):
        return f'Notification Manager for {self.app}'

    @staticmethod
    def notify(text: str, duration=4, background=None) -> None:
        toast(text=text, duration=duration, background=background)


notification_manager = NotificationManager()
