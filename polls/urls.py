from django.urls import path

from . import views
'''
将新的视图添加到，url里面这样才可以被搜索到
某人请求你网站的某一页面时——比如说，
 "/polls/34/" ，Django 将会载入 mysite.urls 模块，
 因为这在配置项 ROOT_URLCONF 中设置了。然后 Django 
 寻找名为 urlpatterns 变量并且按序匹配正则表达式。
 在找到匹配项 'polls/'，它切掉了匹配的文本（"polls/"），
 将剩余文本——"34/"，发送至 'polls.urls' URLconf 做进一步处理。
 在这里剩余文本匹配了 '<int:question_id>/'，
 使得我们 Django 以如下形式调用 detail():
 
 question_id=34 由 <int:question_id>
 上述字符串的 :question_id> 部分定义了将被用于区分匹配模式的变量名，
 而 int: 则是一个转换器决定了应该以什么变量类型匹配这部分的 URL 路径。
'''
'''app_name='polls'为 URL 名称添加命名空间,用于分辨不同app中相同的视图（函数）'''
app_name='polls'
'''
urlpatterns = [
    # ex: /polls/ name将会在模板中用到（html文件中加入python代码）
    path('', views.index, name='index'),
    # ex: /polls/5/  将5赋值给question_id然后调用函数detail(request=<HttpRequest object>, question_id=34)
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]'''
#通用视图的url
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]