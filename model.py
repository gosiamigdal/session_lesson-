import sqlite3
import datetime

# ADMIN_USER="hackbright"
# ADMIN_PASSWORD=5980025637247534551

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("thewall.db")
    DB = CONN.cursor()

def authenticate(username, password):
    query = """SELECT id FROM users WHERE username = ? AND password = ?"""
    DB.execute(query, (username, password,))
    user_id = DB.fetchone()
    return user_id

def get_user_by_name(username):
    query = """SELECT id FROM users WHERE username = ?"""
    DB.execute(query, (username,))
    user_id = DB.fetchone()
    return user_id

def get_user_by_id(user_id):
    query = """SELECT username FROM users WHERE id = ?"""
    DB.execute(query, (user_id,))
    username = DB.fetchone()
    return username[0]

def get_wall_posts(user_id):
    query = """SELECT content, author_id, created_at FROM wall_posts WHERE owner_id = ?"""
    DB.execute(query,(user_id,))
    posts = DB.fetchall()
    posts_result = []
    for post in posts:
        count = 0
        line = []
        for token in post:
            if count == 1:
                author_id = token
                query = """SELECT username FROM users WHERE id =?"""
                DB.execute(query, (author_id,))
                author = DB.fetchone()
                token = author[0]
            line.append(token)
            count += 1
        posts_result.append(line)
    return posts_result

def create_wallpost(author_id, content, owner_id):
    post_date = datetime.datetime.now()
    author = get_user_by_name(author_id)
    owner = get_user_by_name(owner_id)
    query = """INSERT INTO wall_posts VALUES (null, ?, ?, ?, ?)"""
    DB.execute(query, (owner, author, post_date, content,))
    CONN.commit()
    return "posted!"


# def insert():
#     query = """insert into wall_posts values (null, 0, 0, ?, ?)"""
#     DB.execute(query, (datetime.datetime.now(), "Some text") )
	
def main():
    connect_to_db()

if __name__ == "__main__":
   main()
