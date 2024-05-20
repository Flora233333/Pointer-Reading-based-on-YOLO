import cv2
import math
from detect_obj import DetectObj
import numpy as np

from pointer_process import find_lines


def find_center(xy1, xy2, x_hat):
    k = (xy1[1] - xy2[1]) / (xy1[0] - xy2[0] + 0.1)  # 防止除0
    b = xy1[1] - k * xy1[0]
    center = [x_hat, int(k * x_hat + b)]
    return center


def raw2process(show_img, src_img, center_nut, pointer, start):
    xy = []
    show = False
    err = False

    # 简单的一个根据图片大小自动匹配绘图函数线的粗细(tl为thickness的参数)
    tl = round(0.002 * (src_img.shape[0] + src_img.shape[1]) / 2) + 1

    center = [center_nut.center_x, center_nut.center_y]
    bias = 0  # 需修正的参数

    # if src_img is None:
    #     return src_img

    pointer_img = src_img[pointer.y1:pointer.y2, pointer.x1:pointer.x2]

    if pointer_img is not None:
        xy, flag = find_lines(pointer_img, show_img, show)
        if flag is False or xy == [[0, 0], [0, 0]]:
            err = True
    else:
        err = True

    if err:
        print('Warning: detect pointer line err')
        return show_img, 0

    # print(xy)
    # print(pointer.xy)

    xy[0][0] += pointer.x1  # pointer_img -> src_img 检测指针直线坐标修正
    xy[0][1] += pointer.y1
    xy[1][0] += pointer.x1
    xy[1][1] += pointer.y1


    if start[0].xy_is_zero() or start[1].xy_is_zero(): # 根据检测的情况选择不同的算法
        center = find_center(xy[0], xy[1], center_nut.center_x)
    else:
        center = find_center(xy[0], xy[1], center_nut.center_x)
    # center = [center_nut.center_x, center_nut.center_y]
    # center = [center_nut.center_x, center_nut.center_y]
    # pointer[0] = src_img.shape[1] / 2 - 1000  # 重新标定指针
    # pointer[1] = find_center(xy[0], center, src_img.shape[1] / 2 - 1000)[1] + bias

    # 选择相信目标检测的中点
    # cv2.circle(show_img, (pointer.center_x, pointer.center_y), 10, color=(0, 0, 255), thickness=-1)

    # 这个是用霍夫直线解算出的中点
    # pointer.center_x = (xy[0][0] + xy[1][0]) // 2
    # pointer.center_y = (xy[0][1] + xy[1][1]) // 2
    # cv2.circle(src_img, (pointer.center_x, pointer.center_y), 10, color=(0, 0, 255), thickness=-1)

    # point[0] = xy[0][0]  # 重新修正
    # point[1] = xy[0][1]

    # while center[0] > src_img.shape[0] or center[1] > src_img.shape[1]:
    #     center[0] = center[0] // 2
    #     center[1] = center[1] // 2
    # print(f'center = {center}, center_nut = {center_nut}')

    if center[0] > src_img.shape[1] or center[1] > src_img.shape[0]:
        print('Warning: center xy excess img range')
        return show_img, 0


    cv2.line(show_img, (start[0].center_x, start[0].center_y), (center[0], center[1]), (0, 255, 0), tl,
             lineType=cv2.LINE_AA)  # left start
    cv2.line(show_img, (start[1].center_x, start[1].center_y), (center[0], center[1]), (0, 255, 0), tl,
             lineType=cv2.LINE_AA)  # right start

    cv2.line(show_img, (pointer.center_x, pointer.center_y), (center[0], center[1]), (0, 255, 0), tl,
             lineType=cv2.LINE_AA)  # 画指针线
    cv2.circle(show_img, (start[0].center_x, start[0].center_y), 5, color=(0, 0, 255), thickness=-1)
    cv2.circle(show_img, (start[1].center_x, start[1].center_y), 5, color=(0, 255, 255), thickness=-1)
    # cv2.line(show_img, (start[0].center_x, start[0].center_y), (start[1].center_x, start[1].center_y), (0, 255, 0), tl,
    #          lineType=cv2.LINE_AA)

    # cv2.circle(show_img, ((start[0].center_x + start[1].center_x) // 2, (start[0].center_y + start[1].center_y) // 2),
    #            10, color=(0, 0, 255), thickness=-1)

    fix_center_nut_y = center_nut.center_y - bias  # 修正后的中心y坐标

    # cv2.line(src_img, (point[0], point[1]), (center_nut[0], fix_center_nut_y), (0, 255, 0), 5)  # 画指针线

    # cv2.line(show_img, (center[0], 0), (center[0], src_img.shape[0]), (255, 255, 0), 5, lineType=cv2.LINE_AA)  # 中心y轴
    # cv2.line(show_img, (0, center[1]), (src_img.shape[1], center[1]), (255, 255, 0), 5, lineType=cv2.LINE_AA)  # 中心x轴

    a = math.radians(90)  # 旋转到左边-0.1 (-45度)
    r_x = (center[0] - center[0]) * math.cos(a) - (center[1] - src_img.shape[0]) * math.sin(-a) + \
          center[0]
    r_y = (center[0] - center[0]) * math.sin(-a) + (center[1] - src_img.shape[0]) * math.cos(a) + \
          src_img.shape[0]

    # -45度线
    # cv2.line(show_img, (center[0], center[1]), (int(r_x), int(r_y)), (255, 255, 0), 5, lineType=cv2.LINE_AA)

    b = math.radians(90)  # 旋转到右边0.9 (-45度)
    r_x = (center[0] - center[0]) * math.cos(b) - (center[1] - src_img.shape[0]) * math.sin(b) + \
          center[0]
    r_y = (center[0] - center[0]) * math.sin(b) + (center[1] - src_img.shape[0]) * math.cos(b) + \
          src_img.shape[0]

    # print(r_x, r_y)

    # +45度线
    # cv2.line(show_img, (center[0], center[1]), (int(r_x), int(r_y)), (255, 255, 0), 5, lineType=cv2.LINE_AA)

    # 待改善读数精度
    # print(center)

    # print(a, b)
    # print(f'beta={beta * 180 / math.pi}')

    # print(f'center = {center[0], center[1]}')
    # print(f'pointer = {pointer[0], pointer[1]}')

    k_pointer = -(center[1] - pointer.center_y) / (center[0] - pointer.center_x + 0.1)  # +0.1防止除0

    k_start = (center[1] - start[0].center_y) / (center[0] - start[0].center_x + 0.1)  # 防止除0
    b_start = start[0].center_y - k_start * start[0].center_x

    loc_pointer_x = (pointer.center_y - b_start) / (k_start + 0.1)  # 防止除0

    num_by_angle = 0

    if loc_pointer_x > pointer.center_x:  # 判断点在直线左边还是右边
        a = [start[0].center_x - center[0], start[0].center_y - center[1]]  # start向量
        b = [pointer.center_x - center[0], pointer.center_y - center[1]]  # 指针向量
        beta = math.acos(  # ab=|a||b|cos(a)
            (a[0] * b[0] + a[1] * b[1]) / (math.sqrt(a[0] ** 2 + a[1] ** 2) * math.sqrt(b[0] ** 2 + b[1] ** 2)))
        num_by_angle = beta / math.radians(270) * 1 - 0.1
    else:
        a = [start[1].center_x - center[0], start[1].center_y - center[1]]  # start向量
        b = [pointer.center_x - center[0], pointer.center_y - center[1]]  # 指针向量
        beta = math.acos(  # ab=|a||b|cos(a)
            (a[0] * b[0] + a[1] * b[1]) / (math.sqrt(a[0] ** 2 + a[1] ** 2) * math.sqrt(b[0] ** 2 + b[1] ** 2)))
        num_by_angle = 0.9 - (beta / math.radians(270) * 1)

    # print('k_pointer = %f' % k_pointer)

    eps = math.radians(45) - math.atan(k_pointer)  # (180 - 98) / 2
    ra = 1 / math.radians(270)
    num_by_k = ra * eps - 0.1

    # num_by_angle = beta / math.radians(270) * 1 - 0.1

    print(f'num = {num_by_k}')
    print(f'num by angle = {num_by_angle}')
    # 下面还可以变更(如差在一定范围类取加权,超过范围取最小值)
    # avg = 0.3 * num_by_k + 0.7 * num_by_angle
    # print(f'avg = {avg}')

    cv2.putText(show_img, f'num={num_by_angle:.3f}', (pointer.center_x, pointer.center_y + 120),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                (250, 132, 5),
                thickness=tl, lineType=cv2.LINE_AA)

    cv2.circle(show_img, (pointer.center_x, pointer.center_y), 5, color=(0, 0, 255), thickness=-1)

    if show:
        detect = cv2.resize(show_img, (0, 0), fx=0.3, fy=0.3)
        cv2.imshow("detect", detect)
        cv2.waitKey(0)

    return show_img, num_by_angle
