# Trustpilot API French sentiment analysis with CamemBert
## Table of contents
* [General info](#general-info)
* [Installation](#Installation)
* [Folders/FIles](#Folders/FIles)
## General Info
This project is a production of API with reviews of Truspilot to know if the reviews of customers is postive or negative.
To make this french sentiment analysis we use the pre-trained model camemBERT.

## Installation 

All packages you need is on requirements.txt
To use just the API use requirement_api.txt

## Folders/Files
Folders and Files for this Project : 
 * fastapi Folder :<br>
   * Static forder countains styles.css
   * Templates  countains index.html for the render of homepage ('http://127.0.0.1:8000/')

   * main.py: code to lauch the api on localhost and begin the scrap of reviews on the chosen category
   * functions.py: to remove all emoji and unnecessary spaces after the scrap in API
   * model.py: load the pre-train, fine-tuned model of sentiment analysis used in API - used with "camembert_sentiment_anal.pt"     
  * data folder <br> 
    * trustpilot_reviews.csv: Dataset with french reviews of all categories of the website Truspilot. We use this dataset to train the model
    * trustpilot_to_predict.csv: Dataset to test the model
 * model folder
   * camembert_trustpilot.ipynb: Colab which contains the trainning of the model - used with "trustpilot_reviews.csv"
   * Predictions is a notebook for testing the accuracy of the model prediction on dataset
* Files :
  * scrap_trustpilot.py used to create the dataset for model training

## Collab link trained camenBert model on dataset

https://colab.research.google.com/drive/1kyLGR4OifFgsykcqii3LmYUwIxeoQ0VZ#scrollTo=xJ0vCeTDC3gr

## Model save link drive
https://drive.google.com/file/d/1lrPJxmk8qJi2KKPpOSCUv3Je2ZsZBV4q/view
