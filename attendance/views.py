from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Attendance, Break
from django.utils.timezone import now
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404
from django.forms import ModelForm, DateTimeInput
from django.forms import modelformset_factory, DateTimeInput

@login_required
def dashboard(request):
    today = timezone.localdate()
    attendance, _ = Attendance.objects.get_or_create(user=request.user, date=today)
    breaks = Break.objects.filter(attendance=attendance)
    return render(request, 'attendance/dashboard.html', {
        'attendance': attendance,
        'breaks': breaks,
        'now': now(),
    })

@login_required
def clock_in(request):
    attendance, _ = Attendance.objects.get_or_create(user=request.user, date=timezone.localdate())
    if not attendance.clock_in:
        attendance.clock_in = timezone.now()
        attendance.save()
    return redirect('dashboard')

@login_required
def clock_out(request):
    attendance, _ = Attendance.objects.get_or_create(user=request.user, date=timezone.localdate())
    if not attendance.clock_out:
        attendance.clock_out = timezone.now()
        attendance.save()
    return redirect('dashboard')

@login_required
def break_start(request):
    attendance, _ = Attendance.objects.get_or_create(user=request.user, date=timezone.localdate())
    Break.objects.create(attendance=attendance, start=timezone.now())
    return redirect('dashboard')

@login_required
def break_end(request):
    attendance, _ = Attendance.objects.get_or_create(user=request.user, date=timezone.localdate())
    latest_break = Break.objects.filter(attendance=attendance, end__isnull=True).last()
    if latest_break:
        latest_break.end = timezone.now()
        latest_break.save()
    return redirect('dashboard')

@login_required
def history(request):
    attendances = Attendance.objects.filter(user=request.user).order_by('-date')
    return render(request, 'attendance/history.html', {
        'attendances': attendances
    })

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ['clock_in', 'clock_out']
        widgets = {
            'clock_in': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'clock_out': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

@login_required
def edit_attendance(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk, user=request.user)
    form = AttendanceForm(request.POST or None, instance=attendance)

    queryset = Break.objects.filter(attendance=attendance)
    formset = BreakFormSet(request.POST or None, queryset=queryset)

    if request.method == 'POST':
        print("POST受信")
        print("form valid:", form.is_valid())
        print("formset valid:", formset.is_valid())
        if form.is_valid() and formset.is_valid():
            form.save()
            breaks = formset.save(commit=False)
            for b in breaks:
                b.attendance = attendance
                b.save()
            for obj in formset.deleted_objects:
                obj.delete()
            return redirect('history')

    return render(request, 'attendance/edit_attendance.html', {
    'form': form,
    'formset': formset,
    'attendance': attendance,
    'form_errors': form.errors,
    'formset_errors': formset.errors,
    })



BreakFormSet = modelformset_factory(
    Break,
    fields=('start', 'end'),
    widgets={
        'start': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        'end': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
    },
    extra=0,
    can_delete=True
)