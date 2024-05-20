## Pointer Reading based on YOLO

#### Intro

This is a novel approach to pointer meter readings. The features are extracted by the target detection model and digital image processing is performed to get the reading value.

We recommend you to use YOLO as the target detection model. Because this repository is based on YOLO inference.



#### Deploy

We provide two types of inference:

- YOLOv5 use onnx (on CPU)
- YOLOv7 use official library (on GPU)
- Porting Code Interface

##### YOLOv5 use onnx

Prepare your model. (Remember to go into the main file and change the model path)

```bash
pip install -r requirements.txt

python main.py
```



##### YOLOv7 use official library 

We have rewritten detect.py from the official Yolov7 library. Move this file (yolov7_detect.py) directly to the official folder, and it will work.

official Yolov7 library: https://github.com/WongKinYiu/yolov7.git



##### Porting Code Interface

You can refer to the yolov5_dnn.py porting interface and apply it to your own project.

