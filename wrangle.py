import pandas as pd
import env
import os

def get_connection(db_name, username = env.username, host=env.host, password=env.password):
    '''
    This function makes a connection with and pulls from the CodeUp database. It 
    takes the database name as its argument, pulls other login info from env.py.
    Make sure you save this as a variable or it will print out your sensitive user
    info as plain text. 
    '''
    return f'mysql+pymysql://{username}:{password}@{host}/{db_name}'

def wrangle_telco(db_name = 'telco_db', username = env.username, password = env.password, host = env.host):
    '''
    Checks for telco.csv file, if present, pulls current file. If absent, it imports the telco churn database from /n
    the Codeup database and saves to .csv
    Creates telco_df of only 2 year contracts, cleans total_charges, and saves all nums as float64 types
    '''
    filename = 'telco.csv'
    if os.path.isfile(filename):
        telco_df = pd.read_csv(filename, index_col=0)
        telco_df = telco_df[telco_df['contract_type_id']== 3]
        telco_df = telco_df[['customer_id','monthly_charges','tenure','total_charges']]
        telco_df['total_charges'] = telco_df.total_charges.str.replace(' ','0.00').astype('float64')
        telco_df.tenure = telco_df.tenure.astype('float64')
        return telco_df
    else:
        telco_df = pd.read_sql('''SELECT * FROM customers 
                          JOIN internet_service_types USING(internet_service_type_id)
                          JOIN contract_types USING(contract_type_id)
                          JOIN payment_types USING (payment_type_id);''',
                        get_connection('telco_churn'))
        telco_df.to_csv(filename)
        telco_df = telco_df[telco_df['contract_type_id']== 3]
        telco_df = telco_df[['customer_id','monthly_charges','tenure','total_charges']]
        telco_df['total_charges'] = telco_df.total_charges.str.replace(' ','0.00').astype('float64')
        telco_df.tenure = telco_df.tenure.astype('float64')
        return telco_df