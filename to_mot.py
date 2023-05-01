# before running this script first run "process_bounding_box.py" with
# --save_bbox true
import os
import argparse
import pandas as pd

SESSION_DICT = {
    1: '0800_0830',  # 1 is equivalent to 0800_0830
    2: '0830_0900',  # 2 is equivalent to 0830_0900
    3: '0900_0930',  # 3 is equivalent to 0900_0930
    4: '0930_1000',  # 4 is equivalent to 0930_1000
    5: '1000_1030',  # 5 is equivalent to 1000_1030
}

VEHICLE_TYPE = {
    "Car": 0,
    "Bus": 1,
    "Taxi": 0,
    "Heavy Vehicle": 1,
    "Medium Vehicle": 0,
    "Motorcycle": -1,
}


def csv_to_mot(frame_n: int, anott_file: str):
    df = pd.read_csv(anott_file)
    n = len(df["Type"])
    return pd.DataFrame({
        "frame": [frame_n] * n,
        "id": df["ID"],
        "bb_left": df["cx"] - df["box_w"] / 2,
        "bb_top": df["cy"] - df["box_h"] / 2,
        "bb_width": df["box_w"],
        "bb_height": df["box_h"],
        "conf": [-1] * n,
        "x": [-1] * n,
        "y": [-1] * n,
        "z": [-1] * n,
    })


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some parameters.')
    parser.add_argument('--base_dir', type=str, required=True,
                        help='the directory where the data are located')
    parser.add_argument('--session', type=int, choices=range(1, 6), default=3,
                        help='session number from 1 to 5')
    parser.add_argument('--drone', type=int, choices=range(1, 11), default=6,
                        help='A single drone number from 1 to 10')

    args = parser.parse_args()
    drone = args.drone
    session = args.session
    basedir = args.base_dir

    annot_dir = os.path.join(basedir, "20181029_D{:d}_{}".format(
        drone, SESSION_DICT[session]), "Annotations")
    anott_files = sorted([os.path.join(annot_dir, f) for f in os.listdir(
        annot_dir) if f.endswith("_upright.csv")])

    df = pd.concat([csv_to_mot(n, anott_file)
                   for n, anott_file in enumerate(anott_files, 1)])

    df.to_csv(f"{SESSION_DICT[session]}_D{drone}_mot.txt", header=False, index=False)
