import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def load_data(filepath):
    # load data from CSV file
    return pd.read_csv(filepath)


def convert_to_numeric(df, columns):
    # convert specified columns to numeric
    for column in columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df


def calculate_price_range(df, num_bins=10):
    # calculate the average price range for kilometers
    df['Kilometer_Range'] = pd.cut(df['Kilometres'], bins=num_bins)
    return df.groupby('Kilometer_Range')['Price'].mean()


def plot_bar_chart(data, title, xlabel, ylabel, fig_size=(10, 6), color='skyblue'):
    # plotting the bar chart
    fig, ax = plt.subplots(figsize=fig_size)
    data.plot(kind='bar', color=color, ax=ax)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${:,.0f}".format(x)))
    plt.show()


def create_scatter_plot(df, x, y, title, xlabel, ylabel):
    # create a scatter plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df[x], df[y], alpha=0.5, color='blue')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${:,.0f}".format(x)))
    ax.set_ylim([0, max(df[y]) + 5000])
    plt.show()


def create_histogram(df, column, title, xlabel, ylabel, bins=10, fig_size=(10, 6), color='orange'):
    # create a histogram of a specified column
    fig, ax = plt.subplots(figsize=fig_size)
    ax.hist(df[column], bins=bins, color=color)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.show()


def main():
    # set the fileepath
    filepath = 'Australian Vehicle Prices.csv'

    # load data
    df = load_data(filepath)

    # convert to numeric
    df = convert_to_numeric(df, ['Kilometres', 'Price'])

    # calculate and plot average price by year
    average_price_by_year = df.groupby('Year')['Price'].mean()
    plot_bar_chart(average_price_by_year, 'Average Car Price by Year of Manufacture', 'Year', 'Average Price')

    # calculate and plot average price by brand
    average_price_per_brand = df.groupby('Brand')['Price'].mean()
    plot_bar_chart(average_price_per_brand, 'Average Price by Car Brand', 'Brand', 'Average Price', color='teal')

    # create a scatter plot of Kilometres vs. Price
    create_scatter_plot(df, 'Kilometres', 'Price', 'Scatter Plot of Kilometres vs. Price', 'Kilometres', 'Price')

    # calculate and plot average price range by Kilometers
    price_range_by_kilometer = calculate_price_range(df)
    plot_bar_chart(price_range_by_kilometer, 'Average Price by Kilometer Range', 'Kilometer Range', 'Average Price')


if __name__ == "__main__":
    main()
