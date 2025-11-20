from django.apps import AppConfig


class OvinosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ovinos'

    def ready(self):
        import ovinos.signals
