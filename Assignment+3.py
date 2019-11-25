
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.5** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 3 - More Pandas
# This assignment requires more individual learning then the last one did - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.

# ### Question 1 (20%)
# Load the energy data from the file `Energy Indicators.xls`, which is a list of indicators of [energy supply and renewable electricity production](Energy%20Indicators.xls) from the [United Nations](http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls) for the year 2013, and should be put into a DataFrame with the variable name of **energy**.
# 
# Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:
# 
# `['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']`
# 
# Convert `Energy Supply` to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as `np.NaN` values.
# 
# Rename the following list of countries (for use in later questions):
# 
# ```"Republic of Korea": "South Korea",
# "United States of America": "United States",
# "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
# "China, Hong Kong Special Administrative Region": "Hong Kong"```
# 
# There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these, 
# 
# e.g. 
# 
# `'Bolivia (Plurinational State of)'` should be `'Bolivia'`, 
# 
# `'Switzerland17'` should be `'Switzerland'`.
# 
# <br>
# 
# Next, load the GDP data from the file `world_bank.csv`, which is a csv containing countries' GDP from 1960 to 2015 from [World Bank](http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). Call this DataFrame **GDP**. 
# 
# Make sure to skip the header, and rename the following list of countries:
# 
# ```"Korea, Rep.": "South Korea", 
# "Iran, Islamic Rep.": "Iran",
# "Hong Kong SAR, China": "Hong Kong"```
# 
# <br>
# 
# Finally, load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology](http://www.scimagojr.com/countryrank.php?category=2102) from the file `scimagojr-3.xlsx`, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame **ScimEn**.
# 
# Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15). 
# 
# The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
#        'Citations per document', 'H index', 'Energy Supply',
#        'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008',
#        '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
# 
# *This function should return a DataFrame with 20 columns and 15 entries.*

# In[1]:


import pandas as pd
import numpy as np
import re

def energy():
    energy = pd.read_excel('Energy Indicators.xls', convert_numeric=True)
    
    #drop first 16 rows
    energy.drop(energy.index[:16], inplace=True) 
    
    #drop first 2 columns
    energy = energy.drop(['Unnamed: 0', 'Unnamed: 1'], axis=1) 
    
    #rename all the columns
    energy.rename(columns={'Environmental Indicators: Energy': 'Country', 'Unnamed: 3': 'Energy Supply', 
                           'Unnamed: 4': 'Energy Supply per Capita', 
                           'Unnamed: 5': '% Renewable' }, inplace=True) #rename all the columns
    
    #replace missing data with np.NaN values
    energy.replace('...', np.NaN, inplace=True) 
    energy.reset_index(inplace=True,drop=True)
    energy.loc[:,'Energy Supply'] *= 1000000
    
    #drop NA
    energy.dropna(axis=0, how='all', thresh = 2, inplace=True) 
    
    #remove digits from country name
    energy['Country'] = energy['Country'].str.replace('\d+','') 
    
    #regular experssion
    energy['Country'] = energy['Country'].str.replace('\([^)]*\)','')
    
    #update special country names
    energy['Country'] = energy['Country'].replace({"Republic of Korea": "South Korea",
    "United States of America": "United States",
    "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
    "China, Hong Kong Special Administrative Region": "Hong Kong"})  
    
    #Convert argument to a numeric type
    energy['Energy Supply'] = pd.to_numeric(energy['Energy Supply'])
    energy['Energy Supply per Capita'] = pd.to_numeric(energy['Energy Supply per Capita'])
    energy['% Renewable'] = pd.to_numeric(energy['% Renewable'])
    energy['Country'] = energy['Country'].map(lambda x: x.strip())
    return energy

def GDP():   
    GDP = pd.read_csv('world_bank.csv')
    
    #drop first 4 rows
    GDP.drop(GDP.index[:4], inplace=True) 
    GDP.reset_index(inplace=True,drop=True)
    GDP = GDP.rename(columns = {'Data Source' : 'Country'})
    GDP['Country'] = GDP['Country'].replace({"Korea, Rep.": "South Korea", 
    "Iran, Islamic Rep.": "Iran",
    "Hong Kong SAR, China": "Hong Kong"})
    for n in range(2,50):
        GDP = GDP.drop(["Unnamed: " + str(n)],axis=1)
    for n in range(50,60):
        GDP.rename(columns={"Unnamed: " + str(n): str(int(n)+int(1956))}, inplace=True)
    GDP = GDP.drop('World Development Indicators', axis=1)
    GDP = GDP.rename(columns = {'Data Source' : 'Country'})
    return GDP

def ScimEn():
    ScimEn = pd.read_excel('scimagojr-3.xlsx')
    return ScimEn

def answer_one():
    df1 = pd.merge(ScimEn(), energy())
    df1 = pd.merge(df1, GDP())   
    answer_one = df1[:15]
    answer_one = answer_one.set_index('Country')
    return answer_one       

