import argparse


def getbase():
    p = argparse.ArgumentParser()
    p.add_argument("--base", type=str, help="Directory base of data folder")
    args = p.parse_args()
    basedir = args.base
    return basedir
