# Previous Repo Link:https://github.com/smahesh29/Django-ToDo-App

# Forked Repo Link without AWS Changes:[https://github.com/smahesh29/Django-ToDo-App](https://github.com/DivyaMehta1805/Django-ToDo-App)

# Detailed Description of Changes Made By Divya Mehta

## Tasks Completed Per Day (Overview)

This feature of the ToDo application provides a visual representation of tasks completed versus tasks not completed over the past 30 days. It leverages Chart.js to render a bar chart, showing counts of tasks per day. The data is fetched from a backend API endpoint that aggregates tasks based on their completion status.

### 1. Architecture and Functionality

#### View Functions (views.py)

- **tasks_graph(request)**:
  - This view renders the `tasks_graph.html` template.
  - It calls the `tasks_per_day_view` function to prepare the data required for the chart but doesn't pass the data directly to the template; it relies on the frontend to fetch it via an API call.

#### tasks_per_day_view(request)

- This view is responsible for aggregating and providing the task data in JSON format.
- It calculates task counts for completed and not completed tasks over the past 30 days.
- Constructs a dictionary with dates as keys and counts as values.
- Combines and formats the dates and counts into a JSON response.

#### Template (tasks_graph.html)

- **HTML Structure**:
  - The template includes a `<canvas>` element where the Chart.js graph will be rendered.
  - It links to a CSS file for basic styling and includes the Chart.js library for rendering charts.

#### JavaScript Functionality

- Fetches JSON data from the `/tasks_per_day_view/` endpoint.
- Parses the JSON response to extract dates and counts of completed and not completed tasks.
- Uses Chart.js to render a bar chart with:
  - X-axis: Dates.
  - Y-axis: Count of tasks.
  - Two datasets: One for completed tasks and one for not completed tasks.
  - Configures the chart with labels and styling for the data series.

### 2. URLs Configuration (urls.py)

- **URL Patterns**:
  - `path('tasks_per_day_view/', views.tasks_per_day_view, name='tasks_per_day_view')`: Endpoint for fetching task data in JSON format.
  - This URL is used by the frontend JavaScript to retrieve the necessary data for rendering the chart.

### 3. Model (models.py)

- **at Field**:
  - The `at` field in the `Todo` model is a `DateTimeField` that records when a task was created or updated.
  - It is used in the aggregation queries to filter tasks based on their date of creation or completion.

### 4. Data Flow and Connectivity

- **User Interaction**:
  - When the user navigates to the `tasks_graph` page, the `tasks_graph.html` template is rendered, which includes a Chart.js graph.

- **Data Fetching**:
  - The frontend JavaScript makes an HTTP GET request to the `/tasks_per_day_view/` endpoint.
  - The `tasks_per_day_view` view processes this request, aggregates the task data, and returns it as a JSON response.

- **Chart Rendering**:
  - The JavaScript on the `tasks_graph.html` page processes the JSON response.
  - It uses Chart.js to plot the data on a bar chart, displaying completed versus not completed tasks for each day over the last 30 days.



          
# Search Functionality

The search functionality is embedded in the `index.html` template and interacts with the `taskList` view. Users enter a search query into the input field provided in the search form. Submitting the form triggers a GET request to the `taskList` URL with the search query as a parameter. The `taskList` view processes this query and filters the tasks accordingly. The filtered list of tasks is then rendered back to the user on the `index.html` page, showing only those tasks that match the search criteria.

## Views (views.py)

- **taskList(request)**:
  - This view handles the display and search functionality for tasks.
  - Initializes the `TaskSearchForm` with the GET request parameters.
  - Retrieves all tasks from the database.
  - Filters tasks based on the search query (`query`), if provided.
  - Passes the filtered tasks and the form to the `taskList.html` template for rendering.

## Forms (forms.py)

- **TaskSearchForm**:
  - A form used to capture the search query from the user.
  - Includes a single optional field (`query`) for searching tasks.
  - Uses a `TextInput` widget with a class of `form-control` and a placeholder to enhance user experience.

## Templates

