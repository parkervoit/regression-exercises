import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_variable_pairs(data_set, target):
    return sns.pairplot(data_set, hue = target)

def plot_categorical_and_continuous_vars(data_set, cat_var, con_var):
    sns.barplot(data = data_set, y = con_var, x = cat_var)
    plt.show()
    sns.violinplot(data = data_set, y = con_var, x = cat_var)
    plt.show()
    sns.boxplot(data = data_set, y = con_var, x = cat_var)

def heat_corr(data_set):
    return sns.heatmap(data_set.corr(), cmap='Greens', annot=True, linewidth=0.5, mask= np.triu(data_set.corr()))