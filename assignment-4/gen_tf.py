#!/usr/bin/env python3

import os
import argparse
from random import randint

MIN = 0
MAX = 1000
DIR = "tracefiles"


def create_tf() -> str:
    os.makedirs(DIR, exist_ok=True)
    filenum = len(os.listdir(DIR))
    return os.path.join(DIR, "tf_" + str(filenum) + ".csv")

# add main()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--count", required=True, type=int)
    args = parser.parse_args()
    count = args.count

    with open(create_tf(), "w") as tf:
        for i in range(0, count):
            tf.write(f"insert,{randint(MIN, MAX)}\n")
        tf.write("dump")