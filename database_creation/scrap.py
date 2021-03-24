import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import string

import nltk
from nltk import word_tokenize
#nltk.download('punkt')

# url, ouverture page et parsing
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

inp_cat = True
category = ''
while(inp_cat):
    print(dict_cat.keys())
    key = input('choose category: ')
    if key in dict_cat.keys():
        category = dict_cat[key]
        inp_cat = False
    else:
        print('not a category')


trustpilot = f'https://fr.trustpilot.com{category}?numberofreviews=500'
web_page = urllib.request.urlopen(trustpilot)
category_soup = BeautifulSoup(web_page, 'html.parser')
list_company = []

for element in category_soup.find_all('a', {'class': 'link_internal__YpiJI link_wrapper__LEdx5'}):
    company = element.get('href')
    if '/review/' in company and company not in list_company:
        list_company.append(company)

# list_company = ['blablahbla']
# key = input('company: ')
print(list_company)

page_number = [1, 2]
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

# voir contenu
# print(soup.prettify())

list_dates = []
list_reviews = []
list_ratings = []

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

# dataframe
df = pd.DataFrame({'date': list_dates, 'review': list_reviews, 'rating': list_ratings})

# sauvegarde dataframe
df.to_csv(f'trustpilot_reviews_{key}.csv')