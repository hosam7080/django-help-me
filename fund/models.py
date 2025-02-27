from django.db import models
from datetime import datetime

class User(models.Model):
	pass





class Donation(models.Model):
	pass


class Category(models.Model):
	name=models.CharField(max_length=50,unique=True)
	created_at=models.DateTimeField(auto_now_add=True)
	assigned_to=models.ManyToManyField("Project",related_name= 'categories',related_query_name='categories',blank=True)
	class Meta:
		verbose_name_plural="categories"
		ordering=("name",)
	def __str__(self):
		return self.name

class Comment(models.Model):
	content= models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	#written_by = models.ForeignKey('User',related_name= 'comments', on_delete=models.CASCADE)
	project = models.ForeignKey('Project',related_name='comments',on_delete=models.CASCADE)
	class Meta:
		verbose_name_plural="comment"
		ordering=("created_at",)
	def __str__(self):
		return self.content   # هيتمسح بعد كدة دا مؤقتا بس 
		# return self.written_by

class Rate(models.Model):
	rate=models.IntegerField()
	rated_by=models.ForeignKey('User',related_name='rate',on_delete=models.CASCADE)	
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
		verbose_name_plural="replies"
		ordering=("created_at",)
	def __str__(self):
		return self.content 
		# return self.written_by # هيتمسح بعد كدة دا مؤقتا بس 


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
