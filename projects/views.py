from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Project
from taggit.models import Tag
from payments.models import Payment
import random

def home(request):
    # Get all projects for the main projects section
    projects = Project.objects.all().order_by('-created_at')[:3]
    
    # Get 2 random projects for the hero section
    all_projects = list(Project.objects.all())
    random_projects = random.sample(all_projects, min(2, len(all_projects)))
    
    context = {
        'projects': projects,
        'random_projects': random_projects
    }
    
    return render(request, 'projects/home.html', context)


def project_list(request):
    # Get all projects with tags preloaded
    
    projects = Project.objects.prefetch_related('tags').all()
    
    # Get all tags
    tags = Tag.objects.all()
    
    # Get selected tag
    selected_tag = request.GET.get('tag')
    
    # Filter projects by tag if selected
    if selected_tag:
        projects = projects.filter(tags__name__in=[selected_tag]).distinct()
    
    context = {
        'projects': projects,
        'tags': tags,
        'selected_tag': selected_tag
    }
    
    return render(request, 'projects/project_list.html', context)


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