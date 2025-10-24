# =========================================================
# 📘 Step 4 & 5: Pre-processing and Training Data Development
# Dataset: Healthcare Dataset (Kaggle - Prasad Patil)
# Goal: Predict Billing Amount based on patient and admission features
# =========================================================

# --- Import necessary libraries ---
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
import warnings
warnings.filterwarnings("ignore")

# --- Load Dataset ---
url = "https://raw.githubusercontent.com/prasad22/healthcare-dataset/main/healthcare_dataset.csv"
df = pd.read_csv(url)
print("✅ Data Loaded Successfully")
df.head()

# --- Step 1: Inspect Dataset ---
print(df.shape)
df.info()
df.describe(include='all').T

# --- Step 2: Handle Missing Values ---
print("Missing values per column:")
print(df.isnull().sum())

# Fill or drop missing values as appropriate
df = df.dropna(subset=['Billing Amount'])  # ensure target variable has no nulls
df.fillna(df.mode().iloc[0], inplace=True)
print("\n✅ Missing values handled.")

# --- Step 3: Identify Categorical and Numeric Columns ---
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

print("Categorical columns:", categorical_cols)
print("Numeric columns:", numeric_cols)

# --- Step 4: Define Features (X) and Target (y) ---
target = 'Billing Amount'
X = df.drop(columns=[target])
y = df[target]

print("Feature matrix shape:", X.shape)
print("Target variable shape:", y.shape)

# --- Step 5: Train-Test Split ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Training set:", X_train.shape)
print("Test set:", X_test.shape)

# --- Step 6: Preprocessing Pipeline ---
numeric_features = [col for col in X_train.columns if col in numeric_cols]
categorical_features = [col for col in X_train.columns if col in categorical_cols]

numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('encoder', OneHotEncoder(handle_unknown='ignore', drop='first'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

print("✅ Preprocessor ready.")

# --- Step 7: Model Building ---
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(random_state=42),
    "XGBoost": XGBRegressor(random_state=42, n_estimators=200, learning_rate=0.1)
}

results = {}

for name, model in models.items():
    pipe = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])
    pipe.fit(X_train, y_train)
    preds = pipe.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    r2 = r2_score(y_test, preds)
    results[name] = {'MAE': mae, 'RMSE': rmse, 'R2': r2}

results_df = pd.DataFrame(results).T
results_df.sort_values(by='R2', ascending=False)

# --- Step 8: Hyperparameter Tuning for Random Forest ---
rf_pipe = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', RandomForestRegressor(random_state=42))
])

param_grid = {
    'model__n_estimators': [100, 200],
    'model__max_depth': [10, 20, None],
    'model__min_samples_split': [2, 5]
}

grid_search = GridSearchCV(rf_pipe, param_grid, cv=3,
                           scoring='r2', n_jobs=-1, verbose=1)
grid_search.fit(X_train, y_train)

print("✅ Best Parameters Found:")
print(grid_search.best_params_)
print("\nBest R2 Score:", grid_search.best_score_)

# --- Step 9: Evaluate Final Model ---
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)

print("\n--- Final Model Performance ---")
print(f"R2: {r2_score(y_test, y_pred):.4f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred):.4f}")
print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}")

# --- Step 10: Save Cleaned Preprocessed Dataset ---
df.to_csv("healthcare_preprocessed.csv", index=False)
print("✅ Preprocessed dataset saved as 'healthcare_preprocessed.csv'")

# --- Step 11: Model Comparison Summary ---
print("📊 Model Comparison:")
display(results_df.sort_values(by='R2', ascending=False))

print("\n🏆 Best model based on R²:", results_df['R2'].idxmax())
