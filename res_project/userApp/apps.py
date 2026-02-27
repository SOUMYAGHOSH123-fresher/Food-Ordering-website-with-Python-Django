from django.apps import AppConfig


class UserappConfig(AppConfig):
    name = 'userApp'

    def ready(self):
        import userApp.signals

