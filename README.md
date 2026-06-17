## Database Setup

To create a clean local database, run:

```bash
psql -d postgres -f db/setup.sql
```

To connect to the database, run:

psql -d nc_plus_one

## Database Connection

Create a local `.env` file containing your database credentials.

Use the `.env.example` file as a reference.

Credentials should not be committed directly to connection.py