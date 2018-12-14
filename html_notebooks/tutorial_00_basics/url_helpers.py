import urllib.parse, requests, json, re
from requests import Request, Session
from httplib2 import Http


category_alias_instance = "http://10.73.82.181:31823"
mskip_instance = "http://10.73.72.173:31617"
scenario_service_instance = "http://10.71.192.22:8080"
search_service_instance = "http://localhost:8080"

def extract_category(category_alias):
    if category_alias == "listing" or "listing.php" in category_alias:
        return "0"
    else:
        return category_alias


def extract_phrase(string_param):
    string_param_lenght = len("string=")
    without_param_name = string_param[string_param_lenght:]
    return without_param_name


def extract_department(url):
    m = re.search("bmatch=.*\-(.*)\-\d+\-\d+-\d{4}", url)
    if m:
        return m.group(1)
    return "uni"


def extract_phrase(url):
    m = re.search("string=(.*?)\&", url)
    if m:
        return urllib.parse.unquote(m.group(1))
    return ""


def clean_url(url):
    if "http" not in url:
        return None

    prefix_length = len("https://allegro.pl/")
    noprefix = url[prefix_length:]
    parts = noprefix.split("&")
    decoded = urllib.parse.unquote(parts[0])
    parts = decoded.split("?")
    department = extract_department(url)
    phrase = extract_phrase(url)
    category = extract_category(parts[0])
    return (category, phrase, department)


def resolve_category_alias(alias):
    url_template = category_alias_instance + "/category-aliases?alias={}&tree.name=listing-pl"
    headers = {"Accept": "application/json"}
    response = requests.get(url_template.format(alias), headers)
    if response.status_code == 200:
        category_alias = response.json()
        return category_alias["category"]["id"]
    return alias

def resolve_department(categoryId):
    url_template = mskip_instance + "/category-paths/{}"
    headers = {"Accept": "application/json"}
    response = requests.get(url_template.format(categoryId), headers)
    if response.status_code == 200:
        category_path = response.json()
        return (category_path["path"][1]["id"], category_path["path"][1]["name"])
    return "", ""


def resolve_department_from_phrase(phrase):
    url_template = scenario_service_instance + "/scenarios?phrase={}"
    response = requests.get(url_template.format(phrase))
    if response.status_code == 200:
        scenario = response.json()
        boost_param = scenario['boost_parameters']
        for param in boost_param:
            if param["field"] == "cat":
                categoryId = param["value"]
                return resolve_department(categoryId)
    return "0", "uni"
