import argparse
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
import sqlite3
import os

os.system('cls' if os.name == 'nt' else 'clear')


class UserDataProcessor:
    def __init__(self):
        self.users = []

    def import_data(self, files):
        # Load data from JSON, CSV, XML
        # Parameters: files (list): The paths to the SQLite database file.
        # Returns: None
        for file in files:
            if file.endswith('.json'):
                self._load_json(file)
            elif file.endswith('.csv'):
                self._load_csv(file)
            elif file.endswith('.xml'):
                self._load_xml(file)
            elif file.endswith('.db'):
                self._load_db(file)

    def _load_db(self, file):
        # Load data from a SQLite database file
        # Parameters: file (str): The path to the SQLite database file.
        # Returns: None
        conn = sqlite3.connect(file)

        cursor = conn.cursor()

        res = cursor.execute("""SELECT firstname, telephone_number, email, 
                                password, role, created_at FROM users""")
        data = res.fetchall()

        users = []
        for row in data:
            row = list(row)
            row.append([])
            users.append(row)

        # Load children data and associate with users
        res = cursor.execute('SELECT parent_email, name, age FROM children')
        data = res.fetchall()

        for row in data:
            row = list(row)
            for user in users:
                if user[2] == row[0]:
                    user[6].append([row[1], row[2]])

        conn.close()
        self.users = users
    
    def _load_json(self, file):
        # Load data from JSON file
        # Parameters: file (str): The path to the JSON file.
        # Returns: None
        f = open(file)
        data = json.load(f)
        for row in data:
            firstname = row.get('firstname')
            telephone_number = row.get('telephone_number')
            email = row.get('email')
            password = row.get('password')
            role = row.get('role')
            created_at = row.get('created_at')
            children_data = row.get('children', [])
            children = []

            for child in children_data:
                try:
                    if child:
                        name = child['name']
                        age = child['age']
                        children.append([name, age])
                except (AttributeError, ValueError) as e:
                    print(f'Error processing JSON child data: {e}')   

            self.users.append([firstname, telephone_number,
                               email, password, role, 
                               created_at, children])
        f.close()

    def _load_csv(self, file):
        # Load data from CSV file
        # Parameters: file (str): The path to the CSV file.
        # Returns: None
        with open(file, 'r') as data:
            csvreader = csv.reader(data, delimiter=';')
            header = next(csvreader)
            for row in csvreader:
                children_data = row[6].split(',')
                children = []
                for child in children_data:
                    if child:
                        child_data = child.split(' ')
                        child_data[1] = int(child_data[1].replace('(', '').replace(')', ''))
                        name = child_data[0]
                        age = child_data[1]
                        children.append([name, age])
                row[6] = children
                self.users.append(row)

    def _load_xml(self, file):
        # Load data from XML file
        # Parameters: file (str): The path to the XML file.
        # Returns: None
        tree = ET.parse(file)
        root = tree.getroot()

        for users in root.findall('user'):
            firstname = users.find('firstname').text
            telephone_number = users.find('telephone_number').text
            email = users.find('email').text
            password  = users.find('password').text
            role = users.find('role').text
            created_at = users.find('created_at').text
            children = []

            for child in users.findall('./children/child'):
                try:
                    if child:
                        name = child.find('name').text
                        age = int(child.find('age').text)
                        children.append([name, age])
                except Exception as e:
                    print(f'Error processing XML child data: {e}')      

            self.users.append([firstname, telephone_number,
                               email, password, role,
                               created_at, children])

    def validate_emails(self):
        # Validate email addresses in the users data.
        # Returns: None
        new_users = []
        for user in self.users:
            try:
                if user[2]:
                    at_count = user[2].count('@')
                    dot_count = user[2].count('.')
                    if at_count == 1 and dot_count == 1:
                        email_parts = user[2].split('@')
                        username = email_parts[0]
                        domain_parts = email_parts[1].split('.')
                        domain = domain_parts[0]
                        topdomain = domain_parts[1]

                        if len(username) >= 1 and len(domain) >= 1 and 1 <= len(topdomain) <= 4:
                            if topdomain.isalnum():
                                new_users.append(user)
            except Exception as e:
                print(f'Error validating email: {e}')

        self.users = new_users

    def validate_telephone(self):
        # Validate telephone numbers in the users data.
        # Returns: None
        new_users = []
        for user in self.users:
            try:
                if user[1]:
                    if user[1].isnumeric() and len(user[1]) == 9:
                        new_users.append(user)
                    else:
                        user[1] = user[1].replace(' ', '')
                        user[1] = user[1][len(user[1]) - 9:]
                        new_users.append(user)
            except Exception as e:
                print(f'Error validating telephone number: {e}')

        self.users = new_users

    def remove_duplicates(self):
        # This function removes duplicate numbers first.
        # If an account has a duplicated number AND email with another account 
        # then it will first select the newer user with the same number
        # Returns: None
        seen_numbers = {}
        unique_users = []

        for user in self.users:
            first_name, telephone_number, email, _, _, created_at, _ = user
            timestamp = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')

            # Check if number was seen
            if telephone_number in seen_numbers:
                existing_timestamp = seen_numbers[telephone_number]
                if timestamp > existing_timestamp:
                    # Actualize timestamp
                    seen_numbers[telephone_number] = timestamp
                    # Actualize account to newer one
                    unique_users = [u for u in unique_users if u[1] != telephone_number]
                    unique_users.append(user)
            else:
                seen_numbers[telephone_number] = timestamp
                unique_users.append(user)
        
        self.users = unique_users

        seen_emails = {}
        unique_users = []

        for user in self.users:
            first_name, telephone_number, email, _, _, created_at, _ = user
            timestamp = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')

            # Check if email was seen
            if email in seen_emails:
                existing_timestamp = seen_emails[email]
                if timestamp > existing_timestamp:
                    # Actualize timestamp
                    seen_emails[email] = timestamp
                    # Actualize account to newer one
                    unique_users = [u for u in unique_users if u[2] != email]
                    unique_users.append(user)
            else:
                seen_emails[email] = timestamp
                unique_users.append(user)
        
        self.users = unique_users

    def authenticate_user(self, login, password):
        # Authenticate a user based on login (telephone number or email) and password.
        # Parameters: login (str): telephone number or email, password (str).
        # Returns: user (list): The authenticated user's data if successful / None: If authentication fails.
        for user in self.users:
            if user[1] == login or user[2] == login:
                if user[3] == password:
                    return user
                else:
                    return 'Your password is wrong. Try with double quotes around your password'
        return 'Your login is wrong'

    def print_all_accounts(self, login, password):
        # Print the total number of accounts if the user is authenticated as an admin.
        # Parameters: login (str): telephone number or email, password (str).
        # Returns: None
        auth_result = self.authenticate_user(login, password)
        _, _, _, _, role, _, _ = auth_result
        
        if isinstance(auth_result, list):
            if role == 'admin':
                print(len(self.users))
            else:
                print(f'You need admin permission, but your role is: {role}')
        else:
            print(auth_result)

    def print_oldest_account(self, login, password):
        # Print information about the oldest account if the user is authenticated as an admin.
        # Parameters: login (str): telephone number or email, password (str).
        # Returns: oldest_user_data (list): Information about the oldest user [name, email_address, created_at] 
        # / None: If authentication fails.
        auth_result = self.authenticate_user(login, password)
        _, _, _, _, role, _, _ = auth_result

        if isinstance(auth_result, list):
            if role == 'admin':
                oldest_user = [None, None, datetime.now()]

                for user in self.users:
                    timestamp = datetime.strptime(user[5], '%Y-%m-%d %H:%M:%S')

                    if oldest_user[2] > timestamp:
                        oldest_user = [user[0], user[2], timestamp]
                print('name: ' + oldest_user[0])
                print('email_address: ' + oldest_user[1])
                print('created_at: ' + str(oldest_user[2]))
            else:
                print(f'You need admin permission, but your role is: {role}')
        else:
            print(auth_result)

    def group_by_age(self, login, password):
        # Group users children by age and print the count of children for each age if the user is authenticated as an admin.
        # Parameters: login (str): telephone number or email, password (str).
        # Returns: age_counts (dict): Dictionary with age counts / None: If authentication fails.
        auth_result = self.authenticate_user(login, password)
        _, _, _, _, role, _, _ = auth_result

        if isinstance(auth_result, list):
            if role == 'admin':
                age_counts = {}

                for user in self.users:
                    if user[6]:
                        for child in user[6]:
                            age = child[1]

                            if age in age_counts:
                                age_counts[age] += 1
                            else:
                                age_counts[age] = 1
                
                sorted_age_counts = dict(sorted(age_counts.items(), key=lambda item: item[1]))

                for age, count in sorted_age_counts.items():
                    print(f'age: {age}, count: {count}')
            else:
                print(f'You need admin permission, but your role is: {role}')
        else:
            print(auth_result)

    def print_children(self, login, password):
        # Print children information for the authenticated user.
        # Parameters: login (str): telephone number or email, password (str).
        # Returns: None
        auth_result = self.authenticate_user(login, password)

        if isinstance(auth_result, list):
            _, _, _, _, _, _, children = auth_result

            try:
                if children:
                    for child in children:
                        print(f'{child[0]}, {child[1]}')
            except Exception as e:
                print(f'Error printing children: {e}')
        else:
            print(auth_result)   

    def find_similar_children_by_age(self, login, password):
        # Find and print users with similar children by age for the authenticated user.
        # Parameters: login (str): telephone number or email, password (str).
        # Returns: None
        auth_result = self.authenticate_user(login, password)
        if isinstance(auth_result, list):
            _, _, _, _, _, _, children = auth_result
            children_age = []

            if children:
            # Get age of children
                try:
                    for child in children:
                        children_age.append(child[1])
                except Exception as e:
                    print(f'Error finding similar children: {e}')

                # Find children with similar age
                similar_children_data = []
                for user in self.users:
                    try:
                        if user[6]:
                            for child in user[6]:
                                for user_child in children_age:
                                    if user_child == child[1]:
                                        similar_children_data.append(user)
                    except Exception as e:
                        print(f'Error finding similar children: {e}')

                # Removing same users
                unique_users = []
                for user in similar_children_data:
                    if user not in unique_users:
                        unique_users.append(user)

                # Sort children alphabetically
                for user in unique_users:
                    user[6].sort(key=lambda x: x[0], reverse=False)

                # Extract data to display
                display_data = []
                for user in unique_users:
                    base_string = f'{user[0]}, {user[1]}:'
                    for child in user[6]:
                        base_string += f' {child[0]}, {child[1]};'
                    base_string = base_string[:-1]
                    display_data.append(base_string)

                for row in display_data:
                    print(row)

            else:
                print('No children data available for the authenticated user.')

        else:
            print(auth_result)

    def create_database(self, login, password):
        # Create a SQLite database with users and children tables 
        # if the user is authenticated as an admin.
        # Parameters: login (str): telephone number or email, password (str).
        # Returns: None
        auth_result = self.authenticate_user(login, password)

        if isinstance(auth_result, list):
            _, _, _, _, role, _, _ = auth_result

            if role == 'admin':
                conn = sqlite3.connect('users_database.db')
                cursor = conn.cursor()

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        firstname TEXT,
                        telephone_number TEXT,
                        email TEXT,
                        password TEXT,
                        role TEXT,
                        created_at TEXT
                    )
                ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS children (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        parent_email TEXT,
                        name TEXT,
                        age INTEGER,
                        FOREIGN KEY (parent_email) REFERENCES users (email)
                    )
                ''')

                users_data = []
                for user in self.users:
                    users_data.append(tuple(user[:6]))

                cursor.execute('DELETE FROM users')
                cursor.executemany('INSERT INTO users (firstname, telephone_number, email, password, role, created_at) VALUES (?, ?, ?, ?, ?, ?)', users_data)

                children_data_array = []
                for user in self.users:
                    try:
                        if user[6]:
                            for child in user[6]:
                                children_data_array.append([user[2], child[0], child[1]])
                    except Exception as e:
                        print(f'Error creating database: {e}')
                
                children_data = [tuple(user[:3]) for user in children_data_array]

                cursor.execute('DELETE FROM children')
                cursor.executemany('INSERT INTO children (parent_email, name, age) VALUES (?, ?, ?)', children_data)

                conn.commit()
                conn.close()

                print('Database created successfully.')
            else:
                print(f'You need admin permission, but your role is: {role}')
        else:
            print(auth_result)


def main():
    # CLI arguments
    parser = argparse.ArgumentParser(description='Manage user data')
    parser.add_argument('command', help='Command')
    parser.add_argument('--login', required=True, help='User login (email or telephone number)')
    parser.add_argument('--password', required=True, help='User password')
    args = parser.parse_args()

    # Initialize
    data_processor = UserDataProcessor()

    try:
        # Load data
        data_processor.import_data({
            './data/a/b/users_1.csv',
            './data/a/b/users_1.xml',
            './data/a/users.json',
            './data/a/c/users_2.csv',
            './users_database.db'
        })
    
        # Validate emails
        data_processor.validate_emails()
    
        # Validate telephone numbers
        data_processor.validate_telephone()
    
        # Remove duplicated phones and emails
        data_processor.remove_duplicates()
    
        # Perform actions based on commands
        if args.command == 'print-all-accounts':
            data_processor.print_all_accounts(args.login, args.password)
        elif args.command == 'print-oldest-account':
            data_processor.print_oldest_account(args.login, args.password)
        elif args.command == 'group-by-age':
            data_processor.group_by_age(args.login, args.password)
        elif args.command == 'print-children':
            data_processor.print_children(args.login, args.password)
        elif args.command == 'find-similar-children-by-age':
            data_processor.find_similar_children_by_age(args.login, args.password)
        elif args.command == 'create_database':
            data_processor.create_database(args.login, args.password)
        else:
            print('Invalid command')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    main()