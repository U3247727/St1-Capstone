import pandas as pd
import matplotlib.pyplot as plt


# set the path
df = pd.read_csv('Australian Vehicle Prices.csv')
print(df.head())

# convert the Price column to numeric
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# now calculate the average price for each year
average_price_by_year = df.groupby('Year')['Price'].mean()

# create a bar graph
fig, ax = plt.subplots(figsize=(10, 6))
average_price_by_year.plot(kind='bar', color='skyblue', ax=ax)

# formatting display numbers with proper labeling
ax.set_ylabel('Average Price')
ax.set_xlabel('Year')
ax.set_title('Average Car Price by Year of Manufacture')
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))


average_price_1959 = df[df['Year'] == 1959]['Price'].mean()
print(average_price_1959)

# calculate the average price for each brand
average_price_per_brand = df.groupby('Brand')['Price'].mean()
fig, ax = plt.subplots(figsize=(10, 6))
average_price_per_brand.plot(kind='bar', color='teal', ax=ax)

# Formatting the plot
ax.set_ylabel('Average Price')
ax.set_xlabel('Brand')
ax.set_title('Average Price by Car Brand')
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${:,.2f}".format(x)))

# convert 'Kilometres' and 'Price' columns to numeric
df['Kilometres'] = pd.to_numeric(df['Kilometres'], errors='coerce')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# create a scatter plot of Kilometres vs Price
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(df['Kilometres'], df['Price'], alpha=0.5, color='blue')  # Alpha for transparency

# Formatting
ax.set_xlabel('Kilometres')
ax.set_ylabel('Price')
ax.set_title('Scatter Plot of Kilometres vs. Price')

# Formatting
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${:,.0f}".format(x)))

ax.set_ylim([0, max(df['Price']) + 5000])

# Show the plot
plt.show()


