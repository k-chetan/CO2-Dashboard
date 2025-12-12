# Global CO₂ Intelligence Platform 🌍

> **A "Zero-Storage" implementation of modern Data Engineering principles.**
> *Stateless. In-Memory OLAP. Source-Agnostic.*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://co2-dashboard-ck.streamlit.app/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://hub.docker.com/r/kchetan/co2-dashboard)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)

## 📖 Executive Summary

The **Global CO₂ Intelligence Platform** is an interactive analytics engine designed to visualize the trajectory of global emissions from 1750 to the present.

Unlike traditional dashboards that rely on static database connections or local files, this application implements a **Live Streaming "Lakehouse-Lite" Architecture**. Upon initialization, it establishes a secure uplink to the [Our World in Data (OWID)](https://github.com/owid/co2-data) repository, streams the raw dataset into volatile memory (RAM), and performs real-time OLAP transformations using **DuckDB**.

**The Result:** A stateless, serverless application that guarantees data freshness without requiring persistent storage infrastructure.

---

## 🏗️ Architectural Design

The system adheres to the **Dependency Injection** principle, decoupling the *Transformation Logic* from the *Data Source*. This allows the pipeline to operate identically in two distinct modes: local development (file-based) and cloud production (stream-based).

```mermaid
graph LR
    subgraph Cloud [Streamlit Cloud Runtime]
    A[OWID GitHub Raw CSV] -->|HTTPS Stream| B(Pandas Buffer)
    B -->|Injection| C{DuckDB In-Memory OLAP}
    C -->|SQL Transformation| D[Streamlit Frontend]
    end
````

### 1\. The "Zero-Storage" Pattern

In the production environment (Streamlit Cloud), no data is ever written to disk.

1.  **Ingestion:** Python streams the raw CSV via HTTPS directly into a Pandas buffer.
2.  **Injection:** The buffer is registered as a virtual table (`source_data`) in an in-memory DuckDB instance.
3.  **Transformation:** SQL scripts execute vectorized operations to clean, aggregate, and normalize the data.
4.  **Presentation:** The resulting artifact is served to the frontend.

### 2\. Tech Stack & Decisions

| Component | Technology | Rationale |
| :--- | :--- | :--- |
| **Compute Engine** | **DuckDB** 🦆 | Columnar, vectorized execution allows for sub-second aggregations on millions of rows in-process. |
| **Orchestration** | **Python** 🐍 | Handles dependency injection and environment bridging. |
| **Quality Assurance** | **Pandera** 🛡️ | Enforces a strict schema contract at runtime. Invalid data triggers an immediate halt (Fail Fast). |
| **Visualization** | **Streamlit** 📊 | Enables rapid prototyping of interactive data stories. |

-----

## 🔬 Data Science Methodology

To ensure academic rigor, the platform distinguishes between several types of emission metrics.

### Stock vs. Flow

  * **Annual Emissions (Flow):** The amount of CO₂ released in a specific year. This metric highlights current industrial activity.
  * **Cumulative Emissions (Stock):** The total sum of CO₂ released since 1750. Since CO₂ persists in the atmosphere for centuries, this metric is the primary driver of warming and the basis for "Historical Responsibility."

### Normalization

  * **Per Capita:** Adjusts for population size to measure lifestyle impact rather than just total output.
  * **GDP Intensity:** Measures the carbon efficiency of an economy (kg CO₂ per $ of GDP).

### Data Provenance

  * **Primary Source:** The Global Carbon Project (GCP).
  * **Aggregator:** Our World in Data (OWID).
  * **License:** Creative Commons Attribution 4.0 International (CC BY 4.0).

-----

## 🚀 Quick Start

### Live Cloud Version

Access the production deployment directly:
👉 **[Launch Dashboard](https://co2-dashboard-ck.streamlit.app/)**

### Local Development

Reproduce the environment locally using Docker to ensure parity with production.

```bash
# 1. Build the Immutable Runtime
make docker-build

# 2. Run the Test Suite (Pytest)
make test

# 3. Launch the Application
make docker-run
```

-----

## 📂 Project Structure

The codebase is organized into strict layers to separate concerns: Infrastructure, Logic, and Presentation.

```text
.
├── src/                   # [BACKEND LAYER]
│   ├── sql/               # -> Declarative SQL (Business Logic)
│   ├── transform.py       # -> Dependency Injector (Local)
│   └── validation.py      # -> Schema Contracts (Quality Gate)
│
├── stories/               # [FRONTEND LAYER]
│   ├── story_01_...       # -> "Historical Responsibility" Module
│   ├── story_02_...       # -> "Personal Footprint" Module
│   └── ...
│
├── tests/                 # [QA LAYER]
│   └── test_pipeline.py   # -> Unit tests for SQL logic
│
├── app.py                 # [ENTRY POINT] -> Main Controller
├── Dockerfile             # [INFRASTRUCTURE] -> OS Definition
└── Makefile               # [AUTOMATION] -> Developer Experience
```

-----

## 🛡️ Quality Assurance

Reliability is enforced through a dedicated testing suite (`src/tests/`).

  * **Logic Tests:** Verify that rolling averages and aggregations are mathematically correct.
  * **Schema Tests:** Ensure the pipeline rejects data with missing ISO codes or invalid years.
  * **Integration Tests:** Verify the seamless handover between Pandas and DuckDB.

Run the full suite with:

```bash
make test
```

-----

## ⚖️ License & Attribution

**Application Source Code:**
Released under the **MIT License**. Copyright © 2025.

**Data Attribution:**
This project utilizes the **CO₂ and Greenhouse Gas Emissions** dataset.

  * **Source:** [Our World in Data](https://ourworldindata.org/co2-emissions) based on the [Global Carbon Project](https://globalcarbonbudget.org/).
  * **Authors:** Andrew, R. M., & Peters, G. P. (2024); Ritchie, H., Roser, M. (2020).
  * **License:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

> *Disclaimer: This project is an independent educational tool and is not officially affiliated with Our World in Data.*

```
```