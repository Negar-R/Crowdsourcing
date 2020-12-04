import logging

from django.http import HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.models import UserProfile
from tasks.permissions import is_agent
from tasks.models import TaskModel
from tasks.forms import AddTaskForm
from Crowdsourcing.settings import SHOW_TASK_PER_PAGE

# Create your views here.

logger = logging.getLogger(__name__)


class AddTask(View):
    template_name = 'task_form.html'

    @method_decorator([login_required, is_agent])
    def get(self, request):
        form = AddTaskForm()
        logger.debug("GET request method to add_task view")
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

            logger.info('task with id:{} was created by user:{}'
                        .format(task.id, request.user.username))

            return redirect('all_task')
        else:
            err_msg = "Invalid Input"
            context = {
                'err_msg': err_msg,
                'form': form
            }

            logger.info('add_task form error: {}'.format(form.errors))

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

        logger.info('GET request method to get_all_task view')

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

            logger.info('user with username: {} saw owns reported_tasks'
                        .format(request.user.username))

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

        logger.info('user with username: {} saw owns assigned_tasks'
                    .format(request.user.username))

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

            logger.info('user with username: {} assign task_id: {} to own'
                        .format(request.user.username, task_id))

            return HttpResponse('This task assigned to you',
                                content_type="application/json",
                                status=200)
        except Exception as e:

            logger.warning('assigning task_id:{} to username:{} was unsuccessful'
                           .format(task_id, request.user.username))

            return HttpResponse('Error occured',
                                content_type="application/json",
                                status=400)


def seeDescription(request, task_id):
    task = TaskModel.objects.get(id=task_id)
    task_description = task.description
    context = {
        'description': task_description
    }

    logger.info('description of task_id: {} was shown'.format(task_id))

    return render(request, 'show_description.html', context=context)
