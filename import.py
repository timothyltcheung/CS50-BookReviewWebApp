import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def main():
    data = open('books.csv')
    reader = csv.reader(data)
    for ISBN, title, author, year in reader:
        db.execute("INSERT INTO books (ISBN, title, author, year) VALUES (:ISBN, :title, :author, :year)", {"ISBN": ISBN, "title": title, "author": author, "year": year})
        print(f" ISBN: {ISBN}")
    db.commit()


if __name__ == "__main__":
    main()
