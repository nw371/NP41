from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum


class Author(models.Model):
    # cвязь «один к одному» с встроенной моделью пользователей User;
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    # рейтинг пользователя
    rating = models.SmallIntegerField(default = 0)

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора
        poRe = self.post_set.aggregate(SumPostRating = Sum('rating'))
        pstrtng = 0
        pstrtng += poRe.get('SumPostRating')

        # суммарный рейтинг всех комментариев автора
        coRe = self.user.comment_set.aggregate(SumComsRating = Sum('rating'))
        cmmrtng = 0
        cmmrtng += coRe.get('SumComsRating')

        # суммарный рейтинг всех комментариев к статьям автора
        # copoRe = self.post_set.comment.aggregate(SumPostComsRating = Sum('rating'))
        cprtng = 0
        # cprtng += copoRe.get('SumPostComsRating')

        self.rating = pstrtng * 3 + cmmrtng + cprtng
        self.save()

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    # единственное поле: название категории. Поле должно быть уникальным
    name = models.CharField(max_length = 128, unique = True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    news = 'NS'
    article = 'AL'
    TYPES = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    # поле с выбором — «статья» или «новость»
    type = models.CharField(max_length = 2, choices = TYPES, default = news)
    # автоматически добавляемая дата и время создания
    date = models.DateTimeField(auto_now_add = True)
    # заголовок статьи/новости
    name = models.CharField(max_length = 255)
    # текст статьи/новости
    body = models.TextField()
    # рейтинг статьи/новости
    rating = models.SmallIntegerField(default = 0)

    # связь «один ко многим» с моделью Author
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    # связь «многие ко многим» с моделью Category (с дополнительной моделью PostCategory)
    category = models.ManyToManyField(Category, through = 'PostCategory')

    def preview(self):
        preview = self.body[0:123]
        return f"{preview}..."

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class PostCategory(models.Model):
    # связь «один ко многим» с моделью Post
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    # связь «один ко многим» с моделью Category
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    # связь «один ко многим» с моделью Post
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    # связь «один ко многим» с встроенной моделью User
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    # текст комментария
    body = models.TextField()
    # дата и время создания комментария
    date = models.DateField(auto_now_add = True)
    # рейтинг комментария
    rating = models.SmallIntegerField(default = 0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
