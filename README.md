# NC Plus One

## Project Structure

├── api
│ └── routes  # API endpoints
|   ├── users.py
│   ├── venues.py
|   ├── events.py
|   └── rsvps.py
│
├── db
│ ├── queries  # Database queries
│ │ ├── users.py
| | ├── venues.py
| | ├── events.py
| | └── rsvps.py
│ ├── connection.py  # Database connection
│ ├── seed.py  # Seed test data
│ └── setup.sql  # Database setup
│
├── data  # Seed data
├── tests 
| ├── test_seed.py
| └── conftest.py
├── utils
│ └── read_json.py
│
├── main.py  # Application entrypoint
└── requirements.txt



## Installation

Requirements:
- Python 3.10+
- PostgreSQL

Clone the repo:

```bash
git clone https://github.com/Jackp325/py-nc-plus-one.git
```

Create the virtual environment, activate it, and install required libraries:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Database Setup

Create a clean local database:

```bash
psql -d postgres -f db/setup.sql
```

`setup.sql` ensures a clean, new database (nc_plus_one).

## Database Connection

Create a local `.env` file using `.env.example` as a template.

Never commit database credentials to GitHub. Ensure `.env` is included in `.gitignore`.

To connect to the database, run:

```bash
psql -d nc_plus_one
```

## Seed the database

To populate the database with data, run:

```bash
python -m db.seed
```

`seed.py`:
* Removes any data from previous runs
* Rebuilds the table schemas
* Inserts fresh test data

Tables must be dropped and recreated in an order that respects foreign key dependencies.

## How to test

Tests can be run using:

```bash
python -m pytest
```