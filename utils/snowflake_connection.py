# libraries
import os
import sys
import snowflake.connector
import json
import numpy as np
import pandas as pd


### Load Credentials
cred_file = '/Users/adityajoshi/git_repos/shopify_kaggle/utils/.credentials.json'
with open(cred_file) as f:
    creds = json.load(f)

def get_connection(cred=None):
    conn = snowflake.connector.connect(
            user = creds['user']
            ,password = creds['password']
            ,account = creds['account']
            ,warehouse = creds['warehouse']
            ,database = creds['database']
            )
    return conn

def get_dataframe(query, creds=creds, verbose=0):
    ### get dataframe from running select statement query
    if verbose: print('running query...')

    with get_connection(creds) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            try:
                result_set = cur.fetchall()
                colnames = [desc[0] for desc in cur.description]
                df = pd.DataFrame.from_records(result_set, columns=colnames)
            except snowflake.connector.errors.ProgrammingError as e:
                if verbose: print('Error: \n' + e + '\nNo data to display.')
                if verbose: print('done*')
                return
    if verbose: print('done')
    return df
