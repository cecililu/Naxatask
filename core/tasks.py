
from datetime import datetime

from django.utils import timezone

from core.models import SystemSummary


from celery import Celery, shared_task

from core.models import Project

from django.contrib.auth.models import User

from celery.schedules import crontab
 

def get_total_projects():
    return Project.objects.count()


def get_total_user():
    return Project.objects.user()


@shared_task(max_retries=1)
def update_system_summary():
    print("running update........summarry")
    try:
        print('run------------------------------------')
        now = timezone.now()
        year = now.year
        month = now.month
        summary = SystemSummary.objects.create(year=year, month=month)
        summary.total_projects = get_total_projects() # Replace this with your own function to get the total number of projects
        summary.total_users = get_total_user() # Replace this with your own function to get the total number of users
        # Update other summary fields here as needed
        summary.save()
        return "sulccessful"
    except Exception as e:
        return "error"+str(e)


import random  
from datetime import date, timedelta

from core.models import *


@shared_task(max_retries=1)
def add_data():
    for i in range(100000):
        project = Project()
        project.name = 'Project {}'.format(i+1)
        project.time_started = date.today() - timedelta(days=random.randint(0, 1825))
        project.owner = random.choice(Owner.objects.all())
        # project.site_polygon = 'POLYGON((0 0, 0 10, 10 10, 10 0, 0 0))'
        project.created_by = random.choice(User.objects.all())
        project.is_active = random.choice([True, False])
        project.department = random.choice(Department.objects.all())
        
        project.deadline = date.today()+ timedelta(days=random.randint(30, 365))
        project.manpower = random.randint(1, 50)
        project.save()


@shared_task(max_retries=1)
def set_data():
    queryset=Project.objects.all()
    for project in queryset:
        print('seting-active status')
        if project.deadline < date.today():
            project.is_active = False
        else:
            project.is_active = True
        project.save()
    

from django.db.models.functions import TruncWeek
from django.db.models import Count


@shared_task(max_retries=1)
def group_projects_by_week():
    # Get the projects grouped by their week of creation
    projects_by_week = Project.objects.annotate(
        week=TruncWeek('deadline')
    ).values('week').annotate(count=Count('id'))
    
    # Create a dictionary to store the results
    results = {}
    # Iterate through each week and add the count to the results dictionary
    for week in projects_by_week:
       
        m=int(week['week'].strftime('%m'))
        yweek=int(week['week'].strftime('%W'))
        
        
        mweek=yweek/(m*4)
        week_number = week['week'].strftime('%B_week_%W')
        count = week['count']
        results[week_number] = count
    return results