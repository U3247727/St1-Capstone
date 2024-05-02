import pandas as pd
import matplotlib.pyplot as plt


# Adjust the path to where the dataset is unzipped
df = pd.read_csv('Australian Vehicle Prices.csv')
print(df.head())

# Convert the 'Price' column to numeric, coercing errors to NaN (if any non-convertible values are present)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Now calculate the average price for each year
average_price_by_year = df.groupby('Year')['Price'].mean()

# Create a bar graph
fig, ax = plt.subplots(figsize=(10, 6))
average_price_by_year.plot(kind='bar', color='skyblue', ax=ax)

# Formatting y-axis to display full numbers with proper labeling
ax.set_ylabel('Average Price')
ax.set_xlabel('Year')
ax.set_title('Average Car Price by Year of Manufacture')
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))


average_price_1959 = df[df['Year'] == 1959]['Price'].mean()
print(average_price_1959)



# Load your CSV data into a DataFrame
# df = pd.read_csv('your_file.csv')

# Convert the 'Price' column to numeric, coercing errors to NaN (if any non-convertible values are present)
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Calculate the average price for each brand
average_price_per_brand = df.groupby('Brand')['Price'].mean()

# Create a bar graph
fig, ax = plt.subplots(figsize=(10, 6))
average_price_per_brand.plot(kind='bar', color='teal', ax=ax)

# Formatting the plot
ax.set_ylabel('Average Price')
ax.set_xlabel('Brand')
ax.set_title('Average Price by Car Brand')
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${:,.2f}".format(x)))






# Convert 'Kilometres' and 'Price' columns to numeric, coercing errors to NaN (if any non-convertible values are present)
df['Kilometres'] = pd.to_numeric(df['Kilometres'], errors='coerce')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Create a scatter plot of Kilometres vs Price
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(df['Kilometres'], df['Price'], alpha=0.5, color='blue')  # Alpha for transparency

# Formatting the plot
ax.set_xlabel('Kilometres')
ax.set_ylabel('Price')
ax.set_title('Scatter Plot of Kilometres vs. Price')

# Format y-axis to show full numbers, removing scientific notation
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${:,.0f}".format(x)))

# Optional: Adjust axis limits if necessary
# ax.set_xlim([0, max(df['Kilometres']) + 1000])
ax.set_ylim([0, max(df['Price']) + 5000])

# Show the plot
plt.show()


