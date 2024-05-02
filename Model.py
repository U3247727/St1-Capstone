import pandas as pd

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


# reading the csv
df = pd.read_csv('Australian Vehicle Prices.csv')

# replacing all the non-numeric values with NaN (Not a Number)
df['Kilometres'] = pd.to_numeric(df['Kilometres'], errors='coerce')
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# dropping all the rows with any NaN values
df.dropna(inplace=True)

# columns to be dropped
rejectColumns = [
    'Car/Suv', 'Title', 'UsedOrNew', 'Transmission', 'Engine',
    'DriveType', 'FuelType', 'FuelConsumption', 'ColourExtInt',
    'Location', 'CylindersinEngine', 'BodyType', 'Doors', 'Seats'
]

# dropping the columns
df = df.drop(rejectColumns, axis=1)

# applying one-hot encoding to 'Brand' and 'Model' so that i can make numerical
df_encoded = pd.get_dummies(df, columns=['Brand', 'Model'])

# prepare features and target
X = df_encoded.drop('Price', axis=1)
y = df_encoded['Price']

# set up k-folds
kf = KFold(n_splits=4, shuffle=False)

# different models to evaluate
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=20, random_state=42),
}

# evaluating models using cross-validation from the above kfs
model_scores = {}
for name, model in models.items():
    scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')
    model_scores[name] = (-scores.mean()) ** 0.5  # Convert from negative MSE to RMSE
    print(model_scores[name])

# output model scores:
for model_name, rmse in model_scores.items():
    print(f"{model_name} RMSE: {rmse}")

