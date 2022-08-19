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

### ipython

```


```

### Execute dbt
```

```

## Connecting to the postgres database

Execute `docker exec -it dbt_dm_pg psql -U dbt_user -d dbt_db` and you will be able to run SQL:
```
data-management-exercises-dbt % docker exec -it dbt_dm_pg psql -U dbt_user -d dbt_db
psql (14.0 (Debian 14.0-1.pgdg110+1))
Type "help" for help.

dbt_db=# select dbt_execution_id, dbt_inserted_timestamp, count(*) from integration_layer.fact_user_registration group by 1,2 order by 2;
           dbt_execution_id           |    dbt_inserted_timestamp     | count 
--------------------------------------+-------------------------------+-------
 52f445a2-66f2-4947-abfd-e54a7a3cbfb4 | 2022-08-19 12:20:45.964459+00 |    25
 19bd3ff6-6179-408a-8a45-4ae751b10598 | 2022-08-19 12:33:00.227058+00 |     5

```

## Auditability

The act of loading the data in such a way that both the data and the process can be part of an audit.
It also helps in impact analysis, debugging and quality control.

Article available at: .
