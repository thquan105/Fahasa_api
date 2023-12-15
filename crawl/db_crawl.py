import os
import sys
import requests
import mysql.connector
import json
import schedule
import time
# add the directory containing the db module to the Python path
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
sys.path.append(db_path)
from db.db_actions import insert_data


api_url = "https://www.fahasa.com/fahasa_catalog/product/loadCatalog"

headers = {
  'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'X-Requested-With': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
  'sec-ch-ua-platform': '"Windows"',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'host': 'www.fahasa.com',
  'Cookie': 'frontend=25ce42b62fba4fba87697a462a1d7add; frontend_cid=4oERUjGNSzVdg4un'
}

def get_data():
    page_num = 1
    while True:
        params = {'category_id': 2, 'currentPage': page_num}
        response = requests.get(api_url,headers=headers,params=params)
        
        if response.status_code == 200:
            api_data = json.loads(response.text)['product_list']
            # break if no more data
            if not api_data:
                break

            for item in api_data:
                insert_data(item)
                
            page_num += 1
        else:
            print(f"API request failed")
            break

# Lập lịch công việc cào dữ liệu hàng ngày lúc 00:00
# schedule.every().day.at("00:00").do(get_data)

# Vòng lặp để giữ chương trình chạy liên tục
# while True:
#     schedule.run_pending()
#     time.sleep(1)
if __name__ == '__main__':
    # crawl_auto()
    get_data()

