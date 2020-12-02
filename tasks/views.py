from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator
from tasks.models import TaskModel
from tasks.forms import AddTaskForm
from accounts.models import UserProfile
from django.contrib.auth.models import User
from Crowdsourcing.settings import SHOW_TASK_PER_PAGE
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from tasks.permissions import is_agent
# Create your views here.


class AddTask(View):
    template_name = 'task_form.html'

    @method_decorator([login_required, is_agent])
    def get(self, request):
        form = AddTaskForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator([login_required, is_agent])
    def post(self, request):
        form = AddTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            value = form.cleaned_data.get('value')
            estimation = form.cleaned_data.get('estimation')
            deadline = form.cleaned_data.get('deadline')
            description = form.cleaned_data.get('description')

            task = TaskModel.objects.create(title=title,
                                            value=value,
                                            estimation=estimation,
                                            deadline=deadline,
                                            description=description,
                                            reporter=request.user)
            return redirect('all_task')
        else:
            err_msg = "Invalid Input"
            context = {
                'err_msg': err_msg,
                'form': form
            }
            return render(request, self.template_name, context=context)


def getAllTask(request):
    template_name = 'get_task.html'

    if request.method == 'GET':
        tasks = TaskModel.objects.all().order_by('updated_at')
        
        page_number = request.GET.get('page')
        paginator = Paginator(tasks, SHOW_TASK_PER_PAGE)
        tasks = paginator.get_page(page_number)
    
        context = {
            'tasks': tasks,
            'request': request,
        }
        return render(request, template_name, context=context)


@login_required
@is_agent
def getReportedTask(request):
    template_name = 'get_task.html'

    if request.method == 'GET':
        user_type = request.user.userprofile.user_type
        if user_type == UserProfile.AGENT:
            reported_tasks = TaskModel.objects.filter(
                reporter=request.user).order_by('updated_at')

            page_number = request.GET.get('page')
            paginator = Paginator(reported_tasks, SHOW_TASK_PER_PAGE)
            reported_tasks = paginator.get_page(page_number)

            context = {
                'tasks': reported_tasks,
                'request': request
            }
            return render(request, template_name, context=context)


@login_required
def getAssignedTask(request):
    template_name = 'get_task.html'

    if request.method == 'GET':
        assign_tasks = TaskModel.objects.filter(
            assignee=request.user).order_by('updated_at')

        page_number = request.GET.get('page')
        paginator = Paginator(assign_tasks, SHOW_TASK_PER_PAGE)
        assign_tasks = paginator.get_page(page_number)

        context = {
                'tasks': assign_tasks,
                'request': request
        }
        return render(request, template_name, context=context)


@csrf_exempt
@login_required
def assignTask(request):
    template_name = 'get_task.html'

    if request.method == 'POST':
        assignee_name = request.POST.get('assignee')
        task_id = request.POST.get('task_id')

        try:
            task = TaskModel.objects.get(id=task_id)
            assignee = User.objects.get(username=assignee_name)
            task.assignee = assignee
            task.save()
            return HttpResponse('This task assigned to you',
                                content_type="application/json",
                                status=200)
        except Exception as e:
            return HttpResponse('Error occured',
                                content_type="application/json",
                                status=400)


def seeDescription(request, task_id):
    task = TaskModel.objects.get(id=task_id)
    task_description = task.description
    context = {
        'description': task_description
    }
    return render(request, 'show_description.html', context=context)
