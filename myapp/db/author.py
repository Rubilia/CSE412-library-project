class Author:
    def __init__(self, id, name, birth_date, death_date, bio):
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.death_date = death_date
        self.bio = bio

    @staticmethod
    def get_by_id(conn, author_id):
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, birth_date, death_date, bio FROM Author WHERE id = %s", (author_id,))
            row = cur.fetchone()
            if row:
                return Author(*row)
        return None

    @staticmethod
    def search_by_name(conn, name_query):
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, birth_date, death_date, bio FROM Author WHERE name ILIKE %s LIMIT 50", (f"%{name_query}%",))
            rows = cur.fetchall()
            return [Author(*r) for r in rows]

    @staticmethod
    def random_authors(conn, limit=5):
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, birth_date, death_date, bio FROM Author ORDER BY random() LIMIT %s", (limit,))
            rows = cur.fetchall()
            return [Author(*r) for r in rows]

    @staticmethod
    def get_links_for_author(conn, author_id):
        with conn.cursor() as cur:
            cur.execute("SELECT url, title FROM Author_links WHERE author_id = %s", (author_id,))
            return cur.fetchall()  # list of (url, title)
    
    @staticmethod
    def get_works_for_author(conn, author_id):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT w.id, w.title, w.subtitle, w.description, w.first_publish_date
                FROM Work w
                JOIN Work_Authors wa ON wa.work_id = w.id
                WHERE wa.author_id = %s
                LIMIT 50
            """, (author_id,))
            rows = cur.fetchall()
            from .work import Work
            return [Work(*r) for r in rows]
