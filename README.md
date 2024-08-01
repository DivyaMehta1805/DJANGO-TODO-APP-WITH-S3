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



# Docker Configuration

## docker-compose.yml

Defines and runs multi-container Docker applications for the ToDo application.

### Services

- **web**:
  - **Build**: `./app` directory.
  - **Command**: Waits for PostgreSQL to be ready, then starts Gunicorn.
    ```bash
    bash -c 'while !</dev/tcp/db/5432; do sleep 1; done; gunicorn hello_django.wsgi:application --bind 0.0.0.0:8000'
    ```
  - **Volumes**:
    - `./app/:/usr/src/app/`
    - `static_volume:/usr/src/app/staticfiles`
    - `media_volume:/usr/src/app/mediafiles`
  - **Expose**: Port `8000`.
  - **Environment Variables**:
    ```plaintext
    SECRET_KEY=12345
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=postgres
    SQL_USER=postgres
    SQL_PASSWORD=postgres
    SQL_HOST=db
    SQL_PORT=5432
    DATABASE=postgres
    USE_S3=TRUE
    AWS_ACCESS_KEY_ID=<SET IT YOURSELF>
    AWS_SECRET_ACCESS_KEY=<SET IT YOURSELF>
    AWS_STORAGE_BUCKET_NAME=todo-app-bucket-12
    ```
  - **Depends On**: `db`.

- **db**:
  - **Image**: `postgres:15-alpine`.
  - **Volumes**:
    - `postgres_data:/var/lib/postgresql/data/`
  - **Expose**: Port `5432`.
  - **Environment Variables**:
    ```plaintext
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=postgres
    ```

- **nginx**:
  - **Build**: `./nginx` directory.
  - **Volumes**:
    - `static_volume:/usr/src/app/staticfiles`
    - `media_volume:/usr/src/app/mediafiles`
  - **Ports**: `1337:80`.
  - **Depends On**: `web`.

### Volumes

- **postgres_data**: For PostgreSQL data.
- **static_volume**: For static files.
- **media_volume**: For media files.

## Dockerfile

Builds the Docker image for the Django application.

### Instructions

- **Base Image**: `python:3.11.1-alpine`.
  ```dockerfile
  FROM python:3.11.1-alpine

## Dockerfile
Builds the Django app image using `python:3.11.1-alpine`. Sets up environment, installs dependencies, and copies the project into the container.

