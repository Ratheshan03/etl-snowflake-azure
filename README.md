# 🌦️ ETL Pipeline with Azure, Snowflake & Grafana

Welcome to the **Weather Data ETL Pipeline** project! This end-to-end solution automates weather data extraction, transformation, loading (ETL), and visualization using modern cloud and analytics tools. Built with modular, cloud-native components and a Grafana dashboard for real-time monitoring.

> **Live Dashboard**: [Grafana Weather Dashboard](#)  
> *(Replace with actual URL or instructions to access it)*

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [ETL Breakdown](#etl-breakdown)
  - [1. Extraction](#1-extraction)
  - [2. Transformation](#2-transformation)
  - [3. Loading](#3-loading)
- [Visualization with Grafana](#visualization-with-grafana)
- [Setup Guide](#setup-guide)
- [Automation and Scheduling](#automation-and-scheduling)
- [How to Contribute](#how-to-contribute)
- [License](#license)
- [References & Docs](#references--docs)

---

## 🧠 Project Overview

This project collects live weather data from multiple cities, processes it, and makes it accessible via a Snowflake data warehouse. A Grafana dashboard on top of the pipeline provides intuitive visual insights.

**Key Features:**
- Azure Functions for cloud-native ETL automation
- Weather API integration
- Data transformation and cleaning
- Scheduled uploads to Snowflake via Azure Blob Storage
- Real-time visual dashboards with Grafana + Snowflake

---

## 🛠️ Tech Stack

| Layer             | Tool/Service        |
|------------------|---------------------|
| **Language**      | Python              |
| **Orchestration** | Azure Functions     |
| **Storage**       | Azure Blob Storage  |
| **Warehouse**     | Snowflake           |
| **Visualization** | Grafana Cloud       |
| **Scheduling**    | CRON (Azure Timer)  |

---

## 🏗️ Architecture

```text
        +--------------+       +--------------------+
        |  Weather API | ----> |  Python ETL Script |
        +--------------+       +---------+----------+
                                        |
                           +------------v------------+
                           |    Azure Blob Storage   |
                           +------------+------------+
                                        |
                           +------------v------------+
                           |     Snowflake DB        |
                           +------------+------------+
                                        |
                           +------------v------------+
                           |      Grafana Panels     |
                           +-------------------------+
```

---

## ⚙️ ETL Breakdown

### 1. 🔍 Extraction

- **Source**: Public Weather API (e.g., OpenWeatherMap)
- **Cities**: 5 fixed cities, predefined in the code
- **Method**: Python `requests` fetching JSON payloads

### 2. 🔧 Transformation

- Cleaned and parsed required fields:
  - Temperature (converted to Celsius)
  - Humidity, Pressure, Wind Speed
  - Cloud coverage, Sunrise/Sunset
  - Weather Descriptions
- Output saved as: `clean_weather.csv`

### 3. 🚀 Loading

- Upload `clean_weather.csv` to **Azure Blob Storage**
- Trigger Snowflake load using Python Snowflake Connector
- **Snowflake Target:**
  - Database: `ETL_DB`
  - Schema: `ETL_SCHEMA`
  - Table: `WEATHER_DATA`

---

## 📊 Visualization with Grafana

- **Grafana Cloud** connected to **Snowflake** using the **Grafana Snowflake Plugin**
- Created dynamic, city-wise panels for:
  - Temperature trends
  - Humidity, Wind Speed, Cloud coverage
  - Weather conditions (Main/Description)
  - Daily Min/Max temperatures
- Auto-refresh interval: **Every 15 minutes**
- Grafana must be authenticated with **read-only Snowflake credentials**

---

## 🚀 Setup Guide

### 🔧 Prerequisites

- Python 3.10+
- Azure Account
- Snowflake Account
- Grafana Cloud Account

---

### 📁 1. Clone the Repository

```bash
git clone https://github.com/Ratheshan03/etl-snowflake-azure.git
cd etl-snowflake-azure
```

### 2. Setup Python Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create .env file or set environment variables:

```
API_KEY=<your_openweathermap_api_key>
AZURE_STORAGE_CONNECTION_STRING=<your_blob_connection_string>
SNOWFLAKE_USER=<user>
SNOWFLAKE_PASSWORD=<password>
SNOWFLAKE_ACCOUNT=<account>
SNOWFLAKE_DATABASE=ETL_DB
SNOWFLAKE_SCHEMA=ETL_SCHEMA
SNOWFLAKE_WAREHOUSE=ETL_WH
SNOWFLAKE_ROLE=<role>
```

### 4. Deploy Azure Function
Use the Azure Functions Core Tools or Azure Portal

⏲️ Timer Trigger CRON: `0 0 0,12 * * *` (runs every 12 hours)

---

## ⏱️ Automation and Scheduling
Azure Functions timer trigger (CRON: `0 0 0,12 * * *`)

ETL pipeline runs at:
- 00:00 UTC
- 12:00 UTC

Also executes on startup of function host

---

## 👥 How to Contribute
Feel free to contribute to improve or extend this project:

### 💡 Ideas
- Add more cities or make it dynamic
- Include severe weather alerts
- Add historical weather data trend analysis

### 🛠️ Contribution Steps
1. Fork the repo
2. Create your feature branch
```bash
git checkout -b feature/awesome-feature
```
3. Commit your changes
```bash
git commit -m "Add awesome feature"
```
4. Push to the branch
```bash
git push origin feature/awesome-feature
```
5. Open a Pull Request

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📚 References & Docs
- [OpenWeatherMap API Docs](https://openweathermap.org/api)
- [Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/)
- [Azure Functions](https://learn.microsoft.com/en-us/azure/azure-functions/)
- [Snowflake Documentation](https://docs.snowflake.com/)
- [Grafana Snowflake Plugin](https://grafana.com/grafana/plugins/grafana-snowflake-datasource/)
- [Grafana Cloud](https://grafana.com/products/cloud/)

---

Happy Cloud ETL-ing! 🌩️
