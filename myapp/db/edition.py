class Edition:
    def __init__(self, id, title, publish_date, number_of_pages, isbn_13):
        self.id = id
        self.title = title
        self.publish_date = publish_date
        self.number_of_pages = number_of_pages
        self.isbn_13 = isbn_13

    @staticmethod
    def get_by_isbn(conn, isbn):
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, publish_date, number_of_pages, isbn_13 FROM Edition WHERE isbn_13 = %s OR isbn_10 = %s", (isbn, isbn))
            row = cur.fetchone()
            if row:
                return Edition(*row)
        return None

    @staticmethod
    def search_by_title(conn, title_query):
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, publish_date, number_of_pages, isbn_13 FROM Edition WHERE title ILIKE %s LIMIT 50", (f"%{title_query}%",))
            rows = cur.fetchall()
            return [Edition(*r) for r in rows]



    @staticmethod
    def get_by_id(conn, edition_id):
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, publish_date, number_of_pages, isbn_13, subtitle, cover_pic_id, publish_country,
                       first_sentence, title_prefix, weight, description, notes, isbn_10
                FROM Edition
                WHERE id = %s
            """, (edition_id,))
            row = cur.fetchone()
            if row:
                ed = Edition(row[0], row[1], row[2], row[3], row[4])
                # Manually assign extra fields since constructor is limited:
                ed.subtitle = row[5]
                ed.cover_pic_id = row[6]
                ed.publish_country = row[7]
                ed.first_sentence = row[8]
                ed.title_prefix = row[9]
                ed.weight = row[10]
                ed.description = row[11]
                ed.notes = row[12]
                ed.isbn_10 = row[13]

                # Fetch genres
                cur.execute("SELECT genre FROM Edition_Genres WHERE edition_id = %s", (edition_id,))
                ed.genres = [r[0] for r in cur.fetchall()]

                # Fetch languages
                cur.execute("SELECT language FROM Edition_Languages WHERE edition_id = %s", (edition_id,))
                ed.languages = [r[0] for r in cur.fetchall()]

                return ed
        return None