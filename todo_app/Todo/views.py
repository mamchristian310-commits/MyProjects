from django.shortcuts import render,redirect
from .models import Task
from .form import TaskForm
from django.contrib import messages

# Create your views here.

def task_list(request):
    tasks=Task.objects.all().order_by('-created_at')
    return render(request, 'todo/task_list.html', {'tasks':tasks})

def create_task(request):
    if request.method=='POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form=TaskForm()
    return render(request, 'todo/create_task.html', {'form':form})

def update_task(request, pk):
    task=Task.objects.get(pk=pk)
    if request.method=='POST':
        form=TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form=TaskForm(instance=task)
    return render(request, 'todo/update_task.html', {'form':form})
        
        
def delete_task(request, pk):
    task=Task.objects.get(pk=pk)
    if request.method=='POST':
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('task_list')
    return render(request, 'todo/delete_task.html', {'task':task})

    