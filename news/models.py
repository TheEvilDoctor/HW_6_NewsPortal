from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.authorUser.username.title()

    def update_rating(self):
        newrating = sum(Post.objects.filter(author_id=self.authorUser_id).values_list('rating', flat=True)) * 3 + \
                    sum(Comment.objects.filter(commentUser_id=self.authorUser_id).values_list('rating', flat=True)) + \
                    sum(Comment.objects.filter(commentPost_id__author_id=self.authorUser_id).values_list('rating', flat=True))
        self.ratingAuthor = newrating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    TYPE_CHOISES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length=2, choices=TYPE_CHOISES, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.title.title()}: {self.text}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def preview(self):
        preview = f'{self.text[:124]} ...'
        return preview

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text[0:124]}...'
