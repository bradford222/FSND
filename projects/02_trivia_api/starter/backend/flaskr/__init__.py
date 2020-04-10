import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func, select
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    @app.route('/categories', methods=['GET'])
    def retrieve_categories():
        categories = Category.query.order_by(Category.id).all()
        categories_formatted = [category.type for category in categories]

        if len(categories) == 0:
            abort(404)

        return jsonify({
          'success': True,
          'categories': categories_formatted,
        })

    @app.route('/questions', methods=['GET'])
    def retrieve_questions():

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.order_by(Category.id).all()
        categories_formatted = [category.type for category in categories]

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(Question.query.all()),
            'categories': categories_formatted
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id)\
                                    .one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })

        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_or_search_questions():
        body = request.get_json()

        # Check if this is a search or a question add. The front end was
        # written to make these use the same endpoint
        # and the same method type. These should have used different endpoints.
        search_string = request.get_json().get('searchTerm', None)

        if search_string is not None:
            selection = Question.query.filter(Question.question.ilike("%" +
                                              search_string + "%"))\
                                              .order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            categories = Category.query.order_by(Category.id).all()
            categories_formatted = [category.type for category in categories]

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'categories': categories_formatted
            })
        else:
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_difficulty = body.get('difficulty', None)
            new_category = body.get('category', None)

            try:
                question = Question(question=new_question,
                                    answer=new_answer,
                                    category=new_category,
                                    difficulty=new_difficulty)

                question.insert()

                return jsonify({
                    'success': True,
                    'created': question.id,
                })

            except:
                abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def retrieve_questions_for_category(category_id):

        selection = Question.query.filter(
                            Question.category == category_id)\
                            .order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        categories = Category.query.order_by(Category.type).all()
        categories_formatted = [category.type for category in categories]

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': categories_formatted,
            'current_category': category_id
        })

    @app.route('/quizzes', methods=['POST'])
    def quiz_for_category():
        body = request.get_json()
        previous_questions = body.get('previous_questions', [])
        category = body.get('quiz_category')
        category_id = category.get('id')
        category_type = category.get('type')

        try:
            # click means show questions from all categories
            if category_type == 'click':
                question = Question.query.filter(
                              Question.id.notin_(previous_questions))\
                              .order_by(func.random()).first()
            else:
                question = Question.query.filter(
                          Question.category == category_id)\
                              .filter(Question.id.notin_(previous_questions))\
                              .order_by(func.random()).first()

            result = {
                'success': True,
                'quiz_category': category
            }

            if question:
                result['question'] = question.format()

            return jsonify(result)
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 400

    return app
