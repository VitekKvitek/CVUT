import csv
from tqdm import tqdm
import os

old_csv_file = "TCCD_bg.csv"
new_csv_file = "TCCD_all_bg.csv"
source_folder = r"D:\vita\car_data_set\resource\TCCPD_filtered_bbox_checked"


def bg(bg_info):


    with open(old_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        old_csv_list = list(csvreader)

    file_list = os.listdir(source_folder)
    for file_name in tqdm(file_list):

        for row in old_csv_list:

            if row[0] == file_name:
                row.append(bg_info)

    for row in tqdm(old_csv_list):

        with open(new_csv_file, mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(row)


def switch_name():


    with open(old_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        old_csv_list = list(csvreader)

    for row in tqdm(old_csv_list):
        new_row = [0]
        new_row[0] = row[4]
        new_row.extend(row[:4])

        with open(new_csv_file, mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(new_row)


def delete_nobg():
    
    
    new_list = []
    
    with open(old_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        old_csv_list = list(csvreader)
    
    for row in tqdm(old_csv_list):
        if len(row) == 6:
            new_list.append(row)
    
    print(new_list)
    for row in tqdm(new_list):
        with open(new_csv_file, mode="a", newline="") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",")
            csv_writer.writerow(row)

delete_nobg()