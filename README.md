# Local Setup for PostgreSQL

### Step 1: Install PostgreSQL (Linux)

Open your terminal and run the following commands to install PostgreSQL:

```bash
$ sudo apt update
$ sudo apt install -y postgresql postgresql-contrib
$ sudo systemctl start postgresql.service
```

###Step 2: Create Database and User

Switch to the PostgreSQL user and open the PostgreSQL command-line interface:
```bash
$ sudo su postgres
$ psql
```
Now, execute the following SQL commands to create your database and user:
```bash
CREATE DATABASE {{DB_NAME}};
CREATE USER {{DB_USER}} WITH PASSWORD '{{DB_PASSWORD}}';
GRANT ALL PRIVILEGES ON DATABASE {{DB_NAME}} TO {{DB_USER}};
```
#####Replace {{DB_NAME}}, {{DB_USER}}, and {{DB_PASSWORD}} with the actual values found in the db.env file.

##Start script 

```bash 
$ sudo chmod +x scripts/entrypoint.sh
$ 
```