import pandas as pd
import env
import os
from scipy import stats
import sklearn.preprocessing
from sklearn.model_selection import train_test_split

def get_connection(db_name, username = env.username, host=env.host, password=env.password):
    '''
    This function makes a connection with and pulls from the CodeUp database. It 
    takes the database name as its argument, pulls other login info from env.py.
    Make sure you save this as a variable or it will print out your sensitive user
    info as plain text. 
    '''
    return f'mysql+pymysql://{username}:{password}@{host}/{db_name}'
    
def missing_values_table(df):
    '''
    this function takes a dataframe as input and will output metrics for missing values, and the percent of that column that has missing values
    '''
        # Total missing values
    mis_val = df.isnull().sum()
        # Percentage of missing values
    mis_val_percent = 100 * df.isnull().sum() / len(df)
        # Make a table with the results
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        # Rename the columns
    mis_val_table_ren_columns = mis_val_table.rename(columns = {0 : 'Missing Values', 1 : '% of Total Values'})
        # Sort the table by percentage of missing descending
    mis_val_table_ren_columns = mis_val_table_ren_columns[
    mis_val_table_ren_columns.iloc[:,1] != 0].sort_values('% of Total Values', ascending=False).round(1)
        # Print some summary information
    print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
           "There are " + str(mis_val_table_ren_columns.shape[0]) +
           "columns that have missing values.")
        # Return the dataframe with missing information
    return mis_val_table_ren_columns

def wrangle_telco(db_name = 'telco_db', username = env.username, password = env.password, host = env.host):
    '''
    Checks for telco.csv file, if present, pulls current file. If absent, it imports the telco churn database from /n
    the Codeup database and saves to .csv
    Creates telco_df of only 2 year contracts, cleans total_charges, and saves all nums as float64 types
    '''
    filename = 'telco.csv'
    if os.path.isfile(filename):
        telco_df = pd.read_csv(filename, index_col=0)
        return telco_df
    else:
        telco_df = pd.read_sql('''SELECT * FROM customers 
                          JOIN internet_service_types USING(internet_service_type_id)
                          JOIN contract_types USING(contract_type_id)
                          JOIN payment_types USING (payment_type_id);''',
                        get_connection('telco_churn'))
        telco_df = telco_df[telco_df['contract_type_id']== 3]
        telco_df = telco_df[['customer_id','monthly_charges','tenure','total_charges']]
        telco_df['total_charges'] = telco_df.total_charges.str.replace(' ','0.00').astype('float64')
        telco_df.tenure = telco_df.tenure.astype('float64')
        telco_df.to_csv(filename)
        return telco_df
    
def wrangle_zillow(db_name = 'zillow', username = env.username, password = env.password, host = env.host):
    ''' 
    Checks for zillow.csv file and imports it if present. If absent, it will pull in bedroom bathroom counts, sq ft.
    tax value dollar count, year built, tax amount, and fips from properties 2017 in the zillow database. Then it will drop
    nulls and drop duplicates'''
    filename = 'zillow.csv'
    if os.path.isfile(filename):
        zillow_df = pd.read_csv(filename, index_col=0)
        return zillow_df
    else:
        zillow_df = pd.read_sql('''SELECT bedroomcnt, bathroomcnt, calculatedfinishedsquarefeet, 
                                      taxvaluedollarcnt, yearbuilt, taxamount, fips 
                                   FROM properties_2017
                                   WHERE propertylandusetypeid = 261;''', get_connection('zillow'))
        zillow_df = zillow_df.dropna()
        zillow_df = zillow_df.drop_duplicates()
        zillow_df.to_csv('zillow.csv')
        return zillow_df 

