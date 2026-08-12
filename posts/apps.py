from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = "posts"

    def ready(self):
        # Connects delete_post_image_file, which removes an image file from disk.
        # The import must stay here: signals.py imports a model, and models are not ready when Django imports this module.
        from posts import signals  # noqa: F401, PLC0415
