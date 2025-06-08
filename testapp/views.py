# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project, Task
from .forms import TaskForm # We'll define this form next

@login_required # Ensures only logged-in users can access this view
def create_task(request, project_id):
    # 1. Get the Project instance, ensuring it belongs to the logged-in user.
    #    If the project_id doesn't exist or doesn't belong to the user,
    #    get_object_or_404 will raise an Http404 (Not Found).
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # 2. Create the Task instance but DON'T save it to the database yet.
            #    This allows us to set the 'project' foreign key manually.
            task = form.save(commit=False)
            task.project = project # Associate the task with the retrieved project
            task.save() # Now save the task to the database

            # Redirect to the project's detail page or task list
            return redirect('testapp:project_detail', project_id=project.id)
            return redirect('pages:portal-home')
            
    else:
        form = TaskForm()

    return render(request, 'testapp/create_task.html', {
        'form': form,
        'project': project
    })

# Example Project Detail View (for redirection)
@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    tasks = project.tasks.all() # Access tasks related to this project
    return render(request, 'testapp/project_detail.html', {
        'project': project,
        'tasks': tasks
    })