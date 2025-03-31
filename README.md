# LinkZen

LinkZen is a full-stack link management and categorization application designed to streamline the way you save and manage links. It integrates with Gemini for link processing and supports two methods for adding links: through a user-friendly web frontend and via a Telegram bot. Whether you’re curating bookmarks or sharing content, LinkZen provides a modern, API-driven solution for organizing your digital life.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation and Setup](#installation-and-setup)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Environment Variables (.env)](#environment-variables-env)
  - [Creating a Telegram Bot](#creating-a-telegram-bot)
- [Running the Application](#running-the-application)
  - [Running the Backend](#running-the-backend)
  - [Running the Frontend](#running-the-frontend)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview

LinkZen is designed to simplify the process of managing your favorite links. The backend sends links to Gemini for additional processing and categorization, while also offering flexible options for adding new links via a Telegram bot or through the web frontend. This project uses FastAPI for the backend, providing a robust RESTful API, and a Vite-powered frontend for a modern user interface.

## Features

- **Link Categorization:** Automatically categorize and store links with relevant metadata.
- **Gemini Integration:** Forward links to Gemini for enhanced processing.
- **Dual Input Methods:** Add links either through the web interface or via Telegram bot commands.
- **RESTful API:** Built with FastAPI for fast, asynchronous communication.
- **Modern Frontend:** Developed using a Vite template with TypeScript for a responsive design.
- **Lightweight Database:** Uses SQLite for quick and easy local storage.
- **CORS Enabled:** Supports cross-origin resource sharing to integrate with different clients.

## Technologies Used

- **Backend:** Python, FastAPI, SQLite, uvicorn, asyncio
- **Frontend:** TypeScript, Vite, HTML, CSS, JavaScript
- **Bot Integration:** Telegram Bot API
- **Environment Management:** python-dotenv

## Installation and Setup

### Prerequisites

Before you begin, make sure you have the following installed on your system:

- Python 3.8+
- Node.js (v14 or later) and npm
- Git

### Clone the Repository

```bash
git clone https://github.com/naitik2314/LinkZen.git
cd LinkZen
```

### Backend Setup

Navigate to the Backend Directory:

```bash
cd Backend
```

(Optional) Create a Virtual Environment:

```bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
```

Install Python Dependencies:

```bash
pip install -r requirements.txt
```

_Note:_ If a `requirements.txt` file isn’t provided, install at least:

- fastapi
- uvicorn
- python-dotenv

### Frontend Setup

Navigate to the Frontend Directory:

```bash
cd ../Frontend
```

Install Node.js Dependencies:

```bash
npm install
```

### Environment Variables (.env)

Create a `.env` file in the root directory (or in the Backend directory if preferred). This file is used to store sensitive configuration data and should include the following:

```dotenv
# Database configuration
DB_FILE=links.db

# Telegram Bot configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
# (Optional) ID of the Telegram chat where notifications should be sent
TELEGRAM_CHAT_ID=your_telegram_chat_id_here

# Gemini API endpoint (if available)
GEMINI_API_URL=https://your.gemini.api/endpoint
```

Replace `your_telegram_bot_token_here` with the token you receive from Telegram’s BotFather and update the other fields as necessary.

### Creating a Telegram Bot

To create a Telegram bot for LinkZen, follow these steps:

1. Open Telegram and search for **BotFather**.
2. Start a chat with BotFather and send the command:

   ```bash
   /newbot
   ```
3. Follow BotFather’s instructions:
   - Choose a name for your bot.
   - Choose a username that ends with “bot” (e.g., LinkZenBot).
4. **Obtain the Bot Token:**
   - After creation, BotFather will send you a token. Copy this token and paste it into your `.env` file under `TELEGRAM_BOT_TOKEN`.
5. (Optional) **Configure Additional Settings:**
   - You can adjust settings like privacy mode and custom commands through BotFather.

## Running the Application

### Running the Backend

Ensure you’re in the Backend Directory:

```bash
cd Backend
```

Run the FastAPI Application:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

The backend will be accessible at [http://localhost:8000](http://localhost:8000).

### Running the Frontend

Navigate to the Frontend Directory:

```bash
cd ../Frontend
```

Start the Vite Development Server:

```bash
npm run dev
```

You will typically access the frontend at [http://localhost:3000](http://localhost:3000) (or the URL provided in your terminal).

## Project Structure

```bash
LinkZen/
├── Backend/
│   ├── api.py              # Main FastAPI application
│   ├── links.db            # SQLite database (auto-generated)
│   └── ...                 # Other backend files and configurations
├── Frontend/
│   ├── src/                # Frontend source code (e.g., React/Vue components)
│   ├── package.json        # Node.js dependencies and scripts
│   └── README.md           # Frontend-specific instructions
└── .env                    # Environment variables configuration file
```

## Usage

**Adding Links:**

You can add new links either via the web interface or by sending a command/message to the Telegram bot.

**Link Categorization & Gemini Integration:**

When a link is added, the backend processes it, categorizes it, and sends it to Gemini for further handling. Modify the categorization logic or Gemini integration by editing the backend code as required.

**Telegram Bot Interaction:**

Use the Telegram bot (e.g., `/addlink <URL> <category> <optional description>`) to add new links directly from Telegram.

## Contributing

Contributions are welcome! If you want to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Submit a pull request with a detailed explanation of your changes.

For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- **FastAPI:** For providing a modern, fast web framework.
- **Vite:** For enabling a fast and modern development experience for the frontend.
- **Telegram Bot API:** For making bot integrations straightforward.
- **Magic Patterns:** For the design inspiration and initial frontend template.

By following these instructions, you can set up, run, and extend LinkZen on your local machine. Enjoy managing your links seamlessly!