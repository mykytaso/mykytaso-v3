from django import template


register = template.Library()


@register.filter
def abbreviate_number(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value

    if value < 1000:
        return str(value)

    # Determine the appropriate suffix and divisor
    if value >= 1_000_000_000:
        divisor, suffix = 1_000_000_000, "B"
    elif value >= 1_000_000:
        divisor, suffix = 1_000_000, "M"
    else:
        divisor, suffix = 1000, "K"

    result = value / divisor
    if result == int(result):
        return f"{int(result)}{suffix}"
    return f"{result:.1f}{suffix}"
