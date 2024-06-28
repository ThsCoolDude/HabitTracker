from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, HabitRecord
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from datetime import timedelta
from django.contrib.auth import logout
from django.views import View

class logout_view(View):
    def get(self, request, *args, **kwargs):
            logout(request)
            return redirect('login')



@login_required
def habit_list(request):
    if request.method == 'POST':
        for habit_id in request.POST.getlist('habits'):
            habit = Habit.objects.get(id=habit_id, user=request.user)
            date = timezone.now().date()
            record, created = HabitRecord.objects.get_or_create(habit=habit, date=date)
            record.completed = True
            record.save()
        return redirect('habit_list')
    
    habits = Habit.objects.filter(user=request.user)
    today_records = HabitRecord.objects.filter(habit__in=habits, date=timezone.now().date())
    completed_habits = [record.habit.id for record in today_records]

    # Prepare data for the chart
    days = []
    habit_records = []

    # Collect data for the past 7 days
    for i in range(7):
        day = timezone.now().date() - timedelta(days=i)
        days.append(day.strftime("%Y-%m-%d"))
        
        # Calculate the consistency for the day
        daily_completed = 0
        for habit in habits:
            record = HabitRecord.objects.filter(habit=habit, date=day).first()
            if record and record.completed:
                daily_completed += 1

        # Normalize the consistency (0 to 1)
        if habits.count() > 0:
            normalized_value = daily_completed / habits.count()
        else:
            normalized_value = 0

        habit_records.append(normalized_value)
    
    days.reverse()  # To have the oldest date first
    habit_records.reverse()

    return render(request, 'habits/habit_list.html', {
        'habits': habits,
        'completed_habits': completed_habits,
        'days': json.dumps(days),
        'habit_records': json.dumps(habit_records),
    })


@login_required
def habit_detail(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)
    records = HabitRecord.objects.filter(habit=habit).order_by('-date')
    return render(request, 'habits/habit_detail.html', {'habit': habit, 'records': records})

@login_required
def add_habit(request):
    if request.method == 'POST':
        name = request.POST['name']
        habit = Habit.objects.create(name=name, user=request.user)
        return redirect('habit_list')
    return render(request, 'habits/add_habit.html')

@login_required
def record_habit(request, habit_id):
    habit = Habit.objects.get(id=habit_id, user=request.user)
    date = timezone.now().date()
    record, created = HabitRecord.objects.get_or_create(habit=habit, date=date)
    record.completed = not record.completed
    record.save()
    return redirect('habit_detail', habit_id=habit_id)

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    if request.method == 'POST':
        habit.delete()
        return redirect('habit_list')
    return render(request, 'habits/confirm_delete.html', {'habit': habit})