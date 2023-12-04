import argparse
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
import sqlite3
import os
os.system('cls')

class UserDataProcessor:
    def __init__(self):
        self.users = []
        pass


    def import_data(self, files):
        # Load data from JSON, CSV, XML
        #print("load data")
        for file in files:
            if file.endswith(".json"):
                self._load_json(file)
                pass
            elif file.endswith(".csv"):
                self._load_csv(file)
                pass
            elif file.endswith(".xml"):
                self._load_xml(file)
                pass
    

    def _load_json(self, file):
        #print("load json")
        f = open(file)
        data = json.load(f)
        for row in data:
            firstname = row.get("firstname")
            telephone_number = row.get("telephone_number")
            email = row.get("email")
            password = row.get("password")
            role = row.get("role")
            created_at = row.get("created_at")
            children_data = row.get("children", [])
            children = []
            for child in children_data:
                try:
                    if child:
                        name = child['name']
                        age = child['age']
                        children.append([name, age])
                except:
                    pass
            self.users.append([firstname, telephone_number,
                               email, password, role, 
                               created_at, children])
        f.close()
        pass


    def _load_csv(self, file):
        #print("load csv")
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
        #print("load xml")
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
                except:
                    pass            
            self.users.append([firstname, telephone_number,
                               email, password, role,
                               created_at, children])


    def validate_emails(self):
        #print('validate emails')
        new_users = []
        for user in self.users:
            at_count = user[2].count('@')
            dot_count = user[2].count('.')
            if at_count == 1 and dot_count == 1:
                # Splitting email
                email_parts = user[2].split('@')
                username = email_parts[0]
                domain_parts = email_parts[1].split('.')
                domain = domain_parts[0]
                topdomain = domain_parts[1]
                if len(username) >= 1 and len(domain) >= 1 and 1 <= len(topdomain) <= 4:
                    if topdomain.isalnum():
                        new_users.append(user)
        self.users = new_users


    def validate_telephone(self):
        #print('validate telephone')
        new_users = []
        for user in self.users:
            try:
                if user[1].isnumeric() and len(user[1]) == 9:
                    new_users.append(user)
                else:
                    user[1] = user[1].replace(" ", "")
                    user[1] = user[1][len(user[1]) - 9:]
                    new_users.append(user)
            except:
                pass  
        self.users = new_users

    
    def remove_duplicates(self):
        # This function removes duplicate numbers first.
        # If an account has a duplicated number AND email with another account 
        # then it will first select the newer user with the same number
        #print('remove duplicates')
        seen_numbers = {}
        unique_users = []

        for user in self.users:
            first_name, telephone_number, email, _, _, created_at, _ = user
            timestamp = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')

            # check if number was seen
            if telephone_number in seen_numbers:
                existing_timestamp = seen_numbers[telephone_number]
                if timestamp > existing_timestamp:
                    # actualize timestamp
                    seen_numbers[telephone_number] = timestamp
                    # actualize account to newer one
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

            # check if email was seen
            if email in seen_emails:
                existing_timestamp = seen_emails[email]
                if timestamp > existing_timestamp:
                    # actualize timestamp
                    seen_emails[email] = timestamp
                    # actualize account to newer one
                    unique_users = [u for u in unique_users if u[2] != email]
                    unique_users.append(user)
            else:
                seen_emails[email] = timestamp
                unique_users.append(user)
        
        self.users = unique_users


    def authenticate_user(self, login, password):
        #print('authenticate user')
        for user in self.users:
            if user[1] == login or user[2] == login:
                if user[3] == password:
                    return user
                else:
                    return 'Your password is wrong'
        return 'Your login is wrong'


    def print_all_accounts(self, login, password):
        #print('print all accounts')
        auth_result = self.authenticate_user(login, password)
        if isinstance(auth_result, list):
            if auth_result[4] == 'admin':
                print(len(self.users))
            else:
                print(f'You need admin permission, but your role is: {auth_result[4]}')
        else:
            print(auth_result)


    def print_oldest_account(self, login, password):
        #print('print oldest account')
        auth_result = self.authenticate_user(login, password)
        if isinstance(auth_result, list):
            if auth_result[4] == 'admin':
                oldest_user = [None, None, datetime.now()]
                for user in self.users:
                    timestamp = datetime.strptime(user[5], '%Y-%m-%d %H:%M:%S')
                    if oldest_user[2] > timestamp:
                        oldest_user = [user[0], user[2], timestamp]
    
                print('name: ' + oldest_user[0])
                print('email_address: ' + oldest_user[1])
                print('created_at: ' + str(oldest_user[2]))
            else:
                print(f'You need admin permission, but your role is: {auth_result[4]}')
            
        else:
            print(auth_result)


    def group_by_age(self, login, password):
        #print('group by age')
        auth_result = self.authenticate_user(login, password)
        if isinstance(auth_result, list):
            if auth_result[4] == 'admin':
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
                print(f'You need admin permission, but your role is: {auth_result[4]}')
            
        else:
            print(auth_result)


    def print_children(self, login, password):
        #print('print children')
        auth_result = self.authenticate_user(login, password)
        if isinstance(auth_result, list):
            for user in self.users:
                if (user[1] == login or user[2] == login) and user[3] == password:
                    try:
                        if user[6]:
                            for child in user[6]:
                                print(f'{child[0]}, {child[1]}')
                    except:
                        pass
        else:
            print(auth_result)   


    def find_similar_children_by_age(self, login, password):
        #print('find similar children by age')
        auth_result = self.authenticate_user(login, password)
        if isinstance(auth_result, list):
            children_age = []
            # get age of children
            for user in self.users:
                if (user[1] == login or user[2] == login) and user[3] == password:
                    try:
                        if user[6]:
                            for child in user[6]:
                                children_age.append(child[1])
                    except:
                        pass

            # find children with similar age
            similar_children_data = []
            for user in self.users:
                try:
                    if user[6]:
                        for child in user[6]:
                            for user_child in children_age:
                                if user_child == child[1]:
                                    similar_children_data.append(user)
                except:
                    pass

            # removing same users
            unique_users = []
            for user in similar_children_data:
                if user not in unique_users:
                    unique_users.append(user)

            # sort children alphabetically
            for user in unique_users:
                user[6].sort(key=lambda x: x[0], reverse=False)

            # extract data to display
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
            print(auth_result)


    def create_database(self, login, password):
        #print('create database')
        auth_result = self.authenticate_user(login, password)
        if isinstance(auth_result, list):
            if auth_result[4] == 'admin':
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

                last_user_id = cursor.lastrowid

                children_data_array = []
                for user in self.users:
                    try:
                        if user[6]:
                            for child in user[6]:
                                children_data_array.append([user[2], child[0], child[1]])
                    except:
                        pass
                
                children_data = []
                for user in children_data_array:
                    children_data.append(tuple(user[:3]))

                cursor.execute('DELETE FROM children')
                cursor.executemany('INSERT INTO children (parent_email, name, age) VALUES (?, ?, ?)', children_data)

                conn.commit()
                conn.close()

                print('database created')
            else:
                print(f'You need admin permission, but your role is: {auth_result[4]}')
        else:
            print(auth_result)


