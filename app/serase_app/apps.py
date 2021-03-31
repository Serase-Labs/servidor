from django.apps import AppConfig


class SeraseAppConfig(AppConfig):
    name = 'serase_app'

    def ready(self):
        import serase_app.signals
