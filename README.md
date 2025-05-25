# 🏡 Azure Serverless Apartment Availability Alert

A serverless Python scraper that checks apartment availability online and sends email alerts using Azure Functions and SendGrid.

---

## 💡 The Problem

Apartment hunting online is time-consuming and inefficient. Most sites don’t offer custom alerts or APIs, and availability changes daily. I wanted a **hands-off solution** that notifies me when **2-bedroom units** become available on specific floors (1st, 2nd, or 3rd).

---

## 🛠️ Tech Stack

- **Python 3.12**
- `requests` + `BeautifulSoup` for web scraping
- **SendGrid** for email notifications
- **Azure Functions (Timer Trigger)** for serverless automation
- **GitHub** for version control and deployment

---

## 🔎 How It Works

- Every 30 minutes, an Azure Function triggers my Python script.
- The script scrapes apartment listings from [Cortland Las Colinas](https://cortland.com/apartments/the-palmer-at-las-colinas/available-apartments/).
- `BeautifulSoup` parses the HTML and extracts:
  - Unit number
  - Floor
  - Bedroom count
  - Price
- If a **2-bedroom apartment** on **floor 1, 2, or 3** is found, an email is sent via **SendGrid**.

---

## 🧠 Why Azure Functions?

- 💸 **Zero cost** – fits in Azure's free tier
- ⚡ **Timer trigger** – built-in scheduling (like cron jobs)
- 🧼 **Simple deployment** using:

  ```bash
  func azure functionapp publish <your-app-name>
