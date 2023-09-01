import csv
from tqdm import tqdm
import os


old_csv_file = ""
new_csv_file = ""
source_folder = r""


def bg(bg_info):# anotets all files in folder
    with open(old_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        old_list = list(csvreader)

    file_list = os.listdir(source_folder)

    new_list = old_list
    
    for file_name in tqdm(file_list):
        for index,row in enumerate(old_list):
            if row[0] == file_name:
                new_list[index][5] = bg_info
    
    with open(old_csv_file, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerows(new_list)


def switch_name():# swaps name from 6th positon
    with open(old_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        old_list = list(csvreader)

    new_list = []

    for index,row in tqdm(enumerate(old_list)):
        new_list.append(row)
        new_list[index][0] = row[6]
        new_list[index][1:4] = row[1:4]
        new_list[index][5] = None
        new_list[index][6] = None
   
    with open(new_csv_file, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerows(new_list)

def delete_nobg():# delets info about image which does not have bg anotation
    new_list = []
    
    with open(old_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        old_csv_list = list(csvreader)
    
    for row in tqdm(old_csv_list):
        if row[5] in ["0", "1"]:
            new_list.append(row)
    
    with open(new_csv_file, mode="w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerows(new_list)

def add_column():# adds empty column to the 
    with open(old_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        old_csv_list = list(csvreader)
    
    for row in tqdm(old_csv_list):
        row.append("")
    
    with open(old_csv_file, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerows(old_csv_list)

def new_bg_csv(bg):
    new_list = []
    
    with open(old_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)

        old_csv_list = list(csvreader)

        for row in tqdm(old_csv_list):
            if int(row[5]) == bg:
                new_list.append(row)

    with open(new_csv_file, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerows(new_list)

def rewrite_csv_with_csv(): #highly un-effective
    with open(old_csv_file, 'r') as csvfile:
        csvreader1 = csv.reader(csvfile)
        next(csvreader1)
        old_csv_list = list(csvreader1)
    
    with open(new_csv_file, 'r') as csvfile:
        csvreader2 = csv.reader(csvfile)
        next(csvreader2)
        new_csv_list = list(csvreader2)
    
    for src_row in tqdm(old_csv_list):
        for index,new_row in enumerate(new_csv_list):
            if src_row[0] == new_row[0]:
                new_csv_list[index] = src_row
                break
    
    with open(new_csv_file, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerows(new_csv_list)

def rename_files(start_value): #dont kill for this code, but it just works. It is what is    
    with open(old_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        old_list = list(csvreader)
    new_list = old_list
    name = start_value
    
    for index,row in tqdm(enumerate(old_list)):
        name += 1
        new_list[index][0] = str(name) + ".jpg"
    
    with open(old_csv_file, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerows(new_list)

def delete_in_csv_if_not_in_folder():
    file_list = os.listdir(source_folder)
    
    with open(old_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        old_list = list(csvreader)
    new_list = []
    
    for file_name in tqdm(file_list):
        for row in old_list:
            if file_name == row[0]:
                new_list.append(row)
    
    with open(old_csv_file, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerows(new_list)

def sort_order_by_name(): #not working
    with open(old_csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        old_list = list(csvreader)

    sorted_list = sorted(old_list, key=lambda x: int(x[0][:-4]))
    
    with open(old_csv_file, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerows(sorted_list)
