from db_research.research_inserts import run_inserts_tests
from db_research.research_selects import run_selects_tests
from db_research.service.mongo_utils import fill_mongo
from db_research.service.postgres_utils import fill_postgres_db


def run_pg_mongo_tests():
    fill_mongo()
    fill_postgres_db()
    run_selects_tests()
    run_inserts_tests()


if __name__ == "__main__":
    try:
        run_pg_mongo_tests()
    except Exception as ex:
        print(f'Error {ex}')