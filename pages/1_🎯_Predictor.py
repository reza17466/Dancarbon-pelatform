@st.cache_resource
def load_model():
    import os
    model_path = 'models/rsm_model.pkl'
    if not os.path.exists(model_path):
        import pandas as pd
        from sklearn.preprocessing import PolynomialFeatures
        from sklearn.linear_model import LinearRegression
        from sklearn.pipeline import Pipeline
        import joblib

        os.makedirs('models', exist_ok=True)
        df = pd.read_csv('data/box_behnken.csv')
        X = df[['P_bar', 'T_K', 'TiO2_wt']].values
        y = df['X_vv'].values

        model = Pipeline([
            ('poly', PolynomialFeatures(degree=2, include_bias=False)),
            ('linear', LinearRegression())
        ])
        model.fit(X, y)
        joblib.dump(model, model_path)

    return joblib.load(model_path)
