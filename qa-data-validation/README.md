# QA Data Validation Sandbox

This folder contains **Python-based data quality validation and testing** examples using **Pandas** and **pytest**.

The project demonstrates practical, **QA-focused workflows** for:

- validating datasets,
- detecting anomalies and inconsistencies,
- and computing error metrics on _actual vs predicted_ values.

Notebook and tests are organized to show how data validation can be **approached systematically using clear, transparent quality checks.**

---

## Structure

- `pytest.ini` - Pytest configuration (paths, runtime options).
- `requirements.txt` - Core project dependencies (data validation + tests).
- `requirements-notebook.txt` - Additional dependencies for notebook execution.
- `notebooks/` - Jupyter notebooks demonstrating QA-style data validation workflows.
  - `qa_data_validation.ipynb` — Main interactive notebook covering data inspection, cleaning, outlier detection, and error metrics.
- `src/` - Reusable utility functions for data validation.
  - `data_validation_utils.py` — Helper functions for numeric validation, range checks, IQR-based outlier detection, and error metrics (MAE, RMSE).
- `tests/`- Pytest-based unit tests for validation logic.
  - `test_data_validation.py` — Unit tests for validation utilities with assertions and edge-case coverage.
- `data/` - Sample data files for validation and analysis.
  - `metrics_history.csv` — Historical metrics for trend comparison and stability checks.

---

## Requirements

### **Core project:**

- Python 3.10+
- pandas
- numpy
- pytest

### **Notebook execution:**

- matplotlib
- jupyter
- ipykernel

---

## Setup

### 1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

For notebook support:

```bash
pip install -r requirements-notebook.txt
```

### 2. **Project structure is ready:**

The project uses `pytest.ini` to configure Python path and test discovery for automated tests.

---

## Test coverage

Unit tests in `tests/test_data_validation.py` validate:

- Range validation logic
- IQR-based outlier detection
- Error metric calculations (MAE, RMSE)
- Handling of missing, non-numeric, and invalid values

Tests focus on correctness, edge cases, and stability of validation logic.

---

## Data Quality checks (QA View)

### Early checks

1. **Schema validation** — Required columns present
2. **Dataset shape** — Non-empty, reasonable size
3. **Raw missingness** — Count and flag missing values
4. **Duplicate detection** — Identify and report duplicated rows

### Numeric conversion

- Coercion of non-numeric values to NaN
- Preservation of infinities for detection and QA visibility
- Explicit reporting of conversion effects

### Late checks

1. **Range validation** — Values within expected bounds
2. **IQR outlier detection** — Statistical anomaly detection
3. **Error metrics** — MAE and RMSE below acceptable thresholds (if applicable)
4. **Metric stability** — Compare against historical metrics (demo only)

---

## Running the tests

### Run all tests

```bash
pytest tests/
```

### Run a specific test file

```bash
pytest tests/test_data_validation.py
```

### Run a specific test

```bash
pytest tests/test_data_validation.py::test_compute_mae_rmse_simple_case
```

---

## Running the notebook

After installing Jupyter, open the notebook in **one of the following ways**:

### Option 1 — Using Jupyter’s file browser

1. Start Jupyter (e.g. `jupyter lab` or via Anaconda).
2. Navigate to: `qa-data-validation/notebooks/`
3. Open: `qa_data_validation.ipynb`
4. In the notebook menu, click Run > **Run All**.

### Option 2 — From the terminal

Go to project root (`qa-data-validation`) and then:

```bash
jupyter lab notebooks/qa_data_validation.ipynb
```

Then in the notebook menu, click Run > **Run All**.

#### **NOTE:**

> The notebook dynamically adds the project root to `sys.path`, which allows imports from the `src/` directory without extra configuration.

---

## Utility functions

Core validation logic is implemented in `src/data_validation_utils.py`, including:

- Numeric column validation and diagnostics
- Rule-based range checks with reasons
- IQR-based outlier detection
- Error metric calculation (MAE, RMSE)

These utilities are reused by both the notebook and the pytest test suite.

---

## Notes for reviewers

- **Synthetic dataset** — The notebook uses intentionally injected data issues (missing values, outliers, non-numeric entries) for demonstration and validation purposes.
- **Soft vs hard assertions** — The notebook uses soft warnings (print-based checks) to allow end-to-end execution; unit tests use strict assertions.
- **Transparent validation** — All checks produce explicit outputs so results are easy to inspect and understand.
- **Reusable utilities** — Functions in `src/` are designed for reuse in other projects and pipelines.
- **No external APIs** — All validation runs locally using pandas and numpy only.
- **Extensible design** — New validation rules can be added to `data_validation_utils.py` and tested in `test_data_validation.py`.
