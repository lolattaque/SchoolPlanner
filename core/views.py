from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from .ai import generate_ai_suggestions
from django.db.models import Case, When, Value, IntegerField

def welcome(request):
    return render(request, "core/welcome.html")

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        stage = request.POST.get('stage')  # HS or UNI
        if form.is_valid():
            user = form.save()
            user.profile.stage = stage
            user.profile.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, "core/signup.html", {"form": form})

@login_required
def dashboard(request):
    profile = request.user.profile

    if request.method == "POST" and 'update_program' in request.POST:
        profile.target_program = request.POST.get('target_program')
        profile.save()
        return redirect('dashboard')

    if request.method == "POST" and 'add_task' in request.POST:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.stage = profile.stage
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()

    tasks = Task.objects.filter(user=request.user, stage=profile.stage).order_by('completed', 'due_date')
    active_tasks = tasks.filter(completed=False)
    suggestions = generate_ai_suggestions(active_tasks, request.user)

    return render(request, "core/dashboard.html", {
        "tasks": tasks,
        "form": form,
        "suggestions": suggestions,
        "profile": profile,
        "stage": profile.get_stage_display(),
    })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.completed = True
        task.save()
    return redirect('dashboard')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
    return redirect('dashboard')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    return render(request, "core/edit_task.html", {"form": form, "task": task})
