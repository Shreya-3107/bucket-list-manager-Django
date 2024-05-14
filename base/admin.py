from django.contrib import admin
from .models import Task

admin.site.register(Task) #to register the Task model with the /admin of django
"""
this will help us in integrating it and we can 
create users with the help of this by logging into 
django admin site and logging in using super user.
my super user for this project is shreya with pass 
as abcdefgh (or) abcdefg (i dont remember bro TwT)

"""