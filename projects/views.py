from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from taggit.models import Tag
from payments.models import Payment

def home(request):
    projects = Project.objects.all().order_by('-created_at')[:3]
    return render(request, 'projects/home.html', {'projects': projects})

def project_list(request):
    projects = Project.objects.all().order_by('-created_at')
    tags = Tag.objects.all()
    selected_tag = request.GET.get('tag')
    if selected_tag:
        projects = projects.filter(tags__name=selected_tag)
    return render(request, 'projects/project_list.html', {'projects': projects, 'tags': tags, 'selected_tag': selected_tag})

@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user_has_paid = Payment.objects.filter(user=request.user, project=project, status='success').exists()
    return render(request, 'projects/project_detail.html', {'project': project, 'user_has_paid': user_has_paid})

@login_required
def download_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.is_paid:
        # Check if user has purchased the project
        # For now, we'll just allow the download
        pass
    # Logic for secure file download
    # For now, we'll just redirect to the file URL
    return redirect(project.file.url)