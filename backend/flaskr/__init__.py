
from flask import Flask, request, abort, jsonify
from sqlalchemy.sql import text

from models import setup_db, Question, Category
from flask_cors import CORS


QUESTIONS_PER_PAGE = 10


def paginate_questions(request, question_list):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    formatted_questions = [question.format() for question in question_list]
    return formatted_questions[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        return response


    @app.errorhandler(404)
    def page_not_found(e):
        response = {
            "error": "Not Found",
            "message": "The requested resource could not be found.",
            "status_code": 404
        }
        return jsonify(response), 404


    @app.errorhandler(500)
    def internal_server_error(e):
        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred on the server.",
            "status_code": 500
        }
        return jsonify(response), 500

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route("/trivia/v1/categories", methods=['GET'])
    def find_all_categories():
        categories = Category.query.all()
        dict = {}
        for cate in categories:
            dict[cate.id] = cate.type
        return jsonify({
            'categories' : dict
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """


    @app.route("/trivia/v1/questions", methods=["GET"])
    def find_all_question():

        questions = Question.query.order_by(Question.id).all()
        totalQuestions = len(questions)
        questions_list = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.id).all()
        dict = {}
        for cate in categories:
            dict[cate.id] = cate.type

        # currentCategory
        return jsonify({
            'questions': questions_list,
            'totalQuestions': totalQuestions,
            'categories': dict
        }), 200

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route("/trivia/v1/questions/<question_id>", methods=["DELETE"])
    def delete_qes_by_id(question_id):
        try:
            question = Question.query.filter_by(id=question_id).first()
            question.delete()
        except Exception as e:
            return jsonify({
                'message': "Delete question error"
            }), 500
        return jsonify({
            'message': "Delete question successfully"
        }), 200

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route("/trivia/v1/questions", methods=["POST"])
    def add_question():
        try:
            question_text = request.json['question']
            answer = request.json['answer']
            category = request.json['category']
            difficulty = request.json['difficulty']
            if question_text == None or question_text == '':
                return jsonify({
                    "message": "Create question error"
                }), 500
            question = Question(question_text, answer, category, difficulty)
            question.insert()
            return jsonify({
                "message": "Create question successfully"
            }), 201
        except Exception as e:
            print(e)
            return jsonify({
                "message": "Create question error"
            }), 500

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/trivia/v1/quizzes", methods=["POST"])
    def get_next_question():
        try:
            all_category = Category.query.all()

            previous_questions = request.json['previous_questions']
            quiz_category = request.json['quiz_category']
            print("quiz_category: ", quiz_category)
            if quiz_category['id'] == 0:
                questions = Question.query.filter(Question.id.notin_(previous_questions)).all()
            else:
                questions = Question.query.filter(Question.id.notin_(previous_questions),
                     Question.category == quiz_category['id']).all()

        except Exception as e:
            print(e)
            return jsonify({
                "status_message": "Error"
            })
        if len(questions) == 0:
            return jsonify({
                "status_message": "This category is out of questions"
            }), 200
        questions_list = [question.format() for question in questions]
        return jsonify(
            {
                "question": questions_list[0]
            }
        )


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/trivia/v1/questions_search", methods=["POST"])
    def search_question():
        try:
            search_param = request.json['searchTerm']
            search = "%{}%".format(search_param)
            questions_list= Question.query.filter(Question.question.like(search)).all()
            print("questions_list: ",questions_list)
            questions_result = [question.format() for question in questions_list]
            totalQuestions = len(questions_list)

            return jsonify(
                {
                    'questions': questions_result,
                    'totalQuestions': totalQuestions,
                    'currentCategory': 'Entertainment',
                    "message": "successfully"
                }
            ), 200
        except:
            return jsonify({
                "message": "error"
            }), 500

    @app.route("/trivia/v1/categories/<id_category>/questions", methods=["GET"])
    def get_questions_by_category(id_category):
        try:
            questions = Question.query.filter_by(category=text(id_category)).all()
            current_category = Category.query.filter_by(id=text(id_category))
            questions_list = [question.format() for question in questions]
            totalQuestions = len(questions_list)
            currentCategory = [category.format()['type'] for category in current_category]

            return jsonify({
                "questions": questions_list,
                "totalQuestions": totalQuestions,
                "currentCategory": currentCategory,
                "message": "successfully"
            }),200
        except Exception as e:
            print(e)
            return jsonify({
                "message": "error"
            }), 500


    return app
