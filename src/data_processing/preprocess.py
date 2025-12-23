import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from pathlib import Path

from src.data_processing.schema import (
    TARGET_COLUMN,
    CATEGORICAL_COLUMNS,
    NUMERICAL_COLUMNS
)

RAW_DATA_PATH = Path("raw_data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
PROCESSED_DATA_PATH = Path("data/processed.csv")


def load_raw_data() -> pd.DataFrame:
    """Load raw dataset"""
    df = pd.read_csv(RAW_DATA_PATH)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning"""
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df = df.dropna()
    return df


def build_preprocessing_pipeline() -> ColumnTransformer:
    """Create preprocessing pipeline"""

    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median"))
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, NUMERICAL_COLUMNS),
            ("cat", categorical_pipeline, CATEGORICAL_COLUMNS)
        ]
    )

    return preprocessor


def preprocess_and_save():
    """Main preprocessing function"""
    df = load_raw_data()
    df = clean_data(df)

    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN].map({"Yes": 1, "No": 0})

    preprocessor = build_preprocessing_pipeline()
    X_transformed = preprocessor.fit_transform(X)

    processed_df = pd.DataFrame(
        X_transformed.toarray() if hasattr(X_transformed, "toarray") else X_transformed
    )
    processed_df[TARGET_COLUMN] = y.values

    PROCESSED_DATA_PATH.parent.mkdir(exist_ok=True)
    processed_df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("Data preprocessing completed successfully")
    print(f"Processed data saved to: {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    preprocess_and_save()
