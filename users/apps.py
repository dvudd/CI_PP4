from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    App configuration for the users application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        import users.signals
