# Recipe to Vegan Converter

This project aims to convert any recipe into a vegan version using the ingredients available to the user. It utilizes machine learning to understand and adapt recipes, replacing non-vegan ingredients with vegan alternatives. The project includes data scraping, preprocessing, model creation, and an interactive website for easy access.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Folder Structure](#folder-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Project Overview
This tool uses machine learning to convert recipes into vegan-friendly versions by:
- Scraping recipes from various sources
- Preprocessing and cleaning data
- Building an ML model to identify and replace non-vegan ingredients
- Providing a user interface for interaction

## Features
- Convert any recipe to a vegan alternative using your available ingredients
- Support for different recipe categories: Main Course, Drinks, Desserts, Appetizers
- Clean and user-friendly web interface using Flask for backend and React for frontend
- Expandable machine learning model to improve ingredient substitution

## Folder Structure
```bash
.
├── WebScraping            # Extracts recipes from various sources (categories: main course, drinks, desserts, appetizers)
├── DataPreprocessing       # Data cleaning, processing, mapping, combining
├── Model                  # Machine Learning model creation
├── App                    # Full-stack web application with Flask (backend) and React (frontend)
└── README.md              # This readme file
```
## Requirements
- Python 3.x
- Flask
- React
- scikit-learn
- pandas
- requests (for web scraping)
- Other dependencies listed in requirements.txt


## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/vegan-recipe-converter.git
   ```
2. **Navigate to the project directory:**

  ```bash
   cd App
  ```
3. **Install backend dependencies:**

  ```bash
   pip install -r requirements.txt
  ```
4. **Navigate to the App/frontend directory and install frontend dependencies:**

  ```bash
   npm install
  ```

## Usage

1. **Start the Flask backend server:**

   ```bash
   cd App/backend
   python app.py
   ```
2. **Start the React frontend:**

  ```bash
  cd App/frontend
  npm start
  ```
3. **Open your browser and go to http://localhost:3000 to interact with the web app.**





