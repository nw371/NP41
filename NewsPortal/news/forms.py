from django.forms import ModelForm
from .models import Post
#https://docs.djangoproject.com/en/dev/topics/forms/modelforms/#modelforms-overriding-default-fields
#https://django.fun/docs/django/ru/3.1/topics/forms/modelforms/

# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['name', 'body', 'category', 'author']
        labels = {
            'name': 'Заголовок',
            'body': 'Текст',
            'category': 'Категория',
            'author': 'Автор',
        }


class PostEdit(ModelForm):

    class Meta:
        model = Post
        fields = ['name', 'body', 'category', 'author']
        labels = {
            'name': 'Заголовок',
            'body': 'Текст',
            'category': 'Категория',
            'author': 'Автор',
        }