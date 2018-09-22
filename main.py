import pandas as pd
import numpy as np


if __name__ == "__main__":

    print("In main")
    # m = np.loadtxt("processed_features.csv")

    m = pd.read_csv("processed_features.csv")
    print(m)

