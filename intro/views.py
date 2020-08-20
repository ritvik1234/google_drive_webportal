from django.shortcuts import render
from uploadfile.models import COURSE
from uploadfile.models import FILE
from django.shortcuts import redirect

def index(request):
    data = COURSE.objects.all()
    files = {
       "courses" : data,
       "user" : request.user
       }
    return render(request,"intro/homeintro.html",files)

def course(request):
   if request.method == 'GET':
      c_name = (request.GET.get('course')).lower()
      data = FILE.objects.filter(paper_upload__paper__course__code = c_name)
      infos = {
         "files" : data,
         "user" : request.user,
         "course" : c_name
      }
      return render(request,"intro/course_papers.html",infos)
   else:
      return redirect('/')
