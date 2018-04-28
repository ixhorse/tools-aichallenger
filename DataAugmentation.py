import numpy as np
import os
import sys
from PIL import Image, ImageOps, ImageEnhance
import random
import time
from scipy import misc
import matplotlib.pyplot as plt
import cv2
import threading
from threading import Thread
from multiprocessing import Process
from math import ceil, pi, sin, cos

def PCA_Jittering(img):
    img = np.asanyarray(img, dtype='float32')

    img = img / 255.0
    img_size = img.size / 3
    img1 = img.reshape(int(img_size), 3)
    img1 = np.transpose(img1)
    img_cov = np.cov([img1[0], img1[1], img1[2]])
    lamda, p = np.linalg.eig(img_cov)

    p = np.transpose(p)

    alpha1 = random.normalvariate(0, 3)
    alpha2 = random.normalvariate(0, 3)
    alpha3 = random.normalvariate(0, 3)

    v = np.transpose((alpha1 * lamda[0], alpha2 * lamda[1], alpha3 * lamda[2]))
    add_num = np.dot(p, v)

    img2 = np.array([img[:, :, 0] + add_num[0], img[:, :, 1] + add_num[1], img[:, :, 2] + add_num[2]])

    img2 = np.swapaxes(img2, 0, 2)
    img2 = np.swapaxes(img2, 0, 1)
    img2 = (img2 - np.min(img2)) / (np.max(img2) - np.min(img2)) * 255
    return Image.fromarray(np.uint8(img2))

def randomColor(img):
    """
    对图像进行颜色抖动
    :param image: PIL的图像image
    :return: 有颜色色差的图像image
    """
    random_factor = np.random.randint(0, 20) / 10.  # 随机因子
    color_image = ImageEnhance.Color(img).enhance(random_factor)  # 调整图像的饱和度
    random_factor = np.random.randint(5, 15) / 10.  # 随机因子
    brightness_image = ImageEnhance.Brightness(color_image).enhance(random_factor)  # 调整图像的亮度
    random_factor = np.random.randint(5, 15) / 10.  # 随机因子
    contrast_image = ImageEnhance.Contrast(brightness_image).enhance(random_factor)  # 调整图像对比度
    random_factor = np.random.randint(0, 20) / 10.  # 随机因子
    return ImageEnhance.Sharpness(contrast_image).enhance(random_factor)  # 调整图像锐度

def randomGaussian(image, mean=0.2, sigma=0.3):
    """
    对图像进行高斯噪声处理
    :param image:
    :return:
    """

    def gaussianNoisy(im, mean=0.2, sigma=0.3):
        """
        对图像做高斯噪音处理
        :param im: 单通道图像
        :param mean: 偏移量
        :param sigma: 标准差
        :return:
        """
        for _i in range(len(im)):
            im[_i] += random.gauss(mean, sigma)
        return im

    # 将图像转化成数组
    img = np.asarray(image)
    img.flags.writeable = True  # 将数组改为读写模式
    width, height = img.shape[:2]
    img_r = gaussianNoisy(img[:, :, 0].flatten(), mean, sigma)
    img_g = gaussianNoisy(img[:, :, 1].flatten(), mean, sigma)
    img_b = gaussianNoisy(img[:, :, 2].flatten(), mean, sigma)
    img[:, :, 0] = img_r.reshape([width, height])
    img[:, :, 1] = img_g.reshape([width, height])
    img[:, :, 2] = img_b.reshape([width, height])
    return Image.fromarray(np.uint8(img))

def gaussianBlur(img, kernel_size = (5,5), sigma = 0.5):
    """
    高斯模糊
    """
    sigma = np.random.randint(0, 20) / 10
    img = np.asarray(img)
    img = cv2.GaussianBlur(img, kernel_size, sigma)
    return Image.fromarray(np.uint8(img))

def radialTransform(img, out_path):
    """
    极坐标
    """
    img = np.asarray(img)
    for i in range(10):
        for j in range(10):
            img_out = np.zeros(img.shape)
            u = 44 * i
            v = 44 * j
            for m in range(224):
                for r in range(224):
                    theta = 2 * pi * m / 224.0
                    x = u + int(round(r * cos(theta)))
                    y = v + int(round(r * sin(theta)))
                    if x>=0 and x<224 and y>=0 and y<224:
                        img_out[m, r, :] = img[x, y, :]
            save_path = out_path[:-4] + '_radial_' + str(10*i+j) + '.jpg'
            misc.imsave(save_path, img_out)


def worker(dir_list, out_list):
    func_list = [PCA_Jittering, randomColor, gaussianBlur]
    for i in range(len(dir_list)):
        path = dir_list[i]
        print(path)
        for root, dirs, files in os.walk(path):
            for file_name in files:
                t = time.clock()
                if (file_name[-4:] != '.jpg'):
                    continue
                img_path = os.path.join(root, file_name)
                img = Image.open(img_path).resize((224, 224), Image.ANTIALIAS)
                path_out = os.path.join(out_list[i], file_name)
                try:
                    radialTransform(img, path_out)
                except:
                    pass
                print(time.clock() - t)
                # for j in range(len(func_list)):
                #     try:
                #         img_new = func_list[j](img)
                #     except:
                #         print(file_name)
                #     save_name = file_name[:-4] + '_aug_' + str(j) + '.jpg'
                #     save_path = os.path.join(out_list[i], save_name)
                #     try:
                #         misc.imsave(save_path,img_new)
                #     except:
                #         pass
                # plt.imshow(img_new)
                # plt.show()

def main():
    if len(sys.argv) == 2:
        superclass = sys.argv[1]
    else:
        print('Parameters error')
        exit()

    data_path = './trainval_' + superclass + '/train/'
    out_path = './trainval_' + superclass + '/train_radial/'
    record = []
    core = 8

    path_list = [os.path.join(data_path, s) for s in os.listdir(data_path)]
    out_list = [os.path.join(out_path, s) for s in os.listdir(data_path)]

    if not os.path.exists(out_path):
        os.mkdir(out_path)
    for path in out_list:
        if not os.path.exists(path):
            os.mkdir(path)

    length = len(path_list)
    temp = ceil(length / core)
    for i in range(core):
        start = i * temp
        end = (i+1) * temp if (i+1)*temp < length else length
        if(start > end):
            continue
        process = Process(target=worker, args=(path_list[start:end], out_list[start:end]))
        process.start()
        record.append(process)

    for process in record:
        process.join()

if __name__ == '__main__':
    # path1 = "./trainval_Animals/train/A_ant/02abe662644a6bf6bd45e96d4b6955ca.jpg"
    # path2 = './trainval_Animals/train_radial/A_ant/02abe662644a6bf6bd45e96d4b6955ca.jpg'
    # img = Image.open(path1).resize((224, 224), Image.ANTIALIAS)
    # radialTransform(img, path2)
    main()