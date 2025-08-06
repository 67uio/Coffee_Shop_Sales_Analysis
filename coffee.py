
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pyodbc 
from sqlalchemy import create_engine


cafe_sal=pd.read_csv(r"C:\Users\abdala\Downloads\archive (1)\dirty_cafe_sales.csv")
cafe_sal.head(20)

cafe_sal.info()

cafe_sal["Price Per Unit"].unique()
cafe_sal.groupby("Price Per Unit")["Item"].unique()



#make column to have a nan only

cafe_sal['Price Per Unit'] = cafe_sal['Price Per Unit'].replace('ERROR',np.nan)
cafe_sal['Price Per Unit'] = cafe_sal['Price Per Unit'].replace('UNKNOWN',np.nan)

#fill the nan values with mode
mode_val = cafe_sal['Price Per Unit'].mode()[0]
cafe_sal['Price Per Unit'] = cafe_sal['Price Per Unit'].fillna(mode_val)

cafe_sal['Price Per Unit'].isna().sum()

#  DATA VAILDATION : covert numbers in object type to float type 
cafe_sal['Price Per Unit']=cafe_sal['Price Per Unit'].astype(float)


cafe_sal[cafe_sal['Item'].isna()]["Price Per Unit"].value_counts()


### fill a nan of column based of another column ###


#make column to have a nan only
cafe_sal['Price Per Unit'] = cafe_sal['Price Per Unit'].replace('ERROR',np.nan)
cafe_sal['Price Per Unit'] = cafe_sal['Price Per Unit'].replace('UNKNOWN',np.nan)


fill_dict=\
    {
    1.0:"Cookie",
    1.5:"Tea",
    2.0:"Coffee",
    3.0:"Juice",
    4.0:"Sandwich",
    5.0:"Salad",
    }
    
cafe_sal['Item']=cafe_sal['Item'].replace(['UNKNOWN','ERROR'],np.nan)
cafe_sal['Item'] = cafe_sal['Item'].fillna(cafe_sal['Price Per Unit'].map(fill_dict))
cafe_sal['Item'].unique()


cafe_sal.info()


cafe_sal.head()


cafe_sal[:]=cafe_sal[:].replace(['UNKNOWN','ERROR'],np.nan)

## DATA VALIDATION 
cafe_sal["Quantity"]=cafe_sal["Quantity"].astype(float)
cafe_sal["Quantity"] =cafe_sal["Quantity"].fillna(cafe_sal["Quantity"].median())
cafe_sal["Quantity"]=cafe_sal["Quantity"].astype(int)

cafe_sal["Total Spent"]=cafe_sal["Total Spent"].astype(float)
cafe_sal["Total Spent"] =cafe_sal["Quantity"]*cafe_sal['Price Per Unit']


cafe_sal['Location']=cafe_sal['Location'].fillna(cafe_sal['Location'].mode()[0])
cafe_sal['Payment Method']=cafe_sal['Payment Method'].fillna(cafe_sal['Payment Method'].mode()[0])


cafe_sal['Transaction Date']=pd.to_datetime(cafe_sal['Transaction Date'])
cafe_sal['Transaction Date']=cafe_sal['Transaction Date'].fillna(method='bfill')




cafe_sal.info()




sns.histplot(data=cafe_sal,x="Total Spent",bins=10)
plt.show()


sns.barplot(data=cafe_sal,x="Item",y='Total Spent')
plt.show()


#making variables 
server = 'MSI' 
database = 'Cafe_Sales'

connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

from urllib.parse import quote_plus

# Convert special characters in connection string
conn_url = quote_plus(connection_string)

# Create engine
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_url}")

from urllib.parse import quote_plus

# Convert special characters in connection string
conn_url = quote_plus(connection_string)

# Create engine
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={conn_url}")

# Push the DataFrame into SQL Server
cafe_sal.to_sql("Cafe_Sales_details", con=engine, if_exists="replace", index=False)