
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score

def main(strategy, starting_bet, total_cash):
    
    df = pd.read_csv("blackjackdata.csv")

    df['bet_perc'] = df['total_money'] / df['bet_amount']
     
    X = df[['bet_amount', 'total_money']]
    y = df['hands_played']


    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    poly = PolynomialFeatures(degree=2)
    X_train_poly = poly.fit_transform(X_train)
    X_test_poly = poly.transform(X_test)

    model = RandomForestRegressor(n_estimators=75, random_state=42)
    model.fit(X_train_poly, y_train)

    y_pred = model.predict(X_test_poly)

    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    print(f"R-squared: {r2}")
    print(f"Mean Squared Error: {mse}")


    """
    plt.scatter(y_test, y_pred, color='blue', label='Predicted vs Actual')
    plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red', label='Perfect Fit')
    plt.xlabel('Actual Hands Played')
    plt.ylabel('Predicted Hands Played')
    plt.title('Random Forest Regression Predictions')
    plt.legend()
    plt.show()
    """


    own_input = np.array([[starting_bet,total_cash]])  
    own_input_poly = poly.transform(own_input)  
    pred = model.predict(own_input_poly) 


    print(f"Predicted hands played for input {own_input[0][0]}: {np.round(pred[0])}")

    return np.round(pred[0])

if __name__ == "__main__":
    main()
