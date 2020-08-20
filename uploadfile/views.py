from __future__ import print_function
import os

from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload
from django.shortcuts import render
from uploadfile.models import COURSE, PAPER, FILE, PAPER_UPLOAD
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime

@login_required(login_url='/accounts/google/login/?process=login&next=%2Fupload%2F')
def upindex(request):
    return render(request,"uploadfile/home.html",{"islogin" : request.user})

def uploadtask(request):
    if request.method == 'POST':
        """
        Request is what the client is sending to the user.
        A POST request means the client is POSTing or trying to WRITE in the server.
        """
        code = str(request.POST.get('course_code')).lower()
        course_data = COURSE.objects.filter(code = code).first()
        if not course_data :
            course_data = COURSE( name = str(request.POST.get('course_name')).lower(),
                code = code )
            course_data.save()
        else:
            course_data.date = datetime.now()
            course_data.save()

        paper_data = PAPER( paper_type = str(request.POST.get('paper_type')).lower(),
            paper_year = str(request.POST.get('paper_year')).lower(),
            course = course_data )
        paper_data.save()

        paper_upload_data = PAPER_UPLOAD( paper = paper_data,
            uploader = request.user )        # 02/01/2019
        paper_upload_data.save()

        # If the form is submitted
        # This is the API set up thing
        SCOPES = "https://www.googleapis.com/auth/drive"
        store = file.Storage('credentials.json')
        creds = store.get()
        flags = tools.argparser.parse_args(args=[])
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            creds = tools.run_flow(flow, store, flags)

        # since v3 does not support parents, i had to switch back to v2. To use v3, we need to use files.list to get the folder where
        # we want to upload the file (must be public folder)
        service = discovery.build('drive', 'v2', http=creds.authorize(Http())) 

        # In settings.py I have added a line FILE_UPLOAD_MAX_MEMORY_SIZE = 0, by this all files added as Temporary files
        # As in a temporary file is created for each upload
        # Get the temporary uploaded file, request.FILES contain all the files in the request stream, in the form, the file was named myfile
        to_upload = request.FILES.get('myfile')   
        file_metadata = {'title': course_data.code+'_'+paper_data.paper_year+'_'+paper_data.paper_type,
        'parents': [{'id': '1t2xyHEJ6U7z-e59e6m4Ao4gGTNOc9YHD'}]}

        # temporary file path and content_type are methods
        # Temporary files have an attritube temporary_file_path which returns the file path for the temporary file
        media = MediaFileUpload(to_upload.temporary_file_path(),mimetype=to_upload.content_type)
        filee = service.files().insert(body=file_metadata,media_body=media,fields='id').execute()

        # Close the file
        to_upload.close()

        file_data = FILE(paper_upload = paper_upload_data,
            file_url = filee.get('id'), # Retrieve the ID
            file_name = course_data.code+'_'+paper_data.paper_year+'_'+paper_data.paper_type)
        file_data.save()

        return render(request,'uploadfile/basic.html',{"display" : filee.get('id')})

    else:
        return render(request,'uploadfile/home.html',{})