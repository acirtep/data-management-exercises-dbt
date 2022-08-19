from load_raw.utils import get_pg_conn


if __name__ == "__main__":
    pg_conn = get_pg_conn()
    pg_conn.execute("create schema if not exists raw_layer")
    pg_conn.close()
    