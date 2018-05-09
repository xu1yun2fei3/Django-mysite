from django.http import HttpResponse,HttpResponseRedirect
from .models import  Question,Choice
from django.template import loader
from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.urls import reverse
#使用通用视图
from django.views import generic
from django.utils import timezone
'''
每一个视图是一个函数
我们的投票应用中，我们需要下列几个视图：

    问题索引页——展示最近的几个投票问题。
    问题详情页——展示某个投票的问题和不带结果的选项列表。
    问题结果页——展示某个投票的结果。
    投票处理器——用于响应用户为某个问题的特定选项投票的操作。

'''

def index(request):
    #输出最近的五个问题,django 数据库的api
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #output = ', '.join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #得到本app项目下template文件夹下面的 polls/index.html
    template = loader.get_template('polls/index.html')
    #context将会在index.html中用到
    context = {
        'latest_question_list': latest_question_list,
    }
    '''
    render()函数
    「载入模板，填充上下文，再返回由它生成的 HttpResponse 对象」
    是一个非常常用的操作流程。
    于是 Django 提供了一个快捷函数，我们用它来重写 index() 视图：
    '''
   # return HttpResponse(template.render(context, request))
    return render(request,'polls/index.html',context)

def detail(request, question_id):
    #一般方法404页面
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    #一个快捷函数用 get_object_or_404(),
    # 用get() 函数获取一个对象，如果不存在就抛出 Http404 错误
    #get_list_or_404() 函数，工作原理和 get_object_or_404() 一样
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        #request.POST 是一个类字典对象，让你可以通过关键字的名字获取提交的数据
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # HttpResponseRedirect 只接收一个参数：用户将要被重定向的 URL
        #reverse() 函数。这个函数避免了我们在视图函数中硬编码 URL。
        # 它需要我们给出我们想要跳转的视图的名字和该视图所对应的 URL
        # 模式中需要给该视图提供的参数
        #reverse() 调用将返回一个这样的字符串：'/polls/3/results/'
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class IndexView(generic.ListView):
    # generic.ListView) 抽象“显示一个对象列表”
    template_name = 'polls/index.html'
    #template_name 属性是用来告诉 Django 使用一个指定的模板名字，而不是自动生成的默认名字
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    #generic.DetailView 显示一个特定类型对象的详细信息页面
    model = Question
    #ListView 使用一个叫做 <app name>/<model name>_list.html 的默认模板；
    # 我们使用 template_name
    # 来告诉 ListView 使用我们创建的已经存在的 "polls/index.html" 模板
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    '''提供模板文件时都带有一个包含 question 和 latest_question_list 变量的 
    context。对于 DetailView ， question
     变量会自动提供—— 因为我们使用 Django 的模型 (Question)，
      Django 能够为 context 变量决定一个合适的名字。然而对于 ListView，
       自动生成的 context 变量是 question_list。
       为了覆盖这个行为，我们提供 context_object_name 属性，
       表示我们想使用 latest_question_list。作为一种替换方案，
       你可以改变你的模板来匹配新的 context 变量 —— 这是一种更便捷的方法，
       告诉 Django 使用你想使用的变量名。'''

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'