from django.db import models
from django.utils import timezone
from django.urls import reverse
# django 2.0 uses .urls#}
# Create your models here.
#A many-to-one relationship. Requires two positional arguments: the class to which the model is related and the on_delete option. (on_delete isn’t actually required, but not providing it gives a deprecation warning. It will be required in Django 2.0.)

# To create a recursive relationship – an object that has a many-to-one relationship with itself – use models.ForeignKey('self', on_delete=models.CASCADE). #
class Post(models.Model):
    author  = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post',related_name='comments',on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now())
    approved_comments = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse('post_list')

    def __str__(self):
        return self.text
