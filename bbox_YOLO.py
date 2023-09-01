import numpy as np
import os
from tqdm import tqdm # progress bars
import cv2 # computer vision tasks
import glob # files searching, for example speciffic type
import torch # machine learning ?
import torchvision
from einops import rearrange #  reshaping and permuting multi-dimensional arrays or tensors
from torchvision.io import read_video # torch related
from torchvision.utils import flow_to_image, draw_bounding_boxes
from PIL import Image, ImageDraw
import csv #csv file creation, for data storing

class DataLoader():
    def __init__(self, path, transforms=None):
        self.path = path
        self.transforms = transforms
        if os.path.isfile(path) and path[-4:] in [".mp4", ".avi"]:
            # video
            self.type = "video" 
            self.imgs, _, _ = read_video(str(path))
            self.imgs = rearrange(self.imgs, "n h w c -> n c h w")
        elif os.path.isfile(path):
            # single file
            self.type = "file" 
            self.imgs = [path]
        elif os.path.isdir(path):
            # dir of files 
            self.type = "dir" 
            self.imgs = sorted(glob.glob(os.path.join(path, "*.png")))
        else: 
            raise NotImplemented

    def __len__(self):
        if self.type == "video":
            return self.imgs.size(0)
        else:
            return len(self.imgs)

    def __getitem__(self, index):
        if self.type == "video":
            img = self.imgs[index, ...]
        else:
            cvimg = cv2.imread(self.imgs[index])[:,:,::-1]
            img = rearrange(torch.from_numpy(cvimg.copy()), "h w c -> c h w")
        if self.transforms is not None:
            return self.transforms(img)
        return img

def main(params, yolo_net):
    
    out_dir = params["out_dir"]
    image_path = params["image_path"]
    size = params["size"]
    csv_file_name = params["csv_file_name"]
    trash_folder = params["trash_folder"]

    device = "cuda" if torch.cuda.is_available() else "cpu"
    transforms = torchvision.transforms.Compose([ torchvision.transforms.ConvertImageDtype(torch.float32), 
                             torchvision.transforms.Resize(size=size) ])

    yolo_net = yolo_net.to(device)
    dataloader = DataLoader(str(image_path), transforms=transforms)    

    
    for i in range(0, len(dataloader)):
        img1 = dataloader[i].to(device)[None, ...]

        results = yolo_net((255*(img1[0, ...])).cpu().numpy().astype(np.uint8).transpose(1, 2, 0)) 

        x1,y1,x2,y2 = get_bbox_coords(results.xyxy)
        
        if x1 == False:
            copy_to_and_resize(image_path, trash_folder)
            break
        
        copy_to_and_resize(image_path, out_dir)
        write_image_info_to_csv(x1,y1,x2,y2,csv_file_name,image_path)
        break


def write_image_info_to_csv(x1,y1,x2,y2,csv_file_name,image_path):
    last_component = os.path.basename(image_path)
    car_info = last_component.split("_")

    data = [x1,y1,x2,y2,last_component]
    data.extend(car_info)

    with open(csv_file_name, mode="a", newline="") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(data)
    csv_file.close()

def get_bbox_coords(results):
        current_biggest_bbox_area = 0
        for row in results[0]:    
            new_bbox_area = (row[2]-row[0]) * (row[3]-row[1])
            if 2 in row[5] and row[4] > 0.5:
                if current_biggest_bbox_area < new_bbox_area:
                    current_biggest_bbox_area = new_bbox_area
                    current_biggest_bbox = row

        if not current_biggest_bbox_area == 0:
            x1 = int(current_biggest_bbox[0])
            y1 = int(current_biggest_bbox[1])
            x2 = int(current_biggest_bbox[2])
            y2 = int(current_biggest_bbox[3])

            return x1,y1,x2,y2
        else:
            return False,False,False,False
        
def copy_to_and_resize (file_path, output_folder):
    img = Image.open(file_path)
    img = img.resize((640, 480))
    last_component = os.path.basename(file_path)
    destination_path = os.path.join(output_folder, last_component)

    img.save(destination_path)

def draw_bbox(file_path,output_folder, x1,y1,x2,y2):
        img = Image.open(file_path)
        img = img.resize((640, 480))

        rectangle_coords = [(x1, y1), (x2, y2)]
        draw = ImageDraw.Draw(img)
        last_component = os.path.basename(file_path)
        draw.rectangle(rectangle_coords, outline='red')
        
        destination_path = os.path.join(output_folder, last_component)
        img.save(destination_path)

if __name__ == "__main__":
    yolo_net = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    source_folder = r""
    image_list = os.listdir(source_folder)
    
    for data_source in tqdm(image_list):
        params = {
            "out_dir": r"",
            "data_source": data_source,
            "image_path": os.path.join(source_folder, data_source),
            "size": (480, 640),
            "raft_iter": 6,
            "csv_file_name": "TCCPD.csv",
            "trash_folder": r""
        }
        main(params, yolo_net)




