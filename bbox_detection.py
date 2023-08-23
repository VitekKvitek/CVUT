import shutil
import os
from scipy.io import loadmat
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import csv
from tqdm import tqdm
from skimage.metrics import structural_similarity as ssim
class FilesManipulaotr:
    
    
    def __init__(self, source_folder:str, destination_folder:str, csv_file:str) -> None:
    
    
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.csv_file = csv_file
        self.non_regular_folder = r"D:\vita\car_data_set\resource\TCCPD_anomaly"

        with open(self.csv_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            self.rows = list(csvreader)

    
    def calculate_average_color(self,pixel_data, area_size):
        croner_multiplier = 100
    
        outside_of_bbox_r, outside_of_bbox_g, outside_of_bbox_b = 0, 0, 0
        num_pixels = len(pixel_data)
        
        for r, g, b in pixel_data[:-area_size]:
            outside_of_bbox_r += r
            outside_of_bbox_g += g
            outside_of_bbox_b += b
        corner_r, corner_g, corner_b = 0, 0 , 0
        for r, g, b, in pixel_data[-area_size:]:
            corner_r += croner_multiplier * r
            corner_g += croner_multiplier * g
            corner_b += croner_multiplier * b

        total_r = outside_of_bbox_r + corner_r
        total_g = outside_of_bbox_g + corner_g
        total_b = outside_of_bbox_b + corner_b

        average_r = total_r // (num_pixels + croner_multiplier - 1)
        average_g = total_g // (num_pixels + croner_multiplier - 1)
        average_b = total_b // (num_pixels + croner_multiplier - 1)
        
        return average_r + average_g + average_b

    
    def get_bbox_coords(self, file_name):
        
            
        wanted_row = None
        for  row in (self.rows):
            if file_name == row[4]:
                wanted_row = row
        if not wanted_row == None:
            x1 = int(wanted_row[0])
            y1 = int(wanted_row[1])
            x2 = int(wanted_row[2])
            y2 = int(wanted_row[3])
        
            #corner1 = x1,y1
            #corner2 = x2,y2
            return x1,y1,x2,y2
        return None
    #DOES NOT WORK - no bbox details in file_name
    def get_bbox_coords_from_name(self, file_name_list):
        x1 = file_name_list[0] 
        y1 = file_name_list[1]
        x2 = file_name_list[2]
        y2 = file_name_list[3]

        #corner1 = x1,y1
        #corner2 = x2,y2
        return x1,y1,x2,y2

    def copy_files(self):
        
        
        files_to_move = os.listdir(self.source_folder)
        for file_name in files_to_move:
            source_path = os.path.join(self.source_folder, file_name)
            destination_path = os.path.join(self.destination_folder, file_name)

            shutil.copy2(source_path,destination_path)
    

    def filter_by_bg(self):
        
        
        files_to_check = os.listdir(self.source_folder)
        
        image_number = 0
        for file_name in tqdm(files_to_check):
            

            image_number += 1
            
            source_path = os.path.join(self.source_folder, file_name)
            img = Image.open(source_path)
            if img.mode == 'RGB':
                wid, hgt = img.size

                x1,y1,x2,y2 = self.get_bbox_coords(file_name)

                area_size = 20
                top_lef_corner = img.crop((0,0, area_size, area_size))
                top_lef_pixel_data = list(top_lef_corner.getdata())

                bottom_left_corner = img.crop((0,hgt-area_size,area_size,hgt))
                bottom_left_pixel_data = list(bottom_left_corner.getdata())

                bottom_right_corner = img.crop((wid-area_size,hgt-area_size,wid,hgt))
                bottom_right_pixel_data = list(bottom_right_corner.getdata())

                top_right_corner = img.crop((wid-area_size,0,wid,area_size))
                top_right_pixel_data = list(top_right_corner.getdata())



                # Top-stripe area with corners
                top_area = img.crop((0, 0, wid, y1))
                top_pixel_data = list(top_area.getdata())

                # left side area
                left_area = img.crop((0, y1, x1, y2))
                left_pixel_data = list(left_area.getdata())

                # Bottom-stripe area with corners
                bottom_area = img.crop((0, y2, wid, hgt))
                bottom_pixel_data = list(bottom_area.getdata())

                # right side area
                right_area = img.crop((x2, y1, wid, y2))
                right_pixel_data = list(right_area.getdata())
                
                corner_pixel_data = []
                corner_pixel_data.extend(top_pixel_data)
                corner_pixel_data.extend(left_pixel_data)
                corner_pixel_data.extend(bottom_pixel_data)
                corner_pixel_data.extend(right_pixel_data)
                corner_pixel_data.extend(top_lef_pixel_data)
                corner_pixel_data.extend(bottom_left_pixel_data)
                corner_pixel_data.extend(bottom_right_pixel_data)
                corner_pixel_data.extend(top_right_pixel_data)
                
                #print (f"checkuju {image_number} {file_name}")
                averege_color = self.calculate_average_color(corner_pixel_data, area_size)
                
                #r+b+g
                if averege_color > 720:
                    destination_path = os.path.join(self.destination_folder, file_name)
                    img.save(destination_path)
                    os.remove(source_path)
                    #print (f"je bily {image_number} {file_name}")
            else:
                destination_path = os.path.join(self.non_regular_folder, file_name)
                img.save(destination_path)
                os.remove(source_path)

                #print (f"           {file_name} je non regular")


    def filter_by_bbox(self):
        
        
        #print("funkce jede")
        
        files_to_check = os.listdir(self.source_folder)
        image_number = 0
        
        for file_name in tqdm(files_to_check):
            
            #print (f"for jede {image_number}")
            image_number += 1

            source_path = os.path.join(self.source_folder, file_name)
            img = Image.open(source_path)
            
            wid, hgt = img.size
            area = wid * hgt
            area_1percent = area /100

            x1,y1,x2,y2 = self.get_bbox_coords(file_name)
            edge_factor = 50
            #print(x1,y1,x2,y2)
            if x1 >= wid/edge_factor and x2 <= wid-wid/edge_factor and y1 >= hgt/edge_factor and y2 <= hgt-hgt/edge_factor:
                #print(" prvni prosel ")
                bbox_area = (x2-x1)*(y2-y1) 
                bbox_percent_area = bbox_area/area_1percent
                
                if bbox_percent_area >= 30 and bbox_percent_area <= 85:
                    destination_path = os.path.join(self.destination_folder, file_name)
                    img.save(destination_path)
                    #print(f"{file_name} prosel")


    def reverse_filter_by_bbox(self):
            
            
        files_to_check = os.listdir(self.source_folder)
        
        for file_name in tqdm(files_to_check):
    

            source_path = os.path.join(self.source_folder, file_name)
            img = Image.open(source_path)
            
            wid, hgt = img.size
            area = wid * hgt
            area_1percent = area /100

            x1,y1,x2,y2 = self.get_bbox_coords(file_name)
            edge_factor = 50

            bbox_area = (x2-x1)*(y2-y1) 
            bbox_percent_area = bbox_area/area_1percent

            if not( x1 >= wid/edge_factor and x2 <= wid-wid/edge_factor and y1 >= hgt/edge_factor and y2 <= hgt-hgt/edge_factor):
                destination_path = os.path.join(self.destination_folder, file_name)
                img.save(destination_path)
                
            elif not (bbox_percent_area >= 30 and bbox_percent_area <= 85):
                destination_path = os.path.join(self.destination_folder, file_name)
                img.save(destination_path)
                


    def draw_bbox(self):
       
       
        print("funkce jede")
        
        files_to_draw_in = os.listdir(self.source_folder)
        image_number = 0
        
        for file_name in files_to_draw_in:
            print (f"for jede {image_number}")
            image_number += 1

            source_path = os.path.join(self.source_folder, file_name)
            img = Image.open(source_path)

            x1,y1,x2,y2 = self.get_bbox_coords(file_name)
            rectangle_coords = [(x1, y1), (x2, y2)]

            draw = ImageDraw.Draw(img)
            draw.rectangle(rectangle_coords, outline='red')
            
            destination_path = os.path.join(self.destination_folder, file_name)
            img.save(destination_path)
            print(f"{file_name} done")


    def check_duplicates(self):
        file_list = os.listdir(self.source_folder)
        #previous_car_model = file_list[0].split("_")
        #previous_car_model = previous_car_model[:2]
        last_index_used = 0

        same_car = []
        same_car_pixel_array = []

        new_model = True

        image_number = 0

        while not last_index_used == (len(file_list)-1) :
 

            for name in file_list[last_index_used:]:
                car_model = name.split("_")
                car_model = car_model[:2]
                
                image_number +=1
                print(image_number)

                if new_model:
                    previous_car_model = car_model
                    same_car = [name]
                    last_index_used = file_list.index(name)
                    same_car_pixel_array = [0]
                    new_model = False
                elif car_model == previous_car_model:
                    previous_car_model = car_model
                    last_index_used = file_list.index(name)
                    same_car.append(name)
                    same_car_pixel_array.append(0)
                else:
                    new_model = True
                    last_index_used = file_list.index(name)
                    break
            for index,image in enumerate(same_car):
                image_path = os.path.join(self.source_folder, image)
                img = Image.open(image_path)
                img = img.convert("L")
                same_car_pixel_array[index] = np.array(img)
                img.close()
            
            car_copy_list = []
            for i in range (len(same_car_pixel_array)):
                for j in range(i+1, len(same_car_pixel_array)):

                    ssi_index = ssim(same_car_pixel_array[i], same_car_pixel_array[j])
                    
                    if ssi_index >= 0.98 and not same_car[j] in car_copy_list:
                        car_copy_list.append(same_car[j])

            for name in car_copy_list:
                        source_path = os.path.join(self.source_folder, name)
                        destination_path = os.path.join(self.destination_folder, name)
                        shutil.copy2(source_path, destination_path)
                        os.remove(source_path)

TCCPD_test = FilesManipulaotr(r"D:\vita\car_data_set\resource\TCCPD_filtered_bbox_checked", #source
                            r"D:\vita\car_data_set\resource\TCCPD_filtered_bbox_checked_duplicants", #destination
                            "TCCPD.csv") 

TCCPD_test.check_duplicates()

