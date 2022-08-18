# Exercises with dbt to practice data management
This repository is intended as a playground of practicing data management.

It contains the entire setup one might need to load data in a postgres database,
execute dbt and understand the concepts of **auditability**, **traceability** and **reproducibility**.

# How to setup

1. Install docker desktop. Please pay attention to the installation steps according to your OS.
2. `git clone git@github.com:acirtep/data-management-exercises-dbt.git`
3. `cd data-management-exercises-dbt`
4. `docker-compose up --build`

Now you should be able to have 2 services running:
1. dbt_dm_app: this is the service running the dbt docs (at http://localhost:8080) and the python application
2. dbt_dm_pg: this is the service running the postgres database

## Connecting to the python service

`docker exec -it dbt_dm_app bash`

Now you will be in the terminal of the dbt_dm_app container and be able to run:
- python
- ipython
- dbt

### Execute the initial load in raw

```
root@96315e004081:/app/data_management_exercises# ipython
Python 3.9.5 (default, Jun 23 2021, 15:10:59) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.33.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from load_raw.load_user_data import initial_load_raw_user_data

In [2]: initial_load_raw_user_data()

```

### Execute the initial load in the integration layer

```
root@96315e004081:/app/data_management_exercises# dbt run --full-refresh --model event_user_signup
12:27:16  Running with dbt=1.2.0
12:27:17  Found 1 model, 11 tests, 0 snapshots, 0 analyses, 475 macros, 0 operations, 0 seed files, 0 sources, 0 exposures, 0 metrics
12:27:17  
12:27:17  Concurrency: 1 threads (target='dev')
12:27:17  
12:27:17  1 of 1 START incremental model dev_schema.event_user_signup .................... [RUN]
12:27:18  1 of 1 OK created incremental model dev_schema.event_user_signup ............... [SELECT 25 in 0.83s]
12:27:18  
12:27:18  Finished running 1 incremental model in 0 hours 0 minutes and 1.65 seconds (1.65s).
12:27:18  
12:27:18  Completed successfully
12:27:18  
12:27:18  Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1
```

### Execute the incremental load in raw

```
root@96315e004081:/app/data_management_exercises# ipython
Python 3.9.5 (default, Jun 23 2021, 15:10:59) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.33.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from load_raw.load_user_data import load_updated_data

In [2]: load_updated_data()
```

### Execute the incremental load in the integration layer

```
root@96315e004081:/app/data_management_exercises# dbt run --model event_user_signup
12:28:23  Running with dbt=1.2.0
12:28:23  Found 1 model, 11 tests, 0 snapshots, 0 analyses, 475 macros, 0 operations, 0 seed files, 0 sources, 0 exposures, 0 metrics
12:28:23  
12:28:24  Concurrency: 1 threads (target='dev')
12:28:24  
12:28:24  1 of 1 START incremental model dev_schema.event_user_signup .................... [RUN]
12:28:25  1 of 1 OK created incremental model dev_schema.event_user_signup ............... [INSERT 0 5 in 1.09s]
12:28:25  
12:28:25  Finished running 1 incremental model in 0 hours 0 minutes and 1.78 seconds (1.78s).
12:28:25  
12:28:25  Completed successfully
12:28:25  
12:28:25  Done. PASS=1 WARN=0 ERROR=0 SKIP=0 TOTAL=1
```


## Connecting to the postgres database

Execute `docker exec -it dbt_dm_pg psql -U dbt_user -d dbt_db` and you will be able to run SQL:
```
data-management-exercises-dbt % docker exec -it dbt_dm_pg psql -U dbt_user -d dbt_db
psql (14.0 (Debian 14.0-1.pgdg110+1))
Type "help" for help.

dbt_db=# select dbt_execution_id, dbt_inserted_datetime, count(*) from dev_schema.event_user_signup group by 1,2 order by 2 desc;
           dbt_execution_id           |     dbt_inserted_datetime     | count 
--------------------------------------+-------------------------------+-------
 94f9c3f5-aa69-487b-a52d-8b85f1043a76 | 2022-08-18 12:28:25.123057+00 |     5
 305f8642-73a3-4c12-9d4e-34c0c8f33bfd | 2022-08-18 12:27:18.536066+00 |    25
(2 rows)

```

## Auditability
The act of loading the data in such a way that both the data and the process can be part of an audit.
It also helps in impact analysis, debugging and quality control.

