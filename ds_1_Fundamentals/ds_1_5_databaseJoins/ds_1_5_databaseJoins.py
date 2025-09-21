import sqlite3
from pprint import pprint

class DatabaseJoins:
    def __init__(self, db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def create_tables(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                sex TEXT NOT NULL,
                age INTEGER NOT NULL
        )    
        """)

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """)

        self.conn.commit()

    def insert_sample_data(self):
        users = [
            ('utyara3', 'male', 16),
            ('coolboy', 'male', 40),
            ('lily13', 'female', 22),
            ('j3ssy', 'male', 25),
            ('el1sabeth', 'female', 13)
        ]

        posts = [
            ('my data science roadmap', 1),
            ('beauty-blog', 3),
            ('programming', 1),
            ('how to repair your car', 4),
            ('dota2 strategyes', 2),
            ('cs2 grenades', 2),
            ('sqlite3 python', 1)
        ]

        self.cur.executemany("INSERT INTO users(username, sex, age) VALUES (?, ?, ?)", users)
        self.cur.executemany("INSERT INTO posts(topic, user_id) VALUES (?, ?)", posts)
    
    def demonstrate_joins(self):
        #1. Inner JOIN
        query = """
            SELECT u.username, p.topic
            FROM users u
            JOIN posts p
                ON p.user_id = u.id
            ORDER BY u.username
        """
        print("1. Inner Join:\n")
        pprint(self.cur.execute(query).fetchall())

        #2. Outer JOIN (Left)
        query = """
            SELECT u.username, p.topic
            FROM users u
            LEFT JOIN posts p
                ON p.user_id = u.id
            ORDER BY u.username
        """
        print("\nLeft Outer Join:")
        pprint(self.cur.execute(query).fetchall())
        
        #3. Outer JOIN (Right)
        query = """
            SELECT u.username, p.topic
            FROM posts p
            LEFT JOIN users u
                ON p.user_id = u.id
            ORDER BY u.username
        """
        print("\nRight Outer Join:")
        pprint(self.cur.execute(query).fetchall())
        
        #4. Cross Join
        query = """
            SELECT u.username, p.topic
            FROM posts p
            CROSS JOIN users u
        """
        print("\nCross Join:")
        pprint(self.cur.execute(query).fetchall())
        

        #5. Full Join
        query = """
            SELECT u.username, p.topic
            FROM users u
            LEFT JOIN posts p
                ON u.id = p.user_id
            UNION
            SELECT u.username, p.topic
            FROM posts p
            LEFT JOIN users u
                ON u.id = p.user_id
            WHERE u.id IS NULL
            ORDER BY u.username
        """
        print("\nFull Join:")
        pprint(self.cur.execute(query).fetchall())
        #6. Theta Join
        query = """
            SELECT u.username, p.topic
            FROM posts p
            LEFT JOIN users u
                ON u.id != p.user_id
            ORDER BY u.username
        """
        print("\nTheta Join:")
        pprint(self.cur.execute(query).fetchall())

if __name__ == "__main__":
    try:
        db = DatabaseJoins("test_database.db")
        db.create_tables()
        db.insert_sample_data()
        db.demonstrate_joins()
    finally:
        db.conn.close()
