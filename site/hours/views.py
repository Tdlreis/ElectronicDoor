from django.shortcuts import render, get_object_or_404, redirect
from door_user.models import PunchCard, User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import timedelta
import locale

def is_the_user(user, id):
    try:
        door_user = User.objects.get(pk=id)
        if user.username != door_user.user_name:
            return False
        else:
            return True
    except User.DoesNotExist:
        return False
        
@login_required
def hours(request, id):
    if not is_the_user(request.user, id):
        return redirect('index')
    data = []
    try:
        punch_cards = PunchCard.objects.filter(user=id, punch_out_time__isnull=False)
        start_date = punch_cards.earliest('punch_in_time').punch_in_time.date()
        end_date = punch_cards.latest('punch_in_time').punch_in_time.date()

        current_date = start_date

        while current_date <= end_date:
            next_date = current_date + timedelta(days=7)
            time = PunchCard.objects.filter(user=id, punch_in_time__range=[current_date, next_date], punch_out_time__isnull=False)
            hour = 0
            for t in time:
                hour = hour + (t.punch_out_time - t.punch_in_time).total_seconds() / 3600
            values = {
                'start': current_date,
                'end': next_date,
                'hours': hour.__round__(3),
            }
            current_date = next_date + timedelta(days=1)
            data.append(values)

        data.reverse()
        context = {
            'data': data,
            'user': id
        }
    except PunchCard.DoesNotExist:
        context = {
            'data': data,
            'user': id
        }
        pass

    return render(request, 'hours.html', context)

@login_required
def get_data(request, cat, id):
    if not is_the_user(request.user, id):
        return redirect('index')
    punch_cards = PunchCard.objects.filter(user=id, punch_out_time__isnull=False)
    start_date = punch_cards.earliest('punch_in_time').punch_in_time.date()
    end_date = punch_cards.latest('punch_in_time').punch_in_time.date()
       
    current_date = start_date
    data = []

    locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    if cat == 3:
        for p in punch_cards:
            if p.reviw == True:
                validado = "Sim",
            else:
                validado =  "Não",
            values = {
                'in': p.punch_in_time.strftime('%H:%M do dia %d de %B de %Y'),
                'out': p.punch_out_time.strftime('%H:%M do dia %d de %B de %Y'),
                'validated': validado,
            }
            data.append(values)
        data.reverse()
    else:
        while current_date <= end_date:
            if cat == 0:
                next_date = current_date + timedelta(days=30)
            elif cat == 1:
                next_date = current_date + timedelta(days=1)
            elif cat == 2:
                next_date = current_date + timedelta(days=365)
            time = PunchCard.objects.filter(user=id, punch_in_time__range=[current_date, next_date], punch_out_time__isnull=False)
            hour = 0
            for t in time:
                hour = hour + (t.punch_out_time - t.punch_in_time).total_seconds() / 3600
            values = {
                'start': current_date.strftime('%d de %B de %Y'),
                'end': next_date.strftime('%d de %B de %Y'),
                'hours': hour.__round__(3),
            }
            current_date = next_date + timedelta(days=1)
            data.append(values)
        data.reverse()

    
    return JsonResponse({'data': data})