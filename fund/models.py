from django.db import models


class User(models.Model):
	pass


class Project(models.Model):
	pass
	# category = models.ForeignKey("Category", related_name='projects', on_delete=models.SET_NULL, null=True)


class Donation(models.Model):
	pass


class Category(models.Model):
	pass


class Comment(models.Model):
	pass
	# user = models.ForeignKey("User", related_name='comments', on_delete=models.CASCADE)
