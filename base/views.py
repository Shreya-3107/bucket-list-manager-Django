from django.shortcuts import render

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy

from .models import Task

"""
    context_object_name = 'tasks'
    paginate_by = 5
    ordering = ['date_created']

"""

class TaskList(ListView):
    model = Task
    template_name = 'base/task_list.html' #to set the template to be displayed
    context_object_name = 'tasks'
    # making it readable by adding context_object_name as tasks

class TaskDetail(DetailView):
    model = Task
    template_name = 'base/task_detail.html'
    context_object_name = 'task' #this basically changes the reference name of the passed value from object as default to the set value

class TaskCreate(CreateView):
    model = Task
    template_name = 'base/task_form.html'
    fields = '__all__' #or we can add specific needed ones like ['title', 'desc'] and this basically adds the said values to the form by creating said fields
    success_url = reverse_lazy('tasks') #if everything goes well, it redirects the path to 'tasks' as in the urls.py path('', name = 'tasks')
    #success_url basically does redirecting after success

class TaskUpdate(UpdateView):
    model = Task
    template_name = 'base/task_form.html'
    fields = '__all__'
    success_url = reverse_lazy('tasks')

class TaskDelete(DeleteView):
    model = Task
    template_name = 'base/task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')