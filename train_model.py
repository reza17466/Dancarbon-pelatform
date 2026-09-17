"""
DanCarbon Tech — Initial Model Training
Trains the baseline RSM model on the 17-point Box-Behnken design.
Run once: python train_model.py
"""
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error


def train_baseline_model():
    # Load data
    df = pd.read_csv('data/box_behnken.csv')

    X = df[['P_bar', 'T_K', 'TiO2_wt']].values
    y = df['X_vv'].values

    # Build pipeline
    model = Pipeline([
        ('poly', PolynomialFeatures(degree=2, include_bias=False)),
        ('linear', LinearRegression())
    ])

    # Train
    model.fit(X, y)
    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))

    print(f"✅ Model trained successfully")
    print(f"   R²  = {r2:.4f}")
    print(f"   RMSE = {rmse:.4f} v/v")
    print(f"   Data points: {len(df)}")

    # Save
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/rsm_model.pkl')
    print(f"   Saved to: models/rsm_model.pkl")

    return model


if __name__ == "__main__":
    train_baseline_model()
