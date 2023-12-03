import argparse
import json
import csv
import xml.etree.ElementTree as ET
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


def main():
    # initialize
    data_processor = UserDataProcessor()

    # load data
    data_processor.import_data({"./data/a/b/users_1.csv", "./data/a/b/users_1.xml", "./data/a/users.json"})

    # validate emails
    data_processor.validate_emails()

    # print sth
    print(data_processor.users)
    print(len(data_processor.users))

if __name__ == "__main__":
    main()