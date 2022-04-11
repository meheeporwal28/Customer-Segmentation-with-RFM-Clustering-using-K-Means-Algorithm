import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline
import matplotlib.ticker as mticker
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans
import datetime as dt
from datetime import datetime

from google.colab import files
uploaded = files.upload()


import pandas as pd
import io
df = pd.read_csv('Online Retail.csv',  encoding = 'unicode_escape') 
#print(df)
#Data Quality Check and cleaning
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format = "%d-%m-%Y %H:%M")
df.head()
df.shape
df.describe()
df.info()

df.isnull().values.any()
df.isnull().values.sum()
df.isnull().sum()*100/df.shape[0]

order_wise= df.dropna()

order_wise.shape
order_wise.isnull().sum()

#RFM implementation

# Extracting amount by multiplying quantity and unit price and saving the data into amount variable.
amount  = pd.DataFrame(order_wise.Quantity * order_wise.UnitPrice, columns = ["Amount"])
amount.head()

#Monetary Value
#merging amount in order_wise
order_wise = pd.concat(objs = [order_wise, amount], axis = 1, ignore_index = False)

#Monetary Function
# Finding total amount spent per customer
monetary = order_wise.groupby("CustomerID").Amount.sum()
monetary = monetary.reset_index()
monetary.head()

#Frequency Value
#Frequency function
frequency = order_wise[['CustomerID', 'InvoiceNo']]

# Getting the count of orders made by each customer based on customer ID.
k = frequency.groupby("CustomerID").InvoiceNo.count()
k = pd.DataFrame(k)
k = k.reset_index()
k.columns = ["CustomerID", "Frequency"]
k.head()

#Merging amount and frequency Columns
#creating master dataset
master = monetary.merge(k, on = "CustomerID", how = "inner")
master.head()

#Recency Value
recency  = order_wise[['CustomerID','InvoiceDate']]
maximum = max(recency.InvoiceDate)

maximum

#Generating recency function

# Filtering data for customerid and invoice_date
recency  = order_wise[['CustomerID','InvoiceDate']]

# Finding max data
maximum = max(recency.InvoiceDate)

# Adding one more day to the max data, so that the max date will have 1 as the difference and not zero.
maximum = maximum + pd.DateOffset(days=1)
recency['diff'] = maximum - recency.InvoiceDate
recency.head()

# recency by customerid
a = recency.groupby('CustomerID')
a.diff.min()

