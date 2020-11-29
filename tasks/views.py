from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from tasks.models import TaskModel
from tasks.forms import AddTaskForm
from accounts.models import UserProfile
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


#TODO: write a decorator.
class AddTask(View):
    template_name = 'task_form.html'

    def get(self, request):
        form = AddTaskForm()
        return render(request, self.template_name, {'form': form})

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


#TODO: add pageination feature
def getAllTask(request):
    template_name = 'get_task.html'

    if request.method == 'GET':
        tasks = TaskModel.objects.all()
        context = {
            'tasks': tasks,
            'request': request
        }
        return render(request, template_name, context=context)


#TODO: add decorator
def getReportedTask(request):
    template_name = 'get_task.html'

    if request.method == 'GET':
        user_type = request.user.userprofile.user_type
        if user_type == UserProfile.AGENT:
            reported_tasks = TaskModel.objects.filter(reporter=request.user)
            context = {
                'tasks': reported_tasks,
                'request': request
            }
            return render(request, template_name, context=context)


def getAssignTask(request):
    template_name = 'get_task.html'

    if request.method == 'GET':
        assign_tasks = TaskModel.objects.filter(assignee=request.user)
        context = {
                'tasks': assign_tasks,
                'request': request
        }
        return render(request, template_name, context=context)


@csrf_exempt
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
            return HttpResponse('This task assigns to you',
                                content_type="application/json",
                                status=200)
        except Exception as e:
            return HttpResponse('Error eccured',
                                content_type="application/json",
                                status=400)
