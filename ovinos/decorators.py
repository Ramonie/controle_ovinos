from django.shortcuts import redirect
from django.contrib import messages

def admin_or_organizador_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser or request.user.profile.role == "organizador":
            return view_func(request, *args, **kwargs)

        messages.error(request, "Você não tem permissão para acessar esta página.")
        return redirect("perfil")
    return wrapper
