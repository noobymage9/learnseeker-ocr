import cv2 as cv
import numpy as np
from scipy import ndimage

LEFT_DETECT = 1
GROW = 2
# Smaller size -> separate process
def preprocess(image, zone_type = None):
  image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
  image = binarise(image)
  image = skew_correct(image)
  image = denoise(image)
  # if (bool(zone_type)):
  #   image = zone(image, zone_type)
  return image


def binarise(image):
  threshold, binarized = cv.threshold(image, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
  return binarized

def skew_correct(image):
  cannied = cv.Canny(image, 50, 200, None, 3)
  angle_resolution = np.pi / 180
  vote_threshold = 180
  distance_resolution = 1
  lines = cv.HoughLines(cannied, distance_resolution, angle_resolution, vote_threshold)
  skew_angles = []
  if lines is not None:
    for line in lines:
        theta = line[0][1]
        dev_from_hrzntal_in_rad = np.pi / 2 - theta 
        dev_from_hrzntal_in_deg = dev_from_hrzntal_in_rad / np.pi * 180
        if (abs(dev_from_hrzntal_in_deg) < 10):
            skew_angles.append(dev_from_hrzntal_in_deg)
            
  if len(skew_angles) != 0:
    deskew_angle = sum(skew_angles) / len(skew_angles)
    return ndimage.rotate(image, -deskew_angle)
  else:
    return image

def denoise(image):
  aperture_size = 5
  return cv.medianBlur(image, aperture_size)

def zone(image, zone_type):
  rects = initial_zones_of(image)
  if zone_type == LEFT_DETECT:
    rects = left_detect(rects)
  elif zone_type == GROW:
    rects = grow(rects, 1)
  return rects
  

def initial_zones_of(image):
  contours, hier = cv.findContours(cv.bitwise_not(denoised_image), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  rects = []
  for c in contours:
    x, y, w, h = cv.boundingRect(c)
    rects.append((x, y, w, h))
    cv.rectangle(underlay, (x, y), (x + w, y + h), 0, 1)

  # Sort by x coor
  rects.sort(key = lambda x: x[0])
  # For removing encapsulating box if there is
  return list(filter(lambda x: x[0] >= 50 and x[1] >= 50, rects))


def zone_grow(rects, iteration):
  x_thresh = 50
  y_diff = 50

  final_rects = []

  for i in range(iteration):
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
        for internal_index, other_rect in enumerate(rects[(index + 1):], start = (index + 1)):   
          other_left = other_rect[0]
          other_right = other_rect[0] + other_rect[2]
          other_top = other_rect[1]
          other_bottom = other_rect[1] + other_rect[3]
          if ((other_left <= current_right + x_thresh) and (abs(current_top - other_top) <= y_diff or abs(current_bottom - other_bottom) <= y_diff)):
            current_right = other_right
            current_top = min(current_top, other_top)
            current_bottom = max(current_bottom, current_bottom)
            used_rects[internal_index] = True

        final_rects.append([current_left, current_top, current_right - current_left, current_bottom - current_top])
  return final_rects

  def left_detect(rects):
    lowest_x = min(x for (x,y,w,h) in rects if w > 10 and h > 10)
    highest_x = max(x+w for (x,y,w,h) in temp_rects)
    highest_y = max(y+h for (x,y,w,h) in temp_rects)
    question_num_idx = rects.index([rect for rect in rects if lowest_x in rect][0])
    left_most_rect = rects[question_num_idx]
    del rects[question_num_idx]
    question_num_rects = [left_most_rect]
    while(True):
      next_lowest_x = min(x for (x,y,w,h) in rects if w > 10 and h > 10)
      next_left_most_rect_idx = rects.index([rect for rect in rects if next_lowest_x in rect][0])
      next_left_most_rect = rects[next_left_most_rect_idx]
      if next_left_most_rect[0] - left_most_rect[0] <= 15:
        del rects[next_left_most_rect_idx]
        question_num_rects.append(next_left_most_rect)
      else:
        break;
    question_num_rects.sort(key = lambda x: x[1])
    question_crops = []
    for idx, question_num_rect in enumerate(question_num_rects):
      try:
        next_rect = question_num_rects[idx+1]
      except Exception as e:
        print(f'Error message: {e}')
        cv.rectangle(underlay, (question_num_rect[0] - 5, (question_num_rect[1] - 5)), 
                 (highest_x, highest_y), 0, 1)
        question_crops.append(underlay[(question_num_rect[1] - 5):highest_y, (question_num_rect[0] - 5):highest_x])
        break;
        
    question_crops.append(underlay[(question_num_rect[1] - 5):(next_rect[1] - 50), (question_num_rect[0] - 5):highest_x])
    return question_crops

