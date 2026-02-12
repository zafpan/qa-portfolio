# UI Tests (Selenium)

This folder contains **Python-based UI automation** tests using **Selenium WebDriver** that **validate login flows, access control,** and **UI link behavior** of [the-internet.herokuapp.com](https://the-internet.herokuapp.com) demo application.

Tests are structured using the **Page Object Model (POM)** pattern to ensure:

- Clear separation between test logic and UI interactions
- Maintainable and scalable test architecture
- Reusable page components

---

## Structure

- `pytest.ini` - Pytest configuration (paths, logging, runtime options).
- `requirements.txt` - Project dependencies.
- `.env` - Environment configuration (e.g. BASE_URL, HEADLESS) - **NOT committed**
- `pages/` - Page Object Model (POM) layer
  - `base_page.py` - Shared page logic (driver handling, waits, navigation, flash messages etc.).
  - `login_page.py` - Login page object (locators, login action, page load checks).
  - `secure_area_page.py` - Secure area page object (page load checks, logout action).
- `tests/` - Test layer (pytest-based test suites)
  - `conftest.py` - Pytest configuration, fixtures, and hooks for screenshot capture on failure.
  - `test_login_positive.py` - Positive authentication and logout flows.
  - `test_login_negative.py` - Negative authentication, validation, and access-control tests.
  - `test_ui_links.py` - UI/link visibility and navigation tests.
- `artifacts/screenshots` - Automatically generated screenshots captured on test failures.

---

## Requirements

- Python 3.10+
- Selenium 4.x
- Chrome browser (latest)
- pytest
- webdriver-manager (automatic ChromeDriver management)
- python-dotenv (environment variable loading)

#### **NOTE:**

> Tests assume Chrome is installed locally or in CI. `webdriver-manager` manages the driver only, not the browser itself.

---

## Setup

### 1. **Install dependencies:**

```bash
pip install -r requirements.txt
```

### 2. **Set environment variables (optional):**

Create a `.env` file in the project root:

```env
HEADLESS=true
BASE_URL=https://the-internet.herokuapp.com
```

**Defaults if not specified:**

- HEADLESS: `false`
- BASE_URL: `https://the-internet.herokuapp.com`

> **NOTE:** Set `HEADLESS=true` for running browser headless (usually for CI pipelines or non-GUI environments.)

### 3. **Configure test credentials:**

These credentials are exposed as a pytest fixture and reused across tests.

**Edit only if they change in the [demo application](https://the-internet.herokuapp.com/login)**: `tests/conftest.py`

```python
LOGIN_USERNAME = "tomsmith"
LOGIN_PASSWORD = "SuperSecretPassword!"
```

4. **Project structure is ready:**

The project uses `pytest.ini` to configure Python path and test discovery for automated tests.

---

## Test coverage

### Positive Flow

`test_login_positive.py`

- Valid login
- Secure area access
- Logout flow
- Redirect verification
- Flash message validation

### Negative flow

`test_login_negative.py`

- Wrong password
- Empty username
- Empty password
- Unusual input
- Direct access to `/secure` without authentication

### UI validation

`test_ui_links.py`

- Footer link visibility
- Href validation
- Domain verification

---

## Page Object Model (POM)

**Each page object extends a shared `BasePage`**, which provides common browser interaction and navigation capabilities.

- **Locators** are defined within each page class as class-level attributes using Selenium `By` strategies.
- **User interactions** (clicking, typing, waiting, navigation) are encapsulated inside page-object methods.
- **Verification logic** is kept inside the test layer rather than the page objects, preserving clear separation of concerns.

**Page objects** model application behaviour, while **tests** validate expected outcomes.

---

## Fixtures

Defined in `tests/conftest.py`:

- `base_url` (session scope): Base URL for the application (from env or default).
- `valid_credentials` (session scope): Tuple of (username, password).
- `driver` (function scope): Selenium Chrome WebDriver instance.
  - Setup: Launches Chrome, applies browser options, initializes WebDriver.
  - Teardown: Captures screenshot on failure, quits browser.

---

## Running the tests

### Run all tests

```bash
pytest tests/
```

### Run a specific test file

```bash
pytest tests/test_ui_links.py
```

### Run a specific test

```bash
pytest tests/test_ui_links.py::test_footer_elemental_selenium_link_visible
```

### Screenshots on failure

Screenshots are automatically captured on test failure and saved to `artifacts/screenshots/`.

Each screenshot includes:

- test name
- module name
- timestamp

---

## Notes for reviewers

- **No authentication keys or secrets are required** — the project uses the public test app
  [https://the-internet.herokuapp.com](https://the-internet.herokuapp.com)
- **Page Object Model (POM)** separates test logic from UI structure, improving maintainability.
- **Explicit waits** (`WebDriverWait`) are used where dynamic content is expected for stability and reliability.
- **Screenshot capture on failure** is enabled for fast debugging and traceability.
- Tests are **isolated, order-independent**.
