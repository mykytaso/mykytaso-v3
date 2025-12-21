from django import template


register = template.Library()


@register.filter
def abbreviate_number(value):
    """
    Format numbers in abbreviated form.
    - 500 → "500"
    - 11500 → "11.5K"
    - 2500000 → "2.5M"
    """
    try:
        value = int(value)
    except (ValueError, TypeError):
        return value

    if value < 1000:
        return str(value)
    if value < 1_000_000:
        # Format as K (thousands)
        result = value / 1000
        if result == int(result):
            return f"{int(result)}K"
        return f"{result:.1f}K"
    if value < 1_000_000_000:
        # Format as M (millions)
        result = value / 1_000_000
        if result == int(result):
            return f"{int(result)}M"
        return f"{result:.1f}M"
    # Format as B (billions)
    result = value / 1_000_000_000
    if result == int(result):
        return f"{int(result)}B"
    return f"{result:.1f}B"
