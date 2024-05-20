import time
import cv2
import numpy as np

from yolov5_dnn import mult_test, user_detect


def detect_interface(img: np.ndarray) -> float:
    if isinstance(img, np.ndarray):
        num = user_detect(img)
        print(f'\nnum is {num}\n')
        return num
    else:
        print('class error')


# Use yolov5 onnx example to show this pointer reading process
# It use cpu to infer
# If you want use gpu, you need to prepare .pt file
# And you need to port the recognition interface using the official library detect.py
# Here is a yolov7 official library detect.py example: yolov7_detect_pointer.py, in this folder
# You need to put it in the official library folder to run. (https://github.com/WongKinYiu/yolov7.git)

if __name__ == "__main__":
    onnx_path = r'weights/test_yolov5n.onnx'
    input_path = r'./test'
    save_path = r'./output'
    # video=True means use video to detect
    s = time.time()

    mult_test(onnx_path, input_path, save_path, video=False)

    # src_img = cv2.imread('input_image/spin.jpg', 1)
    # detect_interface(src_img)

    e = time.time()

    print(f'cost={(e - s) * 1000 / 21}ms')

    # if srcimg is not None:
    #     srcimg = model.detect(srcimg)
