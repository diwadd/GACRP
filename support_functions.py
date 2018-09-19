import csv
import json
import logging

import global_constants as gc

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(gc.LOGGING_LEVEL)


def read_csv_file(filename):

    f = open(filename)
    raw_data = csv.reader(f)
    raw_data = list(raw_data)

    return raw_data


def process_raw_data(raw_data):

    n = len(raw_data)

    logger.debug("raw_data features: {0}".format(raw_data[0]))

    features_table = []
    for i in range(1, n):
        logger.info("we are at row {0}".format(i))
        raw_data_row = raw_data[i]
        feature_name, feature_row = process_raw_data_row(raw_data_row)

    features_table.append(feature_row)


def process_raw_data_row(raw_data_row):

    def append_to_feature_row(feature_name, feature_row, sub_feature_dict):
        for feature, value in sorted(sub_feature_dict.items()):
            logger.debug("{0} value: {1}".format(feature, value))
            feature_name.append(feature)
            feature_row.append(value)

    device_dict = convert_json_string_to_dict(raw_data_row[gc.RAW_FEATURE_INDEX["device"]])
    geo_network_dict = convert_json_string_to_dict(raw_data_row[gc.RAW_FEATURE_INDEX["geoNetwork"]])
    totals_dict = convert_json_string_to_dict(raw_data_row[gc.RAW_FEATURE_INDEX["totals"]])
    traffic_source_dict = convert_json_string_to_dict(raw_data_row[gc.RAW_FEATURE_INDEX["trafficSource"]])

    adwords_click_info_dict = traffic_source_dict["adwordsClickInfo"]
    traffic_source_dict.pop("adwordsClickInfo", None)

    feature_name = []
    feature_row = []

    logger.debug(" --- raw_data_row contents --- ")
    for feature, index in sorted(gc.RAW_FEATURE_INDEX.items()):
        logger.debug("value of feature {0}: {1}".format(feature, raw_data_row[index]))
        logger.debug(" --- --- --- ")

        if feature != "device" and feature != "geoNetwork" and feature != "totals" and feature != "trafficSource":
            feature_name.append(feature)
            feature_row.append(raw_data_row[index])

    append_to_feature_row(feature_name, feature_row, device_dict)
    append_to_feature_row(feature_name, feature_row, geo_network_dict)
    append_to_feature_row(feature_name, feature_row, totals_dict)
    append_to_feature_row(feature_name, feature_row, traffic_source_dict)
    append_to_feature_row(feature_name, feature_row, adwords_click_info_dict)

    logger.debug("feature name: {0}".format(feature_name))
    logger.debug("feature row: {0}".format(feature_row))

    return feature_name, feature_row

def convert_json_string_to_dict(json_string):
    d = json.loads(json_string)
    return d
