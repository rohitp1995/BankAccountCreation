# BankAccountCreation

## Definition
Nowadays, Due to the overload of work in banking sector it has become very difficult for the employees to verify a document and then fill all the necessary forms in order to create a bankaccount for a customer. It involves lot of manual work and the process hamper other task of the employees 

![readme_app_form](https://user-images.githubusercontent.com/29440153/174050842-cbf063e4-a96a-459b-90c8-315a5f925bff.jpg)

## Problem statement

Given some sample images, we have to create a object detection and text extraction application for creating a bankaccount without much manual intervention

## Proposed Solution

Building an Computer vision based application where user will upload their aadhar image and the bank account will be created without much manual intervention. All the details will be sent to user email id (provided) after account creation

## Data Description

We gathered image data for aadhar card from the internet. The data was already avaialable on the internet so we are not breaching any data privacy of any person
* We captured around 70-80 images for aadhar card and did augmentation to increase the number of images to train a suitable model on those images 
* aadhar card captured are from various states of india 

## Tool Used 
![image](https://user-images.githubusercontent.com/29440153/174068499-c34a7f48-4016-401a-9d18-27ef1caf2711.png)

## how to run (in local system)

* git clone the repository in your system
* pip install -r requirements.txt
* python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
* download the entire model output folder from ```https://drive.google.com/drive/folders/1GDgXKRu__aAtPerpOH0mEnaGKSOPTjff?usp=sharing``` and save it to your local cloned folder
* run the following comand streamlit run app.py

**OR**

* you can pull the docker image from the dockerhub docker pull rohit0506/dockerhub:accountcreator
* get the docker image id by running ```docker images``` command
* after that run ```docker run -p 8501:8501 <image id>

## Application Home Page

![image](https://user-images.githubusercontent.com/29440153/174070120-dc00e502-96d6-417d-b533-75656e2f104f.png)

## Project Demo Video
https://youtu.be/y13RiQ10KYk

## Contributors
https://github.com/rohitp1995/
