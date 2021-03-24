from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.responses import JSONResponse
import uvicorn
import pandas as pd
import json
import re

from bs4 import BeautifulSoup
import urllib.request

from functions import *
from model import *

app = FastAPI()

dict_trustpilot = [
    {
        'category': 'aliments',
        'link': ' /categories/food_beverages_tobacco',
    },
    {
        'category': 'animaux',
        'link': '/categories/animals_pets',
    },
    {
        'category': 'argent',
        'link': '/categories/money_insurance',
    },
    {
        'category': 'beauté',
        'link': '/categories/beauty_wellbeing',
    },
    {
        'category': 'construction',
        'link': '/categories/construction_manufactoring',
    },
    {
        'category': 'education',
        'link': '/categories/education_training',
    },
    {
        'category': 'tech',
        'link': '/categories/electronics_technology',
    },
    {
        'category': 'evenements',
        'link': '/categories/events_entertainment',
    },
    {
        'category': 'loisir_artisanat',
        'link': '/categories/hobbies_crafts',
    },
    {
        'category': 'maison_jardin',
        'link': '/categories/home_garden',
    },
    {
        'category': 'média',
        'link': '/categories/media_publishing',
    },
    {
        'category': 'restau_bar',
        'link': '/categories/restaurants_bars',
    },
    {
        'category': 'santé',
        'link': '/categories/health_medical',
    },
    {
        'category': 'services',
        'link': '/categories/utilities',
    },
    {
        'category': 'services_domicile',
        'link': '/categories/home_services',
    },
    {
        'category': 'services_entreprise',
        'link': '/categories/business_services',
    },
    {
        'category': 'juridique_admin',
        'link': '/categories/legal_services_government',
    },
    {
        'category': 'services_publics',
        'link': '/categories/public_local_services',
    },
    {
        'category': 'mode',
        'link': '/categories/shopping_fashion',
    },
    {
        'category': 'sport',
        'link': '/categories/sports',
    },
    {
        'category': 'voyage',
        'link': '/categories/travel_vacation',
    },
    {
        'category': 'véhicule_transport',
        'link': '/categories/vehicles_transportation',
    },
]

@app.get("/")
async def root():
    return 'hello'

@app.get("/category")
def get_category():
    return dict_trustpilot

@app.get("/trustpilot")
def scrap(category: str = 'aliments', pages: int = 1):
    dict_cat = {
        'aliments': '/categories/food_beverages_tobacco',
        'animaux': '/categories/animals_pets',
        'argent': '/categories/money_insurance',
        'beauté': '/categories/beauty_wellbeing',
        'construction': '/categories/construction_manufactoring',
        'éducation': '/categories/education_training',
        'tech': '/categories/electronics_technology',
        'événements': '/categories/events_entertainment',
        'loisir_artisanat': '/categories/hobbies_crafts',
        'maison_jardin': '/categories/home_garden',
        'média': '/categories/media_publishing',
        'restau_bar': '/categories/restaurants_bars',
        'santé': '/categories/health_medical',
        'services': '/categories/utilities',
        'services_domicile': '/categories/home_services',
        'services_entreprise': '/categories/business_services',
        'juridique_admin': '/categories/legal_services_government',
        'services_publics': '/categories/public_local_services',
        'mode': '/categories/shopping_fashion',
        'sport': '/categories/sports',
        'voyage': '/categories/travel_vacation',
        'véhicule_transport': '/categories/vehicles_transportation'
    }

    # Scrap
    if category in dict_cat.keys():
        cat = dict_cat[category]
        trustpilot = f'https://fr.trustpilot.com{cat}?numberofreviews=500'
        web_page = urllib.request.urlopen(trustpilot)
        category_soup = BeautifulSoup(web_page, 'html.parser')
        list_company = []

        print('companies search...')

        for element in category_soup.find_all('a', {'class': 'link_internal__YpiJI link_wrapper__LEdx5'}):
            company = element.get('href')
            if '/review/' in company and company not in list_company:
                list_company.append(company)

        if pages == 1:
            page_number = [1]
        elif pages > 1:
            page_number = range(1, pages)

        list_url = []

        for company_url in list_company:
            for page in page_number:
                url = f'https://fr.trustpilot.com{company_url}' + f'?page={page}'
                list_url.append(url)

        list_soup = []

        for x in list_url:
            web_page = urllib.request.urlopen(x)
            base_soup = BeautifulSoup(web_page, 'html.parser')
            list_soup.append(base_soup)

        list_dates = []
        list_reviews = []
        list_ratings = []

        print('reviews search...')

        for soup in list_soup:
            for element in soup.find_all('div', {'class': 'review-content'}):
                date = element.find('p', {'class': 'review-content__dateOfExperience'})
                list_dates.append(date)
                text = element.find('p', {'class': 'review-content__text'})
                if text is not None:
                    list_reviews.append(text.getText())
                else:
                    title = element.find('a', {'class': 'link link--large link--dark'}).getText()
                    list_reviews.append(title)
                rating = element.find('div', {'class': 'star-rating star-rating--medium'})
                list_ratings.append(rating)

        print('preprocess...')

        # Preprocess
        list_reviews = remove_spaces(list_reviews)
        list_reviews = remove_emoji(list_reviews)
        tokenized_reviews = tokenize(list_reviews)

        dict_reviews = {'review': list_reviews}

        attention_masks = []
        for seq in tokenized_reviews:
            seq_mask = [float(i > 0) for i in seq]
            attention_masks.append(seq_mask)

        prediction_inputs = torch.tensor(tokenized_reviews)
        prediction_masks = torch.tensor(attention_masks)

        print('predictions...')

        # Predictions with finetuned model (Camembert)
        flat_pred = []
        with torch.no_grad():
            outputs = camembert(prediction_inputs, token_type_ids=None,
                                attention_mask=prediction_masks)
            logits = outputs[0]
            logits = logits.detach().cpu().numpy()
            flat_pred.extend(np.argmax(logits, axis=1).flatten())

        # Formating datas to display
        data = {
            'sentiment': flat_pred,
            'review': list_reviews
                }
        df = pd.DataFrame(data, columns=['sentiment', 'review'])

        df_pos = df[df['sentiment'] == 1]
        df_pos = df_pos['review']
        df_neg = df[df['sentiment'] == 0]
        df_neg = df_neg['review']

        dict_pos = df_pos.to_dict()
        dict_neg = df_neg.to_dict()

        dict_total_reviews = {'Total': len(dict_reviews['review']), 'Positive': len(dict_pos), 'Negative': len(dict_neg)}
        dict_predicted = {'Positive': dict_pos, 'Negative': dict_neg}

        dict_api = {'Count': dict_total_reviews, 'Reviews': dict_predicted}

        return dict_api
    else:
        return 'not a category'
