import cv2 as cv
import numpy as np
import pytesseract as tess
from PIL import Image

img = cv.imread('D:\\app\\github\\DQN_play_sekiro\\imgs\\self_blood=111 next_self_blood=111 boss_blood=168 next_boss_blood=168 action=long_attack reward=2.jpg')
cv.imshow('img', img)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
cv.imshow('bin', binary)
kernel = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))
open_out = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)
cv.imshow('open', open_out)

cv.bitwise_not(open_out, open_out)
cv.imshow('open_out', open_out)
text_img = Image.fromarray(open_out)
text = tess.image_to_string(text_img, 'chi_sim')
print('text:', text)
cv.waitKey(0)