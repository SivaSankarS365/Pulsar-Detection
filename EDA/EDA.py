#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import plotly.express as px
from pylab import rcParams
import warnings
import seaborn as sns 
rcParams["figure.figsize"]=(30,18)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = 15
warnings.filterwarnings("ignore")
warnings.simplefilter(action='ignore', category=FutureWarning)

df = pd.read_csv('../modeling/HTRU_2.csv', header=None)
df.columns = [
    'Mean of the integrated profile',                 
 'Standard deviation of the integrated profile',
 'Excess kurtosis of the integrated profile',
 'Skewness of the integrated profile',
 'Mean of the DM-SNR curve',
 'Standard deviation of the DM-SNR curve',
 'Excess kurtosis of the DM-SNR curve',
 'Skewness of the DM-SNR curve',
 'label'
]


# In[2]:


for i, column in enumerate(df.columns[:-1]): 
    plt.subplot(3, 3, i + 1)
    sns.histplot(df[column], bins=20, kde=True)
    plt.title(column)
plt.tight_layout()
plt.savefig('figures/histogram.png')


# In[4]:


pairplot = sns.pairplot(df, hue='label', diag_kind='hist')
for ax in pairplot.axes.flatten():
    ax.tick_params(axis='x', rotation=45)
for ax in pairplot.axes.flatten():
    ax.tick_params(axis='y', rotation=45)
plt.savefig('figures/pairplot.png')


# In[5]:


sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Matrix")
plt.savefig('figures/correlation_matrix.png')


# In[6]:


sns.countplot(x='label', data=df)
plt.title("Target Class Distribution")
plt.savefig('figures/target_class_distribution.png')


# In[8]:


for i, column in enumerate(df.columns[:-1]):  
    plt.subplot(3, 3, i + 1)
    sns.boxplot(x='label', y=column, data=df)
    plt.title(column)
plt.tight_layout()
plt.savefig('figures/boxplot.png')


# In[11]:


for i, column in enumerate(df.columns[:-1]):  
    plt.subplot(3, 3, i + 1)
    sns.violinplot(x='label', y=column, data=df)
    plt.title(column)
plt.tight_layout()
plt.savefig('figures/violinplot.png')


# In[13]:


for i, column in enumerate(df.columns[:-1]):  # Exclude the target class
    plt.subplot(3, 3, i + 1)
    sns.kdeplot(data=df, x=column, hue='label', fill=True, common_norm=False)
    plt.title(column)
plt.tight_layout()
plt.savefig('figures/kdeplot.png')


# In[ ]:




