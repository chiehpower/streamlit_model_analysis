# Model Analysis via Streamlit

- Mainly I will apply this library [streamlit-image-comparison](https://github.com/fcakyon/streamlit-image-comparison) this feature. 

- The goal is to use this feature to compare the model detecting results. Then we can easily to compare two of different training conditions.

### Features for this tool

1. It can compare the BBOX between GroundTruth and Detections. 
2. One model detects with different conditions. 
3. It can compare the training results with different hyperparameters. 
4. It can compare the results from different architecture models.
5. In this tool, it will also compute the mAP value. 

---
### Requirements 

- The json of COCO format
- Python >= 3.7 (Cannot support Python 3.6)

---

### Installation

```
pip install streamlit streamlit-image-comparison
pip install cv2 numpy alive_progress scikit-image
```
- **pycocotools** *(Very hard to install) for doing analysis use*

  - you need to install `pip install cython` 
  - Install python-dev by `sudo apt-get install python3-dev`
  - `sudo -H python -m pip install pycocotools==2.0.2 ` (On Linux)

  Do not install the latest version of pycocotools.