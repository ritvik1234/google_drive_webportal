from django.contrib import admin
from uploadfile.models import COURSE, PAPER, PAPER_UPLOAD, FILE

# Register your models here.

admin.site.register(COURSE)
admin.site.register(PAPER)
admin.site.register(PAPER_UPLOAD)
admin.site.register(FILE)