# QA Portfolio

A curated QA portfolio showcasing hands-on work across **UI automation, API testing, data validation,** and **performance testing**. Each project is production-style, documented, and runnable with minimal setup.

This repo is intended for hiring managers and QA teams who want to review practical examples of test design, tooling, and automation practices.

Each project is **self-contained** and **documented** in its respective folder.

### Portfolio Architecture

```
QA Portfolio
│
├── UI Automation
│   └── Selenium Tests (POM)
│
├── API Testing
│   ├── ReqRes CRUD
│   └── REST Countries (data-driven)
│
├── Data Validation
│   └── Python Validation Suite
│
└── Performance Testing
    └── JMeter Load Tests
```

### Tooling Summary

- **UI Automation:** Selenium + pytest
- **API Testing:** Postman + Newman
- **Data Validation:** Python (pandas, numpy) + pytest
- **Load Testing:** Apache JMeter
- **CI:** GitHub Actions workflows per project

---

## CI

This portfolio includes four GitHub Actions workflows:

- **Selenium** UI tests
- **Postman/Newman** API tests
- **QA data validation** tests
- **JMeter** load tests

[![selenium-ui](https://github.com/zafpan/qa-portfolio/actions/workflows/selenium.yml/badge.svg)](https://github.com/zafpan/qa-portfolio/actions/workflows/selenium.yml)
[![postman-newman](https://github.com/zafpan/qa-portfolio/actions/workflows/newman.yml/badge.svg)](https://github.com/zafpan/qa-portfolio/actions/workflows/newman.yml)
[![qa-data-validation](https://github.com/zafpan/qa-portfolio/actions/workflows/qa-data-validation.yml/badge.svg)](https://github.com/zafpan/qa-portfolio/actions/workflows/qa-data-validation.yml)
[![jmeter-load](https://github.com/zafpan/qa-portfolio/actions/workflows/jmeter.yml/badge.svg)](https://github.com/zafpan/qa-portfolio/actions/workflows/jmeter.yml)

---

## Projects

### 1. UI Automation (Selenium)

**Path:** [selenium/](selenium/)

**Python + Selenium WebDriver** tests for [the-internet.herokuapp.com](https://the-internet.herokuapp.com/) **using Page Object Model (POM)**.

#### Highlights:

- Positive and negative login flows
- Access-control validation
- UI link checks
- Screenshots on failure

**Details:** [selenium/README.md](selenium/README.md)

---

### 2. API Testing (Postman)

**Path:** [postman/](postman/)

**Two Postman test suites** demonstrating QA-style API testing with assertions, data-driven runs, and variable chaining.

#### — 2.1. ReqRes CRUD Suite

**Path:** [postman/reqres-crud/](postman/reqres-crud/)

- CRUD coverage with chained variables and Flow documentation
- Uses a ReqRes API key (required)

**Details:** [postman/reqres-crud/README.md](postman/reqres-crud/README.md)

#### — 2.2. REST Countries Suite

**Path:** [postman/rest-countries/](postman/rest-countries/)

- Public API tests with positive/negative/edge cases
- CSV-driven collection runs
- No API key required

**Details:** [postman/rest-countries/README.md](postman/rest-countries/README.md)

---

### 3. Data Validation (Python)

**Path:** [qa-data-validation/](qa-data-validation/)

**QA-style data validation utilities, unit tests,** and **a notebook** demonstrating structured checks and error metrics.

#### Highlights:

- Numeric validation helpers
- Range checks, IQR outliers
- MAE/RMSE calculations

**Details:** [qa-data-validation/README.md](qa-data-validation/README.md)

---

### 4. Performance Testing (JMeter)

**Path:** [jmeter/](jmeter/)

**Two JMeter test plans** for ReqRes API under **NORMAL** and **STRESS** profiles.

#### Highlights:

- Parameterized test plans
- Rate-limit handling (HTTP 429 backoff)
- CLI and report generation guidance

**Details:** [jmeter/README.md](jmeter/README.md)

---

## Notes

- **ReqRes API requires an API key** for authenticated endpoints (used in Postman and JMeter projects).
- Reports and large artifacts are excluded via `.gitignore` to keep the repo clean.

---

## Contact

If you have questions or want walkthroughs of any project, feel free to reach out.

---

## License

This project is licensed under the [MIT License](LICENSE)
