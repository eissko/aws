# Actions, resources, and condition keys for AWS services scrapped from html pages to sqlite3 database

This project uses BeautifulSoup web scrapping for getting the IAM condition keys from 'https://docs.aws.amazon.com/service-authorization/latest/reference/' and saving them into local sqlite3 database. 

The html pages are downloaded by python script "iam-download-html.py" to local .\html directory.
Those are later processed by "iam-html-to-db.py" and saved into sqlite3 database named 'amazon_iam.db'.
The data in database can be queried by "iam-query.py" script.

## Disclaimer

This is just experiment. DO NOT USE in production. The project is offered “as-is”, without warranty, and disclaiming liability for damages resulting from using it.

## TODO

- to process Condition keys html table
- to process Resource types html table

## How to use it

Checkout the code and experiment. For simplification you can run the query via "iam-query.py" script as described below by examples.

## Prerequirements

- python
- libraries included in the python

## iam-query.py

- SQL queries are made over local database named "amazon_iam.db" which is part of repository
- Table names are construted from html names which are located in the  .\html directory
- pattern for generating the table names: 'filename.html'.split('_')[1].split('.')[0].replace("-","")
  -  'list_alexaforbusiness.html' -> table name is 'alexaforbusiness'
  -  'list_awsx-ray.html' -> table name is 'awsxray'


## Query examples

- python iam-query.py --tbl 'alexaforbusiness' --query_filter "1=1"

- python iam-query.py --tbl 'amazonec2' --query_filter "actions like 'Run%' and resourcetypes like '%*'"

- python iam-query.py --tbl 'alexaforbusiness' --query_filter "actions='AssociateContactWithAddressBook'"

```json
{
    "actions": "AssociateContactWithAddressBook",
    "description": "Grants permission to associate a contact with a given address book",
    "accesslevel": "Write",
    "resourcetypes": "addressbook*",
    "conditionkeys": "",
    "dependentactions": ""
}
{
    "actions": "AssociateContactWithAddressBook",
    "description": "Grants permission to associate a contact with a given address book",
    "accesslevel": "Write",
    "resourcetypes": "contact*",
    "conditionkeys": "",
    "dependentactions": ""
}
```
