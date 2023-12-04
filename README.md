# Description
### CLI users management
This script is helpful with managing data with different types of files. (.json, .csv, .xml, .db)
The structure of the processed data is as follows:
- `firstname`
- `telephone_number`
- `email`
- `password` in plaintext
- `role`(admin/user)
- `created_at` date in format YYYY-MM-DD HH:MM:SS
- List of `children` with `(name, age)`

## CLI commands
The structure of raw command: `python script.py <command> --login <login> --password <password>`

### Available commands:
Admin:
- `print-all-accounts`
- `print-oldest-account`
- `group-by-age`
- `create_database`
  
Admin or user:
- `print-children`
- `find-similar-children-by-age`

# Examples
This section shows the use of each command.

## `print-all-accounts`
This command shows how many users are in users data.

### Input:

```python

python script.py print-all-accounts --login "kimberlymartin@example.org" --password "ns6REVen+g"

```

### Output:

```
69
```

## `print-oldest-account`
This command shows oldest existing account.

### Input:

```python

python script.py print-oldest-account --login "kimberlymartin@example.org" --password "ns6REVen+g"

```

### Output:

```
name: Justin
email_address: opoole@example.org
created_at: 2022-11-25 02:19:37
```

## `group-by-age`
This command displays the number of all children grouped by age, sorted in ascending order of quantity.

### Input:

```python

python script.py group-by-age --login "kimberlymartin@example.org" --password "ns6REVen+g"

```

### Output:

```
age: 13, count: 3
age: 5, count: 3
age: 3, count: 3
age: 18, count: 4
age: 10, count: 4
age: 14, count: 4
age: 16, count: 5
age: 7, count: 5
age: 6, count: 5
age: 15, count: 5
age: 9, count: 5
age: 4, count: 6
age: 11, count: 7
age: 2, count: 8
age: 8, count: 8
age: 12, count: 8
age: 17, count: 9
age: 1, count: 9
```

## `print-children`
This command shows user's children data.

### Input:

```python

python script.py print-children --login "kimberlymartin@example.org" --password "ns6REVen+g"

```

### Output:

```
Justin, 15
Sarah, 10
```

## `find-similar-children-by-age`
This command shows children with similar age (and their parent) as user's children.

### Input:

```python

python script.py find-similar-children-by-age --login "kimberlymartin@example.org" --password "ns6REVen+g"

```

### Output:

```
Sean, 650232530: Dan, 10
Felicia, 394426853: Jennifer, 2; Omar, 10
Donna, 893849179: Kimberly, 2; Mark, 15; Paul, 1
Amanda, 698312978: Brenda, 1; Christopher, 15; Lisa, 8
Jeffrey, 854869516: Brian, 13; John, 15
Eric, 110355347: Evan, 2; Mary, 1; Mary, 15
Michael, 667574950: Justin, 15; Sarah, 10
Jamie, 608442660: Jesse, 7; Jonathan, 13; Victor, 10
```

## `create_database`
This command allows the administrator to create a database via SQLite with all the collected data. Script allows to read files with .db extension.

### Input:

```python

python script.py create_database --login "kimberlymartin@example.org" --password "ns6REVen+g"

```

### Output:

```
database created
```
