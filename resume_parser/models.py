from django.db import models


# Create your models here.
class Candidate(models.Model):
    name=models.CharField(max_length=20,null=True, blank=True)
    number=models.CharField(max_length=25,null=True, blank=True)
    residence=models.TextField(null=True, blank=True)
    email=models.EmailField(null=True, blank=True)
    languages=models.TextField(max_length=50,null=True, blank=True)
    file_path=models.TextField(null=True, blank=True)
    file_txt=models.TextField(null=True, blank=True)


class Document(models.Model):
    pdf = models.FileField(upload_to='resumes/')
    # pdf = models.FileField(upload_to='')
