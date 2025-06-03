DROP TABLE IF EXISTS articles;

CREATE TABLE articles (
    id INTEGER PRIMARY KEY,
    title TEXT ,
    author_id INTEGER ,
    magazine_id INTEGER ,
    FOREIGN KEY (author_id) REFERENCES authors(id),
    FOREIGN KEY (magazine_id) REFERENCES magazines(id)
);

DROP TABLE IF EXISTS magazines;

CREATE TABLE magazines (
    id INTEGER PRIMARY KEY,
    name TEXT ,
    category TEXT 
);

DROP TABLE IF EXISTS authors;

CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    name TEXT 
);

