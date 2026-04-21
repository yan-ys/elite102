import sqlite3
import time


def empty_db():
      connection = sqlite3.connect('example.db')
      cursor = connection.cursor()
      cursor.execute("DELETE FROM accounts")
      cursor.execute("DELETE FROM transactions")
      connection.commit()
      #account_id = cursor.lastrowid
      connection.close()
      return "emptied"

def create_account(name, initial_balance):
      print("-------Create-Account-------")
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
    print("-------Deposit-------")
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
    ''', ("deposit", amount, account_id))

    if cursor.rowcount < account_id or account_id < 1:
        connection.commit()
        connection.close()
        return('Account not found')
    else:
        connection.commit()
        connection.close()
        return(f"Deposited {amount} into account ID {account_id}")

def withdraw(account_id, amount):
    print("-------Withdraw-------")
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()

    cursor.execute('''
        SELECT balance FROM accounts where id = ?
    ''', (account_id,))

    result = cursor.fetchone()
    if result is None:
        return("Account not found.")
    else:
        balance = result[0]
        if balance < amount:
            connection.commit()
            connection.close()
            return('Insufficient funds.')
        else:
            cursor.execute('''
                UPDATE accounts 
                SET balance = balance - ?
                WHERE id = ?
            ''', (amount, account_id))
            cursor.execute('''
                INSERT INTO transactions (transaction_type, amount, account_num)
                VALUES (?,?,?)
            ''', ("withdrawl", amount, account_id))
            connection.commit()
            connection.close()
            return(f"Withdrew {amount} from account ID {account_id}")


def view():
    print("-------View-------")
    connection = sqlite3.connect('example.db')
    cursor = connection.cursor()
    print("Fetching accounts...(id, name, balance)")
    results = cursor.execute('''
        SELECT * FROM accounts 
    ''')

    print("Results:")
    for row in results:
        print(row)

    print("Fetching transactions...(transaction id, amount, user id)")
    results = cursor.execute('''
        SELECT * FROM transactions
    ''')

    print("Results:")
    for row in results:
        print(row)
    connection.commit()
    #account_id = cursor.lastrowid
    connection.close()
    return "viewed"
    
def numInput(prompt):
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            return user_input
        except:
            print('Invalid input...please enter a numerical value')


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
        print("\n---Banking--Admin--App---\n1. Create an account\n2. Deposit\n3. Withdraw\n4. view accounts and transactions\n5. exit")
        choice = input('Enter the corresponding number to choose an action: ')
        if choice == '1':
            A_name = input('Enter account name: ')
            A_balance = numInput('Enter account balance: ')
            create_account(A_name,A_balance)
        elif choice == '2':
            A_id = numInput('Enter account id: ')
            A_amount = numInput('Enter deposit amount: ')
            print(deposit(A_id, A_amount))
        elif choice == '3':
            A_id = numInput('Enter account id: ')
            A_amount = numInput('Enter withdraw amount: ')
            print(withdraw(A_id, A_amount))
        elif choice == '4':
            view()
        elif choice == '5':
            quit()
        else:
            print('invalid input...enter an integer from the menu above')
        time.sleep(3)
        



if __name__ == "__main__":
    main()
