from db import connection
from article import Article
from author import Author

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value.strip():
            self._name = value
        else:
            raise ValueError("Magazine Name must be a string.")

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and value.strip():
            self._category = value
        else:
            raise ValueError("Category must be a string.")

    def save(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO magazines (name, category) VALUES (?, ?)",(self.name, self.category)
        cursor.execute(sql)
        conn.commit()
        conn.close()

    @classmethod
    def get_by_id(cls, magazine_id):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (magazine_id,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def get_by_name(cls, name):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def get_by_category(cls, category):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE category = ?", (category,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    def articles(self):
        return Article.find_all_by_magazine(self.id)

    def contributors(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON ar.author_id = a.id
            WHERE ar.magazine_id = ?
        """, (self.id,)
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [Author(*row) for row in rows]

    def article_titles(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT title FROM articles
            WHERE magazine_id = ?
        """, (self.id,)
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]

    def contributing_authors(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT a.*, COUNT(ar.id) as article_count
            FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING article_count > 2
        """, (self.id,)
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [Author(*row[:2]) for row in rows]  