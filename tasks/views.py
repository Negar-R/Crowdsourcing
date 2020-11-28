from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from tasks.models import TaskModel
from tasks.forms import AddTaskForm
from django.contrib.auth.decorators import login_required
# Create your views here.

#TODO: add pageination feature
def getAllTask(request):
    template_name = 'get_all_task.html'

    if request.method == 'GET':
        tasks = TaskModel.objects.all()
        print("this is all tasks :", tasks)
        context = {
            'tasks': tasks,
            'request': request
        }
        return render(request, template_name, context=context)


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
