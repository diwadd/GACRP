import support_functions as sf

from custom_logger import logger

if __name__ == "__main__":
    logger.info(" --- In main --- ")

    filename = "trimmed_train.csv"
    # filename = "train.csv"
    # filename = "test.csv"
    raw_data = sf.read_csv_file(filename)

    feature_names_table, feature_values_table = sf.process_raw_data(raw_data)

    sf.save_feature_values_table_as_csv_file(feature_names_table,
                                             feature_values_table,
                                             "processed_features.csv")