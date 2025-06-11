from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """
    Multiplies the value with the argument.
    Usage: {{ value|multiply:arg }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ""


@register.filter
def subtract(value, arg):
    """Subtracts the arg from the value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return value  # Return original value if subtraction fails or types are wrong


@register.filter
def get_range(value):
    """
    Generates a range object for a given integer.
    Useful for iterating a specific number of times in templates.
    Usage: {% for i in some_int|get_range %}
    """
    if isinstance(value, int):
        return range(value)
    return []
