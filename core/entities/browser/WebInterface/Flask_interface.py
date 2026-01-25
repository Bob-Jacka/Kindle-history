"""
Flask driven web engine
"""

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request
)

from data.Wrappers import safe_log

__web_app: Flask = Flask(__name__)


@safe_log
def run_web_app():
    __web_app.run()


##Pages:

@__web_app.route('/')
def root_page():
    return render_template('home.html')


@__web_app.route('/add', methods=['GET', 'POST'])
def add_book_page():
    """
    Page for adding book
    :return:
    """
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # TODO Database connection

        return redirect(url_for('index'))
    return render_template('add_book.html')


@__web_app.route('/remove')
def remove_book_page():
    """
    Page for removing book
    :return:
    """
    return render_template('remove_book.html')


@__web_app.route('/about')
def about_util_page():
    """
    Page with information about utility
    :return:
    """
    return render_template('about.html')


@__web_app.route('/actions')
def actions_page():
    """
    Page with redirect to add book or delete book
    :return:
    """
    return render_template('actions.html')
