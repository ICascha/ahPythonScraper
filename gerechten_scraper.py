import requests
import bs4 as bs
import pandas as pd
from tqdm import tqdm
from time import sleep

get_page = lambda x: f'https://www.ah.nl/allerhande/recepten-zoeken?veel-gebruikt=hoofdgerecht&page={x}'

df = []
for page in tqdm(range(258)):
    response = requests.get(get_page(page))
    soup = bs.BeautifulSoup(response.content, 'html.parser')
    all_links = soup.find_all('a')
    if not response.ok:
        print(f'Error on page {page}')
        continue
    # filter where data-testhook="recipe-card"
    recipe_links = [link for link in all_links if link.get('data-testhook') == 'recipe-card']
    if not recipe_links:
        print(page)
    for recipe_link in recipe_links:
        title = recipe_link['title'].replace('Recept: ', '')
        url = recipe_link['href']
        properties = recipe_link.find_all(class_='recipe-card-properties_property__87cH1')
        propnames = []
        for prop in properties:
            propnames.append(prop.text)
        df.append([title, url, propnames])
    sleep(0.1)
    
df = pd.DataFrame(df, columns=['title', 'url', 'properties'])
df.to_csv('allerhande_hoofdgerechten.csv', index=False)