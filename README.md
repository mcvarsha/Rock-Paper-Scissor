import os
import pickle
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import inspect
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

app = Flask(__name__)

DATA_PATH = os.path.join(os.path.dirname(__file__), 'ProductPriceIndex_inr_no_usd.csv')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model_pipeline.pkl')
LGB_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'best_model_LightGBM.pkl')

# Load dataset
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Could not find data file at {DATA_PATH}. Place your CSV there.")

df = pd.read_csv(DATA_PATH)

# Determine target column: try common names, otherwise pick last column
candidate_targets = ['FarmerPrice', 'farmerprice', 'Farmer_Price', 'Farmer Price', 'price', 'Price']
for t in candidate_targets:
    if t in df.columns:
        target = t
        break
else:
    # default: assume last column is the target
    target = df.columns[-1]

# Prepare features
X = df.drop(columns=[target]).copy()
y = df[target].copy()

# Identify numeric and categorical columns
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

# Keep a small sample of unique values for form dropdowns
categorical_options = {c: sorted(df[c].dropna().unique().tolist())[:50] for c in categorical_cols}

# Build pipeline (preprocessing + model)
# Create OneHotEncoder compatibly across scikit-learn versions
try:
    # sklearn >=1.2 uses `sparse_output`
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
except TypeError:
    # older sklearn uses `sparse`
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_cols),
        ('cat', encoder, categorical_cols)
    ],
    remainder='drop'
)

pipeline = Pipeline([
    ('pre', preprocessor),
    ('model', RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1))
])

results = {}

# Train model if saved model not present
# Prefer a provided LightGBM pickle if available (user-provided full pipeline or model)
if os.path.exists(LGB_MODEL_PATH):
    try:
        with open(LGB_MODEL_PATH, 'rb') as f:
            pipeline = pickle.load(f)
        loaded_from = 'LightGBM'
    except Exception:
        # If loading fails, remove corrupt file to avoid repeated failures
        try:
            os.remove(LGB_MODEL_PATH)
        except Exception:
            pass
        loaded_from = None
else:
    loaded_from = None

if loaded_from is None and os.path.exists(MODEL_PATH):
    try:
        with open(MODEL_PATH, 'rb') as f:
            pipeline = pickle.load(f)
        loaded_from = 'SavedPipeline'
    except Exception:
        try:
            os.remove(MODEL_PATH)
        except Exception:
            pass
        loaded_from = None

if loaded_from is None:
    # Simple train/test split and training
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_val)
    mae = mean_absolute_error(y_val, preds)
    rmse = mean_squared_error(y_val, preds, squared=False)
    r2 = r2_score(y_val, preds)
    results['TrainedPipeline'] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}
    # Save trained pipeline for future runs
    try:
        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(pipeline, f)
    except Exception:
        pass
else:
    # If model loaded, we don't have metrics; compute on a small split for display
    try:
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        preds = pipeline.predict(X_val)
        mae = mean_absolute_error(y_val, preds)
        rmse = mean_squared_error(y_val, preds, squared=False)
        r2 = r2_score(y_val, preds)
        # Label metrics according to source
        if os.path.exists(LGB_MODEL_PATH):
            results['LightGBM (loaded)'] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}
        else:
            results['SavedPipeline (loaded)'] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}
    except Exception:
        if os.path.exists(LGB_MODEL_PATH):
            results['LightGBM (loaded)'] = {'MAE': None, 'RMSE': None, 'R2': None}
        else:
            results['SavedPipeline (loaded)'] = {'MAE': None, 'RMSE': None, 'R2': None}

# Helper to coerce form inputs into a DataFrame matching X's columns
def build_input_df(form: dict):
    input_data = {}
    for col in X.columns:
        val = form.get(col)
        if col in categorical_cols:
            # keep as string
            input_data[col] = val if val is not None else ''
        else:
            # numeric
            try:
                # Allow inputs like '62kg' -> extract numbers
                if isinstance(val, str):
                    v = ''.join(ch for ch in val if (ch.isdigit() or ch=='.' or ch=='-' ))
                    if v == '' or v == '.' or v == '-':
                        raise ValueError
                    input_data[col] = float(v)
                else:
                    input_data[col] = float(val) if val is not None and val != '' else float(X[col].mean())
            except Exception:
                # fallback to mean
                input_data[col] = float(X[col].mean())
    input_df = pd.DataFrame([input_data])
    return input_df, input_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_df, input_data = build_input_df(request.form)
        # Predict
        try:
            pred = pipeline.predict(input_df)[0]
            pred_value = float(pred)
        except Exception as e:
            pred_value = None
            print('Prediction error:', e)
        return render_template('result.html', predicted_price=pred_value, input_summary=input_data)

    # GET: render form
    numeric_stats = {c: {'min': float(X[c].min()), 'max': float(X[c].max()), 'mean': float(X[c].mean())} for c in numeric_cols}
    # Limit options to 50 values to avoid huge dropdowns
    limited_options = {c: categorical_options[c] for c in categorical_cols}
    return render_template('index.html', columns=X.columns.tolist(), numeric_cols=numeric_cols, categorical_cols=categorical_cols, numeric_stats=numeric_stats, categorical_options=limited_options, results=results)

if __name__ == '__main__':
    app.run(debug=True)
