from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect

class CustomLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Пожалуйста, войдите в систему, чтобы просмотреть эту страницу.')
            return redirect(f'{self.get_login_url()}?next={request.path}')
        return super().dispatch(request, *args, **kwargs)

def login_required_with_message(view_func):
    @login_required(login_url='login/')
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Пожалуйста, войдите в систему, чтобы просмотреть эту страницу.')
        return view_func(request, *args, **kwargs)
    return wrapped_view