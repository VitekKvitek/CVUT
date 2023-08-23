import csv
import os
import cv2
import keyboard

source_folder =r"D:\vita\car_data_set\resource\source_test"
file_list = os.listdir(source_folder)
#converts to absolute paths
absolute_paths = [os.path.join(source_folder, file_name) for file_name in file_list]
csv_file = "test.csv"

with open(csv_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            csv_rows = list(csvreader)



current_image_index = 0
def update_row(key, file_name):
    for index, row in enumerate(csv_rows):
        if file_name in row:
             pass
# Function to update the displayed image   
def update_image():
    global current_image_index
    image = cv2.imread(absolute_paths[current_image_index])
    cv2.imshow("Image Viewer", image)

# Initial image display
print(absolute_paths[0])
update_image()

while True:
    key = cv2.waitKey(0) & 0xFF

    # Check if the 'n' key is pressed for the next image
    if key == ord('w') or key == ord('a') or key == ord('s') or key == ord('d'):
        current_image_index = (current_image_index + 1) % len(absolute_paths)
        update_image()

        data = [file_list[current_image_index],chr(key)]
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(data)
    # Check if the 'p' key is pressed for the previous image
    elif key == ord('p'):
        current_image_index = (current_image_index - 1) % len(absolute_paths)
        update_image()
        print("Previous image")

    # Check if the 'esc' key is pressed to quit the viewer
    elif key == 27:
        break

# Close all OpenCV windows
cv2.destroyAllWindows()