- **task_list.html**:
  - Displays the list of tasks with their details including the completion status.
  - Uses a loop to iterate over `todo_list` and renders each task's text, description, and completion status.
  - Provides a message when no tasks are found.

- **index.html**:
  - Includes a search form that posts to the `taskList` view.



# Docker Architecture

## Overview

This project uses Docker to manage a multi-container environment, consisting of a Django web application, a PostgreSQL database, and an Nginx reverse proxy. The architecture is defined using `docker-compose.yml` for orchestration and `Dockerfile` for image creation.

## docker-compose.yml

The `docker-compose.yml` file configures and manages the following services:

- **web**:
  - **Role**: Runs the Django application using Gunicorn as the WSGI server.
  - **Build Context**: The Docker image is built from the `./app` directory.
  - **Command**: Waits for the `db` service (PostgreSQL) to be ready before starting the Gunicorn server.
  - **Volumes**: 
    - Maps the local `./app` directory to `/usr/src/app` in the container.
    - Uses `static_volume` for static files and `media_volume` for media files.
  - **Environment Variables**: Configures Django settings, including database connection parameters and AWS S3 integration.
  - **Dependencies**: Ensures the `web` service starts only after the `db` service is up.

- **db**:
  - **Role**: Provides the PostgreSQL database service.
  - **Image**: Uses `postgres:15-alpine`.
  - **Volumes**: Stores database data persistently in `postgres_data`.
  - **Environment Variables**: Sets up database credentials and default database.

- **nginx**:
  - **Role**: Acts as a reverse proxy to handle HTTP requests and serve static files.
  - **Build Context**: The Docker image is built from the `./nginx` directory.
  - **Volumes**: Shares static and media files with the `web` service.
  - **Ports**: Maps port `1337` on the host to port `80` in the container.

### Volumes

- **postgres_data**: Persistent storage for PostgreSQL database files.
- **static_volume**: Storage for collected static files used by Django.
- **media_volume**: Storage for user-uploaded media files.

## Dockerfile

The `Dockerfile` outlines how to build the Docker image for the Django application:

- **Base Image**: Starts with `python:3.11.1-alpine`, a minimal Python environment based on Alpine Linux.
- **Environment Variables**:
  - `PYTHONDONTWRITEBYTECODE=1`: Prevents Python from generating `.pyc` files.
  - `PYTHONUNBUFFERED=1`: Ensures Python output is sent directly to the terminal without buffering.
- **Working Directory**: Sets `/usr/src/app` as the working directory inside the container.
- **System Dependencies**:
  - Installs necessary build tools and PostgreSQL libraries.
- **Python Dependencies**:
  - Upgrades `pip` and installs dependencies from `requirements.txt`.
- **Project Code**: Copies the Django project code into the Docker image.

### Summary

The Docker architecture includes three primary services: the `web` service (Django app), the `db` service (PostgreSQL), and the `nginx` service (reverse proxy). The `docker-compose.yml` file orchestrates these services, while the `Dockerfile` builds the Docker image for the Django application, ensuring all necessary dependencies and configurations are in place.


# Django AWS S3 Integration Architecture

## Overview

The `settings.py` file configures the Django project to optionally use AWS S3 for static and media file storage.

## Key Functions

- **Secret Key Management**: Retrieves the `SECRET_KEY` from environment variables to enhance security.
- **Debug Mode**: Sets `DEBUG` to `True` for development, which should be turned off in production.
- **Static and Media Files**:
  - **Local Storage**: Configures paths for serving static and media files from local directories if AWS S3 is not used.
  - **AWS S3 Storage**: When enabled, it sets up AWS S3 to store and serve static files and media, using credentials and settings from environment variables.
- **CSRF Protection**: Adds local development URLs to `CSRF_TRUSTED_ORIGINS` to manage Cross-Site Request Forgery (CSRF) protection.
- **Database Configuration**: Allows dynamic configuration of database settings through environment variables, defaulting to SQLite for development.
- **Auto Field Setting**: Defines the default type for auto-generated primary keys.

## Summary

The `settings.py` file ensures the Django application can efficiently handle static and media files both locally and on AWS S3, while also managing environment-specific settings and security configurations.



