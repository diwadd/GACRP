import logging

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

    # sf.process_raw_data_row(raw_data[1])
    # sf.process_raw_data_row(raw_data[2])
    # sf.process_raw_data_row(raw_data[3])

    # d = sf.convert_json_string_to_dict(raw_data[1][2].replace("\\", "\\\\"))

    sf.process_raw_data(raw_data)