from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Category
import random
# Create your views here.

category_dict = {
		'Arts & Literature': 'A',
		'Mathematics': 'B',
		'Geography': 'C',
		'History': 'D',
		'Technology': 'E',
		'Music': 'F',
		'Sports': 'G',
		'Entertainment': 'H',
		'Food': 'I',
		'Others': 'J',
		'FFA': 'K',
	}

all_categories = ['Arts & Literature', 'Mathematics', 'Geography', 'History', 'Technology', 'Music', 'Sports', 'Entertainment', 'Food', 'Others', 'Science']

def key_from_value(_dict, value):
	for cat in _dict:
		if _dict[cat] == value:
			return cat

# Return a random question from the corresponding category
# will also add the question_id to the user session
def generate_random_question(response, category):
	category_db = Category.objects.get(category=category)
	# Get all the questions' id in that cateogry
	id_list = category_db.questions.values_list('id', flat=True)
	# Get the randomly selected question id
	question_id = id_list[random.randint(0,len(category_db.questions.all())-1)]
	selected_question = category_db.questions.get(id=question_id)

	# Store the category and question ID in
	response.session['question_id'] = question_id
	response.session['category'] = category

	return selected_question


def home(response):
	return render(response, "main/home.html", {})


# Contribute question to our databse through appending Category.questions model
def create(response):
	if response.method == "POST":
		append_category = Category.objects.get(category=response.POST.get("category"))
		append_category.questions.create(question=response.POST.get("question"), answer=response.POST.get("answer"))
		return render(response, "main/thankyou.html", {})
	return render(response, "main/create.html", {})


# After user selected category and hit play, we get the category and generate room code which redirect us to the room funciton
def play(response):
	if response.method == "POST":
		if response.POST.get("category"):
			if response.POST.get("category") == 'random':
				category = all_categories[random.randint(0,len(all_categories)-1)]
				return render(response, "main/home.html", {})
			else:
				try:
					cur_category = Category.objects.get(category=response.POST.get("category"))
					new_room_number = len(cur_category.room_no.all()) + 1
					cur_category.room_no.create(room_number=new_room_number)
					room_code = category_dict[response.POST.get("category")] + str(new_room_number)
					return redirect(f'room/{room_code}')
				except:
					return render(response, "main/home.html", {})

	return render(response, "main/play.html", {})


def room(response, room_id):
	if response.method == "POST":
		if response.POST.get("submit_answer"):
			user_answer = response.POST.get("submit_answer")
			question_id = response.session['question_id']

			if Question.objects.get(id=question_id).answer == user_answer:
				response.session['score'] += 1
				return render(response, "main/correct.html", {'room_code': response.session['room_code']})
			else:
				print(response.session['room_code'])
				return render(response, "main/incorrect.html", {'answer': Question.objects.get(id=question_id).answer, 'room_code': response.session['room_code']})
		else:
			return render(response, "main/home.html", {})

	else:
		# Reset users score if they changed room
		try:
			if str(response.session['room_code']) == str(room_id): # user is in the same room
				pass
			else:
				response.session['room_code'] = room_id # user changed room
				response.session['score'] = 0

		# if no room code, they are playing their first game
		except:
			response.session['room_code'] = room_id
			response.session['score'] = 0

		# Basically we are picking a random question for them
		category = key_from_value(category_dict, room_id[0])
		selected_question = generate_random_question(response, category)
		return render(response, "main/room.html", {'Question': selected_question.question, 'score': response.session['score']})


# Display all the questions from our questionbank
def questionbank(response, category):
	if category in all_categories:
		all_questions = Category.objects.get(category=category).questions.all()
		return render(response, "main/questionbank.html", {"questions": all_questions, "category": category})
	else:
		return render(response, "main/home.html", {})

# Display search results
def search_result(response):
	query = response.GET.get('query') #the 'query' corresponds to the name attribute of the input form, it will also be shown in url as ?query=xxx
	if query:
		results = Question.objects.filter(question__icontains=query)
	else:
		results=[]
	return render(response, "main/questionbank.html", {"questions": results, "category": 'SEARCH RESULTS'})



# <---------------------------------------------------------------------------------------------------------------------------------------------------->
from .question_db import geography_questions, art_lit_questions, entertainment_questions
from .question_db import food_questions, mathematic_questions, music_questions, history_questions
from .question_db import language_questions, people_and_place_questions, religion_and_mythology_questions
from .question_db import science_questions, sports_questions, toy_and_games_questions, tech_and_videogames_questions

def add_db(response):

	# for cur_question in math_questions:
	# 	cur_cat = Category.objects.get(category='Mathematics')
	# 	cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	for cur_question in geography_questions:
		cur_cat = Category.objects.get(category='Geography')
		cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	for cur_question in (art_lit_questions + language_questions):
		cur_cat = Category.objects.get(category='Arts & Literature')
		cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	for cur_question in mathematic_questions:
		cur_cat = Category.objects.get(category='Mathematics')
		cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	for cur_question in science_questions:
		cur_cat = Category.objects.get(category='Science')
		cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	for cur_question in history_questions:
		cur_cat = Category.objects.get(category='History')
		cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	for cur_question in tech_and_videogames_questions:
		cur_cat = Category.objects.get(category='Technology')
		cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	for cur_question in music_questions:
		cur_cat = Category.objects.get(category='Music')
		cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	for cur_question in sports_questions:
		cur_cat = Category.objects.get(category='Sports')
		cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	for cur_question in (entertainment_questions + toy_and_games_questions):
		cur_cat = Category.objects.get(category='Entertainment')
		cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	for cur_question in food_questions:
		cur_cat = Category.objects.get(category='Food')
		cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	for cur_question in (people_and_place_questions + religion_and_mythology_questions):
		cur_cat = Category.objects.get(category='Others')
		cur_cat.questions.create(question=cur_question['question'], answer=cur_question['answers'][0])

	return render(response, "main/home.html", {})


