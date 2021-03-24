# Trustpilot API French sentiment analysis
## Table of contents
* [General info](#general-info)
* [Installation](#Installation)
* [Folders/FIles](#Folders/FIles)
## General Info
This project is a production of API with reviews of Truspilot to know if the reviews of customers is postive or negative.
To make this french sentiment analysis we use the pre-trained model camemBERT.

## Installation 

All packages you need is on requirements.txt

## Folders/FIles
Folders and Files for this Project : 
 * fastapi Folder :<br>
   * Static forder countains styles.css
   * Templates  countains index.html for the render of homepage ('http://127.0.0.1:8000/')

   * main.py: code to lauch the api on localhost
   * preprocessing.py: to remove all emoji and html tags during after the scrap in API
   * model.py: load the pre-train, fine-tuned model of sentiment analysis used in API
   * scrap.py: Trustpilot scrap category using in API
  * CSV folder <br>
    * datasets with french reviews of all categories of the website Truspilot. We use this dataset to train the model
 * Exemples_model Folder
   * Countains the trainning in the dataset Truspilot
   * Predictions is a notebook for testing the accuracy of the model prediction on dataset
* Files :
  * prepocessing.py used for remove all emoji/ html in the dataset
  * scrap_trustpilot.py used for create the dataset for trained model 

## Collab link trained camenBert model on dataset

https://colab.research.google.com/drive/1kyLGR4OifFgsykcqii3LmYUwIxeoQ0VZ#scrollTo=xJ0vCeTDC3gr

## Model save link drive
https://drive.google.com/file/d/1lrPJxmk8qJi2KKPpOSCUv3Je2ZsZBV4q/view
