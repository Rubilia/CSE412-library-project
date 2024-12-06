import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import random
from faker import Faker

# Adjust these connection parameters as needed.
DB_DSN = "postgresql://cse412db_owner:2Qqcbp9CvasX@ep-quiet-star-a6r8acx0.us-west-2.aws.neon.tech/cse412db?sslmode=require"

conn = psycopg2.connect(dsn=DB_DSN)
cur = conn.cursor()

# Create tables if they don't exist, based on the initial schema
create_statements = [
    """
    CREATE TABLE IF NOT EXISTS Author (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255),
        birth_date DATE,
        death_date DATE,
        bio TEXT,
        personal_name VARCHAR(255),
        eastern_order BOOLEAN,
        title VARCHAR(255),
        location VARCHAR(255),
        wikipedia VARCHAR(255),
        enumeration VARCHAR(255)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Author_links (
        id SERIAL PRIMARY KEY,
        url VARCHAR(255),
        title VARCHAR(255),
        author_id INT,
        FOREIGN KEY (author_id) REFERENCES Author(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Edition (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        subtitle VARCHAR(255),
        publish_date DATE,
        copyright_date DATE,
        cover_pic_id INT,
        publish_country VARCHAR(255),
        first_sentence TEXT,
        title_prefix VARCHAR(255),
        number_of_pages INT,
        weight DECIMAL,
        description TEXT,
        notes TEXT,
        isbn_13 VARCHAR(13),
        isbn_10 VARCHAR(10),
        edition_number INT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Work (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        subtitle VARCHAR(255),
        description TEXT,
        first_publish_date DATE,
        notes TEXT,
        cover_edition INT,
        first_sentence TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Edition_Genres (
        id SERIAL PRIMARY KEY,
        genre VARCHAR(255),
        edition_id INT,
        FOREIGN KEY (edition_id) REFERENCES Edition(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Edition_Languages (
        id SERIAL PRIMARY KEY,
        language VARCHAR(255),
        edition_id INT,
        FOREIGN KEY (edition_id) REFERENCES Edition(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Work_Authors (
        id SERIAL PRIMARY KEY,
        author_id INT,
        work_id INT,
        FOREIGN KEY (author_id) REFERENCES Author(id),
        FOREIGN KEY (work_id) REFERENCES Work(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Work_Languages (
        id SERIAL PRIMARY KEY,
        language VARCHAR(255),
        work_id INT,
        FOREIGN KEY (work_id) REFERENCES Work(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS Work_Subjects (
        id SERIAL PRIMARY KEY,
        subject VARCHAR(255),
        work_id INT,
        FOREIGN KEY (work_id) REFERENCES Work(id)
    );
    """
]

for stmt in create_statements:
    cur.execute(stmt)

conn.commit()

faker = Faker()
random.seed(420)

# Parameters for data size
num_authors = 500
num_works = 1750
# Aim for about 7000 editions: each work ~4 editions on average
# We'll do 3-5 editions per work.
subjects = ["Fiction", "Literature", "Romance", "Science Fiction", "Fantasy", "History", "Philosophy", "Poetry", "Mystery", "Adventure",
            "Biography", "Religion", "Politics", "Economics", "Psychology", "Drama", "Ethics", "Education", "Art", "Music"]
languages = ["en", "fr", "de", "ja", "es", "ru", "it", "zh", "ar", "pt"]
genres = ["Novel", "Short Stories", "Biography", "Autobiography", "Essay", "Poem", "Play", "Criticism", "Memoir", "Fable"]

def random_date(start_year=1700, end_year=2020):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).date()

def insert_author():
    name = faker.name()
    birth_d = random_date(1700, 1900)
    death_d = birth_d + timedelta(days=random.randint(20000, 30000)) if random.random() < 0.7 else None
    bio = faker.text(max_nb_chars=200)
    personal_name = name
    eastern_order = random.choice([True, False])
    title = random.choice(["Mr.", "Ms.", "Dr.", None])
    location = faker.city() + ", " + faker.country()
    wikipedia = None
    enumeration = None
    cur.execute("""
        INSERT INTO Author (name, birth_date, death_date, bio, personal_name, eastern_order, title, location, wikipedia, enumeration)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (name, birth_d, death_d, bio, personal_name, eastern_order, title, location, wikipedia, enumeration))
    return cur.fetchone()[0]

def insert_work():
    title = faker.sentence(nb_words=random.randint(1,3)).strip(".")
    subtitle = faker.sentence(nb_words=random.randint(1,2)).strip(".") if random.random() < 0.3 else None
    description = faker.text(max_nb_chars=200)
    fp_date = random_date(1800, 2000)
    notes = faker.sentence() if random.random() < 0.2 else None
    first_sentence = faker.sentence()
    cover_edition = None
    cur.execute("""
        INSERT INTO Work (title, subtitle, description, first_publish_date, notes, cover_edition, first_sentence)
        VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (title, subtitle, description, fp_date, notes, cover_edition, first_sentence))
    return cur.fetchone()[0]

