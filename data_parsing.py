# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import requests
# import os
# import time

# # Take URLs to check
# urls = [
#     "https://abit.itmo.ru/program/master/ai",
#     "https://abit.itmo.ru/program/master/ai_product"
# ]

# # https://api.itmo.su/constructor-ep/api/v1/static/programs/10130/plan/abit/pdf

# # Path to save downloaded files
# download_folder = "downloaded_plans"
# os.makedirs(download_folder, exist_ok=True)

# # Setup Selenium WebDriver (using Chrome in this example)
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # run in headless mode
# driver = webdriver.Chrome(options=options)

# for url in urls:
#     driver.get(url)
#     time.sleep(3)  # wait for page to load (adjust if needed)

#     try:
#         # Find the element by exact link text (button or <a> tag)
#         # link_element = driver.find_element(By.LINK_TEXT, "Скачать учебный план")
#         # file_url = link_element.get_attribute("href")
#         file_url = 'https://api.itmo.su/constructor-ep/api/v1/static/programs/10033/plan/abit/pdf'
        
#         # if not file_url:
#         #     # If href is missing, try button's onclick or nested <a>
#         #     file_url = link_element.get_attribute("onclick")  # rare case
#             # You might need additional parsing here if file_url is JS

#         print(f"Found file URL: {file_url}")

#         # Download the file
#         if file_url:
#             response = requests.get(file_url)
#             filename = os.path.join(download_folder, file_url.split("/")[-1])

#             with open(filename, "wb") as f:
#                 f.write(response.content)
#             print(f"Downloaded file saved to: {filename}")

#     except Exception as e:
#         print(f"Could not find or download from {url}: {e}")

# driver.quit()


import requests
import os

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=0, i',
    'referer': 'https://abit.itmo.ru/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
}

urls = {
    'ai': 'https://api.itmo.su/constructor-ep/api/v1/static/programs/10033/plan/abit/pdf', 
    'ai_product': 'https://api.itmo.su/constructor-ep/api/v1/static/programs/10130/plan/abit/pdf'
}
download_folder = "downloaded_plans"
for filename, url in urls.items():
    response = requests.get(url, headers=headers)
    path = os.path.join(download_folder, filename + '.pdf')

    with open(path, "wb") as f:
        f.write(response.content)
    print(f"Downloaded file saved to: {path}")

