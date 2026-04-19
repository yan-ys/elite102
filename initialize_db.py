import sqlite3

DB_NAME = 'example.db'


def initialize_database():
    connection = sqlite3.connect(DB_NAME)
    print("Connected to the database.")
    cursor = connection.cursor()
    print("Cursor created.")
    # Create a sample table
    print("Creating table if it does not exist...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts
            (id integer primary key, 
            name text, 
            balance real)
    ''')

    print("Table created.")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions
            (id integer primary key, 
            transaction_type text, 
            amount real, account_num integer)
    ''')

    # Insert sample data
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM accounts")
    print("Inserting sample data...")
    cursor.execute('''
        INSERT INTO accounts (name, balance) VALUES
        ('Alice', 0),
        ('Bob', 0),
        ('Charlie', 0)
    ''')
    print("Sample data inserted.")
    # Commit the changes and close the connection
    print("Committing changes and closing the connection...")
    connection.commit()
    connection.close()


initialize_database()
