from django.apps import AppConfig

class GessdemnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gessdemn'


    def ready(self):
        from .tasks import start_scheduler
        start_scheduler()