answer_one()


# ### Question 2 (6.6%)
# The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?
# 
# *This function should return a single number.*

# In[2]:


get_ipython().run_cell_magic('HTML', '', '<svg width="800" height="300">\n  <circle cx="150" cy="180" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="blue" />\n  <circle cx="200" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="red" />\n  <circle cx="100" cy="100" r="80" fill-opacity="0.2" stroke="black" stroke-width="2" fill="green" />\n  <line x1="150" y1="125" x2="300" y2="150" stroke="black" stroke-width="2" fill="black" stroke-dasharray="5,3"/>\n  <text  x="300" y="165" font-family="Verdana" font-size="35">Everything but this!</text>\n</svg>')


# In[3]:


def answer_two(): 
    #merge GDP with ScimEn
    df2 = pd.merge(GDP(), ScimEn())
    
    #merge with energy dataframe
    df2 = pd.merge(df2,energy())
    
    #calculate gap
    df2 = len(df2.index)-len(answer_one().index)
    
    return df2


answer_two()


# ## Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by `answer_one()`)

# ### Question 3 (6.6%)
# What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)
# 
# *This function should return a Series named `avgGDP` with 15 countries and their average GDP sorted in descending order.*

# In[4]:


def answer_three():
    years = [str(year) for year in range(int(2006),int(2016))]
    
    #to get top 15 countries
    df3 = answer_one()[:15]
    
    #calculate average GDP
    df3['avgGDP'] = df3[years].mean(axis=1)
    
    #return values in descending order
    return df3['avgGDP'].sort_values(axis=0, ascending=False, inplace=False)

answer_three()


# ### Question 4 (6.6%)
# By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?
# 
# *This function should return a single number.*

# In[5]:


years = [str(year) for year in range(int(2006),int(2016))]

df4 = answer_one()[:15]
df4['avgGDP'] = df4[years].mean(axis=1)

#sort value by avgGDP in descending order
df4 = df4.sort_values(by=['avgGDP'], axis=0, ascending=False, inplace=False)

#index and slicing
df4 = df4.ix[5,'2006':'2015']

def answer_four():
    return (df4.loc['2015'])-(df4.loc['2006'])

answer_four()


# ### Question 5 (6.6%)
# What is the mean `Energy Supply per Capita`?
# 
# *This function should return a single number.*

# In[6]:



def answer_five():
    df5 = answer_one()['Energy Supply per Capita'].mean(axis=0)
    return df5

answer_five()


# ### Question 6 (6.6%)
# What country has the maximum % Renewable and what is the percentage?
# 
# *This function should return a tuple with the name of the country and the percentage.*

# In[7]:


df6 = answer_one()
df6 = df6.sort_values(by=['% Renewable'], axis=0, ascending=False)

# index & slicing
df6 = df6.ix[0,:'% Renewable']

def answer_six():
    df7 = df6['% Renewable']
    country6 = (df6.name,df7)
    return country6
    
answer_six()


# ### Question 7 (6.6%)
# Create a new column that is the ratio of Self-Citations to Total Citations. 
# What is the maximum value for this new column, and what country has the highest ratio?
# 
# *This function should return a tuple with the name of the country and the ratio.*

# In[8]:


df8 = answer_one()

#calculate the ratio of self-citations to total citations
df8['Citratio'] = df8['Self-citations']/df8['Citations']

#re-sorting by Citratio in descending order
df8 = df8.sort_values(by=['Citratio'], axis=0, ascending=False)

def answer_seven():  
    df9 = df8.ix[0,'Citratio']
    df10 = df8.ix[0,:'Citratio']
    df10=df10.name
    country7 = (df10,df9)
    return country7
    
answer_seven()


# ### Question 8 (6.6%)
# 
# Create a column that estimates the population using Energy Supply and Energy Supply per capita. 
# What is the third most populous country according to this estimate?
# 
# *This function should return a single string value.*

# In[9]:


df11 = answer_one()

#population calculation
df11['population'] = df11['Energy Supply']/df11['Energy Supply per Capita']

#re-sorting by population value
df11 = df11.sort_values(by=['population'],axis=0, ascending=False)
def answer_eight():
    df12 = df11.ix[:,'population']
    df12 = df12[2:3]
    return df12.index[0]

answer_eight()


# ### Question 9 (6.6%)
# Create a column that estimates the number of citable documents per person. 
# What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the `.corr()` method, (Pearson's correlation).
# 
# *This function should return a single number.*
# 
# *(Optional: Use the built-in function `plot9()` to visualize the relationship between Energy Supply per Capita vs. Citable docs per Capita)*

# In[10]:


