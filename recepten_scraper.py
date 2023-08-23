import requests
import bs4 as bs
import pandas as pd

def get_ingredients(url):
    try:
        response = requests.get('https://www.ah.nl' + url, timeout=2)
    except Exception as e:
        print(e)
        return []
    if not response.ok:
        print(f'error on url {url}')
        print(response.status_code)
        return []
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    ingredients = soup.find(class_='recipe-preparation_ingredients__WifiN')
    personen = ingredients.find(class_='recipe-ingredients_servings__f8HXF').text.strip().strip('personen').strip()
    ingedrient_list = ingredients.find(class_='recipe-ingredients_ingredientsList__thXVo')
    ingedrient_list = ingedrient_list.find_all('p')
    df = []
    for i in range(0, len(ingedrient_list)-1, 2):
        df.append([ingedrient_list[i].text, ingedrient_list[i+1].text, url, personen])
    return pd.DataFrame(df)

if __name__ == "__main__":
    url = '/allerhande/recept/R-R1198996/traybake-met-vegaballetjes-krieltjes-prei-en-tomaat'
    df = get_ingredients(url)
    print(df)