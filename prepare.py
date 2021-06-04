
import pandas as pd
import env
import os
from scipy import stats
import sklearn.preprocessing
from sklearn.model_selection import train_test_split

def train_validate_test_split(df, seed=123):
    '''
    This function takes in a dataframe, the name of the target variable
    (for stratification purposes), and an integer for a setting a seed
    and splits the data into train, validate and test. 
    Test is 20% of the original dataset, validate is .30*.80= 24% of the 
    original dataset, and train is .70*.80= 56% of the original dataset. 
    The function returns, in this order, train, validate and test dataframes. 
    '''
    train_validate, test = train_test_split(df, test_size=0.2, 
                                            random_state=seed)
    train, validate = train_test_split(train_validate, test_size=0.3, 
                                       random_state=seed)
    return train, validate, test
    
def minmax_scale(data_set):
    '''
    Takes in the dataframe and applies a minmax scaler to it. Can pass a dataframe slice, 
    needs to be numbers. Outputs a scaled dataframe.  
    '''
    scaler = sklearn.preprocessing.MinMaxScaler()
    x_scaled = scaler.fit_transform(data_set)
    x_scaled = pd.DataFrame(x_scaled)
    x_scaled.columns = data_set.columns
    return x_scaled

def std_scale(data_set):
    '''
    Takes in the dataframe and applies a standard scaler to it. Can pass a dataframe slice, 
    needs to be numbers. Outputs a scaled dataframe.  
    '''
    scaler = sklearn.preprocessing.StandardScaler()
    x_scaled = scaler.fit_transform(data_set)
    x_scaled = pd.DataFrame(x_scaled)
    x_scaled.columns = data_set.columns
    return x_scaled

def robust_scale(data_set):
    '''
    Takes in the dataframe and applies a robust scaler to it. Can pass a dataframe slice, 
    needs to be numbers. Outputs a scaled dataframe.  
    '''
    scaler = sklearn.preprocessing.RobustScaler()
    x_scaled = scaler.fit_transform(data_set)
    x_scaled = pd.DataFrame(x_scaled)
    x_scaled.columns = data_set.columns
    return x_scaled