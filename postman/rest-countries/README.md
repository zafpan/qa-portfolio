# REST Countries – QA Demo Testing Suite (Postman)

**QA-focused API tests** against the public [`https://restcountries.com`](https://restcountries.com) API **using Postman, environment variables, assertions, and data-driven collection runs**.

This project is meant as a **small but realistic QA API demo**:

- positive, negative, and edge-case API validations
- response structure and field-level assertions
- parameterized requests using environment variables
- data-driven testing using a CSV file (multiple countries per run)
- validation of behavior across different endpoints and inputs
- controlled use of variable scopes (environment vs local variables)

---

## Structure

- `REST-Countries-QA-Demo-Testing-Suite.postman_collection.json` - Postman collection containing all requests, tests, and edge-case scenarios.
- `REST-Countries-QA-Demo-Env.postman_environment.json` - Environment configuration containing the variables needed to run the tests.
- `countries.csv` - CSV file used for data-driven collection runs (multiple countries in one execution).

---

## Requirements

- Postman Desktop app (v11+ recommended)

#### NOTE:

> **No authentication or API key** is required for the REST Countries API.

---

## Setup

### 1. **Import the collection and environment**

In Postman:

- In Postman: `Import` → select
  - `REST-Countries-QA-Demo-Testing-Suite.postman_collection.json`
  - `REST-Countries-QA-Demo-Env.postman_environment.json`

### 2. **Activate the environment**

Select **REST Countries – QA Demo Env** from the environment dropdown (top-right).

### 3. **Environment variables**

The environment (Environments → `REST Countries – QA Demo Env`) defines default values for:

- `base_url` → `https://restcountries.com/v3.1`
- `country_name` → e.g. Ireland
- `alpha_code` → e.g. IE
- `currency` → e.g. EUR
- `nonexistent_country` → e.g. Wonderland

> **NOTE:**
>
> These values can be:
>
> - **set manually** (for single-request runs), **or**
> - **overridden automatically** during collection runs via `countries.csv`.

---

## What the collection tests do

### 1. Get All Countries (lightweight fields)

- **Endpoint:** `GET {{base_url}}/all?fields=name,cca2,region`
- **Purpose:** Validation of the global listing endpoint using a reduced payload.
- **Assertions:**
  - status `200 OK`
  - response time `< 1200 ms`
  - `Content-Type` header includes `application/json`
  - response is an array with at least 200 countries
  - each entry contains `name`, `cca2`, and `region`

### 2. Get Country by Name (full text)

- **Endpoint:** `GET {{base_url}}/name/{{country_name}}?fullText=true`
- **Purpose:** Validate exact country name lookup.
- **Pre-request script:**
  - If a CSV file is present when running the collection, it sets `country_name` env var, from the CSV for each iteration.
- **Assertions:**
  - status `200 OK`
  - response time `< 1200 ms`
  - `Content-Type` header includes `application/json`
  - response is a non-empty array
  - `country_name` environment variable is not empty
  - `name.common` matches the expected country name
- **Chaining:**
  - saves `cca2` and `capital` to environment as `captured_cca2` and `captured_capital`, respectively.

### 3. Get Country by Alpha Code

- **Endpoint:** `GET {{base_url}}/alpha/{{alpha_code}}`
- **Purpose:** Validate lookup by ISO 3166-1 alpha code.
- **Pre-request script:**
  - If a CSV file is present when running the collection, it sets `alpha_code` env var, from the CSV for each iteration.
- **Assertions:**
  - status `200 OK`
  - response time `< 1200 ms`
  - `Content-Type` header includes `application/json`
  - response is a non-empty array
  - `alpha_code` environment variable is not empty
  - response contains `cca2` matching the requested alpha code

### 4. Get Countries by Currency

- **Endpoint:** `GET {{base_url}}/currency/{{currency}}`
- **Purpose:** Validate that at least one country uses the given currency.
- **Pre-request script:**
  - If a CSV file is present when running the collection, it sets `currency` env var, from the CSV for each iteration.
- **Assertions:**
  - status `200 OK`
  - response time `< 1200 ms`
  - `Content-Type` header includes `application/json`
  - response is a non-empty array
  - `currency` environment variable is not empty
  - at least one country includes the requested currency code

### 5. Negative Case: Unknown Country

- **Endpoint:** `GET {{base_url}}/name/{{nonexistent_country}}?fullText=true`
- **Purpose:** Validate correct handling of unknown resources.
- **Pre-request script:**
  - If a CSV file is present when running the collection, it sets `nonexistent_country` env var, from the CSV for each iteration.
- **Assertions:**
  - status `404 Not Found`
  - `nonexistent_country` environment variable is not empty
  - response contains an error message

### 6. Edge Case: Case-Insensitive Country Name

- **Endpoint:** `GET {{base_url}}/name/{{country_name_funky}}?fullText=true`
- **Purpose:** Verify that the API handles mixed-case input correctly.
- **Pre-request script:**
  - If a CSV file is present when running the collection, it sets `country_name` env var, from the CSV for each iteration.
  - Builds a mixed-case variant of the country name (e.g. `iReLaNd`)
  - Stores it in a **local variable** (`country_name_funky`) to avoid polluting other requests
- **Assertions:**
  - status `200 OK`
  - response time `< 1200 ms`
  - `Content-Type` header includes `application/json`
  - `country_name` environment variable is not empty
  - resolved country name matches the expected canonical name

---

## Data-driven execution (CSV)

The `countries.csv` file enables **running the entire collection across multiple countries.**

Each row represents one test iteration, **injecting its own**:

- `country_name`
- `alpha_code`
- `currency`
- `nonexistent_country`

All assertions are designed to validate behavior consistently across multiple countries rather than a single hardcoded example.

#### **Important Notes:**

- CSV (`iterationData`) values override environment variables during collection runs.
- Local variables are used only when request-specific overrides are needed (e.g. mixed-case tests).

---

## How to run the suite

### A. Run individual requests

1. Go to `Collections` and select the `REST Countries – QA Demo Testing Suite` collection.
2. Ensure the `REST Countries – QA Demo Env` environment is active (from the dropdown in the top-right).
3. Pick a request (e.g. **GET All Countries**).
4. Click **Send** and inspect:
   - status code
   - response time
   - body and test results tabs (Postman test assertions)

### B. Run the full collection (data-driven)

1. Select the `REST Countries – QA Demo Testing Suite` collection.
2. Click the **Run** button.
3. Ensure the `REST Countries – QA Demo Env` environment is active (from the dropdown in the top-right).
4. Attach `countries.csv` in the Runner (`Test data file` → select)
5. Run all iterations.
   - Each iteration executes the same tests for a different country.

---

## Notes for reviewers

- This project focuses on **API validation logic**, not performance or load testing.
- Assertions are designed to:
  - fail clearly when assumptions break
  - catch false positives that could otherwise pass “by luck”
- Variable scoping (environment vs iteration vs local) is intentionally demonstrated.
