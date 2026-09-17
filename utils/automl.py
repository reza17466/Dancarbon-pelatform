"""
AutoML engine: trains a response-surface model automatically
when a project has enough data points.
"""
import numpy as np
import joblib
import os
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score, mean_squared_error


def train_project_model(project_id, data_df, degree=2):
    """
    Train a quadratic response-surface model for a specific project.

    Args:
        project_id: int
        data_df: pandas DataFrame with columns [pressure, temperature, concentration, absorption]
        degree: polynomial degree (default 2)

    Returns:
        dict with keys: model, r2, rmse, n_points, model_path
    """
    if len(data_df) < 5:
        return {
            'success': False,
            'error': f'Need at least 5 points (have {len(data_df)})'
        }

    X = data_df[['pressure', 'temperature', 'concentration']].values
    y = data_df['absorption'].values

    model = Pipeline([
        ('poly', PolynomialFeatures(degree=degree, include_bias=False)),
        ('linear', LinearRegression())
    ])

    model.fit(X, y)
    y_pred = model.predict(X)

    r2 = r2_score(y, y_pred)
    rmse = np.sqrt(mean_squared_error(y, y_pred))

    # Save model
    os.makedirs('models/projects', exist_ok=True)
    model_path = f'models/projects/project_{project_id}.pkl'
    joblib.dump(model, model_path)

    return {
        'success': True,
        'model': model,
        'r2': r2,
        'rmse': rmse,
        'n_points': len(data_df),
        'model_path': model_path,
        'coefficients': model.named_steps['linear'].coef_,
        'intercept': model.named_steps['linear'].intercept_,
    }


def load_project_model(project_id):
    """Load a previously trained model."""
    model_path = f'models/projects/project_{project_id}.pkl'
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None


def predict_for_project(project_id, P, T, C):
    """Make a prediction using a project-specific model."""
    model = load_project_model(project_id)
    if model is None:
        return None
    X = np.array([[P, T, C]])
    return float(model.predict(X)[0])
