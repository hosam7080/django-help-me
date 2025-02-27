from django.db import models


class User(models.Model):
	pass


class Project(models.Model):
	pass
	# category = models.ForeignKey("Category", related_name='projects', on_delete=models.SET_NULL, null=True)


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
	written_by = models.ForeignKey('User',related_name= 'comments', on_delete=models.CASCADE)
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
