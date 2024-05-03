import pandas as pd
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


def load_and_preprocess_data(filepath):
    # load data from CSV
    # handle missing values and drop certain chosen columns
    df = pd.read_csv(filepath)
    df['Kilometres'] = pd.to_numeric(df['Kilometres'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df.dropna(inplace=True)

    reject_columns = [
        'Car/Suv', 'Title', 'UsedOrNew', 'Transmission', 'Engine',
        'DriveType', 'FuelType', 'FuelConsumption', 'ColourExtInt',
        'Location', 'CylindersinEngine', 'BodyType', 'Doors', 'Seats'
    ]
    df = df.drop(reject_columns, axis=1)

    df_encoded = pd.get_dummies(df, columns=['Brand', 'Model'])
    return df_encoded


def setup_data(df):
    # prepare features and target based on the the df
    X = df.drop('Price', axis=1)
    y = df['Price']
    return X, y


def evaluate_models(X, y, n_splits=4):
    # evaluate the two different models using kf cross validate
    kf = KFold(n_splits=n_splits, shuffle=False)
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=20, random_state=42),
    }
    model_scores = {}
    for name, model in models.items():
        scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')
        model_scores[name] = (-scores.mean()) ** 0.5  # Convert from negative MSE to RMSE
        print(f"{name} RMSE: {model_scores[name]}")
    return model_scores


def calculate_average_price_by_year(df):
    # average price for years
    return df.groupby('Year')['Price'].mean()


def main():
    filepath = 'Australian Vehicle Prices.csv'
    df_encoded = load_and_preprocess_data(filepath)
    X, y = setup_data(df_encoded)
    model_scores = evaluate_models(X, y)


if __name__ == "__main__":
    main()
