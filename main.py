import global_constants as gc

from custom_logger import logger


def compare_features_between_test_and_train_data(train_features, test_features):

    logger.info("Check train vs test features...")
    for key, val in sorted(train_features.items()):
        if key not in test_features:
            logger.info("{0} is not present in test features but is present in train set".format(key))

    logger.info("Check test vs train features...")
    for key, val in sorted(test_features.items()):
        if key not in train_features:
            logger.info("{0} is not present in train features but is present in test set".format(key))


if __name__ == "__main__":
    train_features = gc.TRAIN_FEATURE_INDEX
    test_features = gc.TEST_FEATURE_INDEX
    compare_features_between_test_and_train_data(train_features, test_features)