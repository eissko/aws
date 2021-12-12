from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
import re
import sqlite3
import glob
import logging
import traceback
import sys

# https://beautiful-soup-4.readthedocs.io/en/latest/#kinds-of-objects
# https://www.mssqltips.com/sqlservertip/7041/python-example-web-scraping-project/
# https://docs.python.org/3/library/sqlite3.html
# https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html

def clear_str(s:str, removespaces: bool=False, tolower:bool=False):
    if s is None:
        return "none"
    
    if '(*required)' in s:
        s=s.replace('(*required)','')

    replacement=' '
    if removespaces:
        replacement = ''
    
    s =re.sub(r'\s+',replacement,s).strip()
    if tolower:
        s=s.lower()
    
    return s


con = sqlite3.connect(f'amazon_iam.db')
services = glob.glob('html\\*.html')
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)

for svc in services:
    try:
        logger.warning(f'>>>>> processing {svc}')
        amzn_service = svc.split('_')[1].split('.')[0]
        db_table = amzn_service.replace("-","")

        # create table
        with con:
            con.execute(f'''create table if not exists {db_table} (actions varchar,
                description varchar,
                accesslevel varchar,
                resourcetypes varchar,
                conditionkeys varchar,
                dependentactions varchar)''')
        
        # load html contet
        with open(f'{svc}','r') as fp:
            soup = BeautifulSoup(fp, 'html.parser')

        # find tables from page based on tags
        iam_tables = soup.find_all("div",class_="table-contents")
        table_count = len(iam_tables)

        # expecting 3 html tables in the aws page
        if table_count != 3:
            logger.warning(f'=========== warning: amazon service {svc} has no 3 tables in the page')
        # assign tables
        action_tbl = iam_tables[0]
        # resource_types_tbl = iam_tables[1]
        # condition_keys = iam_tables[2]

        # Tag.has_attr()
        # Tag.is_empty_element

        ################################3
        ## table columns

        column_header = action_tbl.thead.find_all("th")

        clmns=[]
        for s in column_header: 
            clmns.append(clear_str(s.text,tolower=True,removespaces=True))

        # go to thead level, and get all rows
        tr_list = action_tbl.thead.find_next_siblings()
        actions_result = {}

        # convert BeautifulSoup objects to 2-dimensional list
        rows = []
        for indx, tr in enumerate(tr_list):
            td_list = tr.find_all("td")
            row=[]
            for x,td in enumerate(td_list):
                row.append(clear_str(td.text) if td.text else "none")
            rows.append(row)

        # loop again and insert rowspan columns to rows
        for indx, tr in enumerate(tr_list):
            td_list = tr.find_all("td")
            
            for x,td in enumerate(td_list):
                if td.has_attr('rowspan') and td['rowspan'].isdigit():
                    rowspan = int(td['rowspan'])
                    if rowspan > 1:
                        for k in range(indx+1,indx+rowspan):
                            rows[k].insert(x,clear_str(td.text) if td.text else "none")
        # save to db
        for row in rows:
            if len(row) ==6:
                with con:
                    con.execute(f'''insert into {db_table}(actions,description,accesslevel,
                                    resourcetypes,conditionkeys,dependentactions) values (?,?,?,?,?,?)''', tuple(row))
            else:
                logger.error(f'========== eror {svc} row has no 6 columns {row}')
    except sqlite3.Error as er:
        exc_type, exc_value, exc_tb = sys.exc_info()
        logger.error(traceback.format_exception(exc_type, exc_value, exc_tb))
    except Exception as err:
        logger.error(f'============== error: Processing {svc} failed with error {err}')

con.close()