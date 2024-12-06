class Work:
    def __init__(self, id, title, subtitle, description, first_publish_date):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.description = description
        self.first_publish_date = first_publish_date

    @staticmethod
    def get_by_id(conn, work_id):
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, subtitle, description, first_publish_date FROM Work WHERE id = %s", (work_id,))
            row = cur.fetchone()
            if row:
                return Work(*row)
        return None

    @staticmethod
    def search_by_title(conn, title_query):
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, subtitle, description, first_publish_date FROM Work WHERE title ILIKE %s LIMIT 50", (f"%{title_query}%",))
            rows = cur.fetchall()
            return [Work(*r) for r in rows]

    @staticmethod
    def get_random_work_id(conn):
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM Work ORDER BY random() LIMIT 1")
            row = cur.fetchone()
            if row:
                return row[0]
        return None

    @staticmethod
    def get_editions_for_work(conn, work_id):
        with conn.cursor() as cur:
            # Fetch the cover_edition id from Work
            cur.execute("SELECT cover_edition FROM Work WHERE id = %s", (work_id,))
            row = cur.fetchone()
            if row and row[0]:
                cover_edition_id = row[0]
                cur.execute("""
                    SELECT id, title, publish_date, number_of_pages, isbn_13
                    FROM Edition
                    WHERE id = %s
                """, (cover_edition_id,))
                from .edition import Edition
                edition_row = cur.fetchone()
                if edition_row:
                    edition = Edition(*edition_row)

                    # Fetch genres
                    cur.execute("SELECT genre FROM Edition_Genres WHERE edition_id = %s", (edition.id,))
                    edition.genres = [r[0] for r in cur.fetchall()]

                    # Fetch languages
                    cur.execute("SELECT language FROM Edition_Languages WHERE edition_id = %s", (edition.id,))
                    edition.languages = [r[0] for r in cur.fetchall()]

                    return [edition]
            return []

    @staticmethod
    def get_authors_for_work(conn, work_id):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT a.id, a.name, a.birth_date, a.death_date, a.bio
                FROM Author a
                JOIN Work_Authors wa ON wa.author_id = a.id
                WHERE wa.work_id = %s
            """, (work_id,))
            from .author import Author
            return [Author(*r) for r in cur.fetchall()]

    @staticmethod
    def get_languages_for_work(conn, work_id):
        with conn.cursor() as cur:
            cur.execute("SELECT language FROM Work_Languages WHERE work_id = %s", (work_id,))
            return [row[0] for row in cur.fetchall()]

    @staticmethod
    def get_subjects_for_work(conn, work_id):
        with conn.cursor() as cur:
            cur.execute("SELECT subject FROM Work_Subjects WHERE work_id = %s", (work_id,))
            return [row[0] for row in cur.fetchall()]

    @staticmethod
    def random_works(conn, limit=5):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, subtitle, description, first_publish_date
                FROM Work
                ORDER BY random()
                LIMIT %s
            """, (limit,))
            rows = cur.fetchall()
            return [Work(*r) for r in rows]


    @staticmethod
    def get_cover_edition_id(conn, work_id):
        with conn.cursor() as cur:
            cur.execute("SELECT cover_edition FROM Work WHERE id = %s", (work_id,))
            row = cur.fetchone()
            if row:
                return row[0]
        return None