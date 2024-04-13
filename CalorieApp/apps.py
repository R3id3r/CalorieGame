from django.apps import AppConfig


class CalorieappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CalorieApp'

    def ready(self):
        import CalorieApp.signals