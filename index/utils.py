from datetime import date
import requests

def get_json_by_date(date:date,page:int=1):
    date_string = f"{date.year}-{date.month}-{date.day}"
    url = "https://index.hu/api/json/"
    headers = {
        "Host": "index.hu",
        "Origin": "https://index.hu",
        "Referer": f"https://index.hu/24ora/?tol={date_string}&ig={date_string}",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26",
        }

    payload = {
        "rovat":"24ora",
        "url_params[pepe]": 1,
        "url_params[tol]": date_string,
        "url_params[ig]": date_string,
        "url_params[p]": page,
    }

    response = requests.get(url, params=payload,headers=headers)
    return response.json()
    