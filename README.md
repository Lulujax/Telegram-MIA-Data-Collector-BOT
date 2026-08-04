# 📡 Telegram MIA Data Collector Bot

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![Architecture](https://img.shields.io/badge/Architecture-Clean%20%7C%20SOLID-success.svg)
![Data Structures](https://img.shields.io/badge/Data%20Structures-Custom%20%7C%20Generics-orange.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

A highly resilient and secure Telegram bot designed to collect structured data and multimedia regarding Missing in Action (MIA) individuals. Built with strict Object-Oriented Programming (OOP) standards, custom data structures, and a robust fallback architecture to ensure zero data loss and 24/7 uptime.

---

## 📌 Project Overview

In crisis environments, data collection must be flawless. This bot provides a seamless, sequential survey flow for families and NGOs to securely submit critical information (such as DNA profiles, physical descriptions, and last known locations). 

To guarantee absolute stability, the core logic bypasses standard high-level collections and relies entirely on manually implemented data structures, custom exception handling, and an isolated local ledger system.

## 🚀 Engineering & Architecture Highlights

This repository serves as a practical implementation of advanced software engineering concepts:

* **Pure OOP & SOLID Principles:** Strict encapsulation of all entity states. Variables are aggressively protected (`_private`), and state mutations only occur through controlled interfaces (getters/setters).
* **Custom Generic Data Structures:** Built entirely from scratch. Native Python collections (`list`, `dict` for core flow) were discarded in favor of:
  * `CustomNode[generic_type]`
  * `CustomQueue[generic_type]`
  * `CustomList[generic_type]`
* **Finite State Machine (FSM):** The survey flow is driven by a dynamically managed Queue of `SurveyQuestion` objects. It effortlessly handles mandatory fields, skipped questions, and multi-file media uploads (e.g., 1/3, 2/3 photo limits) without losing session context.
* **Custom Exception Handling:** Internal flow control utilizes custom typed exceptions (`InvalidValueException`, `EmptyDataStructureException`) to prevent corrupted data from ever reaching the storage layer.
* **Isolated I/O Storage:** Dynamically generates sanitized, unique directories for each user based on their Telegram ID. All text answers and media files are stored locally, with responses appended securely to individual `.csv` ledgers.
* **24/7 Watchdog Resilience:** Includes a custom `.bat` looping architecture designed for Windows Server Task Scheduler. It instantly recovers the Python interpreter from API 409 Conflicts, network drops, or OS-level memory wipes.

---

## ⚙️ How It Works (The Flow)

1. **Initialization:** User sends `/start`. A unique session state and local folder are instantly allocated.
2. **Data Collection:** The FSM prompts the user step-by-step. If a user uploads multiple photos simultaneously, the bot processes each item sequentially, validating against the active question.
3. **Completion:** Data is flushed to a `user_data.csv` ledger.
4. **Notification:** An automated alert is securely dispatched to the system administrator's Telegram ID.

---

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.8+
* `pyTelegramBotAPI` package

### Deployment Steps

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/Telegram-MIA-Data-Collector.git](https://github.com/yourusername/Telegram-MIA-Data-Collector.git)
   cd Telegram-MIA-Data-Collector
   ```

2. **Install dependencies:**
   ```bash
   pip install pyTelegramBotAPI
   ```

3. **Configuration:**
   * Open `main.py`.
   * Replace `bot_access_token` with your secure Telegram Bot Token.
   * Replace `admin_chat_id` with the numerical Telegram ID of the receiving administrator.
   * Ensure the `root_data_path` points to your desired local storage directory.

4. **Run the Bot (Development):**
   ```bash
   python main.py
   ```

5. **Run the Bot (Production / Windows Server):**
   * Edit `arrancar_bot.bat` to match your local paths.
   * Configure the Windows Task Scheduler to run the `.bat` file on startup with highest privileges.

---

## ⚠️ Security & Privacy Disclaimer

This repository handles highly sensitive human data. 
* **Never** commit the actual `bot_access_token` to version control.
* Ensure the `.gitignore` file includes the `User_Data/` directory, `*.csv` files, and `registro_consola.txt` to prevent accidental leaks of PII (Personally Identifiable Information).

---

*Developed with a focus on code robustness, scalability, and clean architecture.*