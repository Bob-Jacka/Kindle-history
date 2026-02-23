"""
Flask driven web engine
"""
from time import sleep

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request
)

from data.Wrappers import safe_log

__web_app: Flask = Flask(__name__, static_url_path='/static')


class Dp:
    """
    Static web interface dependencies
    """
    history_mod: None
    bql_interpreter: None


@safe_log
def run_web_app():
    """
    Entry point to web interface run
    :return:
    """
    run_database()
    __web_app.run()


@safe_log
def run_database():
    """
    Run database object
    :return:
    """
    Dp.bql_interpreter.test_interpreter()


##Pages handlers:

@__web_app.route('/', methods=['GET'])
def root_page():
    return render_template('home.html')


@__web_app.route('/add', methods=['GET', 'POST'])
def add_book_page():
    """
    Page for adding book
    :return: page
    """
    if request.method == 'POST':
        title = request.form.fromkeys('title', '')  # book name
        author = request.form.fromkeys('author', None)  # optional
        book_category = request.form.fromkeys('category', None)  # optional
        book_type = request.form.fromkeys('book_type', '')
        if book_type is 'text' or 'audio':
            pass
        else:
            # TODO think of better parse parameter
            Dp.bql_interpreter.parse_sentence(Dp.bql_interpreter.Static_expressions.add_record_exp1(title, 'bookdb'))

        sleep(1)
        return redirect(url_for('root_page'))
    return render_template('add_book.html')


@__web_app.route('/remove', methods=['GET', 'POST'])
def remove_book_page():
    """
    Page for removing book
    :return: page
    """
    if request.method == 'POST':
        title = request.form['title']  # required parameter
        # TODO Database connection and action

        sleep(1)  # sleep
        return redirect(url_for('root_page'))
    return render_template('remove_book.html')


@__web_app.route('/about', methods=['GET'])
def about_util_page():
    """
    Page with information about utility
    :return: page
    """
    return render_template('about.html')


@__web_app.route('/actions', methods=['GET'])
def actions_page():
    """
    Page with redirect to add book or delete book
    :return: page
    """
    return render_template('actions.html')
