from contextlib import suppress
from pathlib import Path

from django.db import transaction
from django.db.models.signals import post_delete
from django.dispatch import receiver

from posts.models import PostImage


@receiver(post_delete, sender=PostImage)
def delete_post_image_file(sender, instance, **kwargs):
    """
    Remove the file from disk when its row goes, and the directory when it empties.

    Deleting a Post cascades to its images, and Django's collector sends
    post_delete for each one, thus the files of a deleted post go too.

    on_commit is necessary: post_delete fires inside the transaction. Without it
    a rollback would leave a row that points to a file that is already deleted.
    """

    image_file = instance.file
    if not image_file:
        return

    # Read the directory now: file.delete() clears the name, thus .path would raise afterwards.
    image_directory = Path(image_file.path).parent

    def remove_file_and_empty_directory():
        image_file.delete(save=False)

        # Django deletes the file only, never its directory, thus posts/<post_id>/ would stay behind empty.
        # rmdir refuses a directory that is not empty, so one image of three leaves it alone and the last one takes it away.
        # suppress covers the race of two deletes that finish together.
        with suppress(OSError):
            image_directory.rmdir()

    transaction.on_commit(remove_file_and_empty_directory)
