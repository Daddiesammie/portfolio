from django.db import models

class Profile(models.Model):
    full_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='resume/profile/')
    about_me = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=200)
    website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

class Education(models.Model):
    EDUCATION_TYPES = [
        ('HIGH_SCHOOL', 'High School'),
        ('BACHELOR', 'Bachelor Degree'),
        ('MASTER', 'Master Degree'),
        ('PHD', 'PhD'),
        ('DIPLOMA', 'Diploma'),
        ('CERTIFICATE', 'Certificate'),
        ('OTHER', 'Other')
    ]
    
    education_type = models.CharField(max_length=20, choices=EDUCATION_TYPES, null=True)
    school = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    field = models.CharField(max_length=200)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    achievements = models.TextField(blank=True)

class Experience(models.Model):
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    achievements = models.TextField(blank=True)
    technologies_used = models.TextField(blank=True)

class TechnicalSkill(models.Model):
    SKILL_CATEGORIES = [
        ('FRONTEND', 'Frontend Development'),
        ('BACKEND', 'Backend Development'),
        ('DATABASE', 'Database'),
        ('DEVOPS', 'DevOps'),
        ('MOBILE', 'Mobile Development'),
        ('OTHER', 'Other')
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES)
    proficiency = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    years_of_experience = models.IntegerField(default=0)

class Language(models.Model):
    PROFICIENCY_LEVELS = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('FLUENT', 'Fluent'),
        ('NATIVE', 'Native')
    ]
    
    name = models.CharField(max_length=100)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_LEVELS)

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technologies = models.TextField()
    url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='resume/projects/', blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True, blank=True)
    highlights = models.TextField(blank=True)

class Certification(models.Model):
    name = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date_obtained = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=200, blank=True)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)

class Award(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200)
    date_received = models.DateField()
    description = models.TextField()

class Reference(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    relationship = models.CharField(max_length=200)
    description = models.TextField(blank=True)
