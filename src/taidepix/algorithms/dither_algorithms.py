import numpy as np
from PIL import Image
import random

class DitherAlgorithms:
    @staticmethod
    def floyd_steinberg(img: Image.Image) -> Image.Image:
        print("Floyd-Steinberg dithering .... ")
        arr = np.array(img, dtype=np.float32)
        h, w = arr.shape
        for y in range(h):
            for x in range(w):
                old_pixel = arr[y, x]
                new_pixel = 0 if old_pixel < 128 else 255
                arr[y, x] = new_pixel
                quant_error = old_pixel - new_pixel
                if x + 1 < w:
                    arr[y, x + 1] += quant_error * 7 / 16
                if y + 1 < h and x > 0:
                    arr[y + 1, x - 1] += quant_error * 3 / 16
                if y + 1 < h:
                    arr[y + 1, x] += quant_error * 5 / 16
                if y + 1 < h and x + 1 < w:
                    arr[y + 1, x + 1] += quant_error * 1 / 16
        arr = np.clip(arr, 0, 255)
        return Image.fromarray(arr.astype(np.uint8), mode='L')

    @staticmethod
    def simple_threshold(img: Image.Image, threshold=128) -> Image.Image:
        print("Simple thresholding .... ")
        arr = np.array(img)
        arr = np.where(arr < threshold, 0, 255)
        return Image.fromarray(arr.astype(np.uint8), mode='L')

    @staticmethod
    def random_dither(img: Image.Image) -> Image.Image:
        print("Random dithering .... ")
        arr = np.array(img)
        noise = np.random.randint(0, 256, arr.shape)
        arr = np.where(arr + noise/2 < 128, 0, 255)
        return Image.fromarray(arr.astype(np.uint8), mode='L')

    @staticmethod
    def ordered_dither(img: Image.Image) -> Image.Image:
        print("Ordered dithering .... ")
        bayer = np.array([[ 0, 48, 12, 60, 3, 51, 15, 63],
                          [32, 16, 44, 28, 35, 19, 47, 31],
                          [ 8, 56, 4, 52, 11, 59, 7, 55],
                          [40, 24, 36, 20, 43, 27, 39, 23],
                          [ 2, 50, 14, 62, 1, 49, 13, 61],
                          [34, 18, 46, 30, 33, 17, 45, 29],
                          [10, 58, 6, 54, 9, 57, 5, 53],
                          [42, 26, 38, 22, 41, 25, 37, 21]])
        bayer = bayer / 64.0 * 255
        arr = np.array(img)
        h, w = arr.shape
        for y in range(h):
            for x in range(w):
                threshold = bayer[y % 8, x % 8]
                arr[y, x] = 0 if arr[y, x] < threshold else 255
        return Image.fromarray(arr.astype(np.uint8), mode='L')

    @staticmethod
    def atkinson(img: Image.Image) -> Image.Image:
        print("Atkinson dithering .... ")
        arr = np.array(img, dtype=np.float32)
        h, w = arr.shape
        for y in range(h):
            for x in range(w):
                old_pixel = arr[y, x]
                new_pixel = 0 if old_pixel < 128 else 255
                arr[y, x] = new_pixel
                quant_error = (old_pixel - new_pixel) / 8
                for dx, dy in [(1,0),(2,0),(-1,1),(0,1),(1,1),(0,2)]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < w and 0 <= ny < h:
                        arr[ny, nx] += quant_error
        arr = np.clip(arr, 0, 255)
        return Image.fromarray(arr.astype(np.uint8), mode='L')

    @staticmethod
    def burkes(img: Image.Image) -> Image.Image:
        print("Burkes dithering .... ")
        arr = np.array(img, dtype=np.float32)
        h, w = arr.shape
        for y in range(h):
            for x in range(w):
                old_pixel = arr[y, x]
                new_pixel = 0 if old_pixel < 128 else 255
                arr[y, x] = new_pixel
                quant_error = old_pixel - new_pixel
                for dx, dy, factor in [
                    (1,0,8/32),(2,0,4/32),
                    (-2,1,2/32),(-1,1,4/32),(0,1,8/32),(1,1,4/32),(2,1,2/32)
                ]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < w and 0 <= ny < h:
                        arr[ny, nx] += quant_error * factor
        arr = np.clip(arr, 0, 255)
        return Image.fromarray(arr.astype(np.uint8), mode='L')

    @staticmethod
    def sierra(img: Image.Image) -> Image.Image:
        print("Sierra dithering .... ")
        arr = np.array(img, dtype=np.float32)
        h, w = arr.shape
        for y in range(h):
            for x in range(w):
                old_pixel = arr[y, x]
                new_pixel = 0 if old_pixel < 128 else 255
                arr[y, x] = new_pixel
                quant_error = old_pixel - new_pixel
                for dx, dy, factor in [
                    (1,0,5/32),(2,0,3/32),
                    (-2,1,2/32),(-1,1,4/32),(0,1,5/32),(1,1,4/32),(2,1,2/32),
                    (-1,2,2/32),(0,2,3/32),(1,2,2/32)
                ]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < w and 0 <= ny < h:
                        arr[ny, nx] += quant_error * factor
        arr = np.clip(arr, 0, 255)
        return Image.fromarray(arr.astype(np.uint8), mode='L')

    @staticmethod
    def jjn(img: Image.Image) -> Image.Image:
        print("JJN dithering .... ")
        arr = np.array(img, dtype=np.float32)
        h, w = arr.shape
        for y in range(h):
            for x in range(w):
                old_pixel = arr[y, x]
                new_pixel = 0 if old_pixel < 128 else 255
                arr[y, x] = new_pixel
                quant_error = old_pixel - new_pixel
                for dx, dy, factor in [
                    (1,0,7/48),(2,0,5/48),
                    (-2,1,3/48),(-1,1,5/48),(0,1,7/48),(1,1,5/48),(2,1,3/48),
                    (-2,2,1/48),(-1,2,3/48),(0,2,5/48),(1,2,3/48),(2,2,1/48)
                ]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < w and 0 <= ny < h:
                        arr[ny, nx] += quant_error * factor
        arr = np.clip(arr, 0, 255)
        return Image.fromarray(arr.astype(np.uint8), mode='L')

    @staticmethod
    def stucki(img: Image.Image) -> Image.Image:
        print("Stucki dithering .... ")
        arr = np.array(img, dtype=np.float32)
        h, w = arr.shape
        for y in range(h):
            for x in range(w):
                old_pixel = arr[y, x]
                new_pixel = 0 if old_pixel < 128 else 255
                arr[y, x] = new_pixel
                quant_error = old_pixel - new_pixel
                for dx, dy, factor in [
                    (1,0,8/42),(2,0,4/42),
                    (-2,1,2/42),(-1,1,4/42),(0,1,8/42),(1,1,4/42),(2,1,2/42),
                    (-2,2,1/42),(-1,2,2/42),(0,2,4/42),(1,2,2/42),(2,2,1/42)
                ]:
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < w and 0 <= ny < h:
                        arr[ny, nx] += quant_error * factor
        arr = np.clip(arr, 0, 255)
        return Image.fromarray(arr.astype(np.uint8), mode='L')
