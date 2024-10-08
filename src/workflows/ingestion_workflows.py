"""Pipeline for ingesting the data into the vector store."""

import logging
import sys

from dotenv import load_dotenv

sys.path.append("./src")

from utils.load_configuration import load_yaml_configuration
from models.data_ingester import DataIngester
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    config_path = "./configs/configuration.yaml"
    config = load_yaml_configuration(config_path)
    data_ingester = DataIngester(config)
    data_ingester.initialize_elements()
    data_ingester.ingest_data()


if __name__ == "__main__":
    main()
