import matplotlib.pyplot as plt
from pandas.core.common import flatten
import copy
import numpy as np
import random
from torchvision.utils import save_image
import torch
from torch import nn
from torch import optim
import torch.nn.functional as F
from torchvision import datasets, transforms, models
from torch.utils.data import Dataset, DataLoader
import albumentations as A
from albumentations.pytorch import ToTensorV2
import cv2
from tqdm import tqdm
import glob

#Giving data path
train_data_path = 'aadhar_images/*' 

train_image_paths = [] #to store image paths in list

for data_path in glob.glob(train_data_path):
    train_image_paths.append(glob.glob(data_path))
    
train_image_paths = list(flatten(train_image_paths))
random.shuffle(train_image_paths)

train_transforms = A.Compose(
    [
        
        A.RandomBrightnessContrast(p=0.5),
        A.Sharpen(alpha=(0.2, 0.5), lightness=(0.5, 1.0), always_apply=False, p=0.5),
        A.ToGray(always_apply=False, p=0.5),
       
        A.RandomBrightnessContrast(brightness_limit=(-0.1,0.1), contrast_limit=(-0.1, 0.1), p=0.5),
        ToTensorV2(),
    ]
)

class Imagedataset(Dataset):
    def __init__(self, image_paths, transform=False):
        self.image_paths = image_paths
        self.transform = transform
        
    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_filepath = self.image_paths[idx]
        image = cv2.imread(image_filepath
        
        if self.transform is not None:
            image = self.transform(image=image)["image"]
    return image


def save_augmentations(dataset, idx=0, samples=5, cols=5, random_img = False):
    
    dataset = copy.deepcopy(dataset)
    #we remove the normalize and tensor conversion from our augmentation pipeline
    dataset.transform = A.Compose([t for t in dataset.transform])
        
    for i in range(samples):
        
        idx = np.random.randint(1,len(train_image_paths))
        image = dataset[idx]
        image
        save_image(image, 'img'+str(i+10)+'.png')
        
        
       

save_augmentations(train_dataset,np.random.randint(1,len(train_image_paths)))



