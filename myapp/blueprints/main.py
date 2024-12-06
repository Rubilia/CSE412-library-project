from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from ..db.pool import get_conn, put_conn
from ..db.author import Author
from ..db.work import Work
from ..db.edition import Edition
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Initially load random works and authors
    conn = get_conn()
    works = Work.random_works(conn, limit=6)
    authors = Author.random_authors(conn, limit=6)
    put_conn(conn)
    return render_template('index.html', works=works, authors=authors)

@main_bp.route('/random_data')
def random_data():
    # Return JSON for 6 random works and authors
    conn = get_conn()
    works = Work.random_works(conn, limit=6)
    authors = Author.random_authors(conn, limit=6)
    put_conn(conn)

    def author_to_dict(a):
        return {
            'id': a.id,
            'name': a.name,
            'bio': a.bio,
            'birth_date': str(a.birth_date),
            'death_date': str(a.death_date) if a.death_date else None
        }

    def work_to_dict(w):
        return {
            'id': w.id,
            'title': w.title,
            'subtitle': w.subtitle,
            'description': w.description,
            'first_publish_date': str(w.first_publish_date)
        }

    return jsonify({
        'authors': [author_to_dict(a) for a in authors],
        'works': [work_to_dict(w) for w in works]
    })

@main_bp.route('/search', methods=['GET','POST'])
def search():
    results = []
    query = ""
    search_type = request.form.get('search_type', 'title')

    if request.method == 'POST':
        query = request.form.get('q', '').strip()
        conn = get_conn()
        if search_type == 'title':
            results = Work.search_by_title(conn, query)
            if not results:
                results = Edition.search_by_title(conn, query)
        elif search_type == 'author':
            results = Author.search_by_name(conn, query)
        elif search_type == 'isbn':
            ed = Edition.get_by_isbn(conn, query)
            results = [ed] if ed else []
        put_conn(conn)

    return render_template('search.html', results=results, query=query, search_type=search_type)

@main_bp.route('/random')
def random_work():
    conn = get_conn()
    work_id = Work.get_random_work_id(conn)
    put_conn(conn)
    if work_id:
        return redirect(url_for('main.work_detail', work_id=work_id))
    return render_template('random.html', error="No works found.")

@main_bp.route('/work/<int:work_id>')
def work_detail(work_id):
    conn = get_conn()
    work = Work.get_by_id(conn, work_id)
    if not work:
        put_conn(conn)
        return render_template('work_detail.html', work=None)

    editions = Work.get_editions_for_work(conn, work_id)
    authors = Work.get_authors_for_work(conn, work_id)
    languages = Work.get_languages_for_work(conn, work_id)
    subjects = Work.get_subjects_for_work(conn, work_id)
    # Fetch notes, cover_edition, first_sentence from work already included in model
    cover_edition_id = Work.get_cover_edition_id(conn, work_id)
    cover_edition = None
    if cover_edition_id:
        cover_edition = Edition.get_by_id(conn, cover_edition_id)
    put_conn(conn)
    return render_template('work_detail.html', work=work, editions=editions, authors=authors, languages=languages, subjects=subjects, cover_edition=cover_edition)

@main_bp.route('/author/<int:author_id>')
def author_detail(author_id):
    conn = get_conn()
    author = Author.get_by_id(conn, author_id)
    works = Author.get_works_for_author(conn, author_id)
    links = Author.get_links_for_author(conn, author_id)
    put_conn(conn)
    return render_template('author_detail.html', author=author, works=works, links=links)
