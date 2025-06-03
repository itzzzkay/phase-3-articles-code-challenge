from db import connection
from lib.models.article import Article
from lib.models.magazine import Magazine
from article import Article

class Author :
    def __init__(self, id , name):
        self.id = id
        self.name =name

    @classmethod
    def get_by_id(cls, author_id):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?",(author_id,))
        rows = cursor.fetchone()
        conn.close()
        return cls(*rows) if rows else None

    @classmethod
    def get_by_name(cls, name):
        conn= connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        return cls (*row)if row else None
     
    def get_articles(self):
        conn = connection.get_connection( )
        cursor =conn.cursor()
        cursor.execute("SELECT * FROM articles  WHERE author_id =?",(self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(*row)for row in rows]
    
    def save(self):
        conn = connection.get_connection()
        cursor = cursor()
        cursor.execute = ("INSERT INTO authors (name) VALUES (?)", (self.name,))
        conn.commit()
        self.id = cursor.lastrowid
        conn.close()
        return self
    
    def magazines(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        sql = """ 
                        SELECT DISTINCT m. * FROM magazines m 
                        JOIN articles a ON m.id = a.magazine_id WHERE a.author_id = ?
                        """,(self.id,)
        cursor.execute (sql)
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(*row)for row in rows]
    

    def add_article(self, magazine, title):
        article = Article(None, title, self.id, magazine.id)
        article.save()
        return article


    def topic_areas(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        sql = """
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        """, (self.id,)
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]    