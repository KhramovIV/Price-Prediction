from bs4 import BeautifulSoup
import os
import pandas as pd

class parse_html:
    def __init__(self):
        #self.soup = BeautifulSoup()
        self.contents = [html for html in sorted(os.listdir('.')) if '.html' in html]

    def parse_html(self, html):
        with open(html, 'r', encoding='utf8') as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")
        print(f"Открыт файл {html}")
        news_data = []
        items = soup.find_all(class_="list-item")
        for item in items:
            text = item.find(class_="list-item__content").find(class_="list-item__title").text
            try:
                date, views = item.find_all(class_="list-item__info-item")
            except ValueError:
                print(f'Пропускаем файл {html}')
                break
            date = date.text
            views = views.text
            tags = item.find(class_="list-item__tags").find(class_="list-item__tags-list").find_all(class_="list-tag m-add")
            tag_text = []
            href = []
            for tag in tags:
                tag_text.append(tag.text)
                href.append(tag['href'])

            news_data.append({"text": text, 
                              "date": date, 
                              "views": views, 
                              "tag_text": tag_text, 
                              "href": href})
            
        print(f"Файл {html} успешно прочитан")
        html_df = pd.DataFrame(news_data)
        return html_df
    
    def parse_htmls(self):
        df = pd.DataFrame(columns=['text', 'date', 'views', 'tag_text', 'href'])
        for html in self.contents:
            temp_df = self.parse_html(html)
            df = pd.concat([df, temp_df], axis=0)

        df.to_csv("data.tsv", sep='\t')


MyParser = parse_html()
#MyParser.parse_html(MyParser.contents[0])
MyParser.parse_htmls()