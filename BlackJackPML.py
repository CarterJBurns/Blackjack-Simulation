import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, StackingRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor
import traceback

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

    df_method = df[df['method_encoded'] == encoded_strategy].copy()
    
    if df_method.empty:
        raise ValueError(f"No data found for the strategy '{strategy}' (encoded as {encoded_strategy}).")

    df_method['bet_percentage'] = df_method['bet_amount'] / df_method['total_money']

    X = df_method[['bet_amount', 'total_money', 'bet_percentage']]
    y = df_method['hands_played']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
   
    print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
    
    rf = RandomForestRegressor(n_estimators=200, random_state=42)
    gbm = GradientBoostingRegressor(n_estimators=100, random_state=42, validation_fraction=0.1, n_iter_no_change=10)
    xgb = XGBRegressor(n_estimators=100, random_state=42)

    stacking_regressor = StackingRegressor(
        estimators=[('rf', rf), ('gbm', gbm)],
        final_estimator=xgb
    )

    
    param_grid = {
        'rf__n_estimators': [100],  
        'gbm__learning_rate': [0.1],  
        'gbm__n_estimators': [100],  
        'final_estimator__learning_rate': [0.1]  
    }

    
    grid_search = GridSearchCV(estimator=stacking_regressor, param_grid=param_grid, cv=3, scoring='r2', n_jobs=-1, verbose=3)

    print("Starting grid search...")

    try:
        grid_search.fit(X_train, y_train)
        print("Grid search completed.")
    except Exception as e:
        print(f"Error during grid search fitting: {e}")
        traceback.print_exc()
        return

    best_model = grid_search.best_estimator_  
    
    
    if not hasattr(best_model, 'estimators_'):
        print("Best model (StackingRegressor) is still not fitted.")
        return

    
    try:
        y_pred = best_model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"Strategy {strategy} (encoded as {encoded_strategy}):")
        print(f"Mean Squared Error: {mse}")
        print(f"R-squared: {r2}\n")
    except Exception as e:
        print(f"Error during prediction: {e}")
        traceback.print_exc()
        return

    
    userdatapredict = pd.DataFrame({
        'bet_amount': [starting_bet],
        'total_money': [total_cash],
        'bet_percentage': [starting_bet / total_cash]
    })

    
    userdatapredict_scaled = scaler.transform(userdatapredict)

    
    print(f"X_train shape: {X_train.shape}, userdatapredict_scaled shape: {userdatapredict_scaled.shape}")

    try:
        predicted_hands_played = best_model.predict(userdatapredict_scaled)
        print('here')  
        predicted_hands_played = float(predicted_hands_played[0])
    except Exception as e:
        print(f"Error during prediction: {e}")
        traceback.print_exc()
        return

    print(f"Predicted hands played for strategy {strategy}: {predicted_hands_played}")
    
    return round(predicted_hands_played, 2)

if __name__ == "__main__":
    main()  
