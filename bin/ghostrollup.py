import argparse


from grollup import rollup


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',
                        '--input')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
