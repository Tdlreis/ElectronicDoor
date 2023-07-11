from django.shortcuts import render
from door_user.models import PunchCard
from hours.views import format_hour
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from door_user.views import staff_chek

# Create your views here.
@login_required
@user_passes_test(staff_chek, login_url='index')
def validation(request):
    data = []
    try:
        nonValidated = PunchCard.objects.filter(punch_out_time__isnull=False, reviw=False).order_by('punch_in_time')
        for n in nonValidated:
            values = {
                'name': n.user.user_name,
                'in': n.punch_in_time,
                'out': n.punch_out_time,
                'hours': format_hour((n.punch_out_time - n.punch_in_time).total_seconds()),
                'id': n.pk,
            }
            print(values)
            data.append(values)
        context = {
            'data': data,
        }
    except PunchCard.DoesNotExist:
        context = {
            'data': data
        }
        pass

    return render(request, 'validation.html', context)

@login_required
@user_passes_test(staff_chek, login_url='index')
def validate(request, id):
    punch_card = PunchCard.objects.get(id=id)
    punch_card.reviw = True
    punch_card.save()

    return JsonResponse({'success': True})