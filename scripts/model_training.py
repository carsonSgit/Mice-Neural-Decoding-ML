import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor

def train_model(final_df, final_df_imputed):
    results = {}
    
    # Train model with dropped NaNs
    y = final_df.dropna()[['Forward Position', 'Lateral Position']]
    X = final_df.dropna().drop(['Forward Position', 'Lateral Position'], axis=1)
    model = RandomForestRegressor(random_state=0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0, shuffle=False)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse_dropped = mean_squared_error(y_test, y_pred)
    results['Dropped NaNs MSE'] = mse_dropped

    # Train model with imputed data
    y_imputed = final_df_imputed[['Forward Position', 'Lateral Position']]
    X_imputed = final_df_imputed.drop(['Forward Position', 'Lateral Position'], axis=1)
    imputed_model = RandomForestRegressor(random_state=0)

    X_train_imputed, X_test_imputed, y_train_imputed, y_test_imputed = train_test_split(X_imputed, y_imputed, test_size=0.2, random_state=0, shuffle=False)
    imputed_model.fit(X_train_imputed, y_train_imputed)
    y_pred_imputed = imputed_model.predict(X_test_imputed)
    mse_imputed = mean_squared_error(y_test_imputed, y_pred_imputed)
    results['Imputed MSE'] = mse_imputed

    return results
