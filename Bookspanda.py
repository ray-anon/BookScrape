import pandas as pd

df = pd.read_csv("BooksData/books_info.csv")

# Removing £  character  and convert to float and multiplying with the stocks left
df['total_value'] = df['Price'].str.replace(r'[£]', '', regex=True).astype(float) * df['Stocks']
cols = list(df.columns)

# rearranging the columns
modified_df = df[cols[0:2] + cols[3:5] + [cols[2]] + [cols[5]]]
modified_df.to_csv('more_files/modified.csv' , index=False)

#books which are expensive
Exp_df  = df.loc[df['Price'] > '£25']
Exp_df.to_csv('more_files/Expensive_Books.csv' , index=False)

#books Which have less stock
stock_df = df.loc[df['Stocks'] <= 5]
stock_df.to_csv('more_files/Less_stocks.csv' , index=False)


# saving the files category of the book
category = df['Type'].unique()
for  category_name in category:
    new_df  = df.loc[df['Type'] == category_name]
    new_df.to_csv(f"Category/{category_name}.csv" , index=False)