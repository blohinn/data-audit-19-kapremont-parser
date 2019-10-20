import json
import requests
from bs4 import BeautifulSoup

from requests_html import HTMLSession

URL = 'https://www.reformagkh.ru/overhaul/overhaul/services/{}?finished=1&byYear=1'

session = HTMLSession()

with open('simple_json.json', 'r') as f:
    data = json.loads(f.read())


def get_soup(reformagkh_id):
    url = URL.format(reformagkh_id)
    # print(url)
    html = requests.get(url).text
    return BeautifulSoup(html, 'html.parser')


def get_2018_year_table(years_div):
    for year_div in years_div:
        year_head = year_div.findChildren('div', recursive=False)[0]
        year = int(year_head.find('p').get_text().replace(' ', '').replace('\n', '')[:4])
        if year == 2018:
            return year_div

    return None


def get_year_table_tbodies(year_div):
    table_tag = year_div.find('table')
    tbodies = table_tag.findChildren('tbody', recursive=False)

    return tbodies


def get_value_by_tr(tr):
    return tr.find_all('td')[1].get_text().strip().replace('\n', '')


def get_info_by_year_info_row(row):
    # {'job', 'price': {'plan', 'total'}, 'customer': {'name', 'inn'}, 'performer': {'name', 'inn'}}
    # 'contract': {'date_conclusion', 'contract_completion_date_plan', 'date_act_accepting'}
    trs = row.find_all('tr', class_='leaders')

    try:
        _job = row.find('td').get_text().strip()
    except:
        _job = None

    try:
        _price_plan = float(get_value_by_tr(trs[0])) if get_value_by_tr(trs[0]) != 'Не заполнено' else None
    except:
        _price_plan = None

    try:
        _price_total = float(get_value_by_tr(trs[2])) if get_value_by_tr(trs[2]) != 'Не заполнено' else None
    except:
        _price_total = None

    try:
        _customer_name = get_value_by_tr(trs[3]) if get_value_by_tr(trs[3]) != 'Не заполнено' else None
    except:
        _customer_name = None

    try:
        _customer_inn = int(get_value_by_tr(trs[4])) if get_value_by_tr(trs[4]) != 'Не заполнено' else None
    except:
        _customer_inn = None

    try:
        _performer_name = get_value_by_tr(trs[5]) if get_value_by_tr(trs[5]) != 'Не заполнено' else None
    except:
        _performer_name = None

    try:
        _performer_inn = int(get_value_by_tr(trs[6])) if get_value_by_tr(trs[6]) != 'Не заполнено' else None
    except:
        _performer_inn = None

    try:
        _date_conclusion = get_value_by_tr(trs[7]) if get_value_by_tr(trs[7]) != 'Не заполнено' else None
    except:
        _date_conclusion = None

    try:
        _date_contract_completion_plan = get_value_by_tr(trs[8]) if get_value_by_tr(trs[8]) != 'Не заполнено' else None
    except:
        _date_contract_completion_plan = None

    try:
        _date_act_accepting = get_value_by_tr(trs[9]) if get_value_by_tr(trs[9]) != 'Не заполнено' else None
    except:
        _date_act_accepting = None

    return {
        'job': _job,
        'price': {
            'plan': _price_plan,
            'total': _price_total,
        },
        'customer': {
            'name': _customer_name,
            'inn': _customer_inn,
        },
        'performer': {
            'name': _performer_name,
            'inn': _performer_inn,
        },
        'contract': {
            'date_conclusion': _date_conclusion,
            'date_contract_completion_plan': _date_contract_completion_plan,
            'date_act_accepting': _date_act_accepting,
        },
    }


def parse_data_for_house(reformagkh_id):
    soup = get_soup(reformagkh_id)
    tab = soup.find('div', class_='tab')
    location_lists_inside_tab = tab.find('div', class_='location_lists')
    years = location_lists_inside_tab.findChildren('div', recursive=False)

    year_2018 = get_2018_year_table(years)
    if not year_2018:
        return None

    tbodies = get_year_table_tbodies(year_2018)

    result = []
    for tbody in tbodies:
        info = get_info_by_year_info_row(tbody)
        result.append(info)

    return result


results = []
for house_data in data:
    # todo заменить
    jobs = parse_data_for_house(house_data['reformagkh_id'])
    _ = {
        'address': house_data['address'],
        'lat': house_data['lat'],
        'lng': house_data['lng'],
        'reformagkh_id': house_data['reformagkh_id'],
        'jobs': jobs,
    }
    results.append(_)
    break
    # parse_data_for_house(2907968)

print(json.dumps(results))
