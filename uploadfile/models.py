"""
Owner- Divyanshu (2017CSB1074)

"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import datetime


class COURSE(models.Model):
	# already inbuilt auto increment id
	name = models.CharField(max_length = 100)
	code = models.CharField(max_length = 6)		# enter the code without '-', for eg MAL201 is valid, but MAL-201 is not
	date = models.DateTimeField(default=datetime.now())
	class Meta:
		verbose_name_plural = "courses"

	def __str__(self):
		return str(self.code)


class PAPER(models.Model):
	# already inbuilt auto increment id
	PPR_TYPE = (
		('m', 'Mid Semester'),
		('e', 'End Semester'),
		('q', 'Quiz'),
	)
	paper_type = models.CharField(max_length = 1, choices = PPR_TYPE)
	paper_year = models.CharField(max_length = 4)
	date = models.DateTimeField(default=datetime.now())
	course = models.ForeignKey(
		COURSE,
		on_delete=models.CASCADE,
	)

	class Meta:
		verbose_name_plural = "papers"

	def __str__(self):
		return str(self.course) + '_' + str(self.paper_year) + '_' + str(self.paper_type)


class PAPER_UPLOAD(models.Model):
	# already inbuilt auto increment id
	paper = models.ForeignKey(
		PAPER,
		on_delete=models.CASCADE,
	)
	uploader = models.ForeignKey(
		User,		# use social account to store personal information
		on_delete=models.CASCADE,
	)
	date = models.DateTimeField(default=datetime.now())
	class Meta:
		verbose_name_plural = "paper uploads"

	def __str__(self):
		return str(self.paper) + '_' + str(self.uploader)


class FILE(models.Model):
	# already inbuilt auto increment id
	paper_upload = models.ForeignKey(
		PAPER_UPLOAD,
		on_delete=models.CASCADE,
	)
	file_url = models.CharField(max_length=40)
	file_name = models.CharField(max_length=100)
	date = models.DateTimeField(default=datetime.now())
	class Meta:
		verbose_name_plural = "files"

	def __str__(self):
		return str(self.file_name)