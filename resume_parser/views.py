from django.shortcuts import render
from resume_parser.core import *
from django.db import models
from resume_parser.models import Candidate, Document
from resume_parser.forms import DocumentForm, FilterForm
import os


def index(request):
    resumes=[]
    resume_txt=''

    #File Upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(pdf = request.FILES['pdf'])
            newdoc.save()
            media = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/media/"
            resume_path=os.path.join(media,newdoc.pdf.name)
            resumes.append(resume_path.replace("\\","/"))
    else:
        form = DocumentForm()
    #NLP
    for resume in resumes:
        for page in extract_text_from_pdf(resume):
            resume_txt += ' ' + page
        candidate=Candidate()
        candidate.name=name(resume_txt)
        candidate.residence=residence(resume_txt)
        candidate.number=number(resume_txt)
        candidate.email=email(resume_txt)
        candidate.languages=languages(resume_txt)
        candidate.file_path=resume
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
    matched_candidates=[]
    matched_skills=[]
    #Filter Input and NLP
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            req_skills=(form.cleaned_data['skills'].replace(","," ")).split()
            for candidate in candidates:
                if match_skills(candidate.file_txt,req_skills) != None:
                    matched_candidates.append(candidate)
                    matched_skills.append(match_skills(candidate.file_txt,req_skills))

    l=len(matched_candidates)
    output=dict(zip(matched_candidates,matched_skills))

    context={
    "form":form,
    "len":len(candidates),
    "output":output,
    "l":l
    }
    return render(request, "Filter.html", context)
