from uuid import uuid4

from slugify import slugify


def generate_unique_slug(model, name, separator="-", max_length=50, exclude_pk=None):
    """
    Generate a unique slug for a Django model instance.

    Args:
        model: Django model class to check for slug uniqueness
        name: Base name to generate slug from
        separator: Character to use as separator (default: "-")
        max_length: Maximum length of the slug (default: 50)
        exclude_pk: Primary key to ignore when looking for collisions. Pass the
            instance's own primary key when you regenerate the slug of a row
            that already exists. If you do not, its current slug counts as a
            collision and "my-post" becomes "my-post-1".

    Returns:
        str: Unique slug for the model
    """
    base_slug = slugify(name, separator=separator)[:max_length]
    slug = base_slug
    counter = 1

    queryset = model.objects.all()
    if exclude_pk is not None:
        queryset = queryset.exclude(pk=exclude_pk)

    while queryset.filter(slug__iexact=slug).exists():
        suffix = f"{separator}{counter}"
        slug = f"{base_slug[: max_length - len(suffix)]}{suffix}"
        counter += 1

        if counter > 9999:
            uuid_suffix = f"{separator}{uuid4()}"
            slug = f"{base_slug[: max_length - len(uuid_suffix)]}{uuid_suffix}"
            break

    return slug
