from django.db import transaction
from django.db.models.signals import post_delete
from django.dispatch import receiver

from posts.models import PostImage


@receiver(post_delete, sender=PostImage)
def delete_post_image_file(sender, instance, **kwargs):
    """
    Remove the file from disk when its row goes.

    Deleting a Post cascades to its images, and Django's collector sends
    post_delete for each one, thus the files of a deleted post go too.

    on_commit is necessary: post_delete fires inside the transaction. Without it
    a rollback would leave a row that points to a file that is already deleted.
    """

    file = instance.file
    if file:
        transaction.on_commit(lambda: file.delete(save=False))
