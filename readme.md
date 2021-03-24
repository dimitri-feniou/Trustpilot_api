# Trustpilot API French sentiment analysis with CamemBert
## Table of contents
* [General info](#general-info)
* [Installation](#Installation)
* [Folders/FIles](#Folders/FIles)
## General Info
This project is a production of API with reviews of Truspilot to know if the reviews of customers is postive or negative.
To make this french sentiment analysis we use the pre-trained model camemBERT.

## Installation 

All packages you need is on requirements.txt. <br/>
To use just the API use requirements_api.txt

## How to use

* http://127.0.0.1:8000/category - to see the list of categories
* http://127.0.0.1:8000/trustpilot?category={category}&pages={number_pages} - with the chosen category in {category} and the number of pages scraped in {number_pages}. Peux potentiellement bugger selon la categorie et le nombre de pages choisi.
 * http://127.0.0.1:8000/trustpilot - with default values as "aliments" and "1"

## Folders/Files
Folders and Files for this Project : 
 * fastapi Folder :<br>
   * Static forder countains styles.css
   * Templates  countains index.html for the render of homepage ('http://127.0.0.1:8000/')

   * main.py: code to lauch the api on localhost and begin the scrap of reviews on the chosen category
   * functions.py: to remove all emojis and unnecessary spaces after the scrap in API
   * model.py: load the pre-train, fine-tuned model of sentiment analysis used in API - used with "camembert_sentiment_anal.pt"     
 * data folder :<br>
   * trustpilot_reviews.csv: dataset with french reviews of all categories of the website Truspilot. We use this dataset to train the model
   * trustpilot_to_predict.csv: dataset to test the model  
 * model folder :  
   * camembert_trustpilot.ipynb: colab which contains the trainning of the model - used with "trustpilot_reviews.csv"  
   * predictions.ipynb: colab for testing the accuracy of the model predictions - used with "trustpilot_to_predict.csv"  
 * database_creation folder :  
   * scrap.py: used to create the dataset for model training   
   * merge.py: to merge the scraped datasets  
   * cleaning.py: used to remove emojis and unnecessary space in the training dataset  

## Colab link CamemBert training on dataset

https://colab.research.google.com/drive/1kyLGR4OifFgsykcqii3LmYUwIxeoQ0VZ#scrollTo=xJ0vCeTDC3gr

## Model save link drive

https://drive.google.com/file/d/1lrPJxmk8qJi2KKPpOSCUv3Je2ZsZBV4q/view

## Google slide link

https://docs.google.com/presentation/d/1khh3OWh9W8eaibgVRB7Lw2EJp52GP9zbCpV53CiI3s4/edit#slide=id.gca5633d238_3_19

## Contributors
Terence COLLIN, Dimitri FENIOU
