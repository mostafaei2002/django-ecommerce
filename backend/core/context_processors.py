from .models import Category


def category_context(request):
    categories = Category.objects.all().filter(parent_category=None)

    return {"global_categories": categories}
