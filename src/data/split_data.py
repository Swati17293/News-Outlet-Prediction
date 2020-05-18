import pandas as pd
import os
from sklearn.model_selection import train_test_split

def main():

    train_data_path_tmp = 'data/raw/train_tmp.csv'
    train_data_path = 'data/raw/Train.csv'
    test_data_path = 'data/raw/Test.csv'
    valid_data_path = 'data/raw/Valid.csv'

    df = pd.read_csv("data/raw/dataset.csv")
    train_tmp, valid = train_test_split(df, test_size=0.1, random_state=81)
    train_tmp.to_csv (train_data_path_tmp, header=False, index=False)
    valid.to_csv (valid_data_path, header=False, index=False)

    df = pd.read_csv("data/raw/train_tmp.csv")
    train, test = train_test_split(df, test_size=0.1, random_state=81)
    train.to_csv (train_data_path, header=False, index=False)
    test.to_csv (test_data_path, header=False, index=False)

    os.remove("data/raw/train_tmp.csv")
    

if __name__ == "__main__":
    main()