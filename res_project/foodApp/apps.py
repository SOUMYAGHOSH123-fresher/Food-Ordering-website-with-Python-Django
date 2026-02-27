from django.apps import AppConfig


class FoodappConfig(AppConfig):
    name = 'foodApp'

    def ready(self):
        import foodApp.signals
