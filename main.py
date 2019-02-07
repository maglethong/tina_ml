import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlrd
import pickle
import os
from typing import List

import data as data_reader


# Func defs


def deserialize(path) -> List[data_reader.Columns]:
    print("Deserializing data")
    with open(path, "rb") as f:
        return pickle.loads(f.read())


def serialize(path, content: List[data_reader.Columns]):
    print("Serializing data")
    serialized = pickle.dumps(content)
    with open(path, "wb") as f:
        f.write(serialized)


file = "data\\Diabetes_HR_für_Markus2.xlsm"
serializedFile = "data\\serialized.bin"

# Read data
data = ''
if os.path.exists(serializedFile):
    data = deserialize(serializedFile)
else:
    data = data_reader.Columns().read_excel(file)
    serialize(serializedFile, data)


def plot(file, data: List[data_reader.Columns]):
    plt.plot()

    for index, (x, y, color) in enumerate(data):
        plt.scatter(x, y, alpha=0.5, c=color, s=3)
        # if index > 500:
        #    break

    plt.savefig(file)
    plt.show()


def ogtt_result_color_picker(ogtt_result):
    if ogtt_result == 1:
        return 'green'
    elif ogtt_result == 4:
        return 'red'
    else:
        return 'orange'


def normalize(data: List[data_reader.Columns], attributes: List[str]):
    if attributes.__sizeof__() < 2:
        print("At least 2 attributes!")
        return

    max = data_reader.Columns()
    min = data_reader.Columns()

    # Find Max/Min
    for attr in attributes:
        max.__setattr__(attr, data[0].__getattribute__(attr))
        min.__setattr__(attr, data[0].__getattribute__(attr))

    for item in data:
        for attr in attributes:
            v = item.__getattribute__(attr)
            if max.__getattribute__(attr) < v:
                max.__setattr__(attr, v)
            elif min.__getattribute__(attr) > v:
                min.__setattr__(attr, v)

    # Normalize
    for item in data:
        for attr in attributes:
            old = item.__getattribute__(attr)
            mi = min.__getattribute__(attr)
            ma = max.__getattribute__(attr)
            new = (old - mi) / (ma - mi)
            item.__setattr__(attr, new)


def dist(a: data_reader.Columns, b: data_reader.Columns, attributes: List[str]) -> float:
    if attributes.__sizeof__() < 2:
        print("At least 2 attributes!")
        return -1

    sum = 0.0
    for attr in attributes:
        v1 = a.__getattribute__(attr)
        v2 = b.__getattribute__(attr)
        sum += (v1 + v2) * (v1 + v2)

    return sum.__pow__(1 / attributes.__sizeof__())
    # TODO Idea: Other dist calculation (non euclidean)


def knn(item: data_reader.Columns, data: List[data_reader.Columns], k: int=3) -> int:
    return item.ogtt_result  # TODO calc
# TODO Idea: k com pesos
# big K => less noise sensitive
# small K => more precise

def run_and_evaluate(data: List[data_reader.Columns]):
    # only first sample (last result from each person)
    data = list(filter(lambda x: x.sample_number == 1, data))

    attributes = [
        's01_chylo_a',
        's02_chylo_b',
        's03_chylo_rem',
        's04_vldl_a',
        's05_vldl_b',
        's06_idl',
        's07_idl_a',
        's08_idl_b',
        's09_idl_c',
        's10_idl_d',
        's11_idl_e',
        's12_hdl_a',
        's13_hdl_b',
        's14_hdl_c',
        's15_hdl_d'
    ]
    normalize(data, attributes)


    knn(data[0], data, 3)

    print(dist(data[0], data[1], attributes))


# plot_data = list(filter(lambda x: x.sample_number == 1, data))

# plot_data = list(map(lambda x: (x.weight, x.height, ogtt_result_color_picker(x.ogtt_result)), plot_data))

# plot('.\\data\\out\\test.png', plot_data)

run_and_evaluate(data)

