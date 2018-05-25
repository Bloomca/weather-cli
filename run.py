from app import get_city_data
from app.settings import check_keys


if __name__ == "__main__":
  # we can't proceed without API keys
  check_keys()

  get_city_data()
