## About The Project

### Postgres-Seed: A Brief Overview

`postgres-seed` is a streamlined application that specializes in loading specific CSV files, processing them, and inserting the data into a PostgreSQL database. The application does not have a front-end but exposes its API using a FastAPI server.

#### API Interaction

The API can be accessed in several ways:

1. **Browser**: Thanks to FastAPI's built-in support for Swagger, you can easily interact with the API directly from your web browser.
   
2. **API Testing Tools**: For a more advanced interaction, tools like Postman or Insomnia can be used to test the API endpoints.

By providing a flexible yet focused functionality, `postgres-seed` aims to simplify the data seeding process for PostgreSQL databases.

## API Workflow

The application's API comprises several POST methods that should be used in the following sequence to ensure correct data loading and processing:

### 1. Reset Database

- **Endpoint**: `reset_db`
- **Function**: Removes all tables and indexes in the database.

### 2. Initialize Tables

- **Endpoint**: `init_tables`
- **Function**: Initializes database tables based on predefined templates.

### 3. Load and Process Config Files

- **Endpoint**: `config_files/parse_files`
- **Function**: Reads, processes, and stores configuration CSV files as temporary files in the container.
- **Note**: The application currently ignores `moreinstrumentinfo.csv` as this file is not consistent.

### 4. Load and Process Raw Data Files

- **Endpoint**: `raw_data/parse_files`
- **Function**: Reads, processes, and stores raw data CSV files as temporary files in the container.

### 5. Seed Database

- **Endpoint**: `seed_db`
- **Function**: Loads the temporary files and inserts them into the appropriate database tables.

Please adhere to this sequence when interacting with the API to ensure proper data handling and storage.

## How to Use

### Prerequisites

It is strongly recommended to use a Unix-based operating system (Linux, WSL2, macOS).

### Setup

1. **Clone the Repository**:  
   First, clone this repository to your local machine.

2. **Download the Required Data Repository**:  
   Clone the following repository, which contains the required data: [pysystemtrade](https://github.com/robcarver17/pysystemtrade).

3. **Create .env File**:  
   In the root folder, create a `.env` file and include the following lines:

    ```env
    DB_NAME=postgres_seeder
    DB_USER=postgres
    DB_PASSWORD=postgres
    POSTGRES_SERVER=db_postgres
    DB_PORT=5432
    SRC_PATH=./src
    DATA_PATH=path_to_repository/pysystemtrade/data/futures
    SQL_SCRIPT_PATH=./src/scripts/create_databases.sql
    ```

### Software Installation

4. **Install Docker**:  
   Download and install [Docker](https://www.docker.com/).

5. **Install Make**:  
   Download and install [Make](https://www.gnu.org/software/make/manual/make.html).

### Running the Project

6. **Open Terminal in Repository Folder**:  
   Navigate to the folder containing this repository.

7. **Check Make Installation**:  
   Use the command `make cheers` to check if Make is installed correctly.

8. **Run the Application**:  
   Use the command `make run`. Then, open [localhost](http://localhost:8000/docs) for API control and [pgadmin](http://localhost:5050/browser/) for database control panel.

### Running as Development Environment

#### Prerequisites for Development

- Python 3.10
- pyenv
- venv
- poetry

#### Setup Virtual Environment

1. **Install Python 3.10**:  
   Make sure Python 3.10 is installed on your system.

2. **Install pyenv, venv, and poetry**:  
   If not already installed, install pyenv, venv, and poetry.

3. **Create a Virtual Environment**:  
   Create a virtual environment for your project using your preferred method (pyenv, venv, etc.).

#### Install Dependencies and Activate Environment

4. **Install Required Libraries**:  
   Open your terminal and navigate to the project folder, then run:

    ```bash
    poetry install
    ```

   This will install all necessary libraries into your virtual environment.

5. **Activate Virtual Environment**:  
   Activate the virtual environment by running:

    ```bash
    poetry shell
    ```

Now, your development environment is set up and activated, and you're ready to proceed with development tasks.


