from uuid import uuid4

from slugify import slugify


def generate_unique_slug(model, name, separator="-", max_length=50):
    """
    Generate a unique slug for a Django model instance.

    Args:
        model: Django model class to check for slug uniqueness
        name: Base name to generate slug from
        separator: Character to use as separator (default: "-")
        max_length: Maximum length of the slug (default: 50)

    Returns:
        str: Unique slug for the model
    """
    base_slug = slugify(name, separator=separator)[:max_length]
    slug = base_slug
    counter = 1

    while model.objects.filter(slug__iexact=slug).exists():
        suffix = f"{separator}{counter}"
        slug = f"{base_slug[:max_length - len(suffix)]}{suffix}"
        counter += 1

        if counter > 9999:
            uuid_suffix = f"{separator}{uuid4()}"
            slug = f"{base_slug[:max_length - len(uuid_suffix)]}{uuid_suffix}"
            break

    return slug
