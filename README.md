# pNUEMA-Vision-toolbox

This is the repository for utilizing pNEUMA Vision dataset.

## Contents:
- [Dataset Overview](#dataset-overview)
- [Toolbox Overview](#toolbox-overview)
- [Notes on the Dataset](#notes-on-the-dataset)



## Dataset Overview
- This dataset is the expansion of [pNEUMA](https://open-traffic.epfl.ch/) dataset by taking account of imagery parts collected from drones.
- Every 10th frame of the drone videos has been processed with following annotations:
    - **NEW Features (only in pNEUMA Vision)**
        - images of frame
        - vehicle locations (x, y coordinates in image)
        - azimuths (clockwise, x-axis being 0&deg;)
    - **Inherited Features (from pNUEMA)**
        - vehicle ID
        - vehicle type
        - timestamp

- You can download the dataset from the following links: [link](https://doi.org/10.5281/zenodo.7426506)

- If you are using this dataset, please cite the following paper: [paper link](https://doi.org/10.1016/j.trc.2022.103966)

- If you want to contribute to this dataset and repository please contact us at: sohyeong.kim@epfl.ch

    <!-- <details>
    <summary> 2018/10/29 09:00 - 09:30 </summary>

    | Location | Download Link   | 
    |--------|---|
    |  D1 |  TBA |
    | D2 |  TBA |   
    | D3 | TBA   | 
    | D4 |  TBA |   
    | D5 | TBA   | 
    | D6 |  TBA |   
    | D7 | TBA   | 
    | D8 |  TBA |   
    | D9 | TBA   | 
    | D10 |  TBA |   
    </details>
    <details>
    <summary> 2018/10/29 08:00 - 08:30 </summary>

    | Location | Download Link   | 
    |--------|---|
    |  D2 |  TBA |
    | D3 |  TBA |  
    </details>
    <details>
    <summary> 2018/10/29 08:30 - 09:00 </summary>

    | Location | Download Link   | 
    |--------|---|
    |  D2 |  TBA |
    | D3 |  TBA |  
    </details>
    <details>
    <summary> 2018/10/29 09:30 - 10:00 </summary>

    | Location | Download Link   | 
    |--------|---|
    |  D2 |  TBA |
    | D3 |  TBA |  
    </details>
    <details>
    <summary> 2018/10/29 10:00 - 10:30 </summary>

    | Location | Download Link   | 
    |--------|---|
    |  D2 |  TBA |
    | D3 |  TBA |  
    | D8 |  TBA |
    </details> -->



## Toolbox Overview
- This toolbox is a collection of functions that can be used to process bounding boxes for pNEUMA Vision dataset as per in the (paper)[link_here].
- You can create two types of bounding boxes: rotated and axis-aligned.
- Session defines the time interval of the video. Please note the session number like following. 
    - session 1 is equivalent to 08:00 - 08:30
    - session 2 is equivalent to 08:30 - 09:00
    - session 3 is equivalent to 09:00 - 09:30
    - session 4 is equivalent to 09:30 - 10:00
    - session 5 is equivalent to 10:00 - 10:30

- Example usage of the toolbox is given below.
    - **Rotated bounding box**
        ```
        python process_bounding_box.py --base_dir BASE_DIR --drone DRONE_NUM --session SESSION_NUM
        ```
    - **Axis-aligned bounding box**
        ``` 
        python process_bounding_box.py --base_dir BASE_DIR --drone DRONE_NUM --session SESSION_NUM --rotate_bbox
        ```
    - **Save bounding boxes information in a csv file**
    
        The csv file containing bounding box information will be saved in the same directory as the annotations.
        ```
        python process_bounding_box.py --base_dir BASE_DIR --drone DRONE_NUM --session SESSION_NUM --save_bbox
        ```
    - **Turn-off visualization while processing**
        ```
        python process_bounding_box.py --base_dir BASE_DIR --drone DRONE_NUM --session SESSION_NUM --dont_show
        ```

## Notes on the Dataset
- **20181029_D3_0900_0930**
    - Frames #1616 and #1617 are black frames.
- **20181029_D10_0900_0930**
    - Frames #401-#403 and #720-#806 are heavily occluded during the stabilization process due to strong winds.
