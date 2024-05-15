from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

"""
    context_object_name = 'tasks'
    paginate_by = 5
    ordering = ['date_created']
    refer the ccbv.co.uk website for info

"""

#the LoginRequiredMin basically restricts the user who is not logged in from accessing the views directly through link unless they log back in

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True #prevents the user from staying on this page after authentication
    
    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True 
    success_url = reverse_lazy('tasks')

    #once the form is submitted and validated, this makes sure the user is logged in
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form) 

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/task_list.html' #to set the template to be displayed
    context_object_name = 'tasks'
    # making it readable by adding context_object_name as tasks

    def get_context_data(self, **kwargs): #we are overriding already exisiting function here to set the context, which is a dictionary and we're giving the key as task and setting value by filtering out what the user has alone
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(is_complete=False)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith = search_input) #title__icontains
        
        context['search_input'] = search_input
        #setting this will help us to make the default value of the search input to be the one the user previously typed. without this it keeps getting refreshed making it tough for the user to track. for this to work fully, we should add the variable search_input as the {{}} in the value field of input form
        
        return context
        #we can send these as the context to our views

class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'base/task_detail.html'
    context_object_name = 'task' #this basically changes the reference name of the passed value from object as default to the set value

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'base/task_form.html'
    fields = ['title', 'desc', 'is_complete'] #or we can add specific needed ones like ['title', 'desc'] and this basically adds the said values to the form by creating said fields
    success_url = reverse_lazy('tasks') #if everything goes well, it redirects the path to 'tasks' as in the urls.py path('', name = 'tasks')
    #success_url basically does redirecting after success

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'base/task_form.html'
    fields = ['title', 'desc', 'is_complete'] 
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskUpdate, self).form_valid(form)

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/task_confirm_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')