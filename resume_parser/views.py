from django.shortcuts import render
from resume_parser.core import *
from django.db import models
from resume_parser.models import Candidate, Document
from resume_parser.forms import DocumentForm, FilterForm
import os


def index(request):
    resumes=[]
    resume_txt=''

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(pdf = request.FILES['pdf'])
            newdoc.save()
            print(newdoc.pdf.name)
            # print(newdoc.pdf.size)
            # print(rf"C:\Users\Seif\Desktop\Project - Copy\media\resumes\{newdoc.pdf.name[7:]}")
            # resumes.append(os.path.join(os.getcwd(), f'..\media\{newdoc.pdf.name}'))
            resumes.append(rf"C:\Users\Seif\Desktop\Project - Copy\media\resumes\{newdoc.pdf.name[7:]}")
    else:
        form = DocumentForm()

    for resume in resumes:
        for page in extract_text_from_pdf(resume):
            resume_txt += ' ' + page
        candidate=Candidate()
        candidate.name=name(resume_txt)
        candidate.residence=residence(resume_txt)
        candidate.number=number(resume_txt)
        candidate.email=email(resume_txt)
        candidate.languages=languages(resume_txt)
        candidate.file_path=str(resume[51:])
        candidate.file_txt=resume_txt
        candidate.save()
        resume_txt=''
        candidate=None

    candidates=Candidate.objects.all()
    context={
    "candidates":candidates,
    "len":len(candidates),
    "form":form
    }
    return render(request, 'Index.html', context)

def filter(request):
    form = FilterForm()
    candidates=Candidate.objects.all()
    successful_candidates=[]
    matched_skills=[]


    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            req_skills=(form.cleaned_data['skills'].replace(","," ")).split()
            for candidate in candidates:
                if match_skills(candidate.file_txt,req_skills) != None:
                    successful_candidates.append(candidate)
                    matched_skills.append(match_skills(candidate.file_txt,req_skills))
    output=dict(zip(successful_candidates,matched_skills))
    context={
    "form":form,
    # "candidates":successful_candidates,
    # "skills":matched_skills,
    "len":len(successful_candidates),
    "output":output,
    }
    return render(request, "Filter.html", context)
