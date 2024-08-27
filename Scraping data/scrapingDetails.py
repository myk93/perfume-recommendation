import json
import requests
from bs4 import BeautifulSoup


# Function to extract data from each webpage
def extract_data(webPage):
    response = requests.get(webPage)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract details
    ingredients_div = soup.find('div', {'class': 'lg:hidden text-center leading-8 text-16'})
    ingredients = []
    if ingredients_div:
        ingredients = [item.text for item in ingredients_div.find_all('a')] + [item.text for item in
                                                                               ingredients_div.find_all('span', {
                                                                                   'class': 'text-black'})]
    details_div = soup.find('div', {
        'class': 'w-full sm:w-[80%] md:w-[60%] lg:w-[33%] flex flex-col items-center lg:items-start lg:self-start h-max order-last lg:-mt-5'})
    family = subfamily = classification = None
    price = None
    if details_div:
        family_div = details_div.find('div', {
            'class': 'order-1 flex flex-col gap-2 items-center justify-center text-center p-3'})
        if family_div:
            family = family_div.find('p', {'class': 'text-12 xl:text-14 text-black text-center'}).text

        subfamily_div = details_div.find('div', {
            'class': 'order-2 flex flex-col gap-2 items-center justify-center text-center p-3'})
        if subfamily_div:
            subfamily = subfamily_div.find('p', {'class': 'text-12 xl:text-14 text-black text-center'}).text

        classification_div = details_div.find('div', {'class': 'flex flex-col gap-4'})
        if classification_div:
            classification = classification_div.find('dd', {'class': 'text-16'}).text

        price_div = details_div.find('div', {
            'class': 'flex flex-col items-center lg:flex-row lg:justify-between lg:pt-5 gap-12 lg:gap-4 pb-5 lg:pb-0'})
        if price_div:
            price_spans = price_div.find('dd', {'class': 'text-16 flex gap-2'}).find_all('span')
            price = price_spans[0].decode_contents().count("black")

    # Extract additional details
    additional_details_div = soup.find('div', {'class': 'py-4 bg-white rounded-lg px-6 relative'})
    concepts = origin = gender = year = None
    perfume_categories = []
    if additional_details_div:
        origin_div = additional_details_div.find('dt', string='Origin')
        if origin_div:
            origin = origin_div.find_next_sibling('dl').text

        gender_div = additional_details_div.find('dt', string='Gender')
        if gender_div:
            gender = gender_div.find_next_sibling('dl').text

        year_div = additional_details_div.find('dt', string='Year')
        if year_div:
            year = year_div.find_next_sibling('dl').text

        concept_div = additional_details_div.find('dt', string='Concepts')
        if concept_div:
            concept = concept_div.find_next_sibling('dl').find_all('span')
            concepts = [span.text.replace(", ","") for span in concept]

        perfume_category_div = additional_details_div.find('dt', string='Perfume category')
        if perfume_category_div:
            perfume_category_spans = perfume_category_div.find_next_sibling('dl').find_all('span')
            perfume_categories = [span.text for span in perfume_category_spans]

    # Extract description
    description_div = soup.find('div', {'data-state': 'open', 'data-orientation': 'vertical', 'class': 'group'})
    description = None
    if description_div:
        description_section = description_div.find('span', {'class': 'text-16 md:text-18 font-light markdown'})
        if description_section:
            description = description_section.get_text(strip=True)

    ingredients = [ingredient.replace(" ", "").replace("|", "") for ingredient in ingredients if ingredient.strip()]
    perfume_categories = [category.replace(", ", "") for category in perfume_categories if category.strip()]

    return {
        'family': family,
        'subfamily': subfamily,
        'classification': classification,
        'price': price,
        'origin': origin,
        'gender': gender,
        'year': year,
        'perfume_categories': perfume_categories,
        'ingredients': ingredients,
        'concept': concepts,
        'description': description
    }


all_perfumes_data = []

# Load the names.json file
with open('name.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

# Process each entry
for entry in data:
    name = entry['name']
    webPage = entry['webPage']
    extracted_data = extract_data(webPage)
    all_perfumes_data.append({
        'name': name,
        'webPage': webPage,
        'data': extracted_data
    })

# Save all perfumes data to a single JSON file
with open('all_perfumes2.json', 'w', encoding="utf-8") as outfile:
    json.dump(all_perfumes_data, outfile, indent=4, ensure_ascii=False)