def answer_nine():
    df13 = answer_one()
    df13['Citable docs per Capita'] = df13['Citable documents']/df11['population']
    df14 = pd.to_numeric(df13['Citable docs per Capita'])
    df15 = pd.to_numeric(df13['Energy Supply per Capita'])
    return df14.corr(df15)

answer_nine()


# In[11]:


#def plot9():
 #   import matplotlib as plt
  #  %matplotlib inline
   # 
   # Top15 = answer_one()
    #Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    #Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    #Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


# In[12]:


#plot9() # Be sure to comment out plot9() before submitting the assignment!


# ### Question 10 (6.6%)
# Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.
# 
# *This function should return a series named `HighRenew` whose index is the country name sorted in ascending order of rank.*

# In[13]:


def answer_ten():
    df16 = answer_one()
    n = df16['% Renewable'].mean()
    print(n)
    print(df16['% Renewable'])
    df16['HighRenew'] = np.where(df16['% Renewable']>=n, 0, 1)
    df16 = df16['HighRenew']
    df16 = pd.Series(sorted(df16))  
    return df16

answer_ten()


# ### Question 11 (6.6%)
# Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.
# 
# ```python
# ContinentDict  = {'China':'Asia', 
#                   'United States':'North America', 
#                   'Japan':'Asia', 
#                   'United Kingdom':'Europe', 
#                   'Russian Federation':'Europe', 
#                   'Canada':'North America', 
#                   'Germany':'Europe', 
#                   'India':'Asia',
#                   'France':'Europe', 
#                   'South Korea':'Asia', 
#                   'Italy':'Europe', 
#                   'Spain':'Europe', 
#                   'Iran':'Asia',
#                   'Australia':'Australia', 
#                   'Brazil':'South America'}
# ```
# 
# *This function should return a DataFrame with index named Continent `['Asia', 'Australia', 'Europe', 'North America', 'South America']` and columns `['size', 'sum', 'mean', 'std']`*

# In[14]:


def answer_eleven():

    ContinentDict  = {'China':'Asia', 
                      'United States':'North America', 
                      'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}

    df17 = pd.DataFrame(columns = ['size', 'sum', 'mean', 'std'])
    for elements in set(ContinentDict.values()):        
        df17.loc[elements] = 0
        
    df18 = answer_one()
    df18data= df18.groupby(ContinentDict)
    
    for a,b in df18data:
        EstPop = (b['Energy Supply']/b['Energy Supply per Capita'])
        df17.loc[a]=[len(b),EstPop.sum(),EstPop.mean(),EstPop.std()]
        df17.sort_index(axis=0, level=None, ascending=True, inplace=True)
        
    return df17

answer_eleven()


# ### Question 12 (6.6%)
# Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?
# 
# *This function should return a __Series__ with a MultiIndex of `Continent`, then the bins for `% Renewable`. Do not include groups with no countries.*

# In[15]:


def answer_twelve():
    ContinentDict  = {'China':'Asia', 
                    'United States':'North America', 
                    'Japan':'Asia', 
                    'United Kingdom':'Europe', 
                    'Russian Federation':'Europe', 
                    'Canada':'North America', 
                    'Germany':'Europe', 
                    'India':'Asia',
                    'France':'Europe', 
                    'South Korea':'Asia', 
                    'Italy':'Europe', 
                    'Spain':'Europe', 
                    'Iran':'Asia',
                    'Australia':'Australia', 
                    'Brazil':'South America'}
  
    df19 = answer_one()
    df20 = pd.DataFrame([ContinentDict])
    df20 = df20.T
    df19['Continents'] = df20[0]
    df19['Bins'] = pd.cut(df19['% Renewable'],5)
    return df19.groupby([df19['Continents'],df19['Bins']]).size() # size of n dimensional object

answer_twelve()


# ### Question 13 (6.6%)
# Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.
# 
# e.g. 317615384.61538464 -> 317,615,384.61538464
# 
# *This function should return a Series `PopEst` whose index is the country name and whose values are the population estimate string.*

# In[16]:


def answer_thirteen():
    df21 = df11['population']
    format1 = '{:,}'.format(123456789)
    df22 = []
    for elements in df21:
        df22.append('{:,}'.format(elements))
    df21 = pd.DataFrame(df21)
    df21['PopEst'] = df22
    return df21['PopEst'].astype(str)


answer_thirteen()


# ### Optional
# 
# Use the built in function `plot_optional()` to see an example visualization.

# In[17]:


#def plot_optional():
 #   import matplotlib as plt
  #  %matplotlib inline
   # Top15 = answer_one()
    #ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
     #               c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
      #                 '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
       #             xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    #for i, txt in enumerate(Top15.index):
     #   ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    #print("This is an example of a visualization that can be created to help understand the data. \
#This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' \
#2014 GDP, and the color corresponds to the continent.")


# In[18]:


#plot_optional() # Be sure to comment out plot_optional() before submitting the assignment!

