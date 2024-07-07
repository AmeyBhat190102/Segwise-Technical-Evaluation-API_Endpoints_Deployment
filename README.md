# Game Data Analytics API

## Overview

This project is a web service for a game analytics company that allows data analysts to upload a CSV file containing game data and query the data through a RESTful API. The application is built using Flask and uses a SQLite database for storage.

## Features

- **Upload CSV Data**: Upload game data from a CSV file hosted on a URL.
- **Query Data**: Query the game data based on various parameters.
- **View Data**: Display the game data in a table format on the frontend.

## Prerequisites

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Requests
- Pandas

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/game-data-analytics.git
   cd game-data-analytics```

### API Usage

To interact with the Game Data Analytics API, you can utilize the following endpoints:

#### Upload CSV Data

- **Endpoint**: `/upload`
- **Method**: `POST`
- **Description**: Upload a CSV file containing game data from a specified URL. The request body should include a JSON object with the `csv_url` parameter pointing to the CSV file's URL.

### Query Data

- **Endpoint**: `/query`
- **Method**: `GET`
- **Description**: Query the game data based on various parameters.

#### Query Parameters

- `name`: Filter by game name (partial match)
- `appid`: Filter by AppID
- `release_date`: Filter by release date
- `required_age`: Filter by required age
- `price`: Filter by price
- `price_gt`: Filter by price greater than
- `price_lt`: Filter by price less than
- `dlc_count`: Filter by DLC count
- `supported_languages`: Filter by supported languages (partial match)
- `windows`: Filter by Windows support (`true` or `false`)
- `mac`: Filter by Mac support (`true` or `false`)
- `linux`: Filter by Linux support (`true` or `false`)
- `positive`: Filter by number of positive reviews
- `negative`: Filter by number of negative reviews
- `score_rank`: Filter by score rank
- `developers`: Filter by developers (partial match)
- `publishers`: Filter by publishers (partial match)
- `categories`: Filter by categories (partial match)
- `genres`: Filter by genres (partial match)
- `tags`: Filter by tags (partial match)
- `aggregate`: Perform aggregate functions (`max_price`, `min_price`, `avg_price`)

### Local Setup of This Project

- `docker build -t flask-app .`
- `docker run -p 5000:5000 flask-app`

