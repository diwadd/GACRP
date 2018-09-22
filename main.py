import logging

import numpy as np

import support_functions as sf
import global_constants as gc

logger = logging.getLogger(__name__)

file_handler = logging.FileHandler("logs.log")
file_handler.setLevel(gc.LOGGING_LEVEL)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")

handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(file_handler)
logger.setLevel(gc.LOGGING_LEVEL)


if __name__ == "__main__":
    logger.info(" --- In main --- ")

    filename = "trimmed_train.csv"
    raw_data = sf.read_csv_file(filename)

    logger.debug("features: {0}".format(raw_data[0]))

    feature_names_table, feature_values_table = sf.process_raw_data(raw_data)

    logger.info("Feature names {0}\n".format(feature_names_table))
    logger.info(feature_values_table[0])
    logger.info(feature_values_table[1])

    sf.save_feature_values_table_as_csv_file(feature_names_table,
                                             feature_values_table,
                                             "processed_features.csv")