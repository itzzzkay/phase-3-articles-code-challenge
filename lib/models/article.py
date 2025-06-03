from db import connection
from author import Author
from magazine import Magazine

class Article:
    def __init__(self, id, title, author_id, magazine_id ):
        self.id = id
        self.author_id = author_id
        self.title= title
        self.magazine_id =magazine_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and value.strip():
            self._title = value
        else:
            raise ValueError("Article Title must be a string.")
        


    def save(self):
        conn = connection.get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",(self.title, self.author_id, self.magazine_id)
        
        cursor.execute(sql)
        conn.commit()
        conn.close()

    @classmethod
    def get_all_articles_by_author(cls, author_id):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (author_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]
    
    @classmethod
    def get_article_by_title(cls, title):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        row = cursor.fetchone()
        conn.close()
        return cls(*row) if row else None

    @classmethod
    def get_article_by_id(cls,article_id):
        conn = connection.get_connection()
        cursor =conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id= ?", (article_id))
        rows =cursor.fetchone()
        conn.close()
        return cls(*rows) if rows else None

    @classmethod
    def find_all_articles_by_magazine(cls, magazine_id):
        conn = connection.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (magazine_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]


    def get_author(self):
        return Author.get_by_id(self.author_id)
    
    def get_magazine(self):
        return Magazine.get_by_id(self.magazine_id)
    
    

