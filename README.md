Here is the rewritten `README.md`.

I have stripped away the marketing language and focused strictly on the architectural patterns, technical decisions, and data methodology. It uses standard industry terminology (e.g., "In-Memory ETL," "Dependency Injection") rather than buzzwords.

-----

**File:** `README.md`

````markdown
# Global CO₂ Analysis Platform

> **A stateless data visualization application implementing in-memory ETL and source-agnostic SQL transformations.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://co2-dashboard-ck.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://hub.docker.com/r/kchetan/co2-dashboard)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

## Overview

The **Global CO₂ Analysis Platform** is a dashboard for exploring global emissions data from 1750 to the present.

The application utilizes a **stateless architecture**. Upon initialization, the system fetches the raw dataset via HTTP from the [Our World in Data (OWID)](https://github.com/owid/co2-data) repository. Data processing—including cleaning, casting, and aggregation—is performed entirely in volatile memory (RAM) using DuckDB, eliminating the need for persistent local storage or an external database connection.

---

## Architecture & Data Flow

The pipeline implements **Dependency Injection** to decouple data extraction from data transformation. This allows the application to function identically whether the data source is a local file (development environment) or a live URL stream (production environment).



```mermaid
graph LR
    subgraph Runtime [Container Runtime]
    A[Remote CSV Source] -->|HTTPS Fetch| B(Pandas DataFrame)
    B -->|Register View| C{DuckDB In-Memory}
    C -->|SQL Transformation| D[Streamlit Frontend]
    end
````

### Technical Implementation

1.  **Ingestion:** The raw CSV is read directly into a Pandas DataFrame.
2.  **Injection:** The DataFrame is registered as a virtual table (`source_data`) within an in-memory DuckDB instance.
3.  **Transformation:** SQL scripts (`src/sql/`) execute vectorized operations to generate analytical views. These scripts are source-agnostic and operate solely on the `source_data` abstraction.
4.  **Validation:** The transformed data is validated against a strict `pandera` schema before rendering.

### Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Compute** | **DuckDB** | Provides vectorized SQL execution for in-process OLAP operations. |
| **Orchestration** | **Python** | Manages environment bridging and dependency injection. |
| **Validation** | **Pandera** | Enforces data types and domain constraints (e.g., non-null ISO codes). |
| **Frontend** | **Streamlit** | UI rendering and state management. |

-----

## Data Methodology

The dashboard visualizes data from the **Global Carbon Project**, aggregated by Our World in Data.

### Metric Definitions

  * **Annual Emissions:** The quantity of CO₂ released in a given calendar year.
  * **Cumulative Emissions:** The running total of CO₂ released since 1750. This metric is used to assess historical contribution to atmospheric concentration.
  * **Per Capita:** Total emissions divided by population, normalizing for demographic size.
  * **GDP Intensity:** Emissions per unit of Gross Domestic Product, serving as a proxy for carbon efficiency.

-----

## Project Structure

The repository follows a layered architecture separating infrastructure, business logic, and presentation code.

```text
.
├── src/                   # Backend Logic
│   ├── sql/               # -> Declarative SQL transformations
│   ├── transform.py       # -> Local pipeline orchestration
│   └── validation.py      # -> Schema definitions
│
├── stories/               # Frontend Modules
│   ├── story_01_...       # -> Individual visualization components
│   └── ...
│
├── tests/                 # Quality Assurance
│   └── test_pipeline.py   # -> Pytest suite for SQL logic
│
├── app.py                 # Application Entry Point
├── Dockerfile             # Container definition
└── Makefile               # Task automation
```

-----

## Quality Assurance

Reliability is verified through a dedicated test suite located in `src/tests/`.

  * **Logic Tests:** Verify the mathematical accuracy of SQL aggregations (e.g., rolling averages).
  * **Schema Tests:** Ensure the pipeline correctly handles edge cases such as missing values or invalid date ranges.

Run the test suite locally:

```bash
make test
```

-----

## Quick Start

### Production Deployment

The application is deployed on Streamlit Cloud:
👉 **[Launch Application](https://co2-dashboard-ck.streamlit.app/)**

### Local Development

To reproduce the environment locally using Docker:

```bash
# 1. Build the image
make docker-build

# 2. Run tests
make test

# 3. Launch container
make docker-run
```

-----

## License & Attribution

**Source Code:**
Licensed under the **MIT License**.

**Data Source:**

  * **Dataset:** [CO₂ and Greenhouse Gas Emissions](https://github.com/owid/co2-data)
  * **Primary Source:** [Global Carbon Project](https://globalcarbonbudget.org/)
  * **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

<!-- end list -->

> *Disclaimer: This project is an independent educational tool and is not officially affiliated with Our World in Data.*

```
```