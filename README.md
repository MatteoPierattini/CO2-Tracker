
# CO2-Tracker

This is a web application that allows users to calculate their personal CO2 daily emissions and visualize them on their own personal dashboard. The application provides an easy way for individuals to track their environmental impact based on their daily activities.

## Features

- Calculate personal daily CO2 emissions
- View statistics and trends on a personalized dashboard
- Save and track historical emissions data

## Technologies Used

- **Python**: Core backend logic of the application.
- **Flask**: Used as the web framework to handle HTTP requests and render templates.
- **HTML/CSS/JavaScript**: Frontend technologies for rendering the user interface and dashboard.
- **SQLite**: Used to store user data and historical CO2 emission logs.
- **Bootstrap**: For responsive and easy-to-use user interface components.
- **Chart.js**: For visualizing the user's CO2 emission data.


## Prerequisites

To run this app locally, you will need to have the following installed:

- **Python 3.x**
- **Flask** and **Flask-Session** Python packages
- **SQLite** for local database management

## Installation Instructions

### 1. Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/yourrepository.git
cd yourrepository
```

### 2. Set Up a Virtual Environment

Set one up using the following commands:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

To start the Flask application, use the following command:

```bash
flask run
```

The app will run locally at `http://127.0.0.1:5000/`. Open this URL in your web browser to access the app.

## Usage

1. **Sign Up**: Create an account by signing up.
2. **Log In**: Log into your account to access the dashboard.
3. **Set a Goal**: Set your monthly carbon footprint reduction goal.
4. **Track Emissions**: Log your CO2 emissions from transportation, energy, and food consumption.
5. **View Progress**: Check the dashboard to see your progress with data visualizations.
