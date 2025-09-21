import sqlite3


class DatabaseManager:
    def __init__(self, db_name: str) -> None:
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def create_tables(self):
        """Create normalized tables"""
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                age INTEGER 
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                price REAL NOT NULL,
                category TEXT
            )
            """
        )

        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                user_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                order_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES product(product_id)
            )
            """
        )

        self.conn.commit()

    def insert_sample_data(self) -> None:
        """Insert sample data into tables"""
        users = [
            (1, "Alex", "alex@gmail.com", 30),
            (2, "Alice", "alice@gmail.com", 19),
            (3, "Fred", "fred@gmail.com", 27),
            (4, "Rick", "rick@gmail.com", 60),
            (5, "Morty", "morty@gmail.com", 15),
            (6, "Guest", "guest@gmail.com", 99)
        ]

        products = [
            (101, "Laptop", 499.99, "Electronics"),
            (102, "Headphones", 19.99, "Electronics"),
            (103, "Book", 5.99, "Education"),
            (104, "Desk", 149.99, "Furniture")
        ]

        orders = [
            (1001, 1, 101, 1, "2025-01-17"),
            (1002, 4, 103, 5, "2025-01-18"),
            (1003, 3, 104, 1, "2025-01-19"),
            (1004, 5, 102, 2, "2025-01-20"),
            (1005, 2, 103, 1, "2025-01-21"),
            (1006, 1, 103, 3, "2025-01-22"),
            (1007, 5, 104, 1, "2025-01-23"),
        ]

        self.cur.executemany("INSERT INTO users VALUES (?, ?, ?, ?)", users)
        self.cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)
        self.cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders)

        self.conn.commit()

    def execute_query(self, query: str) -> list[dict]:
        """Execute SQL query and return results as dictionaries"""
        self.cur.execute(query)
        columns = [desc[0] for desc in self.cur.description]
        result = self.cur.fetchall()

        return [dict(zip(columns, row)) for row in result]


    def print_demo(self, query):
        results = self.execute_query(query)
        
        for row in results:
            print(f"    {row}")
    
    def demonstrate_relation_algebra(self):
        """Demonstrate realtion algebra operations"""
        #1. Selection
        print("Selection:")
        query = "SELECT * FROM users WHERE age >= 30"
        self.print_demo(query)

        #2. Projection
        print("\nProjection:")
        query = "SELECT name, email FROM users"
        self.print_demo(query)

        #3. Natural Inner Join
        print("\nNatural Join:")
        query = """
            SELECT u.name, p.product_name, o.quantity, o.order_date
            FROM users u
            JOIN orders o ON u.user_id = o.user_id
            JOIN products p ON p.product_id = o.product_id
        """
        self.print_demo(query)

        #4. Union
        print("\nUnion:")
        query = """
            SELECT name FROM users
            UNION
            SELECT product_name FROM products
        """
        self.print_demo(query)

        #5. Difference
        print("\nDifference:")
        query = """
            SELECT user_id, name
            FROM users
            WHERE user_id NOT IN (SELECT DISTINCT user_id FROM orders)
        """
        self.print_demo(query)


if __name__ == "__main__":
    db = DatabaseManager("test_database.db")
    db.create_tables()
    if input("Insert data (y/n): ").lower() == "y":
        db.insert_sample_data()
    db.demonstrate_relation_algebra()


