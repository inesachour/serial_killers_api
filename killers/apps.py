from django.apps import AppConfig


class KillersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'killers'
    
    def ready(self):
        import killers.signals  # Import signals to register them