def main():
    # CLI arguments
    parser = argparse.ArgumentParser(description="Manage user data")
    parser.add_argument("command", help="Command")
    parser.add_argument("--login", required=True, help="User login (email or telephone number)")
    parser.add_argument("--password", required=True, help="User password")
    #parser.add_argument("files", nargs="+", help="List of data files to process")
    args = parser.parse_args()

    # initialize
    data_processor = UserDataProcessor()

    # load data
    data_processor.import_data({"./data/a/b/users_1.csv", "./data/a/b/users_1.xml", "./data/a/users.json"})

    # validate emails
    data_processor.validate_emails()

    # validate telephone numbers
    data_processor.validate_telephone()

    # remove duplicated phones and emails
    data_processor.remove_duplicates()

    # perform actions based on commands
    if args.command == "print-all-accounts":
        data_processor.print_all_accounts(args.login, args.password)
    elif args.command == "print-oldest-account":
        data_processor.print_oldest_account(args.login, args.password)
    elif args.command == "group-by-age":
        data_processor.group_by_age(args.login, args.password)
    elif args.command == "print-children":
        data_processor.print_children(args.login, args.password)
    elif args.command == "find-similar-children-by-age":
        data_processor.find_similar_children_by_age(args.login, args.password)
    elif args.command == "create_database":
        data_processor.create_database(args.login, args.password)
    else:
        print("Invalid command")

if __name__ == "__main__":
    main()