
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, StackingRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

def main(strategy, starting_bet, total_cash):
    
    strategy_mapping = {
        'M': 0,
        'P': 1,
        'R': 2,
        'F': 3
    }
    encoded_strategy = strategy_mapping.get(strategy, 3)

    print(f'Arrived: {encoded_strategy} (for strategy {strategy}), Starting Bet: {starting_bet}, Total Cash: {total_cash}')
    
    
    df = pd.read_csv('blackjackdata.csv')
    df['method_encoded'] = pd.factorize(df['method'])[0]

    df_method = df[df['method_encoded'] == encoded_strategy]

    if df_method.empty:
        raise ValueError(f"No data found for the strategy '{strategy}' (encoded as {encoded_strategy}).")

   
    df_method['bet_total_interaction'] = df_method['bet_amount'] * df_method['total_money']
    
    X = df_method[['bet_amount', 'total_money', 'bet_total_interaction']]
    y = df_method['hands_played']

    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
   
    
    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    gbm = GradientBoostingRegressor(n_estimators=200, random_state=42)
    lasso = make_pipeline(PolynomialFeatures(degree=2, include_bias=False), Lasso(alpha=0.01))
    xgb = XGBRegressor(n_estimators=200, random_state=42)

    
    stacking_regressor = StackingRegressor(
        estimators=[('rf', rf), ('gbm', gbm), ('lasso', lasso)],
        final_estimator=xgb
    )


    stacking_regressor.fit(X_train, y_train)

    
    y_pred = stacking_regressor.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Strategy {strategy} (encoded as {encoded_strategy}):")
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}\n")

    userdatapredict = pd.DataFrame({
        'bet_amount': [starting_bet],
        'total_money': [total_cash],
        'bet_total_interaction': [starting_bet * total_cash]
    })

    userdatapredict_scaled = scaler.transform(userdatapredict)
    predicted_hands_played = stacking_regressor.predict(userdatapredict_scaled)

    predicted_hands_played = float(predicted_hands_played[0])

    print(f"Predicted hands played for strategy {strategy}: {predicted_hands_played}")
    return round(predicted_hands_played, 2)

if __name__ == "__main__":
    main()
