from django.shortcuts import render
from .models import (
    Profile, Education, Experience, TechnicalSkill, 
    Language, Project, Certification, Award, Reference
)

def resume(request):
    context = {
        'profile': Profile.objects.first(),
        'education': Education.objects.all().order_by('-end_date'),
        'experience': Experience.objects.all().order_by('-start_date'),
        'technical_skills': TechnicalSkill.objects.all().order_by('category'),
        'languages': Language.objects.all(),
        'projects': Project.objects.all().order_by('-start_date'),
        'certifications': Certification.objects.all().order_by('-date_obtained'),
        'awards': Award.objects.all().order_by('-date_received'),
        'references': Reference.objects.all()
    }
    return render(request, 'resume/resume.html', context)
