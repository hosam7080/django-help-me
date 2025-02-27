from django.db import models

from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import re


from datetime import datetime


class User(AbstractUser):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=255)
	mobile_phone = models.CharField(max_length=11, unique=True)

	#the profile needs (pillow) installed,,, use (python -m pip install Pillow) to get pillow
	profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True) #should change where the to save the pictures are saved

	def clean(self):
		# Custom phone number validation
		if not re.match(r"^(010|011|012|015)\d{8}$", self.mobile_phone):
			raise ValidationError("Phone number must be 11 digits and start with 010, 011, 012, or 015.")
		
	def __str__(self):
		return f'{self.first_name} {self.last_name}'





class Donation(models.Model):
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	donated_by = models.ForeignKey('User', related_name='donations', on_delete=models.SET_NULL, null=True)
	project = models.ForeignKey('Project', related_name='donations', on_delete=models.CASCADE)
	donation_date = models.DateTimeField(auto_now_add=True)
	class Meta:
		verbose_name_plural = "donations"
		ordering = ("donation_date",)

	def __str__(self):
		return 'Donation of {} by {} for project {}'.format(self.amount, self.donated_by, self.project)


class Category(models.Model):
	name = models.CharField(max_length=50,unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	assigned_to = models.ManyToManyField("Project",related_name= 'categories',related_query_name='categories',blank=True)
	class Meta:
		verbose_name_plural = "categories"
		ordering = ("name",)

	def __str__(self):
		return self.name

class Comment(models.Model):
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	#written_by = models.ForeignKey('User',related_name= 'comments', on_delete=models.CASCADE)
	project = models.ForeignKey('Project',related_name='comments',on_delete=models.CASCADE)
	class Meta:
		verbose_name_plural = "comment"
		ordering = ("created_at",)

	def __str__(self):
		return self.content   # هيتمسح بعد كدة دا مؤقتا بس 
		# return self.written_by

class Rate(models.Model):
	rate = models.IntegerField()
	rated_by = models.ForeignKey('User',related_name='rate',on_delete=models.CASCADE)	
	project = models.ForeignKey('Project',related_name='rate',on_delete=models.CASCADE)

	def __str__(self):
		return str(self.rate) # هيتمسح بعد كدة دا مؤقتا بس 
		# return self.rated_by


class Reply(models.Model):
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	written_by = models.ForeignKey('User', related_name='reply', on_delete=models.CASCADE)
	comment = models.ForeignKey('Comment', related_name='reply', on_delete=models.CASCADE)
	class Meta:
		verbose_name_plural = "replies"
		ordering = ("created_at",)

	def __str__(self):
		return self.content 
		# return self.written_by # هيتمسح بعد كدة دا مؤقتا بس 



class Picture(models.Model):
	image = models.ImageField(upload_to='media/')
	created_at = models.DateTimeField(auto_now_add=True)
	project = models.ForeignKey('Project', related_name='pictures', on_delete=models.CASCADE)
	class Meta:
		verbose_name_plural = "pictures"
		ordering = ("project",)

	def __str__(self):
		return self.image.url

class Report(models.Model):

    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name="reported_comments")
    
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reports")
    

    reason = models.TextField(blank=True, null=True)  


    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Report by {self.reported_by} on comment {self.comment.id}"		

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name	


class Project(models.Model):
	title=models.CharField(max_length=255,null=True)
	details=models.TextField(null=True, blank=True)
	created_at=models.DateTimeField(auto_now_add=True,null=True)
	total_target = models.DecimalField(max_digits=10, decimal_places=2,null=True) 
	start_time = models.DateTimeField(null=True)
	end_time = models.DateTimeField(null=True)
	#owner=models.ForeignKey(User,related_name='created_by', on_delete=models.SET_NULL, null=True)
	category = models.ForeignKey(Category, related_name='category', on_delete=models.SET_NULL, null=True)
	tags = models.ManyToManyField(Tag, blank=True, related_name="projects")

	def __str__(self):
		return self.title

