import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
	# Create and configure the app
	app = Flask(__name__)
	setup_db(app)

	'''
	Set up CORS. Allow '*' for origins.
	'''
	CORS(app)

	'''
	Use the after_request decorator to set Access-Control-Allow
	'''
	@app.after_request
	def after_request(response):
		response.headers.add(
			'Access-Control-Allow-Headers',
			'Content-Type,Authorization,true'
			)
		response.headers.add(
			'Access-Control-Allow-Methods',
			'GET,PUT,POST,DELETE,OPTIONS'
			)
		return response

	'''
	Create an endpoint to handle GET requests
	for all available categories.
	'''
	@app.route('/categories')
	def retrieve_categories():
		try:
			# Retrieve all categories
			categories = Category.query.order_by(Category.id).all()

			# No categories found
			if not len(categories):
				abort(404)

			# Return a dictionary of categories in key:value format
			return jsonify({
				'success': True,
				'categories': {category.id: category.type for category in categories}
			})
		except Exception:
			abort(422)

	'''
	Helper funtion for paginating questions
	'''
	def paginate_questions(request, selection):
		page = request.args.get('page', 1, type=int)
		start = (page - 1) * QUESTIONS_PER_PAGE
		end = start + QUESTIONS_PER_PAGE

		questions = [question.format() for question in selection]
		current_questiosns = questions[start:end]

		return current_questiosns

	'''
	Create an endpoint to handle GET requests for questions,
	including pagination (every 10 questions).
	This endpoint should return a list of questions,
	number of total questions, current category, categories.

	TEST: At this point, when you start the application
	you should see questions and categories generated,
	ten questions per page and pagination at the bottom
	of the screen for three pages.
	Clicking on the page numbers should update the questions.
	'''
	@app.route('/questions')
	def retrieve_questions():
		try:
			# Retrieve all questions
			questions = Question.query.order_by(Question.id).all()
			current_questions = paginate_questions(request, questions)

			# Retrieve all categories
			categories = Category.query.order_by(Category.id).all()

			# Count the number of questions in each category
			current_category = [question['category'] for question in current_questions]

			# No questions found
			if not len(current_questions):
				abort(404)

			# Return questions and categories
			return jsonify({
				'success': True,
				'questions': current_questions,
				'total_questions': len(questions),
				'categories': {category.id: category.type for category in categories},
				'current_category': current_category
			})
		except:
			abort(422)

	'''
	Create an endpoint to DELETE question using a question ID.

	TEST: When you click the trash icon next to a question,
	the question will be removed.
	This removal will persist in the database and when you refresh the page.
	'''
	@app.route('/questions/<int:question_id>', methods=['DELETE'])
	def delete_question(question_id):
		try:
			# Retrieve the question given the question id
			question = Question.query.filter(Question.id == question_id).one_or_none()

			# Question not found
			if not question:
				abort(404)

			# Delete the question
			question.delete()

			# Return response of action performed
			return jsonify({
				'success': True,
				'deleted': question_id
			})
		except:
			abort(422)

	'''
	Create an endpoint to POST a new question,
	which will require the question and answer text,
	category, and difficulty score.

	TEST: When you submit a question on the "Add" tab,
	the form will clear and the question will appear at the end of the last page
	of the questions list in the "List" tab.
	'''
	@app.route('/questions', methods=['POST'])
	def create_question():
		try:
			# Retrieve question values from user request
			body = request.get_json()

			# Create a new question
			question = Question(**body)

			# Insert the newly created question into repository
			question.insert()

			# Return response of action performed
			return jsonify({
				'success': True,
				'created': question.id,
			})
		except:
			abort(422)

	'''
	Create a POST endpoint to get questions based on a search term.
	It should return any questions for whom the search term
	is a substring of the question.

	TEST: Search by any phrase. The questions list will update to include
	only question that include that string within their question.
	Try using the word "title" to start.
	'''
	@app.route('/questions/search', methods=['POST'])
	def search_questions():
		try:
			# Retrieve search term from user request
			body = request.get_json()
			search_term = body.get('searchTerm', None)

			# Search term found
			if search_term:
				# Retrieve questions that match the search term
				search_results = Question.query.filter(
					Question.question.ilike(f'%{search_term}%')
					).all()
				# Return quetions and count of questions in each category
				return jsonify({
					'success': True,
					'questions': [question.format() for question in search_results],
					'total_questions': len(search_results),
					'current_category': [
						question.format()['category'] for question in search_results
						]
				})
			else:
				abort(404)
		except:
			abort(422)

	'''
	Create a GET endpoint to get questions based on category.

	TEST: In the "List" tab / main screen, clicking on one of the
	categories in the left column will cause only questions of that
	category to be shown.
	'''
	@app.route('/categories/<int:category_id>/questions')
	def retrieve_questions_by_category(category_id):
		try:
			# Retrieve questions given the category id
			questions = Question.query.filter(
				Question.category == str(category_id)
				).all()

			# Retrieve the category type given id
			category_type = Category.query.filter(
				Category.id == category_id
				).one_or_none().type

			# No matches found
			if not questions:
				abort(404)

			# Return questions that matched the given category id and its type
			return jsonify({
				'success': True,
				'questions': [question.format() for question in questions],
				'total_questions': len(questions),
				'current_category': category_type
			})
		except:
			abort(404)

	'''
	Create a POST endpoint to get questions to play the quiz.
	This endpoint should take category and previous question parameters
	and return a random questions within the given category,
	if provided, and that is not one of the previous questions.

	TEST: In the "Play" tab, after a user selects "All" or a category,
	one question at a time is displayed, the user is allowed to answer
	and shown whether they were correct or not.
	'''
	@app.route('/quizzes', methods=['POST'])
	def retrieve_quiz():
		try:
			# Retrieve previous questions and category from user request
			body = request.get_json()
			previous_questions = body.get('previous_questions', [])
			quiz_category = body.get('quiz_category', None)

			# No category or previous questions found
			if not(quiz_category or previous_questions):
				abort(400)
			else:  # Category or previous questions found
				if not(quiz_category['id']):  # All categories selected
					total_questions = Question.query.all()  # Retrieve all questions
				else:  # Retrieve questions given the category id
					total_questions = Question.query.filter_by(
						category=quiz_category['id']
						).all()

			# Find questions that are not in previous questions
			available_questions = [
				question for question in total_questions
				if question.id not in previous_questions
				]
			# Choose a random question if any
			random_question = (
				available_questions[random.randrange(0, len(available_questions), 1)]
				if len(available_questions) else None
				)

			# Return the random chosen question
			return jsonify({
				'success': True,
				'question': random_question.format()
			})
		except:
			abort(422)

	'''
	Create error handlers for all expected errors
	including 404 and 422.
	'''
	@app.errorhandler(404)
	def not_found(error):
		return jsonify({
			'success': False,
			'error': 404,
			'message': 'resource not found'
		}), 404

	@app.errorhandler(422)
	def unprocessable(error):
		return jsonify({
			'success': False,
			'error': 422,
			'message': 'unprocessable'
		}), 422

	@app.errorhandler(400)
	def bad_request(error):
		return jsonify({
			'success': False,
			'error': 400,
			'message': 'bad request'
		}), 400

	@app.errorhandler(405)
	def not_found(error):
		return jsonify({
			'success': False,
			'error': 405,
			'message': 'method not found'
		}), 405

	return app
