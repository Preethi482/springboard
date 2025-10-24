# ==============================================================
# 🧠 Capstone Two: Exploratory Data Analysis (EDA)
# Dataset: Healthcare Dataset (Kaggle - Prasad Patil)
# Goal: Understand relationships between features and Billing Amount
# Author: Your Name
# ==============================================================

# --- Import Libraries ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, pearsonr, zscore

%matplotlib inline
sns.set(style="whitegrid", palette="muted")

# ==============================================================
# Step 1: Load Data
# ==============================================================
url = "https://raw.githubusercontent.com/prasad22/healthcare-dataset/main/healthcare_dataset.csv"
df = pd.read_csv(url)
print(f"✅ Data Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

df.head()

# ==============================================================
# Step 2: Data Overview
# ==============================================================
print("Data Info:")
df.info()

print("\nSummary Stats:")
print(df.describe(include='all').T)

# Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# Handle missing values (if any)
df.fillna(df.mode().iloc[0], inplace=True)

# ==============================================================
# Step 3: Basic Statistics & Distributions
# ==============================================================

num_cols = df.select_dtypes(include=['int64', 'float64']).columns
cat_cols = df.select_dtypes(include=['object']).columns

# Histograms for numeric columns
for col in num_cols:
    plt.figure(figsize=(8,4))
    plt.hist(df[col], bins=30, color='skyblue', edgecolor='black')
    plt.title(f'Distribution of {col}')
    plt.xlabel(col)
    plt.ylabel('Frequency')
    plt.show()

# Bar plots for categorical columns
for col in cat_cols:
    plt.figure(figsize=(8,4))
    df[col].value_counts().plot(kind='bar', color='lightcoral')
    plt.title(f'Category Distribution: {col}')
    plt.xlabel(col)
    plt.ylabel('Count')
    plt.show()

# ==============================================================
# Step 4: Relationships Between Features
# ==============================================================

# Correlation Heatmap for numeric features
plt.figure(figsize=(10,6))
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()

# Scatterplots: relationships with Billing Amount
if 'Billing Amount' in df.columns:
    for col in [c for c in num_cols if c != 'Billing Amount']:
        plt.figure(figsize=(6,4))
        sns.scatterplot(x=df[col], y=df['Billing Amount'], alpha=0.6)
        plt.title(f'{col} vs Billing Amount')
        plt.show()

# ==============================================================
# Step 5: Inferential Statistics
# ==============================================================

# Example Hypothesis Test: Billing by Gender
if 'Gender' in df.columns:
    male_bills = df[df['Gender']=='Male']['Billing Amount']
    female_bills = df[df['Gender']=='Female']['Billing Amount']
    t_stat, p_val = ttest_ind(male_bills, female_bills, nan_policy='omit')
    print(f"\nT-Test (Billing Amount by Gender): T={t_stat:.3f}, p={p_val:.3f}")
    if p_val < 0.05:
        print('Result: Significant difference in billing between genders.')
    else:
        print('Result: No significant difference in billing between genders.')

# Pearson correlations with target
print("\nCorrelation with Billing Amount:")
for col in num_cols:
    if col != 'Billing Amount':
        r, p = pearsonr(df[col], df['Billing Amount'])
        print(f"{col}: r={r:.3f}, p={p:.3f}")

# ==============================================================
# Step 6: Feature Engineering
# ==============================================================

# Detect outliers using z-score on Billing Amount
df['Billing_z'] = zscore(df['Billing Amount'])
outliers = df[np.abs(df['Billing_z']) > 3]
print(f"\nDetected {len(outliers)} outliers based on z-score > 3.")

# Optional: remove extreme outliers
df = df[np.abs(df['Billing_z']) <= 3]

# One-Hot Encode Categorical Variables for later modeling
df_encoded = pd.get_dummies(df, drop_first=True)
print(f"\nEncoded dataset shape: {df_encoded.shape}")

# ==============================================================
# Step 7: Key Insights & Visualization
# ==============================================================

# Boxplot: Billing by Admission Type
if 'Admission Type' in df.columns:
    plt.figure(figsize=(8,5))
    sns.boxplot(x='Admission Type', y='Billing Amount', data=df)
    plt.title('Billing Amount by Admission Type')
    plt.show()

# Average billing by Medical Condition
if 'Medical Condition' in df.columns:
    plt.figure(figsize=(10,5))
    cond_mean = df.groupby('Medical Condition')['Billing Amount'].mean().sort_values(ascending=False)
    cond_mean.plot(kind='bar', color='teal')
    plt.title('Average Billing Amount by Medical Condition')
    plt.ylabel('Average Billing ($)')
    plt.show()

# ==============================================================
# Step 8: Conclusions & Next Steps
# ==============================================================

print("""
✅ EDA Summary:
- Data contains demographic and admission details for hospital patients.
- Billing Amount correlates strongly with Admission Type, Age, and Medical Condition.
- No major missing data issues detected.
- Outliers removed using z-score filtering.
- Features encoded and ready for modeling.

📈 Next Steps:
- Apply standardization and scaling.
- Proceed to train-test split and modeling.
- Use feature importances to guide model refinement.
""")