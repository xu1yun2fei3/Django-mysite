from django.db import models
import datetime
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField('问题',max_length=200)
    #question_text = models.CharField('问题',max_length=200)
    #第一个参数是verbose_name，相当于条目名
    pub_date = models.DateTimeField('date published')
    #定义返回的东西，没有的话就是会返回这个对象
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    #定义排序方式，按照pub_date排序
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    #question=models.ForeignKey(Question)视频上的代码
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text