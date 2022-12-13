import pandas as pd
import numpy as np
import cv2
import os
import argparse
import bbox_functions

SESSION_DICT = {
            1: '0800_0830',  # 1 is equivalent to 0800_0830
            2: '0830_0900',  # 2 is equivalent to 0830_0900
            3: '0900_0930',  # 3 is equivalent to 0900_0930
            4: '0930_1000',  # 4 is equivalent to 0930_1000
            5: '1000_1030',  # 5 is equivalent to 1000_1030
        }

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process some parameters.')
    parser.add_argument('--base_dir', type=str, required=True,
                        help='the directory where the data are located')
    parser.add_argument('--drone', type=int, choices=range(1,11), default=6,
                        help='A single drone number from 1 to 10')
    parser.add_argument('--session', type=int, choices=range(1,6), default=3,
                        help='session number from 1 to 5')
    parser.add_argument('--rotate_bbox', type=bool, default=False,
                        help='If set, process the rotated bounding box otherwise process the axis-aligned bounding box')
    parser.add_argument('--save_bbox', type=bool, default=False,
                        help='If set, save the bounding box in the same folder as the annotation files')
    parser.add_argument('--dont_show', type=bool, default=False, 
                        help='If set, do not show the bounding box on the image')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    # ----------------------------- #
    inputArgs = parse_arguments()
    basedir = inputArgs.base_dir
    drone = inputArgs.drone
    session = inputArgs.session
    is_rotated_box =  inputArgs.rotate_bbox
    save_bbox_info = inputArgs.save_bbox
    dont_show = inputArgs.dont_show
    # ----------------------------- #

    if not os.path.exists(os.path.join(basedir, "20181029_D{:d}_{}".format(drone, SESSION_DICT[session]))):
        print("The following directory does not exist >>", os.path.join(basedir, "20181029_D{:d}_{}".format(drone, SESSION_DICT[session])))
        exit()

    frame_dir = os.path.join(basedir, "20181029_D{:d}_{}".format(drone, SESSION_DICT[session]), "Frames")
    annot_dir = os.path.join(basedir, "20181029_D{:d}_{}".format(drone, SESSION_DICT[session]), "Annotations")

    # Print the number of files in each directory
    print("Number of frames: {}".format(len(os.listdir(frame_dir))))
    print("Number of annotations: {}".format(len(os.listdir(annot_dir))))

    # Get the list of file basename in the frame directory
    file_names = [os.path.basename(x).split('.')[0] for x in os.listdir(frame_dir)]
    file_names.sort()

    for fname in file_names[:]:

        img = cv2.imread(os.path.join(frame_dir, fname + ".jpg"))
        annot_df = pd.read_csv(os.path.join(annot_dir, fname + ".csv"))
        annot_df = annot_df.loc[annot_df['Type'] != 'Bicycle'].reset_index(drop=True)
        annot_df = annot_df.loc[annot_df['Type'] != 'Undefined'].reset_index(drop=True)
        annot_df = annot_df.loc[annot_df['Type'] != 'Pedestrian'].reset_index(drop=True)

        if is_rotated_box:
            annot_df['p1'] = None
            annot_df['p2'] = None
            annot_df['p3'] = None
            annot_df['p4'] = None
            label = 'rotated'
        else:
            annot_df['cx'] = None
            annot_df['cy'] = None
            annot_df['box_w'] = None
            annot_df['box_h'] = None
            label = 'upright'


        for i in range(len(annot_df)):
            veh_id = annot_df.iloc[i]['ID']
            veh_type = annot_df.iloc[i]['Type']
            veh_x = annot_df.iloc[i]['x_img [px]']
            veh_y = annot_df.iloc[i]['y_img [px]']
            veh_az = annot_df.iloc[i]['Angle_img [rad]']

            box_rect_info = bbox_functions.create_bbox_for_vehicles(veh_type, (veh_x, veh_y), veh_az)
            box_rect_info_within_frame = bbox_functions.adjust_bbox_for_crop(box_rect_info, veh_type,
                                                    (0,0), img.shape[1], img.shape[0],
                                                    intersect_area_threshold= 0.2)
            if box_rect_info_within_frame is not None:
                if is_rotated_box:
                    rotated_box = np.round(box_rect_info_within_frame).astype(int)
                    annot_df.at[i, 'p1'] = rotated_box[0]
                    annot_df.at[i, 'p2'] = rotated_box[1]
                    annot_df.at[i, 'p3'] = rotated_box[2]
                    if len(rotated_box) == 3:
                        annot_df.at[i, 'p4'] = rotated_box[2]
                    else:
                        annot_df.at[i, 'p4'] = rotated_box[3]

                    # For visualization
                    cv2.drawContours(img, [rotated_box], 0, (0, 255, 0), 2)
                    cv2.circle(img, (veh_x, veh_y), radius=5, color=(255, 0, 255), thickness=-1)
                    cv2.putText(img, "Frame: {}".format(fname), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                else:
                    flat_box = cv2.boundingRect(box_rect_info_within_frame.astype(np.float32))
                    xbox, ybox, wbox, hbox = np.round(flat_box).astype(int)
                    annot_df.at[i, 'cx'] = xbox
                    annot_df.at[i, 'cy'] = ybox
                    annot_df.at[i, 'box_w'] = wbox
                    annot_df.at[i, 'box_h'] = hbox

                    # For visualization
                    cv2.rectangle(img, (xbox, ybox), (xbox + wbox, ybox + hbox), (0, 255, 0), 2)
                    cv2.circle(img, (veh_x, veh_y), radius=5, color=(255, 0, 255), thickness=-1)
                    cv2.putText(img, "Frame: {}".format(fname), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        

        if not dont_show:
            if is_rotated_box:
                cv2.imshow("Rotated Bounding box", img)
            else:
                cv2.imshow("Axis-aligned Bounding box", img)

            # if esc is pressed, exit
            if cv2.waitKey(10) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

        if save_bbox_info:
            annot_df.to_csv(os.path.join(annot_dir, fname + "_{}.csv".format(label)), index=False)

   


