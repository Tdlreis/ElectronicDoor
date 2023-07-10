from .models import User, Punch, HoursWorked
from datetime import datetime
from django.shortcuts import render, redirect
from hours_app.forms import UserForm
from django.core.paginator import Paginator
from django.urls import reverse


def index(request):
    users = User.objects.all()
    user_data = []
    for user in users:
        punches = user.punch_set.all().order_by('punch_time')
        total_hours = 0.0
        in_time = None
        for punch in punches:
            if punch.is_in:
                in_time = punch.punch_time
            else:
                if in_time:
                    out_time = punch.punch_time
                    duration = out_time - in_time
                    total_hours += duration.total_seconds() / 3600
                    in_time = None
        user_data.append({'user': user, 'total_hours': total_hours})
    return render(request, 'index.html', {'users': user_data})


def form(request):

    data = {}
    data['form'] = UserForm()
    return render(request, 'form.html', data)


def create(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse('index'))  # Update the redirect to 'index' view



def edit(request, pk):
    data = {}
    data['db'] = User.objects.get(pk=pk)
    data['form'] = UserForm(instance=data['db'])
    return render(request, 'form.html', data)


def update(request, pk):
    data = {}
    data['db'] = User.objects.get(pk=pk)
    form = UserForm(request.POST or None, instance=data['db'])
    if form.is_valid():
        form.save()
        return redirect('index')


def delete(request, pk):
    db = User.objects.get(pk=pk)
    db.delete()
    return redirect('index')


def detail(request, user_id):
    user = User.objects.get(pk=user_id)
    # Calculate hours worked and update HoursWorked model
    punches = user.punch_set.all().order_by('punch_time')
    total_hours = 0.0
    in_time = None
    for punch in punches:
        if punch.is_in:
            in_time = punch.punch_time
        else:
            if in_time:
                out_time = punch.punch_time
                duration = out_time - in_time
                total_hours += duration.total_seconds() / 3600
                in_time = None

    hours_worked, _ = HoursWorked.objects.get_or_create(user=user)
    hours_worked.hours = total_hours
    hours_worked.save()

    return render(request, 'detail.html', {'user': user, 'total_hours': total_hours})


def punch_in(request, user_id):
    user = User.objects.get(pk=user_id)
    current_time = datetime.now()
    last_punch = user.punch_set.last()

    if not last_punch or not last_punch.is_in:
        Punch.objects.create(user=user, punch_time=current_time, is_in=True)

    return redirect('detail', user_id=user_id)


def punch_out(request, user_id):
    user = User.objects.get(pk=user_id)
    current_time = datetime.now()
    last_punch = user.punch_set.last()

    if last_punch and last_punch.is_in:
        Punch.objects.create(user=user, punch_time=current_time, is_in=False)

        # Calculate hours worked and update HoursWorked model
        punches = user.punch_set.all().order_by('punch_time')
        total_hours = 0.0
        in_time = None
        for punch in punches:
            if punch.is_in:
                in_time = punch.punch_time
            else:
                if in_time:
                    out_time = punch.punch_time
                    duration = out_time - in_time
                    total_hours += duration.total_seconds() / 3600
                    in_time = None

        hours_worked, _ = HoursWorked.objects.get_or_create(user=user)
        hours_worked.hours = total_hours
        hours_worked.save()

    return redirect('detail', user_id=user_id)



