from functools import wraps

from django.http import Http404


def superuser_only(view_func):
    """Make a view superuser only."""

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404

        return view_func(request, *args, **kwargs)

    return _wrapped_view
