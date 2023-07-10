from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required, user_passes_test

from .models import User, Rfid
from door_user.forms import UserForm, RfidForm

def staff_chek(user):
    return user.is_staff

# Create your views here.
@login_required
def index(request):
    if not request.user.is_staff:
        door_user = get_object_or_404(User, user_name=request.user.username)
        return redirect('hours/'+str(door_user.pk)+'/')

    users = User.objects.all()
    user_data = []
    for user in users:
        user_data.append({'user': user})
    return render(request, 'index.html', {'users': user_data})

@login_required
@user_passes_test(staff_chek, login_url='index')
def create(request):
    form = UserForm(request.POST or None)
    RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=1)
    formset = RfidFormFormset(request.POST or None, queryset=Rfid.objects.none())


    context = {
        "form": form, 
        "formset": formset
    }
    
    if form.is_valid() and formset.is_valid():
        parent = form.save(commit=False)
        parent.save()

        for form in formset:
            if form.has_changed():
                child = form.save(commit=False)
                child.user = parent
                child.save()

        context['message'] = "Updated successfully"
        return redirect(reverse('index'))
    
    return render(request, 'form.html', context)

@login_required
@user_passes_test(staff_chek, login_url='index')
def update(request, id):
    obj = get_object_or_404(User, id=id)
    form = UserForm(request.POST or None, instance=obj)

    RfidFormFormset = modelformset_factory(Rfid, form=RfidForm, extra=0)
    qs = obj.rfid_set.all()
    formset = RfidFormFormset(request.POST or None, queryset=qs)


    context = {
        "form": form, 
        "formset": formset,
        "objct": obj
    }
    
    if form.is_valid() and formset.is_valid():
        parent = form.save(commit=False)
        parent.save()

        for form in formset:
            if form.has_changed():
                child = form.save(commit=False)
                child.user = parent
                child.save()

        context['message'] = "Updated successfully"
        return redirect(reverse('index'))
    
    return render(request, 'form.html', context)

@login_required
@user_passes_test(staff_chek, login_url='index')
def delete(request, pk):
    db = User.objects.get(pk=pk)
    db.delete()
    return redirect('index')

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)