def insert_work_authors(work_id, author_ids):
    for a_id in author_ids:
        cur.execute("""
            INSERT INTO Work_Authors (author_id, work_id) VALUES (%s,%s)
        """, (a_id, work_id))

def insert_work_languages(work_id):
    num_w_lang = random.randint(1,2)
    for _ in range(num_w_lang):
        lang = random.choice(languages)
        cur.execute("""
            INSERT INTO Work_Languages (language, work_id) VALUES (%s,%s)
        """, (lang, work_id))

def insert_work_subjects(work_id):
    num_sub = random.randint(2,4)
    chosen_sub = random.sample(subjects, num_sub)
    for subj in chosen_sub:
        cur.execute("""
            INSERT INTO Work_Subjects (subject, work_id) VALUES (%s,%s)
        """, (subj, work_id))

def insert_edition(work_id):
    e_title = faker.sentence(nb_words=random.randint(1,3)).strip(".")
    subtitle = faker.sentence(nb_words=1).strip(".") if random.random() < 0.3 else None
    publish_date_val = random_date(1900, 2020)
    copyright_date = publish_date_val if random.random() < 0.2 else None
    cover_pic_id = None
    publish_country = faker.country()
    first_sentence = faker.sentence()
    title_prefix = random.choice(["Vol. I", "Vol. II", "New Edition", None])
    number_of_pages = random.randint(100, 1000)
    weight = round(random.uniform(0.5, 2.5), 2)
    description = faker.text(max_nb_chars=200)
    notes = faker.sentence() if random.random() < 0.3 else None
    isbn_13 = ''.join([str(random.randint(0,9)) for _ in range(13)])
    isbn_10 = ''.join([str(random.randint(0,9)) for _ in range(10)])
    edition_number = random.randint(1, 10)

    cur.execute("""
        INSERT INTO Edition (title, subtitle, publish_date, copyright_date, cover_pic_id, publish_country,
                             first_sentence, title_prefix, number_of_pages, weight, description, notes, isbn_13,
                             isbn_10, edition_number)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id
    """, (e_title, subtitle, publish_date_val, copyright_date, cover_pic_id, publish_country,
          first_sentence, title_prefix, number_of_pages, weight, description, notes, isbn_13, isbn_10, edition_number))
    edition_id = cur.fetchone()[0]

    # Edition Genres (1-2)
    num_gen = random.randint(1,2)
    for _ in range(num_gen):
        genre = random.choice(genres)
        cur.execute("""
            INSERT INTO Edition_Genres (genre, edition_id)
            VALUES (%s,%s)
        """, (genre, edition_id))

    # Edition Languages (1-2)
    num_e_lang = random.randint(1,2)
    for _ in range(num_e_lang):
        lang = random.choice(languages)
        cur.execute("""
            INSERT INTO Edition_Languages (language, edition_id)
            VALUES (%s,%s)
        """, (lang, edition_id))

    return edition_id

def insert_author_links(author_id):
    # ~40% of authors get a link
    if random.random() < 0.4:
        url = faker.url()
        link_title = random.choice(["Author Official Page", "Personal Website", "Blog", "Profile"])
        cur.execute("""
            INSERT INTO Author_links (url, title, author_id)
            VALUES (%s,%s,%s)
        """, (url, link_title, author_id))

# Insert Authors
author_id_list = []
for _ in range(num_authors):
    a_id = insert_author()
    author_id_list.append(a_id)

# Insert Works and related data
# Each work gets 1-3 random authors
# Each work gets languages and subjects
# Then each work gets 3-5 editions
for _ in range(num_works):
    w_id = insert_work()

    num_auth_for_work = random.randint(1,3)
    chosen_authors = random.sample(author_id_list, num_auth_for_work)
    insert_work_authors(w_id, chosen_authors)
    insert_work_languages(w_id)
    insert_work_subjects(w_id)

    # Insert editions
    num_editions = random.randint(3,5)
    for __ in range(num_editions):
        insert_edition(w_id)

# Insert Author links
for a_id in author_id_list:
    insert_author_links(a_id)

conn.commit()
cur.close()
conn.close()

print("Data inserted successfully with Faker-generated synthetic data.")
