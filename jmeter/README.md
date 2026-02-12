# ReqRes Load Tests (JMeter)

This folder contains **two Apache JMeter test plans** that exercise the [ReqRes API](https://reqres.in) under **NORMAL** and **STRESS** load profiles.

Both plans share the same structure and sampler (request) coverage; they **differ only in load configuration parameters and throughput targets**.

---

## Design decision: API choice and rate limits

This project uses the **ReqRes** public demo API intentionally.

ReqRes was selected because it provides:

- realistic CRUD-style endpoints,
- predictable request/response behavior
- support for authenticated requests,
- behavior suitable for both functional and load-testing demonstrations.

#### **IMPORTANT NOTE ON RATE LIMITS**

> **ReqRes applies request limits on free API keys.**
> The **NORMAL** test plan is designed to stay within typical free-tier limits, while the **STRESS** plan is intentionally illustrative.
>
> The purpose of these tests is to demonstrate **load-test design, parameterisation, assertions, and rate-limit handling (HTTP 429 backoff)**, not to stress a public demo API indefinitely.
>
> If HTTP **429 (Too Many Requests)** responses occur, allow time for the limit window to reset or run the plans in GUI mode for inspection only.
>
> For unrestricted execution, alternative APIs (or internal services) would normally be used in real-world environments.

---

## Structure

- `plans/ReqRes_LoadTests_NORMAL.jmx` - JMeter test plan configured for **normal load** profiles.
- `plans/ReqRes_LoadTests_STRESS.jmx` - JMeter test plan configured for **stress load** profiles.
- `reports/` - Directory where **HTML reports** are generated when running JMeter via CLI.
- `results/` - Directory where **JTL (JMeter Test Log) files** are written, for both CLI and GUI executions.

---

## Requirements

- Apache JMeter 5.5+ (plans are saved with jmeter="5.6.3")
- Java compatible with your JMeter installation
- ReqRes API key from [reqres.in](https://reqres.in)

---

## Setup

Both plans define these variables:

- `API_KEY` (default: **CHANGEME**)
- `BASE_URL` (default: `reqres.in`)
- `CONNECT_TIMEOUT_MS` (default: `10000`)
- `RESPONSE_TIMEOUT_MS` (default: `30000`)
- `NUM_THREADS_DEFAULT` (NORMAL: `3`, STRESS: `10`)
- `RAMP_TIME_DEFAULT` (NORMAL: `3`, STRESS: `10`)
- `LOOPS_DEFAULT` (NORMAL: `5`, STRESS: `10`)
- `USER_ID` (default: `2`)
- `USER_NAME` (default: `Panos`)
- `USER_JOB` (default: `QA Engineer`)
- `JTL_FILE` (NORMAL: `results/results_normal.jtl`, STRESS: `results/results_stress.jtl`)

and the following pacing settings:

- **Constant Throughput Timer** is active in both plans:
  - **NORMAL** targets `30.0`
  - **STRESS** targets `100.0`
- **Uniform Random Timer** adds jitter per sampler:
  - delay `200ms`, range `800ms`

---

## What the test plans do

Each user (thread) iteration executes:

### **Read Operation (randomized)**

- `GET /api/users?page=1` → expect **200**
- `GET /api/users?page=2` → expect **200**
- `GET /api/users/${USER_ID}` → expect **200** (with JSON assertions)

### **Write Operations (sequential)**

- `POST /api/users` → expect **201** (with JSON assertions)
- `PUT /api/users/${USER_ID}` → expect **200**
- `PATCH /api/users/${USER_ID}` → expect **200**
- `DELETE /api/users/${USER_ID}` → expect **204**

### **Global safety assertion**

A top-level response assertion checks:

- **status NOT 401 (Unauthorized)** with message: `Unexpected 401: API key missing/invalid`

### **Backoff on HTTP 429**

A **JSR223 PostProcessor (Groovy)** runs after each write sampler inside the Write Operations controller

- If response code is **429**, it sleeps for:
  - `Retry-After` seconds (if present and numeric), otherwise **60s**
  - and an additional random jitter of **0–2000ms**

---

## Assertions

**Status code assertions**

- `GET` expects **200** (with distinct names per sampler)
- `POST` expects **201**
- `PUT` expects **200**
- `PATCH` expects **200**
- `DELETE` expects **204**
- `Global` assertion fails if **401** occurs for any sampler

**JSON assertions**

On `GET /api/users/${USER_ID}`:

- `$.data.id == ${USER_ID}` (with JSON validation enabled)
- `$.data.email exists` (presence check)

On `POST /api/users`:

- `$.id exists`
- `$.createdAt exists`

#### **NOTE:**

> JSON assertions are intentionally minimal to validate response structure without coupling load tests to business logic.

---

## Runtime overrides

The plans are designed to be overridden from the command line using JMeter properties:

- API key override:
  - `-JAPI_KEY=...` overrides `API_KEY`
- Thread/ramp/loops override:
  - `-JNUM_THREADS=...` overrides `NUM_THREADS_DEFAULT`
  - `-JRAMP_TIME=...` overrides `RAMP_TIME_DEFAULT`
  - `-JLOOPS=...` overrides `LOOPS_DEFAULT`
- Output file override:
  - `-JJTL_FILE=...` overrides `JTL_FILE`

#### **NOTES:**

> The **only required runtime property** is `API_KEY`, as it has no valid default value.
>
> - If `API_KEY` is not provided, samplers will be sent with the placeholder value `CHANGEME` and they will fail with **401 Unauthorized**.
> - The global **“status NOT 401”** assertion is designed to fail fast and surface authentication issues early in the test run.

---

## Running the tests

### Option A: JMeter GUI (quick validation)

1. Open JMeter
2. File → Open → navigate to `jmeter/plans` → select `ReqRes_LoadTests_NORMAL.jmx` or `ReqRes_LoadTests_STRESS.jmx`
3. Set `API_KEY` and any variables you want
4. Run

### Option B: JMeter CLI (load execution)

Go to project root (`jmeter`) and then:

#### **Run NORMAL:**

```bash
jmeter -n -t plans/ReqRes_LoadTests_NORMAL.jmx \
 -JAPI_KEY=CHANGEME \
 -JNUM_THREADS=3 \
 -JRAMP_TIME=3 \
 -JLOOPS=5 \
 -JJTL_FILE=results/results_normal.jtl
```

#### **Run STRESS:**

```bash
jmeter -n -t plans/ReqRes_LoadTests_STRESS.jmx \
 -JAPI_KEY=CHANGEME \
 -JNUM_THREADS=10 \
 -JRAMP_TIME=10 \
 -JLOOPS=10 \
 -JJTL_FILE=results/results_stress.jtl
```

#### **NOTES:**

> - Ensure that the **directory specified by `JTL_FILE` exists** before execution; otherwise, JMeter may fail to write the `.jtl` output file.
> - Only **`API_KEY` must be explicitly provided**, as it does not have a valid default value. All **other properties are optional** and only required if you want to override their defaults.
> - Result files are written via **Simple Data Writer**, controlled by `JTL_FILE`, so the `-l` CLI option is intentionally not used.

---

## Generating HTML Reports

Apache JMeter can generate an HTML performance report from a `.jtl` results file produced during a non-GUI run.
The HTML report is generated **at the end of test execution** or **from an existing results file**, depending on how the CLI is invoked.

- The report output directory must not exist or must be empty before running the command; JMeter will fail if files are already present.

#### **Important clarification**

> The test plans write results using **Simple Data Writer** via the `JTL_FILE` variable (overridable with `-JJTL_FILE`).
> When generating HTML reports, the **same JTL file must also be passed to JMeter via `-l`**.
>
> This does **not** create a second results file — it only tells JMeter which existing `.jtl` file to use for HTML report generation.

### Option A: Generate HTML report as part of the test run

You can append the following options to any existing non-GUI execution command:

```bash
-l path/to/results.jtl \
-e -o path/to/reports/folder
```

**Example (NORMAL load):**

Go to project root (`jmeter`) and then:

```bash
jmeter -n -t plans/ReqRes_LoadTests_NORMAL.jmx \
 -JAPI_KEY=CHANGEME \
 -JNUM_THREADS=3 \
 -JRAMP_TIME=3 \
 -JLOOPS=5 \
 -JJTL_FILE=results/results_normal.jtl \
 -l results/results_normal.jtl \
 -e -o reports/normal
```

In this mode:

- The test runs normally
- Results are written via **Simple Data Writer**
- The HTML report is generated automatically after the run completes

### Option B: Generate HTML report from existing results (no re-run)

If a `.jtl` file already exists, you can generate the HTML report without executing the test again:

```bash
jmeter -g path/to/results.jtl -o path/to/reports/folder
```

**Example (NORMAL load):**

Go to project root (`jmeter`) and then:

```bash
jmeter -g results/results_normal.jtl -o reports/normal
```

This approach is **recommended for STRESS tests** and large result files, as it avoids report-generation overhead and additional memory/CPU usage during load execution.

---

## Results output

Both plans enable:

- **Simple Data Writer** → writes execution results to the location controlled by `JTL_FILE`.

All other listeners (Summary Report, Aggregate Report, View Results Tree, View Results in Table) are included but **disabled by default** to keep test execution lightweight and suitable for load testing.

---

## Notes for reviewers

- ReqRes is a public demo API and **enforces limits on free API keys.** The **STRESS plan** is **included to demonstrate** load-test structure and 429 handling, **not sustained traffic against a public API.**
- `POST/PUT/PATCH/DELETE` endpoints may not represent persistent state (common for demo APIs).
- Randomized read operations are used to avoid cache bias and better simulate real usage patterns.
- The 429 backoff is implemented as a **PostProcessor** that sleeps the current thread; it intentionally trades throughput for stability when rate limited.
