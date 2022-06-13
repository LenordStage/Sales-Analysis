import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from collections import Counter
import calendar

Sales_April_2019 = pd.read_csv('Sales_April_2019.csv')
Sales_August_2019 = pd.read_csv('Sales_August_2019.csv')
Sales_December_2019 = pd.read_csv('Sales_December_2019.csv')
Sales_February_2019 = pd.read_csv('Sales_February_2019.csv')
Sales_January_2019 = pd.read_csv('Sales_January_2019.csv')
Sales_July_2019 = pd.read_csv('Sales_July_2019.csv')
Sales_June_2019 = pd.read_csv('Sales_June_2019.csv')
Sales_March_2019 = pd.read_csv('Sales_March_2019.csv')
Sales_May_2019 = pd.read_csv('Sales_May_2019.csv')
Sales_November_2019 = pd.read_csv('Sales_November_2019.csv')
Sales_October_2019 = pd.read_csv('Sales_October_2019.csv')
Sales_September_2019 = pd.read_csv('Sales_September_2019.csv')

all_months_data = pd.concat([Sales_April_2019, Sales_August_2019, Sales_December_2019, Sales_February_2019, Sales_January_2019, Sales_July_2019, Sales_June_2019, Sales_March_2019, Sales_May_2019, Sales_November_2019, Sales_October_2019, Sales_September_2019])

all_months_data['Month'] = all_months_data['Order Date'].str[0:2]
all_months_data = all_months_data.drop_duplicates()
all_months_data = all_months_data.dropna(axis=0, how ='any')
all_months_data.rename(columns = {'Quantity Ordered':'Qty', 'Purchase Address':'Address'}, inplace=True)
all_months_data.rename(columns = {'Price Each':'Price', 'Order Date':'Date'}, inplace=True)
temp_all_months_data = all_months_data[all_months_data['Date'].str[0:2] == 'Or']

all_months_data = all_months_data[all_months_data['Date'].str[0:2] != 'Or']

all_months_data['Month'] = all_months_data['Month'].astype('int16')
all_months_data['Price'] = pd.to_numeric(all_months_data['Price'])
all_months_data['Qty'] = pd.to_numeric(all_months_data['Qty'])
all_months_data['City'] = all_months_data['Address'].apply(lambda x: x.split(',')[1] )
all_months_data['State'] = all_months_data['Address'].apply(lambda x: x.split(' ')[4] )
all_months_data['City_State'] = all_months_data['City'] + ' ' + all_months_data['State']
all_months_data['Zip '] = all_months_data['Address'].apply(lambda x: x.split(' ')[5] )
all_months_data['Date'] = pd.to_datetime(all_months_data['Date'])
all_months_data['Hour'] = all_months_data['Date'].dt.hour
all_months_data['Minute'] = all_months_data['Date'].dt.minute
all_months_data['Sales'] = all_months_data['Qty'] * all_months_data['Price']
all_months_data['Sales'] = pd.to_numeric(all_months_data['Sales'])
all_months_data.to_csv('all_months_data.csv', index=False)
#df2 = df['math'].sum()
df = all_months_data['Sales'].sum()

sales_totals = all_months_data.groupby('Month').sum()
sales_totals.drop(['Qty', 'Price', 'Hour', 'Minute'], axis=1, inplace=True)
sales_totals.to_csv('sales_totals.csv')
sales_totals_b = pd.read_csv('sales_totals.csv')
sales_totals_b['Month'] = sales_totals_b['Month'].apply(lambda x: calendar.month_abbr[x])
al = sns.barplot(x = 'Month', y='Sales', data=sales_totals_b)
sns.set_palette("pastel")
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)
plt.xlabel('Month')
plt.ylabel('Sales in Dollars')
plt.title('Sales by Month')
for p in al.patches:
    al.annotate(format(p.get_height(), '.0f'),
                   (p.get_x() + p.get_width() / 2,
                    p.get_height()), ha='center', va='center',
                   size=8, xytext=(0, 8),
                   textcoords='offset points')
plt.rcParams['figure.figsize'] = [10, 10]
plt.show()
plt.savefig('Sales_Months.png')

######## The code below got the data for the dictionary in nearly the right format. I then 
##### edited it to get the data I wanted for the chart. 

#most_profitable_city = all_months_data.groupby('City_State').sum()
#most_profitable_city.drop(['Qty', 'Price', 'Month'], axis=1, inplace=True)
#profitable_city = most_profitable_city.to_dict('split')
#print(profitable_city)

