from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum, Count, Avg


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    url = models.CharField(max_length=250, verbose_name="URL", null=True,blank=True) #didn't understand what's the purpose of this field

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alias = models.CharField(max_length=250, verbose_name="Псевдоним")
    photo = models.ImageField(upload_to="authors/", verbose_name="Фото")

    @property
    def karma(self):
        posts = self.posts
        return sum((post.rating for post in posts))

    @property
    def posts(self):
        return Post.objects.filter(author=self)

    def __str__(self):
        return self.alias


Statuses = (
    (1, u'Опубликованный'),
    (2, u'Ожидающий'),
    (3, u'Отклоненный'),
)


class Post(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название")
    link = models.CharField(max_length=250, verbose_name="Ссылка",blank=True,null=True)
    image = models.ImageField(upload_to="posts/", verbose_name="Основная картинка")
    text = models.TextField(max_length=523000, verbose_name="Текст поста")
    category = models.ForeignKey(Category, verbose_name="Категория")
    creation_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    status = models.PositiveSmallIntegerField(choices=Statuses, default=2, verbose_name="Статус")
    author = models.ForeignKey(Author,verbose_name="Автор")

    def __str__(self):
        return self.name

    @property
    def rating(self):
        qs = Review.objects.filter(post=self)
        avg_rating = qs.aggregate(Avg('mark')).get('mark__avg')
        return avg_rating if avg_rating else 0.0


class Comment(models.Model):
    user = models.ForeignKey(User)
    text = models.TextField(max_length=1000,verbose_name="Текст комментария")
    creation_date = models.DateField(auto_now_add=True, verbose_name="Дата создания")
    post = models.ForeignKey(Post)


class Review(models.Model):
    class Meta:
        unique_together = (('user','post'))
    user = models.ForeignKey(User)
    mark = models.FloatField(verbose_name="Рейтинг", validators=[MaxValueValidator(5.0), MinValueValidator(0.0)],
                               default=0.0)
    post = models.ForeignKey(Post)