"""
Flask driven web engine
"""
from time import sleep

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request, flash
)

from data.Wrappers import safe_log

__web_app: Flask = Flask(__name__, static_url_path='/static')


class Dp:
    """
    Static web interface dependencies
    """
    history_mod: None
    transfer_mod: None
    stat_mod: None


@safe_log
def run_web_app():
    """
    Entry point to web interface run
    :return:
    """
    __web_app.run()


##Pages handlers:

@__web_app.route('/', methods=['GET'])
def root_page():
    return render_template('home.html')


@__web_app.route('/add', methods=['GET', 'POST'])
def add_book_page():
    """
    Page for adding book to read history
    :return: page
    """
    if Dp.transfer_mod is None:
        flash("Error, transfer module is not initialized")
        return redirect(url_for('root_page'))

    if request.method == 'POST':
        title = request.form.fromkeys('title', '')  # book name
        author = request.form.fromkeys('author', None)  # optional
        book_category = request.form.fromkeys('category', None)  # optional
        book_type = request.form.fromkeys('book_type', '')
        if book_type == 'text' or book_type == 'audio':
            pass
        else:
            pass
            # TODO think of better parse parameter

        sleep(1)
        return redirect(url_for('root_page'))
    return render_template('add_book.html')


@__web_app.route('/remove', methods=['GET', 'POST'])
def remove_book_page():
    """
    Page for removing book
    :return: page
    """
    if Dp.transfer_mod is None:
        flash("Error, transfer module is not initialized")
        return redirect(url_for('root_page'))

    if request.method == 'POST':
        title = request.form['title']  # required parameter

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


@__web_app.route('/history', methods=['GET'])
def history_page():
    view = request.args.get('view', 'all')

    if view == 'favourites':
        books = Dp.history_mod.list_favourite_books()
    elif view == 'all':
        books = Dp.history_mod.list_all_read_book()
    else:
        flash("Error in history module")
        return redirect(url_for('root_page'))
    return render_template('history.html', books=books)


@__web_app.route('/stats', methods=['GET'])
def statistics_page():
    """
    Page with reading statistics
    """
    if Dp.stat_mod is None:
        flash("Error, statistics module is not initialized")
        return redirect(url_for('root_page'))

    if Dp.history_mod is None:
        flash("Error, history module is not initialized")
        return redirect(url_for('root_page'))

    total_books = 0
    audio_books = 0
    categories = {}
    recent_books = []

    return render_template('statistics.html',
                           total_books=total_books,
                           audio_books=audio_books,
                           categories=categories,
                           recent_books=recent_books)


@__web_app.route('/stats/calculate', methods=['POST'])
def calculate_speed():
    """
    Calculate reading speed
    """
    from datetime import datetime
    start_date_str = request.form.get('start_date')
    period = request.form.get('period', 'year')

    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        calculated_speed = "..."

    return redirect(url_for('statistics_page'))
