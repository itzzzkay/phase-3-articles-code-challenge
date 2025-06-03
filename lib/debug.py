from models.author import Author
author = Author.get_by_id(1)
print(author.name)