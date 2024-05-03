import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import Model

def make_prediction(year, brand, kilometers, model_choice):
    # load data
    filepath = 'Australian Vehicle Prices.csv'
    df_encoded = Model.load_and_preprocess_data(filepath)
    X, y = Model.setup_data(df_encoded)

    if model_choice == "linear":
        model = LinearRegression()
    elif model_choice == "random_forest":
        model = RandomForestRegressor(n_estimators=20, random_state=42)
    else:
        raise ValueError("Invalid model choice. Please choose 'linear' or 'random_forest'.")

    model.fit(X, y)

    # create a new Df with input
    input_data = pd.DataFrame({
        'Year': [year],
        'Brand_' + brand: [1],
        'Kilometres': [kilometers]
    })

    # fill missing columns with 0
    missing_cols = set(X.columns) - set(input_data.columns)
    input_data = pd.concat([input_data, pd.DataFrame({col: [0] for col in missing_cols}, index=input_data.index)], axis=1)

    # make sure the columns are in the same order as the original csv
    input_data = input_data[X.columns]

    predicted_price = model.predict(input_data)
    return predicted_price[0]
if __name__ == "__main__":
    year = int(input("Enter the year: "))
    brand = input("Enter the brand: ")
    kilometers = int(input("Enter the kilometers: "))
    model_choice = input("Enter 'linear' for Linear Regression or 'random_forest' for Random Forest: ")

    predicted_price = make_prediction(year, brand, kilometers, model_choice)
    print(f"Predicted Price: ${predicted_price:.2f}")