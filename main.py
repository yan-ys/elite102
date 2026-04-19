import sqlite3

def empty_db():
      connection = sqlite3.connect('example.db')
      cursor = connection.cursor()
      cursor.execute("DELETE FROM accounts")
      cursor.execute("DELETE FROM transactions")
      connection.commit()
      #account_id = cursor.lastrowid
      connection.close()

def create_account(name, initial_balance):
      connection = sqlite3.connect('example.db')
      cursor = connection.cursor()

      cursor.execute('''
        INSERT INTO accounts (name, balance)
        VALUES (?,?)
      ''', (name, initial_balance))

      connection.commit()
      account_id = cursor.lastrowid
      connection.close()

      print(f"Account created with ID = {account_id} created with balance {initial_balance}")
      return account_id

def deposit(account_id, amount):
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()

    cursor.execute('''
        UPDATE accounts
        SET balance = balance + ?
        WHERE id = ?
    ''', (amount, account_id))

    cursor.execute('''
        INSERT INTO transactions (transaction_type, amount, account_num)
        VALUES (?,?,?)
    ''', ("withdraw", amount, account_id))

    if cursor.rowcount == 0:
        print('Account not found')
    else:
        print(f"Deposited {amount} into account ID {account_id}")
    connection.commit()
    connection.close()

def withdraw(account_id, amount):
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()

    cursor.execute('''
        SELECT balance FROM accounts where id = ?
    ''', (account_id,))

    result = cursor.fetchone()
    if result is None:
        print("Account not found.")
    else:
        balance = result[0]
        if balance < amount:
            print('Insufficient funds.')
        else:
            cursor.execute('''
                UPDATE accounts 
                SET balance = balance - ?
                WHERE id = ?
            ''', (amount, account_id))
            print(f"Withdrew {amount} from account ID {account_id}")
    connection.commit()
    connection.close()

def view():
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()
    print("Fetching accounts with a balance greater than 0...")
    results = cursor.execute('''
        SELECT * FROM accounts WHERE balance > 0
    ''')

    print("Results:")
    for row in results:
        print(row)

    print("Fetching transactions...")
    results = cursor.execute('''
        SELECT * FROM transactions
    ''')

    print("Results:")
    for row in results:
        print(row)
    connection.commit()
    #account_id = cursor.lastrowid
    connection.close()
    

def main():
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()

    # test CRUD
    acc_id = create_account("Person", 100)
    #acc_id = 3
    deposit(4, 50)
    withdraw(4, 30)

    empty_db()
    turn_on = True
    while(turn_on):
        print("---Banking--Admin--App---\n1. Create an account\n2. Deposit\n3. Withdraw\n4. view accounts")
        choice = input('Enter the corresponding number to choose an action: ')
        if choice == '1':
            A_name = input('Enter account name: ')
            A_balance = int(input('Enter account balance: '))
            create_account(A_name,A_balance)
        elif choice == '2':
            A_id = int(input('Enter account id: '))
            A_amount = int(input('Enter deposit amount: '))
            deposit(A_id, A_amount)
        elif choice == '3':
            A_id = int(input('Enter account id: '))
            A_amount = int(input('Enter withdraw amount: '))
            withdraw(A_id, A_amount)
        elif choice == '4':
            view()



if __name__ == "__main__":
    main()
