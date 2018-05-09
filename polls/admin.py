from django.contrib import admin
from .models import Question,Choice


#关联对象,继承StackedInline，还有其他的如TabularInline
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

#实现字段的分组
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    #显示字段格式
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    #过滤器，在后台添加一个过滤器，过滤的字段是pub_date
    list_filter = ['pub_date']
    #在列表的顶部添加一个搜索框，输入待搜项时，Django 将搜索 question_text 字段
    search_fields = ['question_text']

#admin.site.register(Question)注册Question
#注册Question并且定义了显示的字段
admin.site.register(Question,QuestionAdmin)

# Register your models here.
