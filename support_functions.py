import csv
import json

import global_constants as gc

from custom_logger import logger


def print_dict(d):
    for key, val in sorted(d.items()):
        logger.info("key: {0} -- value: {1}".format(key, val))


def pass_feature_names_to_dict(feature_names, feature_names_dict):

    nf = len(feature_names)
    if nf in feature_names_dict:
        for i in range(nf):
            feature_names_dict[nf].add(feature_names[i])

    else:
        feature_names_dict[nf] = set()
        for i in range(nf):
            feature_names_dict[nf].add(feature_names[i])


def read_csv_file(filename):

    f = open(filename)
    raw_data = csv.reader(f)
    raw_data = list(raw_data)

    return raw_data


def process_raw_data(raw_data):
    """
    Takes the data from the csv file and converts them into
    a python list.

    :param raw_data:
    :return:
    """

    n = len(raw_data)

    logger.debug("raw_data features: {0}".format(raw_data[0]))

    feature_names_table = []
    feature_values_table = []

    # Different rows have different length. We store the distribution of the lengths.
    number_of_rows_dict = {}
    feature_names_dict = {}
    for i in range(1, n):
        raw_data_row = raw_data[i]
        feature_names, feature_row = process_raw_data_row(raw_data_row)

        nf = len(feature_row)
        if nf in number_of_rows_dict:
            number_of_rows_dict[nf] = number_of_rows_dict[nf] + 1
        else:
            number_of_rows_dict[nf] = 1

        pass_feature_names_to_dict(feature_names, feature_names_dict)

        logger.info("we are at row {0}, number of features {1}".format(i, nf))

        if i == 1:
            feature_names_table = feature_names

        feature_values_table.append(feature_row)

    print_dict(number_of_rows_dict)

    # Print feature_names_dict. Here we would like to also print the number of elements of
    # each value (Every value is a set of features).
    for key, val in sorted(feature_names_dict.items()):
        logger.info(" --- --- --- ")
        logger.info("key: {0} -- len(val): {1}".format(key, len(val)))

        for f in val:
            logger.info(f)


    return feature_names_table, feature_values_table


def process_raw_data_row(raw_data_row):
    """
    Take a row from the original csv file with the data and
    unpacks the row, its json fields, in to a simple python list.

    :param raw_data_row:
    :return:
    """

    def append_to_feature_row(feature_names, feature_row, sub_feature_dict):
        for feature, value in sorted(sub_feature_dict.items()):
            logger.debug("{0} value: {1}".format(feature, value))
            feature_names.append(feature)
            feature_row.append(value)

    # Convert json string to python dict.
    device_dict = json.loads(raw_data_row[gc.RAW_FEATURE_INDEX["device"]])
    geo_network_dict = json.loads(raw_data_row[gc.RAW_FEATURE_INDEX["geoNetwork"]])
    totals_dict = json.loads(raw_data_row[gc.RAW_FEATURE_INDEX["totals"]])
    traffic_source_dict = json.loads(raw_data_row[gc.RAW_FEATURE_INDEX["trafficSource"]])

    adwords_click_info_dict = traffic_source_dict["adwordsClickInfo"]
    traffic_source_dict.pop("adwordsClickInfo", None)

    feature_names = []
    feature_row = []

    logger.debug(" --- raw_data_row contents --- ")
    for feature, index in sorted(gc.RAW_FEATURE_INDEX.items()):
        logger.debug("value of feature {0}: {1}".format(feature, raw_data_row[index]))
        logger.debug(" --- --- --- ")

        if feature != "device" and feature != "geoNetwork" and feature != "totals" and feature != "trafficSource":
            feature_names.append(feature)
            feature_row.append(raw_data_row[index])

    append_to_feature_row(feature_names, feature_row, device_dict)
    append_to_feature_row(feature_names, feature_row, geo_network_dict)
    append_to_feature_row(feature_names, feature_row, totals_dict)
    append_to_feature_row(feature_names, feature_row, traffic_source_dict)
    append_to_feature_row(feature_names, feature_row, adwords_click_info_dict)

    logger.debug("feature name: {0}".format(feature_names))
    logger.debug("feature row: {0}".format(feature_row))

    return feature_names, feature_row


def save_feature_values_table_as_csv_file(feature_names_table,
                                          feature_values_table,
                                          filename):

    with open(filename, "w") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL)
        w.writerow(feature_names_table)

        n = len(feature_values_table)
        for i in range(n):
            # logger.info("Writing row {0}".format(i))
            w.writerow(feature_values_table[i])