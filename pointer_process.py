import cv2
import math


# k = 0


def draw_line(line, src_img):
    flag = False
    sum_x1 = 0
    sum_y1 = 0
    sum_x2 = 0
    sum_y2 = 0
    if line is not None:
        flag = True
        # print(f'line_num={len(line)}')
        for i in range(0, len(line)):
            rho = line[i][0][0]
            theta = line[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            sum_x1 += x1
            sum_y1 += y1
            sum_x2 += x2
            sum_y2 += y2
            # cv2.line(src_img, (x1, y1), (x2, y2), (255, 0, 0), 3, cv2.LINE_AA)
        sum_x1 = sum_x1 // len(line)
        sum_y1 = sum_y1 // len(line)
        sum_x2 = sum_x2 // len(line)
        sum_y2 = sum_y2 // len(line)
        src_img = cv2.cvtColor(src_img, cv2.COLOR_GRAY2BGR)
        cv2.line(src_img, (sum_x1, sum_y1), (sum_x2, sum_y2), (0, 255, 0), 3, cv2.LINE_AA)

    return flag, [[sum_x1, sum_y1], [sum_x2, sum_y2]], src_img


#  可以考虑裁剪长边来增加霍夫的稳定性
def find_lines(pointer_img, show_img, show=False):
    # global k
    lines = []
    line_threshold = 180
    deta = 2  # 搜索步长
    search_num = 90
    assert search_num * deta <= line_threshold, 'search exceed line_threshold'

    # 所有阈值都要细调
    # ret, img_ = cv2.threshold(img, 170, 205, cv2.THRESH_TRUNC + cv2.THRESH_OTSU)
    # cv2.imshow("erosion", img)
    # if cv2.waitKey(1) == ord('q'):
    #     return False, [[0, 0], [0, 0]]
    # k += 1
    # cv2.imwrite(f'pointer{k}.jpg', pointer_img)
    src_pointer_img = pointer_img.copy()
    pointer_img = cv2.cvtColor(pointer_img, cv2.COLOR_BGR2GRAY)

    pointer_img = cv2.GaussianBlur(pointer_img, (3, 3), 0)

    _, thres = cv2.threshold(pointer_img, 100, 255, cv2.THRESH_OTSU)

    # opening = cv2.morphologyEx(thres, cv2.MORPH_OPEN, (5, 5), iterations=10)

    img_erode = cv2.erode(thres, (5, 5), iterations=5)

    # test = cv2.Canny(test, 160, 205)
    img_blur2 = cv2.GaussianBlur(img_erode, (5, 5), 0)

    img_canny = cv2.Canny(img_blur2, 160, 205)

    img_blur3 = cv2.GaussianBlur(img_canny, (3, 3), 0)

    for i in range(search_num):  # 霍夫可变阈值
        lines = cv2.HoughLines(img_blur3, 1, math.pi / 180, line_threshold)  # 线的阈值要调
        if lines is None:
            line_threshold -= deta
            # print(line_threshold)
        elif len(lines) >= 1:
            # print(len(lines))
            break

    flag, xy, img_target = draw_line(lines, img_blur3)
    # cv2.imshow("pointer", img_target)
    while show:
        src_showimg = cv2.resize(show_img, (0, 0), fx=0.3, fy=0.3)
        cv2.imshow("src_img", src_showimg)
        cv2.imshow("pointer", img_erode)
        cv2.imshow('img_canny', img_canny)
        cv2.imshow("pointer-process", img_target)
        cv2.imshow('src_pointer_img', src_pointer_img)

        cv2.imwrite('article_img/1.0.png', src_pointer_img)
        cv2.imwrite('article_img/1.1.png', img_erode)
        cv2.imwrite('article_img/1.2.png', img_canny)
        cv2.imwrite('article_img/1.3.png', img_target)

        if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
            show = False

    # if cv2.waitKey(1) == ord('q'):
    #     return flag, xy
    # print(flag, xy)
    return xy, flag

# img = cv2.imread("./pointer/8.jpg", 0)
# img_erode1 = find_lines(img)
# cv2.imshow("erosion", img_erode1)
# cv2.waitKey(0)

# def nothing(x):
#     pass
#
#
# # 创建窗口
# cv2.namedWindow('Canny')
#
# # 创建滑动条，分别对应Canny的两个阈值
# cv2.createTrackbar('threshold1', 'Canny', 0, 255, nothing)
# cv2.createTrackbar('threshold2', 'Canny', 0, 255, nothing)
#
# while (1):
#
#     # 返回当前阈值
#     threshold1 = cv2.getTrackbarPos('threshold1', 'Canny')
#     threshold2 = cv2.getTrackbarPos('threshold2', 'Canny')
#
#     img_output = cv2.Canny(img, threshold1, threshold2)
#
#     # 显示图片
#     cv2.imshow('original', img)
#     cv2.imshow('Canny', img_output)
#
#     # 空格跳出
#     if cv2.waitKey(1) == ord(' '):
#         break
#
#     # 摧毁所有窗口
# cv2.destroyAllWindows()
