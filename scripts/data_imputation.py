import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

def impute_data(final_df):
    imputer = IterativeImputer(max_iter=10, random_state=0)
    numerical_data = final_df.to_numpy()
    imputed_data = imputer.fit_transform(numerical_data)
    final_df_imputed = pd.DataFrame(imputed_data, columns=final_df.columns, index=final_df.index)
    return final_df_imputed
