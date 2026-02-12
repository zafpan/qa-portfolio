import numpy as np  # for numerical operations
import pandas as pd  # for DataFrame manipulations
from src.data_validation_utils import (
    compute_mae_rmse,
    iqr_outlier_fraction,
    validate_numeric_column,
    values_out_of_range_with_reason,
)  # functions to test


def test_values_out_of_range_with_reason_flags_high_and_invalid():
    """
    Test that `values_out_of_range_with_reason` correctly identifies
    values that are too high and non-numeric/missing values.
    We expect:
    - 300 is too high for range (0, 200)
    - "text" and None are non-numeric/missing
    """

    df = pd.DataFrame(
        {
            "value": [50, 150, 300, "text", None],
        }
    )
    expected_range = (0, 200)

    out = values_out_of_range_with_reason(df, "value", expected_range)  # Get out-of-range rows

    # We expect:
    # - 300  -> "too high"
    # - "text", None -> "not numeric / missing"
    assert len(out) == 3

    reasons = set(out["reason"])
    assert reasons == {"too high", "not numeric / missing"}

    # Sanity check: the row with 300 is marked "too high"
    high_row = out[pd.to_numeric(out["value"], errors="coerce") == 300]
    assert not high_row.empty
    assert high_row["reason"].iloc[0] == "too high"


def test_iqr_outlier_fraction_zero_for_constant_data():
    """
    Test that `iqr_outlier_fraction` returns 0.0 when all values are the same.
    We expect:
    - no outliers in this case.
    """

    df = pd.DataFrame({"value": [100, 100, 100, 100, 100]})

    frac = iqr_outlier_fraction(df, "value")

    assert frac == 0.0


def test_iqr_outlier_fraction_detects_single_clear_outlier():
    """
    Test that `iqr_outlier_fraction` detects a single clear outlier.
    We expect:
    - 500 is an outlier among a reasonable range of other values.
    """

    df = pd.DataFrame({"value": [100, 101, 99, 102, 98, 500]})

    frac = iqr_outlier_fraction(df, "value")

    # 1 out of 6 values is clearly an outlier, but depending on IQR,
    # the exact fraction can vary a bit. We just assert it's in a
    # reasonable range around 20%.
    assert 0.15 <= frac <= 0.25


def test_compute_mae_rmse_simple_case():
    """
    Test that `compute_mae_rmse` computes correct MAE and RMSE for a simple case.
    We expect:
    - MAE = 10, RMSE = 10
    - Returned DataFrame has correct error columns.
    """

    actual = pd.Series([100, 100])
    predicted = pd.Series([90, 110])

    mae, rmse, df = compute_mae_rmse(actual, predicted)

    # Errors: [-10, +10] -> abs errors [10, 10], squared [100, 100]
    # MAE = 10, RMSE = 10
    assert mae == 10
    assert rmse == 10

    # Check that the returned df has the expected columns and 2 rows
    assert list(df.columns) == ["actual", "predicted", "abs_error", "squared_error"]
    assert len(df) == 2


def test_validate_numeric_column_runs_without_error(capsys):
    """
    We mainly want to ensure `validate_numeric_column` does not crash
    on mixed-type data.
    - It prints diagnostics;
    - Don't assert on content here - just a short inspection of output.

    Parameters
    ----------
    capsys : pytest fixture
        Captures stdout/stderr output.
    """

    df = pd.DataFrame(
        {
            "value": [1, 0, "", "text", None, np.inf, -5, True, False],
        }
    )

    # Should not raise any exception
    validate_numeric_column(df, "value")

    # Capture and inspect output if desired:
    captured = capsys.readouterr()
    assert "Missing values:" in captured.out
    assert "Non-numeric values:" in captured.out
