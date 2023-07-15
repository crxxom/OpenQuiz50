from django.db import models

# Create your models here.

class Category(models.Model):
	category = models.CharField(max_length=100)

	def __str__(self):
		return self.category

class Question(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
	question = models.CharField(max_length=300)
	answer = models.CharField(max_length=300)

	def __str__(self):
		return self.question

class Room(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='room_no')
	room_number = models.IntegerField()

	def __str__(self):
		return str(self.category) + str(self.room_number)


