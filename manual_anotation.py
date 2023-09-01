import csv
import os
import cv2
import keyboard
from PIL import Image, ImageDraw, ImageFont


image_folder =r""
csv_file = ""
current_image_index = 0

with open(csv_file, mode="r", newline="") as csvfile:
    csvreader = csv.reader(csvfile)
    header = next(csvreader)
    csv_rows = list(csvreader)

def find_first_not_marked(csv_rows):
    for row in csv_rows:
        if row[6] == "":
            return csv_rows.index(row)
    
    return len(csv_rows) - 1
def update_row_orientation(key, current_image_index, csv_rows):
    label = None
    
    if key == "1":
        label = "left_front"
    elif key == "2":
        label = "front"
    elif key == "3":
        label = "right_front"
    elif key == "4":
        label = "left"
    elif key == "5":
        label = "unspecified"
    elif key == "6":
        label = "right"
    elif key == "7":
        label = "left_back"
    elif key == "8":
        label =  "back"
    elif key == "9":
        label = "right_back"
    else:
        label = "not_a_car"

    csv_rows[current_image_index][6] = label
    
    with open(csv_file, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        header_writer = csv.writer(csvfile, delimiter= ",")

        header_writer.writerow(header)
        csv_writer.writerows(csv_rows)

    return csv_rows

def update_row_bg(key, current_image_index, csv_rows):
    label = None
    if key == "/":
        label = "1"
    else:
        label = "0"

    csv_rows[current_image_index][5] = label
    
    with open(csv_file, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        header_writer = csv.writer(csvfile, delimiter= ",")


        header_writer.writerow(header)
        csv_writer.writerows(csv_rows)

    return csv_rows            
# Function to update displayed image   
def update_image(current_image_index, csv_rows):
    orientation = csv_rows[current_image_index][6]
    bg = csv_rows[current_image_index][5]
    fname = csv_rows[current_image_index][0]
    image_path = os.path.join(image_folder, fname)

    color = (0, 0, 255)  # Red BGR
    font = cv2.FONT_HERSHEY_SIMPLEX

    image = cv2.imread(image_path)

    resized_image = cv2.resize(image, (640, 480))
    h, w, channels = resized_image.shape
    x_coords = int(w/3)
    y_coords = int(h/10)

    bg_y_coords = y_coords + int(h/5)

    cv2.putText(resized_image, orientation, (x_coords, y_coords ), font, 1, color, 2)
    cv2.putText(resized_image, bg, (x_coords, bg_y_coords), font, 1, color, 2)

    cv2.imshow("Image Viewer", resized_image)

# Initial image display

update_image(current_image_index,csv_rows)
while True:
    key = chr(cv2.waitKey(0) & 0xFF)
    if key in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']: 
        csv_rows = update_row_orientation(key, current_image_index, csv_rows)
        if current_image_index < len(csv_rows) - 1:
            current_image_index += 1 
            update_image(current_image_index,csv_rows)
    
    elif key in ['/','*']:
        csv_rows = update_row_bg(key,current_image_index, csv_rows)
        if current_image_index < len(csv_rows) - 1:
            current_image_index += 1 
            update_image(current_image_index,csv_rows)
    
    elif key == '-':
        if current_image_index > 0:
            current_image_index -= 1  
            update_image(current_image_index,csv_rows)
    
    elif key =='+':
        if current_image_index < len(csv_rows) - 1:
            current_image_index += 1 
            update_image(current_image_index,csv_rows)
    
    elif key == '.':
        current_image_index = find_first_not_marked(csv_rows)
        update_image(current_image_index,csv_rows)
    
    # Check if the 'esc' key is pressed to quit the viewer
    elif ord(key) == 27:
        break
    
    print(current_image_index)

# Close all OpenCV windows
cv2.destroyAllWindows()