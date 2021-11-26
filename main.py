import streamlit as st
from streamlit_image_comparison import image_comparison
import cv2
import os
import json
import numpy as np

st.set_page_config(
    page_title="Streamlit Image Comparison",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <h2 style='text-align: center'>
    Model Visualization Analysis
    </h2>
    """,
    unsafe_allow_html=True,
)

st.write("##")

with st.form(key="Streamlit Image Comparison"):
    # image one inputs
    st.write("Please put the GT and detection json files in the Image folder (at the same folder)")
    img_folder = st.text_input("Dataset folder path:", value="dataset")
    lst_img= os.listdir(img_folder)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        # img1_url = st.text_input("Image one URL:", value=IMAGE_TO_URL["sample_image_1"])
        gt_json = st.text_input("GroundTruth json path:", value="trainval.json")
        gt_json = os.path.join(img_folder, gt_json)
    with col2:
        det_json = st.text_input("Image two text:", value="detection.json")
        det_json = os.path.join(img_folder, det_json)
    with col3:
        img3_text = st.text_input("Image quantity:", value="10", key=int)

    col1, col2 = st.columns([1, 1])
    with col1:
        starting_position = st.slider(
            "Starting position of the slider:", min_value=0, max_value=100, value=50
        )
    with col2:
        width = st.slider(
            "Component width:", min_value=400, max_value=1000, value=700, step=100
        )

    # boolean parameters
    col1, col2, col3, col4 = st.columns([1, 3, 3, 3])
    with col2:
        show_labels = st.checkbox("Show labels", value=True)
    with col3:
        make_responsive = st.checkbox("Make responsive", value=True)
    with col4:
        in_memory = st.checkbox("In memory", value=True)

    # centered submit button
    col1, col2, col3 = st.columns([6, 4, 6])
    with col2:
        submit = st.form_submit_button("Update Render 🔥")

#### ***************************************
### Gt
try :
    with open(gt_json, 'r') as reader:
        jf_gt = json.loads(reader.read())

    images = jf_gt['images']
    annotations = jf_gt['annotations']


    image_list = {}
    for i in images:
        image_list[i['id']] = i['file_name']
except:
    st.error("Cannot find the GT file.")

### Detection
try :
    with open(det_json, 'r') as reader:
        jf_det = json.loads(reader.read())

    images_det = jf_det['images']
    annotations_det = jf_det['annotations']

    image_list_det = {}
    for de in images_det:
        image_list_det[de['id']] = de['file_name']
except:
    st.error("Cannot find the Detection file.")
#### ***************************************

ind = 1

for imgname in lst_img:
    if imgname[-4:] !=".jpg" and imgname[-4:] !=".png" and imgname[-4:] !=".bmp": continue
    
    imgname_location = os.path.join(img_folder, imgname)
    
    st.write(f"{ind}. image name is : ", imgname)

    img = cv2.imread(imgname_location) 
    ori_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gt_image = ori_image.astype(np.uint8).copy()
    det_image = ori_image.astype(np.uint8).copy()

    try:
        for i in annotations:
            img_name = image_list[i['image_id']]

            ### bbox = x1 y1 w h
            if img_name == imgname:
                bbox = i['bbox']
                x1 = int(bbox[0])
                y1 = int(bbox[1])
                x2 = int(bbox[0])+int(bbox[2])
                y2 = int(bbox[1])+int(bbox[3])

                cv2.rectangle(gt_image, (x1, y1), (x2, y2), color=[255, 0, 255], thickness=1)
    except:
        pass

    try:
        for i_det in annotations_det:
            
            img_name_det = image_list_det[i_det['image_id']]
            if img_name_det == imgname:
                ### BBOX
                bbox = i_det['bbox']
                x1 = int(bbox[0])
                y1 = int(bbox[1])
                x2 = int(bbox[0])+int(bbox[2])
                y2 = int(bbox[1])+int(bbox[3])

                cv2.rectangle(det_image, (x1, y1), (x2, y2), color=[255, 0, 255], thickness=1)

                ### Score
                scores = i_det['score']
                str_score = '{0:.2f}'.format(scores)
                print(str_score)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(det_image, str_score, (x1, y2), font, 1, [0, 0, 0], 1, cv2.LINE_AA)
    except:
        pass

    static_component = image_comparison(
        img1=gt_image,
        img2=det_image,
        label1='GT',
        label2='Detection',
        width=width,
        starting_position=starting_position,
        show_labels=show_labels,
        make_responsive=make_responsive,
        in_memory=in_memory,
    )

    ind += 1

    if ind == int(img3_text):
        break