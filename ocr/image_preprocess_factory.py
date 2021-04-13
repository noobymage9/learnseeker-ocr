import cv2 as cv
import numpy as np
import copy
from scipy import ndimage

# Skew Correction
CANNY_THRESHOLD_1 = 50
CANNY_THRESHOLD_2 = 200
CANNY_APERTURE_SIZE = 3
HOUGH_ANGLE_RESOLUTION = np.pi / 180
HOUGH_VOTE_THRESHOLD = 180
HOUGH_DISTANCE_RESOLUTION = 1
DEV_FROM_HRZ_IN_DEG = 10

# Denoise
MEDIAN_BLUR_APERTURE_SIZE = 5

# Zone
MINIMAL_RECT_SIZE = 10
MINIMAL_RECT_X = 10
MINIMAL_RECT_Y = 10

# Left Detect
LEFT_RECT_DIFF_THRESHOLD = 20
QUESTION_BLK_MARGIN = 5

# Grow
GROW_ITERATION = 10
X_THRESH = 50
Y_DIFF = 50

# Rectangles are in x, y, w, h
# Image crop are in y:y+h, x:x+w

# Smaller size -> separate process
def preprocess(image):
  image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
  image = binarise(image)
  image = skew_correct(image)
  image = denoise(image)
  return image

