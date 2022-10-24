from passlib.context import CryptContext

from kivymd.uix.label import MDLabel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_aqi_category(num: int) -> str:
    if num in range(51):
        return 'good'
    elif num in range(51, 101):
        return 'moderate'
    elif num in range(101, 151):
        return 'unhealthy for sensitive groups'
    elif num in range(151, 201):
        return 'unhealthy'
    elif num in range(201, 301):
        return 'very unhealthy'
    return 'hazardous'


class APPLabel(MDLabel):
    halign = 'center'
    theme_text_color = 'Custom'
    font_style = 'H2'
    colors = {
        'good': (120/255, 233/255, 81/255, 1),
        'moderate': (253/255, 217/255, 41/255, 1),
        'unhealthy for sensitive groups': (1, 139/255, 56/255, 1),
        'unhealthy': (1, 58/255, 83/255, 1),
        'very unhealthy': (174/255, 87/255, 181/255, 1),
        'hazardous': (170/255, 96/255, 121/255, 1)
    }

    def __init__(self, aqi=None, **kwargs):
        if aqi is not None:
            self.text_color = self.colors.get(aqi)
        if aqi == 'home_city':
            self.halign = 'left'
            self.text_color = (253/255, 217/255, 41/255, 1)
        super(APPLabel, self).__init__(**kwargs)
