from .models import Category


def categories(request):
    """
    Контекстный процессор, который добавляет все категории в контекст шаблона
    """
    return {
        "categories": Category.objects.all(),
    }