profitable_city = {'City_State': ['Atlanta GA', 'Austin TX', 'Boston MA', 'Dallas TX', 
'LA. CA', 'NYC. NY', 'Pld. ME', 'Pld. OR', 'SF. CA', 'Seattle WA'],
 'Sales':[2794199, 1818044, 3658628, 2765374, 5448304, 4661867, 4493214, 1870011, 8254744, 2745046 ]}


am= sns.barplot(data=profitable_city, x = 'City_State', y='Sales')
sns.set_palette("pastel")
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)
plt.xlabel('City')
plt.ylabel('Sales in Dollars')
plt.title('Sales by City')
for p in am.patches:
    am.annotate(format(p.get_height(), '.0f'),
                   (p.get_x() + p.get_width() / 2,
                    p.get_height()), ha='center', va='center',
                   size=8, xytext=(0, 8),
                   textcoords='offset points')
plt.rcParams['figure.figsize'] = [10, 10]
plt.show()
#plt.savefig('Sales_By_City.png')

sns.displot(data=all_months_data, x='Hour', kind='kde')
plt.title('Number of Sales by Hour')
plt.rcParams['figure.figsize'] = [10, 10]
plt.show()
#plt.savefig('Number of Sales by Hour.png')

sns.lineplot(x='Hour', y='Sales', data= all_months_data)
plt.title('Sales Totals by Hour')
plt.rcParams['figure.figsize'] = [10, 10]
plt.show()
#plt.savefig('Sales Totals by Hour.png')

#print(all_months_data.head(10))

duplicate_orders = all_months_data[all_months_data['Order ID'].duplicated(keep=False)]
duplicate_orders['Grouped'] = duplicate_orders.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
duplicate_orders = duplicate_orders[['Order ID', 'Grouped']].drop_duplicates()

count2 = Counter()
for row in duplicate_orders['Grouped']:
    row_list = row.split(',')
    count2.update(Counter(combinations(row_list, 2)))
    
count2df = pd.DataFrame.from_dict(count2, orient='index').reset_index()
count2df.to_csv('count2dfb.csv')
count2dfc = pd.read_csv('count2dfb.csv')
count2dfc.rename(columns = {'index':'items', '0':'number'}, inplace=True)
count2dfd = count2dfc[['items','number']].sort_values('number', ascending=False).nlargest(9,'number')
ar= sns.barplot(data=count2dfd, x ='number', y='items')
sns.set_palette("pastel")
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)
plt.ylabel('Products in Pairs')
plt.xlabel('Number of Sales')
plt.title('Number of Sales by Prodcuts-Grouped')
plt.rcParams['figure.figsize'] = [10, 10]
plt.show()
plt.savefig('Number of Sales by Prodcuts-Grouped-2.png')
    
count3 = Counter()
for row in duplicate_orders['Grouped']:
    row_list = row.split(',')
    count3.update(Counter(combinations(row_list, 3)))

count3df = pd.DataFrame.from_dict(count3, orient='index').reset_index()
count3df.to_csv('count3dfb.csv')
count3dfc = pd.read_csv('count3dfb.csv')
count3dfc.rename(columns = {'index':'items', '0':'number'}, inplace=True)
count3dfd = count3dfc[['items','number']].sort_values('number', ascending=False).nlargest(9,'number')

at= sns.barplot(data=count3dfd, x ='number', y='items')
sns.set_palette("pastel")
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)
plt.ylabel('Products in Triples')
plt.xlabel('Number of Sales')
plt.title('Number of Sales by Prodcuts-Grouped')
plt.rcParams['figure.figsize'] = [10, 10]
plt.show()
plt.savefig('Number of Sales by Prodcuts-Grouped-3.png')

df3 = all_months_data.groupby('Product').sum()
df3.drop(['Minute', 'Hour', 'Month', 'Price', 'Sales'], axis=1, inplace=True)
df4= df3.to_dict('split')
#print(df4)

df4 = {'Product': ['20in Monitor', '27in 4K Gaming Monitor', '27in FHD Monitor', '34in Ultrawide Monitor',
           'AA Batteries (4-pack)', 'AAA Batteries (4-pack)', 'Apple Airpods',
           'Bose SS Headphones', 'Flatscreen TV', 'Google Phone', 'LG Dryer',
           'LG Washing Machine', 'Lightning Chg, Cable', 'Macbook Pro Laptop',
           'ThinkPad Laptop', 'USB-C Charging Cable', 'Vareebadd Phone', 'Wired Headphones',
           'iPhone'],'Qty':[4126, 6239, 7541, 6192, 27615, 30986, 15637, 13430, 4813, 5529, 646, 666, 23169, 4725,
            4128, 23931, 2068, 20524, 6847]}
