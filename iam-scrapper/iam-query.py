import sqlite3
import argparse
import json
import os

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--tbl', dest='table', action='store', help='name of sql table')
parser.add_argument('--db', dest='database', action='store', help='name of sql database', default='amazon_iam')
parser.add_argument('--query_filter', dest='query_filter', action='store', help='sql query filter e.g. actions = "WithdrawByoipCidr"')

args = parser.parse_args()

def main(table:str, database: str, query_filter: str):
    con = sqlite3.connect(os.path.join(os.path.dirname(os.path.realpath(__file__)),f'{database}.db'))

    with con:
        query_result = con.execute(f'SELECT * FROM {table} WHERE {query_filter}') 

    for row in query_result:                                       
        print(json.dumps(dict(zip(('actions','description','accesslevel','resourcetypes','conditionkeys','dependentactions'),row)),indent=4))
    con.close()


if __name__ == "__main__":
   main(database=args.database, table=args.table, query_filter=args.query_filter)