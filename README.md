# Data Intensive Application: Global CO₂ Analysis

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32-ff4b4b)
![DuckDB](https://img.shields.io/badge/DuckDB-SQL-yellow)
![Docker](https://img.shields.io/badge/Docker-Container-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A production-grade data engineering application that transforms raw environmental data into ten distinct analytical narratives.

## 🚀 Project Overview

This is not just a dashboard; it is a demonstration of rigorous **Data Engineering** principles applied to climate science. The application ingests 70+ years of raw emissions data, processes it through a declarative SQL pipeline, and serves interactive insights via a containerized Streamlit interface.

### The "SQL-First" Philosophy
Unlike traditional notebooks that bury logic in Python loops, this project uses **DuckDB** as an in-process OLAP engine. All data transformations are written in declarative SQL, ensuring performance, readability, and reproducibility.

## 📊 The 10 Data Stories

The application answers ten critical questions about the history of climate change:

1.  **Historical Responsibility:** Who holds the most cumulative debt for atmospheric CO₂?
2.  **The Personal Footprint:** How does lifestyle and wealth correlate with per capita emissions?
3.  **The Global Trend:** Visualizing the "Great Acceleration" since 1950.
4.  **Today's Heavy Hitters:** The geopolitical shift of emissions from West to East.
5.  **The Great Acceleration:** Analyzing the exponential growth of non-OECD emissions.
6.  **The Fuel Mix:** The hidden dominance of coal in the modern industrial baseload.
7.  **Volatility & Shocks:** How the 2008 Crisis and COVID-19 impacted the carbon curve.
8.  **The Hope Story:** Evidence of "Decoupling" (GDP growth vs. Emissions decline).
9.  **Consumption vs. Production:** The impact of "offshoring" pollution via trade.
10. **The Analyst's View:** A multivariate analysis of Wealth, Population, and Carbon.

## 🛠️ Architecture

The system follows a **"Lakehouse-Lite"** topology:

```mermaid
graph LR
    A[Raw Data (OWID)] -->|Ingest| B(Pandas Buffer)
    B -->|Load| C{DuckDB Engine}
    C -->|SQL Transform| D[Cleaned Data]
    D -->|Validate| E[Pandera Schema]
    E -->|Serve| F[Streamlit App]


Core Technologies

    Ingestion: Python requests & pandas

    Transformation: DuckDB (SQL)

    Validation: Pandera (Schema Contracts)

    Visualization: Plotly Express & Streamlit

    Containerization: Docker

💻 Local Setup

You can run this application locally using Python.

Prerequisites: Python 3.9+


# 1. Clone the repository
git clone [https://github.com/k-chetan/CO2-Dashboard.git](https://github.com/k-chetan/CO2-Dashboard.git)
cd CO2-Dashboard

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py


# Build the image
docker build -t co2-app .

# Run the container (Access at localhost:8501)
docker run -p 8501:8501 co2-app

🔮 Future Roadmap (v2.0)

    Predictive Inference: Integration of Prophet for CO₂ forecasting.

    AI Architect: A RAG-based chatbot to query the underlying SQL logic.

    CI/CD: GitHub Actions workflow for automated data refreshing.

Built by Chetan K. Data Source: Our World in Data (OWID).