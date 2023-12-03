import argparse
import json
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
import os
os.system('cls')

class UserDataProcessor:
    def __init__(self):
        self.users = []
        pass


    def import_data(self, files):
        # Load data from JSON, CSV, XML
        print("load data")
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
        print("load json")
        f = open(file)
        data = json.load(f)
        for row in data:
            firstname = row.get("firstname")
            telephone_number = row.get("telephone_number")
            email = row.get("email")
            password = row.get("password")
            role = row.get("role")
            created_at = row.get("created_at")
            children = row.get("children", [])
            self.users.append([firstname, telephone_number,
                               email, password, role, 
                               created_at, children])
        f.close()
        pass


    def _load_csv(self, file):
        print("load csv")
        with open(file, 'r') as data:
            csvreader = csv.reader(data, delimiter=';')
            header = next(csvreader)
            for row in csvreader:
                self.users.append(list(row))


    def _load_xml(self, file):
        print("load xml")
        tree = ET.parse(file)
        root = tree.getroot()
        for users in root.findall('user'):
            firstname = users.find('firstname').text
            telephone_number = users.find('telephone_number').text
            email = users.find('email').text
            password  = users.find('password').text
            role = users.find('role').text
            created_at = users.find('created_at').text
            children = users.find('children').text
            self.users.append([firstname, telephone_number,
                               email, password, role,
                               created_at, children])


    def validate_emails(self):
        print('validate emails')
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
        print('validate telephone')
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
        print('remove duplicates')
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


    def print_all_accounts(self, login, password):
        print('print all accounts')
        #for user in self.users:
        #    print(user)
        print(len(self.users))
        pass


    def print_oldest_account(self):
        print('print oldest account')
        pass


    def group_by_age(self):
        print('group by age')
        pass


    def print_children(self):
        print('print children')
        pass


    def find_similar_children_by_age(self):
        print('find similar children by age')
        pass


    def create_database(self):
        print('create database')
        pass


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
        data_processor.print_oldest_account()
    elif args.command == "group-by-age":
        data_processor.group_by_age()
    elif args.command == "print-children":
        data_processor.print_children()
    elif args.command == "find-similar-children-by-age":
        data_processor.find_similar_children_by_age()
    elif args.command == "create_database":
        data_processor.create_database()
    else:
        print("Invalid command")

    # print sth
    #print(data_processor.users)
    #print(len(data_processor.users))
    #print(args.command)

if __name__ == "__main__":
    main()