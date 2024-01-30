from django.contrib.auth.forms import AuthenticationForm

from . import forms


def authentication_context(request):
    login_form = AuthenticationForm()

    return {"login_form": login_form}
