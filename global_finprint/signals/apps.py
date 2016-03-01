from django.apps import AppConfig


class SignalConfig(AppConfig):
    name = 'global_finprint.signals'

    def ready(self):
        import global_finprint.signals.signals
