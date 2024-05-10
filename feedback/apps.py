from django.apps import AppConfig

class FeedbackConfig(AppConfig):
    name = 'feedback'

    def ready(self):
        # Import your signals here
        import feedback.signals
