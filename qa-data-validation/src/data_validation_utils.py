"""
Utility functions for QA-style data validation on numeric columns.

These helpers are used both in the notebook (for exploration / explanation)
and in pytest tests (for automated checks).
"""

import numpy as np  # for numerical operations
import pandas as pd  # for DataFrame manipulations


def validate_numeric_column(df: pd.DataFrame, col_name: str) -> None:
    """
    Run QA-style checks on a column that is expected to be numeric.

    Prints a small diagnostic summary including:
    - dtype
    - missing values
    - empty strings
    - non-numeric values (via coercion)
    - infinities
    - booleans
    - zeros (including & excluding booleans)
    - negatives

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame containing the column.
    col_name : str
        Name of the column to validate.

    Returns
    -------
    None
        This function is side-effect only (prints diagnostics).
    """

    if col_name not in df.columns:
        raise KeyError(f"Column '{col_name}' not found in DataFrame. Available: {list(df.columns)}")

    col = df[col_name]

    # Convert invalid entries into NaN to analyze them safely.
    numeric_col = pd.to_numeric(col, errors="coerce")

    print(f"\n--- Column: `{col_name}` ---")
    print("dtype:", col.dtype)

    # 1) Missing values
    missing = col.isna().sum()
    print("Missing values:", missing)

    # 2) Empty strings (only meaningful for string-like cells)
    str_mask = col.apply(lambda x: isinstance(x, str))
    empty_strings = (col[str_mask].str.strip() == "").sum()
    print("Empty strings:", empty_strings)

    # 3) Non-numeric via coercion
    non_numeric = numeric_col.isna().sum() - col.isna().sum()  # exclude original NaNs
    print("Non-numeric values:", non_numeric)

    # 4) Infinities
    infinities = np.isinf(numeric_col).sum()
    print("Infinite values:", infinities)

    # 5) Booleans
    bool_mask = col.map(type).eq(bool)
    booleans = int(bool_mask.sum())
    print("Boolean values:", booleans)

    # 6) Zero values (including booleans)
    zeros_incl = (numeric_col == 0).sum()
    print("Zero values (including booleans):", zeros_incl)

    # 7) Zero values (excluding booleans)
    zeros_excl = ((numeric_col == 0) & (~bool_mask)).sum()
    print("Zero values (excluding booleans):", zeros_excl)

    # 8) Negatives
    negatives = (numeric_col < 0).sum()
    print("Negative values:", negatives)


def values_out_of_range_with_reason(
    df: pd.DataFrame,
    col: str,
    value_range: tuple[float, float],
) -> pd.DataFrame:
    """
    Return a DataFrame of rows where values in `col` are outside `value_range`.

    Also includes a 'reason' column indicating why each value is out of range:
    - 'too high'
    - 'too low'
    - 'not numeric / missing'

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    col : str
        Column name to check.
    value_range : tuple[float, float]
        (lower, upper) bounds for valid values.

    Returns
    -------
    pd.DataFrame
        DataFrame of out-of-range rows with 'reason' column.
    """

    if col not in df.columns:
        raise KeyError(f"Column '{col}' not found in DataFrame. Available: {list(df.columns)}")

    lower, upper = value_range

    # Convert to numeric; invalid values become NaN
    numeric = pd.to_numeric(df[col], errors="coerce")

    # Out-of-range mask
    mask = ~numeric.between(lower, upper)  # identify out-of-range values
    result = df.loc[mask].copy()  # create a DataFrame of out-of-range values
    n = numeric.loc[result.index]  # corresponding numeric values

    result["reason"] = ""
    result.loc[n > upper, "reason"] = "too high"
    result.loc[n < lower, "reason"] = "too low"
    result.loc[n.isna(), "reason"] = "not numeric / missing"

    return result


def iqr_outliers(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Return a DataFrame of IQR-based outliers for a given column.

    Uses Tukey's rule: values outside [Q1 - 1.5*IQR, Q3 + 1.5*IQR]
    are considered outliers.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    col : str
        Column name to check.

    Returns
    -------
    pd.DataFrame
        DataFrame of outlier rows with 'iqr_lower_bound' and 'iqr_upper_bound' columns.
    """

    # Check if column exists
    if col not in df.columns:
        raise KeyError(f"Column '{col}' not found in DataFrame. Available: {list(df.columns)}")

    # Convert to numeric; invalid values become NaN
    numeric = pd.to_numeric(df[col], errors="coerce")

    Q1 = numeric.quantile(0.25)  # first quartile
    Q3 = numeric.quantile(0.75)  # third quartile
    IQR = Q3 - Q1  # interquartile range

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    mask = (numeric < lower_bound) | (numeric > upper_bound)  # identify outliers
    out = df[mask].copy()
    out["iqr_lower_bound"] = lower_bound
    out["iqr_upper_bound"] = upper_bound

    return out


def iqr_outlier_fraction(df: pd.DataFrame, col: str) -> float:
    """
    Return the fraction of rows that are IQR-based outliers for a given column.

    The value is in [0, 1], where:
    - 0.0 means no outliers
    - 0.2 means 20% of valid values are outliers

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    col : str
        Column name to check.

    Returns
    -------
    float
        Fraction of outlier rows among valid numeric entries.
    """

    # Check if column exists
    if col not in df.columns:
        raise KeyError(f"Column '{col}' not found in DataFrame. Available: {list(df.columns)}")

    # Convert to numeric; invalid values become NaN
    numeric = pd.to_numeric(df[col], errors="coerce")

    valid_count = numeric.notna().sum()  # count of valid numeric entries

    # avoid division by zero; define as 0.0 if no valid entries
    if valid_count == 0:
        return 0.0

    outliers_df = iqr_outliers(df, col)  # DataFrame of IQR outliers
    outlier_count = len(outliers_df)

    return outlier_count / valid_count  # fraction of outliers


def compute_mae_rmse(
    actual: pd.Series,
    predicted: pd.Series,
) -> tuple[float, float, pd.DataFrame]:
    """
    Compute MAE and RMSE between two numeric Series and return the
    cleaned metrics DataFrame used for the calculation.

    Any NaN or infinite values in either input series are dropped before
    computing the metrics.

    NOTE:
    In a larger production system, this functionality is often split into
    two separate functions:
      - one that builds the error DataFrame
      - one that computes metrics from that DataFrame

    Here they are combined for convenience inside this demo notebook.

    Parameters
    ----------
    actual : pd.Series
        Actual values.
    predicted : pd.Series
        Predicted values.

    Returns
    -------
    (mae, rmse, df) : (float, float, pd.DataFrame)
        MAE, RMSE, and a cleaned DataFrame containing:
            - 'actual'
            - 'predicted'
            - 'abs_error'
            - 'squared_error'
    """

    df = pd.DataFrame({"actual": actual, "predicted": predicted}).copy()

    # Drop rows where either value is missing or infinite, before evaluating accuracy
    # For metric calculation we require both actual and predicted to be present and finite.
    df = df.replace([np.inf, -np.inf], np.nan)  # replace infinities with NaN
    df = df.dropna(
        subset=["actual", "predicted"]
    )  # drop rows with NaN in either column

    # If no valid data remains, return NaN for both metrics
    if df.empty:
        return float("nan"), float("nan"), df

    df["abs_error"] = (df["actual"] - df["predicted"]).abs()  # absolute error
    df["squared_error"] = (df["actual"] - df["predicted"]) ** 2  # squared error

    mae = df["abs_error"].mean()  # mean absolute error
    rmse = float(np.sqrt(df["squared_error"].mean()))  # root mean square error

    return mae, rmse, df