ap= sns.barplot(data=df4, x ='Qty', y='Product')
sns.set_palette("pastel")
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)
plt.ylabel('Product')
plt.xlabel('Number of Sales')
plt.title('Number of Sales by Product')
plt.rcParams['figure.figsize'] = [10, 10]
plt.show()
#plt.savefig('Number of Sales by Product.png')


df5 = all_months_data.groupby('Product').sum()
df5.drop(['Minute', 'Hour', 'Month', 'Price', 'Qty'], axis=1, inplace=True)
df5['Sales'] = pd.to_numeric(df5['Sales'])
df5['Sales'] = df5['Sales'].round(2)
df6= df5.to_dict('split')
#print(df6)
df6 = {'Product': ['20in Monitor', '27in 4K Gaming Monitor', '27in FHD Monitor', '34in Ultrawide Monitor',
                   'AA Batteries (4-pack)', 'AAA Batteries (4-pack)', 'Apple Airpods',
                   'Bose SS Headphones', 'Flatscreen TV', 'Google Phone', 'LG Dryer',
                   'LG Washing Machine', 'Lightning Charging Cable', 'Macbook Pro Laptop', 'ThinkPad Laptop',
                   'USB-C Charging Cable', 'Vareebadd Phone', 'Wired Headphones', 'iPhone'], 'Sales':[453818.74,
                2433147.61, 1131074.59, 2352898.08, 106041.6, 92648.14, 2345550.0, 1342865.7,
                1443900.0, 3317400.0, 387600.0, 399600.0, 346376.55, 8032500.0, 4127958.72,
                285975.45, 827200.0, 246082.76, 4792900.0]}
aq= sns.barplot(data=df6, x ='Sales', y='Product')
sns.set_palette("pastel")
sns.despine(fig=None, ax=None, top=True, right=True, left=False, bottom=False, offset=None, trim=False)
plt.ylabel('Product')
plt.xlabel('Total Sales Dollars')
plt.title('Total Sales in Dollars by Prodcut')
plt.rcParams['figure.figsize'] = [10, 10]
plt.show()
#plt.savefig('Total Sales in Dollars by Prodcut.png')

df7 = all_months_data.groupby('Product').sum()
df7.drop(['Minute', 'Hour', 'Month', 'Price'], axis=1, inplace=True)
df7['Sales'] = pd.to_numeric(df7['Sales'])
df7['Sales'] = df7['Sales'].round(2)
df8= df7.to_dict('split')
#print(df8)
df8 = {'Product': ['20in Monitor', '27in 4K Gaming Monitor', '27in FHD Monitor', '34in Ultrawide Monitor',
                   'AA Batteries (4-pack)', 'AAA Batteries (4-pack)', 'Apple Airpods',
                   'Bose SS Headphones', 'Flatscreen TV', 'Google Phone', 'LG Dryer',
                   'LG Washing Machine', 'Lightning Charging Cable', 'Macbook Pro Laptop', 'ThinkPad Laptop',
                   'USB-C Charging Cable', 'Vareebadd Phone', 'Wired Headphones', 'iPhone'], 'Sales':[453818.74,
                2433147.61, 1131074.59, 2352898.08, 106041.6, 92648.14, 2345550.0, 1342865.7,
                1443900.0, 3317400.0, 387600.0, 399600.0, 346376.55, 8032500.0, 4127958.72,
                285975.45, 827200.0, 246082.76, 4792900.0], 'Qty':[4126, 6239, 7541, 6192, 27615, 30986, 15637, 13430, 4813, 5529, 646, 666, 23169, 4725,
            4128, 23931, 2068, 20524, 6847]}
                                                                   
ax = plt.subplots()
ax = sns.barplot  (y=df8['Product'], x=df8['Sales'], color='whitesmoke')
ax = sns.barplot  (y=df8['Product'], x=df8['Qty'], color='k')  
ax.set(xlabel='Grey is Sales, Black is Quantity', ylabel='Products')     
plt.show()                                                                           
                                                                                                      
                                                                                                      
                                                                                                      

