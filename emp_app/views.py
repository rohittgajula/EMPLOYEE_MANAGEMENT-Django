from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from datetime import datetime

from django.db.models import Q                            # Q-objects concept 

def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()

    context = {
        'emps':emps
    }
    return render(request, 'view_all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        role = request.POST['role']
        dept = int(request.POST['dept'])

        new_emp =  Employee(first_name=first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, role_id = role, dept_id = dept, hire_date = datetime.now())
        new_emp.save()
        print(new_emp)
        return redirect('/all_emp')
    elif request.method == 'GET':
        return render(request, 'add_emp.html')
    else:
        return HttpResponse("Distraction occured")

def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed  = Employee.objects.get(id = emp_id)
            emp_to_be_removed.delete()
            return redirect('/')
        except:
            return HttpResponse("Please enter a valid EMP ID")

    emps = Employee.objects.all()

    context = {
        'emps':emps
    }
    return render(request, 'remove_emp.html', context)

def filter_emp(request):
    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']

        emps = Employee.objects.all()
                                        # below is formets to be writen.
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:            # icontains is used to filter either using single letter, it maybe upper-case or lower-case
            emps = emps.filter(role__name = role)

        context = {
            'emps':emps
        }

        return render(request, 'view_all_emp.html', context)
    
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse("An exception occured")

    return render(request, 'filter_emp.html', context)

