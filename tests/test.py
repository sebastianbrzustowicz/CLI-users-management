import unittest
import sys
from io import StringIO
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from script import UserDataProcessor
os.system('cls' if os.name == 'nt' else 'clear')

class TestUserDataProcessor(unittest.TestCase):
    def setUp(self):
        self.data_processor = UserDataProcessor()
        self.test_files = {
            '../data/a/b/users_1.csv',
            '../data/a/b/users_1.xml',
            '../data/a/users.json',
            '../data/a/c/users_2.csv',
            '../users_database.db'
        }

    def test_00_load_data_from_json(self):
        print('\nData completeness test from JSON file')
        self.data_processor._load_json('../data/a/users.json')
        self.assertEqual(len(self.data_processor.users), 31, 'Users not loaded from json file')

    def test_01_json_data(self):
        print('\nJSON data sample validation')
        self.data_processor._load_json('../data/a/users.json')
        output = ['Michael', '(48)667574950', 'kimberlymartin@example.org', 'ns6REVen+g', 'admin', '2023-11-19 20:42:33', [['Justin', 15], ['Sarah', 10]]]
        self.assertEqual(self.data_processor.users[7], output, 'Loaded json data is not appropriate')

    def test_02_load_data_from_xml(self):
        print('\nData completeness test from XML file')
        self.data_processor._load_xml('../data/a/b/users_1.xml')
        self.assertEqual(len(self.data_processor.users), 15, 'Users not loaded from xml file')

    def test_03_xml_data(self):
        print('\nXML data sample validation')
        self.data_processor._load_xml('../data/a/b/users_1.xml')
        output = ['Brandy', '00686983157', 'andrew36@example.net', '(UVIl#9&q7', 'admin', '2022-12-04 08:30:37', [['Teresa', 4]]]
        self.assertEqual(self.data_processor.users[0], output, 'Loaded xml data is not appropriate')

    def test_04_load_data_from_csv(self):
        print('\nData completeness test from CSV file')
        self.data_processor._load_csv('../data/a/c/users_2.csv')
        self.assertEqual(len(self.data_processor.users), 20, 'Users not loaded from csv file')

    def test_05_csv_data(self):
        print('\nCSV data sample validation')
        self.data_processor._load_csv('../data/a/c/users_2.csv')
        output = ['Don', '612660796', 'tamara37@example.com', 'jQ66IIlR*1', 'user', '2023-08-23 23:27:09', [['Michael', 12], ['Theresa', 6], ['Judith', 1]]]
        self.assertEqual(self.data_processor.users[0], output, 'Loaded csv data is not appropriate')

    def test_06_load_data_from_db(self):
        print('\nData completeness test from DB file')
        self.data_processor._load_db('../users_database.db')
        self.assertEqual(len(self.data_processor.users), 84, 'Users not loaded from db file')

    def test_07_db_data(self):
        print('\nDB data sample validation')
        self.data_processor._load_db('../users_database.db')
        output = ['Russell', '817730653', 'jwilliams@example.com', '4^8(Oj52C+', 'admin', '2023-05-15 21:57:02', [['Rebecca', 11], ['Christie', 17]]]
        self.assertEqual(self.data_processor.users[0], output, 'Loaded db data is not appropriate')

    def test_08_import_data(self):
        print('\nImporting multiple files')
        self.data_processor.import_data({
            '../data/a/b/users_1.csv',
            '../data/a/b/users_1.xml',
            '../data/a/users.json',
            '../data/a/c/users_2.csv',
        })
        self.assertEqual(len(self.data_processor.users), 82, 'Files are lodaded wrongly')

    def test_09_validate_emails(self):
        print('\nEmails validation')
        self.data_processor.import_data({'../data/a/b/users_1.csv'})
        self.data_processor.validate_emails()
        self.assertEqual(len(self.data_processor.users), 12, 'Emails are validated wrongly')

    def test_10_process_telephone_numbers(self):
        print('\nTelephone numbers validation')
        self.data_processor.import_data({'../data/a/c/users_2.csv'})
        self.data_processor.validate_telephone()
        self.assertEqual(len(self.data_processor.users), 18, 'Telephone numbers are validated wrongly')

    def test_11_remove_duplicates(self):
        print('\nRemove duplicates')
        self.data_processor.import_data({'../data/a/c/users_2.csv'})
        self.data_processor.remove_duplicates()
        self.assertEqual(len(self.data_processor.users), 15, 'Duplicates are removed wrongly')

    def test_12_user_authentication(self):
        print('\nAuthentication - successful')
        self.data_processor.import_data({'../data/a/c/users_2.csv'})
        output = self.data_processor.authenticate_user('ashleyhall@example.net', '#0R0UT&yw2')
        expected = ['Cassandra', '088691177', 'ashleyhall@example.net', '#0R0UT&yw2', 'admin', '2023-01-14 22:11:14', [['Joshua', 1], ['Brittany', 14]]]
        self.assertEqual(output, expected, 'Account authentication unexpectedly failed')

    def test_13_user_authentication(self):
        print('\nAuthentication - wrong login')
        self.data_processor.import_data({'../data/a/c/users_2.csv'})
        output = self.data_processor.authenticate_user('12345678@example.net', '#0R0UT&yw2')
        expected = 'Your login is wrong'
        self.assertEqual(output, expected, 'Expected wrong login message')

    def test_14_user_authentication(self):
        print('\nAuthentication - wrong password')
        self.data_processor.import_data({'../data/a/c/users_2.csv'})
        output = self.data_processor.authenticate_user('ashleyhall@example.net', '12345678')
        expected = 'Your password is wrong. Try with double quotes around your password'
        self.assertEqual(output, expected, 'Expected wrong password message')

    def test_15_print_all_accounts(self):
        print('\nPrint all account')
        self.data_processor.import_data({'../data/a/c/users_2.csv'})
        self.data_processor.validate_emails()
        self.data_processor.validate_telephone()
        self.data_processor.remove_duplicates()
        captured_output = StringIO()
        sys.stdout = captured_output
        self.data_processor.print_all_accounts('greenmadison@example.net', '&S1XUo94)k')
        printed_value = captured_output.getvalue().strip()
        sys.stdout = sys.__stdout__
        self.assertEqual(printed_value, '14', 'Printing accounts is wrong')

    def test_16_print_oldest_account(self):
        print('\nPrint oldest account')
        self.data_processor.import_data({'../data/a/c/users_2.csv'})
        self.data_processor.validate_emails()
        self.data_processor.validate_telephone()
        self.data_processor.remove_duplicates()
        captured_output = StringIO()
        sys.stdout = captured_output
        self.data_processor.print_oldest_account('greenmadison@example.net', '&S1XUo94)k')
        printed_value = captured_output.getvalue().strip()
        sys.stdout = sys.__stdout__
        output = 'name: Madeline\nemail_address: matthewdecker2@example.com\ncreated_at: 2022-12-05 04:34:20'
        self.assertEqual(printed_value, output, 'Printing oldest account is wrong')

    def test_17_group_by_age(self):
        print('\nGroup by age')
        self.data_processor.import_data({'../data/a/c/users_2.csv'})
        self.data_processor.validate_emails()
        self.data_processor.validate_telephone()
        self.data_processor.remove_duplicates()
        captured_output = StringIO()
        sys.stdout = captured_output
        self.data_processor.group_by_age('greenmadison@example.net', '&S1XUo94)k')
        printed_value = captured_output.getvalue().strip()
        sys.stdout = sys.__stdout__
        output = 'age: 12, count: 1\nage: 5, count: 1\nage: 7, count: 1\nage: 15, count: 1\nage: 2, count: 1'
        self.assertEqual(printed_value[0:86], output, 'Grouping by age is wrong')

    def test_18_print_children(self):
        print('\nPrint children')
        self.data_processor.import_data({'../data/a/c/users_2.csv'})
        self.data_processor.validate_emails()
        self.data_processor.validate_telephone()
        self.data_processor.remove_duplicates()
        captured_output = StringIO()
        sys.stdout = captured_output
        self.data_processor.print_children('greenmadison@example.net', '&S1XUo94)k')
        printed_value = captured_output.getvalue().strip()
        sys.stdout = sys.__stdout__
        output = 'Kristin, 14'
        self.assertEqual(printed_value, output, 'Printing children is wrong')

    def test_19_find_similar_children_by_age(self):
        print('\nFind similar children by age')
        self.data_processor.import_data({'../data/a/c/users_2.csv'})
        self.data_processor.validate_emails()
        self.data_processor.validate_telephone()
        self.data_processor.remove_duplicates()
        captured_output = StringIO()
        sys.stdout = captured_output
        self.data_processor.find_similar_children_by_age('greenmadison@example.net', '&S1XUo94)k')
        printed_value = captured_output.getvalue().strip()
        sys.stdout = sys.__stdout__
        output = 'Kevin, 227397825: Kristin, 14\nCassandra, 088691177: Brittany, 14; Joshua, 1'
        self.assertEqual(printed_value, output, 'Finding similar children by age is wrong')

    def test_20_create_database(self):
        print('\nCreating database')
        self.data_processor.import_data({'../data/a/c/users_2.csv'})
        self.data_processor.validate_emails()
        self.data_processor.validate_telephone()
        self.data_processor.remove_duplicates()
        captured_output = StringIO()
        sys.stdout = captured_output
        self.data_processor.create_database('greenmadison@example.net', '&S1XUo94)k')
        printed_value = captured_output.getvalue().strip()
        sys.stdout = sys.__stdout__
        output = 'Database created successfully.'
        self.assertEqual(printed_value, output, 'Creating database is wrong')

if __name__ == '__main__':
    unittest.main()