def binarise(image):
  threshold, binarized = cv.threshold(image, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
  return binarized

def skew_correct(image):
  cannied = cv.Canny(image, CANNY_THRESHOLD_1, CANNY_THRESHOLD_2, None, CANNY_APERTURE_SIZE)
  lines = cv.HoughLines(cannied, HOUGH_DISTANCE_RESOLUTION, HOUGH_ANGLE_RESOLUTION, HOUGH_VOTE_THRESHOLD)
  skew_angles = []
  if lines is not None:
    for line in lines:
        theta = line[0][1]
        dev_from_hrzntal_in_rad = np.pi / 2 - theta 
        dev_from_hrzntal_in_deg = dev_from_hrzntal_in_rad / np.pi * 180
        if (abs(dev_from_hrzntal_in_deg) < DEV_FROM_HRZ_IN_DEG):
            skew_angles.append(dev_from_hrzntal_in_deg)
            
  if len(skew_angles) != 0:
    deskew_angle = sum(skew_angles) / len(skew_angles)
    return ndimage.rotate(image, -deskew_angle)
  else:
    return image

def denoise(image):
  return cv.medianBlur(image, MEDIAN_BLUR_APERTURE_SIZE)
  
def zone(image, zone_type):
  images = []
  rects = initial_zones_of(image)

  if zone_type == "LEFT_DETECT":
    rects = left_detect(rects, image)
  elif zone_type == "GROW":
    rects = zone_grow(rects, GROW_ITERATION)
  else:
    rects = rects
  rects = remove_corrupted(rects)
  rects.sort(key = lambda x: x[1])
  print("FINAL RECTS")
  display(rects)
  for rect in rects:
    images.append(image[rect[1]:rect[1] + rect[3], rect[0]:rect[0] + rect[2]])
  return images


def initial_zones_of(image):
  height, width = image.shape
  # Remove black border from deskewing
  contours, hier = cv.findContours(cv.bitwise_not(image[20:height -20, 20:width - 20].copy()), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  rects = []
  for c in contours:
    x, y, w, h = cv.boundingRect(c)
    rects.append((x, y, w, h))
  # Sort by x coor
  rects.sort(key = lambda x: x[0])
  # Ignore rects from noise, missed by denoise
  return remove_corrupted(rects)

def left_detect(rects, image):
  print("ALL RECTS")
  display(rects)
  lowest_x = min(x for (x,y,w,h) in rects)
  height, width = image.shape
  question_num_idx = rects.index([rect for rect in rects if lowest_x in rect][0])
  left_most_rect = rects[question_num_idx]
  del rects[question_num_idx]
  question_num_rects = [left_most_rect]
  while(True):
    next_lowest_x = min(x for (x,y,w,h) in rects)
    next_left_most_rect_idx = rects.index([rect for rect in rects if next_lowest_x in rect][0])
    next_left_most_rect = rects[next_left_most_rect_idx]
    if next_left_most_rect[0] - left_most_rect[0] <= LEFT_RECT_DIFF_THRESHOLD:
      del rects[next_left_most_rect_idx]
      question_num_rects.append(next_left_most_rect)
    else:
      break;
  question_num_rects.sort(key = lambda x: x[1])
  rects = []
  print("CAPTURED QN NUM BLOCK")
  display(question_num_rects)
  for idx, question_num_rect in enumerate(question_num_rects):
    try:
      next_rect = question_num_rects[idx+1]
    except Exception as e:
      print(f'Error message: {e}')
      rects.append([question_num_rect[0] - QUESTION_BLK_MARGIN, question_num_rect[1] - QUESTION_BLK_MARGIN, width - question_num_rect[0], 
               height - question_num_rect[1]])
      break;
    rects.append([question_num_rect[0] - QUESTION_BLK_MARGIN, question_num_rect[1] - QUESTION_BLK_MARGIN, width - question_num_rect[0], 
              next_rect[1] - QUESTION_BLK_MARGIN - question_num_rect[1]])
  print("AFTER CAPTURE")
  display(rects)
  return rects

def zone_grow(rects, iteration):

  final_rects = []

  for i in range(iteration):
    # print(f'Iteration {i}')
    # display(rects)
    # print()
    if len(final_rects) != 0:
      rects = copy.deepcopy(final_rects) 
    used_rects = [False for rect in rects] 
    final_rects = []

    for index, rect in enumerate(rects):
     
      if (used_rects[index] == False):
        current_left = rect[0]
        # x + width
        current_right = rect[0] + rect[2]
        
        current_top = rect[1]
        # y + height
        current_bottom = rect[1] + rect[3]

        used_rects[index] = True
        
        # All other rects
        for internal_index, other_rect in enumerate(rects):
          if index == internal_index or used_rects[internal_index] == True:
            continue   
          other_left = other_rect[0]
          other_right = other_rect[0] + other_rect[2]
          other_top = other_rect[1]
          other_bottom = other_rect[1] + other_rect[3]
          if ((other_left <= current_right + X_THRESH) and (abs(current_top - other_top) <= Y_DIFF or abs(current_bottom - other_bottom) <= Y_DIFF)):
            current_right = max(current_right, other_right)
            current_top = min(current_top, other_top)
            current_bottom = max(current_bottom, other_bottom)
            used_rects[internal_index] = True
            break

        final_rects.append([current_left - QUESTION_BLK_MARGIN, current_top - QUESTION_BLK_MARGIN, current_right + 2 * QUESTION_BLK_MARGIN - current_left, current_bottom + 2 * QUESTION_BLK_MARGIN - current_top])
  # rects, weights = cv.groupRectangles(final_rects, 0, 0.5)
  # Remove duplicates
  print("Removed Overlapped")
  display(rects)
  print("Removed dupes")
  rects = set(map(tuple, rects))
  return rects

def remove_overlap(rects):
  rects.sort(key = lambda x: x[1])
  while(True):
    temp = []
    exist = False
    for outer_idx, current_rect in enumerate(rects):
      final_x = current_rect[0]
      final_y = current_rect[1]
      final_w = current_rect[2]
      final_h = current_rect[3]
      for inner_idx, other_rect in enumerate(rects):
        if outer_idx == inner_idx:
          continue
        if overlap(current_rect, other_rect):
          print("TRUE")
          exist = True
          final_w = max(other_rect[0] + other_rect[2], current_rect[0] + current_rect[2]) - current_rect[0]
          final_h = max(other_rect[1] + other_rect[3], current_rect[1] + current_rect[3]) - current_rect[1]
          temp.append([final_x, final_y, final_w, final_h])
          break
      if exist == False:
        temp.append([final_x, final_y, final_w, final_h])
    if exist == False:
      break
    else:
      rects = temp
  return rects

def overlap(rect_a, rect_b):
  print(f'Rectangle A: {rect_a}')
  print(f'Rectangle B: {rect_b}')
  print()
  if rect_a[0] >= (rect_b[0] + rect_b[2]) or rect_b[0] >= (rect_a[0] + rect_a[2]):
    return False
  if rect_a[1] >= (rect_b[1] + rect_b[3]) or rect_b[1] >= (rect_a[1] + rect_a[3]):
    return False
  return True

def display(rects):
  for rect in rects:
    print(f'{rect[0]}, {rect[1]}, {rect[2]}, {rect[3]}')

def remove_corrupted(rects):
  return list(filter(lambda rect: rect[0] > MINIMAL_RECT_X and rect[1] > MINIMAL_RECT_Y and rect[2] > MINIMAL_RECT_SIZE and rect[3] > MINIMAL_RECT_SIZE, rects))