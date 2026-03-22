"""
Flask driven web engine
"""
from time import sleep

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from core.entities.Book_data import Book_data
from data.Wrappers import safe_log

__web_app: Flask = Flask(__name__, static_url_path='/static')


class Dp:
    """
    Static web interface dependencies
    """
    history_mod: None
    transfer_mod: None
    stat_mod: None
    local_logger: None


class Cache:
    all_books: list[dict] = None
    fav_books: list[dict] = None
    all_book_count: int = 0
    fav_book_count: int = 0


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
    if Dp.transfer_mod is None or Dp.history_mod is None:
        flash("Error, transfer or history module is not initialized")
        return redirect(url_for('root_page'))

    if request.method == 'POST':
        book: Book_data = Book_data()

        title = request.form.get('title')  # book name
        author = request.form.get('author')  # optional
        book_category = request.form.get('category')  # optional
        book_type = request.form.get('book_type')

        book.set_book_name(title)
        book.set_book_author(author)
        book.set_book_category(book_category)
        book.set_book_type(book_type)

        Dp.history_mod.add_new_book_to_history(book)
        Dp.local_logger.log(f'Added book data - {book}')

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
        if Cache.fav_books is None:
            books = Dp.history_mod.list_favourite_books()
            book_count = len(books)
            Cache.fav_books = books
            Cache.fav_book_count = book_count
        else:
            Dp.local_logger.log('Using cache value for favourite')
            books = Cache.fav_books
            book_count = len(books)
    elif view == 'all':
        if Cache.all_books is None:
            books = Dp.history_mod.list_all_read_book()
            book_count = len(books)
            Cache.all_books = books
            Cache.all_book_count = book_count
        else:
            Dp.local_logger.log('Using cache value for all books')
            books = Cache.all_books
            book_count = len(books)
    else:
        flash("Error in history module")
        return redirect(url_for('root_page'))
    return render_template('history.html', books=books, book_count=book_count)


@__web_app.route('/stats', methods=['GET'])
def statistics_page():
    """
    Page with reading statistics in form of web
    """
    if Dp.stat_mod is None:
        flash("Error, statistics module is not initialized")
        return redirect(url_for('root_page'))

    if Dp.history_mod is None:
        flash("Error, history module is not initialized")
        return redirect(url_for('root_page'))

    total_books_count: int = 0
    audio_books: int = 0
    categories: dict = {}
    recent_books: list[str] = []

    if Cache.all_book_count == 0 and Cache.fav_book_count == 0:
        data = Dp.history_mod.count_all_books()  # all book list, fav list, count
        total_books_count = data[2]

        Dp.local_logger.log('Update all books and favourite book data')
        Cache.all_books = data[0]
        Cache.fav_books = data[1]
    else:
        Dp.local_logger.log('Using cache total books count')
        total_books_count = Cache.fav_book_count + Cache.all_book_count

    return render_template('statistics.html',
                           total_books=total_books_count,
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
