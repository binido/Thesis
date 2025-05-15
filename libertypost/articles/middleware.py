from django.http import Http404
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin


class AdminAccessMiddleware(MiddlewareMixin):
    """
    Промежуточное ПО, которое проверяет, является ли пользователь администратором
    при доступе к панели администратора Django.
    Для неадминистраторов возвращает ошибку 404 вместо перенаправления на страницу входа.
    """

    def process_request(self, request):
        """
        Метод вызывается для каждого запроса до вызова представления.
        """
        resolved_path = resolve(request.path)
        if resolved_path.app_name == "admin" or resolved_path.namespace == "admin":
            if not request.user.is_authenticated or not request.user.is_superuser:
                raise Http404("Страница не найдена")

        return None
