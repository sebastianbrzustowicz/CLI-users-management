import argparse
from UserDataProcessor import UserDataProcessor
import os

os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # CLI arguments
    parser = argparse.ArgumentParser(description='Manage user data')
    parser.add_argument('command', help='Command (possible user commands: print-children, find-similar-children-by-age)')
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
