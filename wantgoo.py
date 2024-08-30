import os
import requests
import json
from bs4 import BeautifulSoup
from xhtml2pdf import pisa

class Wantgoo:
    def __init__(self, club_id):
        self.club_id = club_id

    def scrape(self):
        url = f'https://www.wantgoo.com/club/{self.club_id}/course/units'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
        }
        
        # 發送 HTTP 請求並獲取網頁內容
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'

        # 資料
        result = response.json()               
        return result

data = Wantgoo('26')
jsondata = data.scrape()

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'cookie':'BIDDB84D-DE5C-4DC5-BFE4-F1A43EC9FD7F; client_fingerprint=d0533ac2f569bb4482d6f3fce13abb71cc46b118ed175c09235f706fb50b6b6d; ad-popup-overlay-8=1724860800000; _gid=GA1.2.1545288126.1724894911; _gcl_au=1.1.1802339018.1724894911; _clck=12wqztb%7C2%7Cfoq%7C0%7C1702; member_token=eyJpZCI6MTc0NiwidXNlck5hbWUiOiJhODczNTAyNEBzdG1haWwuZmp1LmVkdS50dyJ9~9259d7e3df00697541da58bff5b0bd7d780c144e9147dbd247ab8af2ce34b9fd; member_id=1746; user_name=a8735024@stmail.fju.edu.tw; FCNEC=%5B%5B%22AKsRol_meqozXfUUcXZFT81zYPjnAArDhENkiMk4ZcYRO-Xyc3XLzpx5gg2lUFKxBp7XwsbKBbRzopwICxkbJ6EcBE_1XBsnbZZtzzT3qLdjx-vFexn6MFb9r_g3vwiqGwFe_1lWFgc7GtY5MDCbc85S5bVCQKvwHg%3D%3D%22%5D%5D; cf_clearance=JrpT.bcm7CqOt2EvrogX_pMpy.m06Y9ec2hNUcs0tYs-1724922969-1.2.1.1-qkiKDHUieggAen1D8zS17oq268WIVWqzKgUVvqyNlr4mC04Cyv3hFJO2X8uNISLGQglPFdfYFgTjdLRYsKhh3WK3diwSoMZwC..zrc.gYKKAOn.HfQJ703lrw4lOuNPO3kBe7P52kDz5p.RxdrZnF1h2CUQsiPb0iwurLrVEL.S.dgQ0Z46Ybt.8n4Vi2K9o9x21q_4KTqT30cmUrDmgh5Uia_Ykp_b4woUvY8UF._337E8DFb3_OnryRt8NMtYITcMsc3KAbsIZGfjGfeG_lA0MkA2qYf2dX2AfoX8Pii0gS7g7.e55l_DUK.avws59Q2AfbUaObaDEqZvUpSN0Bl_9ZiMB3bLuVKTOqM4RUzW38nT.Yc531Nmt6ADdIYT_h4VJFTtSF_kSzlcodVZOJg; _clsk=vyupbc%7C1724922973666%7C32%7C1%7Cx.clarity.ms%2Fcollect; club_26_member_token=eyJjbHViSWQiOjI2LCJtZW1iZXJObyI6MTc0Niwicm9sZSI6Ik5vcm1hbCIsImdvb2RUaHJ1IjoiMjAyNS0wNS0xNlQxMTo0OTo1NS43MiJ9~6692ef957893155f4acdfb262c4553b7867afae1a4542dd9860532b02a40e313; _ga_FCVGHSWXEQ=GS1.1.1724921260.4.1.1724923238.59.0.0; _ga=GA1.2.1323436522.1724894911; _gat_gtag_UA_6993262_2=1'
}

def convert_html_to_pdf(source_html, output_filename):
    # 將 HTML 內容轉換為 PDF
    result_file = open(output_filename, "w+b")
    pisa_status = pisa.CreatePDF(source_html, dest=result_file, encoding='utf8')
    result_file.close()
    return pisa_status.err


for d in jsondata:
    link = 'https://www.wantgoo.com/club/26/course/' + str(d['id']) + '/section/' + str(d['chapters'][0]['sections'][0]['id']) + '/details'

    response = requests.get(link, headers=header)
    content = response.content.decode('utf-8')
    dd = json.loads(content)

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(dd['content'], 'html.parser')

    # 將 HTML 內容轉換為 PDF
    pdf_content = f"""
    <html>
    <head>
        <meta charset='utf8'/>
        <style>
            @font-face {{
                font-family: 'NotoSansTC';
                src: url(D:/yuan_Python_Program/static/NotoSansTC-Regular.ttf) format('truetype');
            }}
            body {{
                font-family: 'NotoSansTC';
            }}
        </style>
    </head>
    <body>
        {str(soup)}
    </body>
    </html>
    """

    # 使用 xhtml2pdf 將 HTML 轉換為 PDF
    output_path = os.path.join(os.getcwd(), f"{dd['topic']}.pdf")
    convert_html_to_pdf(pdf_content, output_path)

    print(f"PDF created successfully at {output_path}")