from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import time
from bs4 import BeautifulSoup

from Settings import Settings

class crawler:

    def __init__(self, name):
        self.name = name

    def Table_1(self,html, nr):
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table')
        if nr == 28:
            titles = Settings.titles1
        elif nr == 29:
            titles = Settings.titles2
        elif nr == 31:
            titles = Settings.titles3
        elif nr == 34:
            titles = Settings.titles4    
        else:
            print("Ungültige Nummer für die Tabelle")
            return    
        # Iterieren über Zeilen und Spalten und Daten zusammenfügen
        result_texts = []
        result_diff = []
        for i, row in enumerate(table.find_all('tr')[1:]):  # Starte ab dem zweiten Dateneintrag (Überschrift überspringen)
            columns = row.find_all('td')
            text = titles[i] + " "  # Hänge den Titel vor den Text
            for col in columns:
                cell_text = col.get_text().strip()
                if "%" in cell_text:  # Prüfen, ob "%" im Text vorhanden ist
                    text += cell_text + " "
                    if "+" in cell_text:
                        diff = Settings.col_green
                    elif "-" in cell_text:
                        diff = Settings.col_red
            if "%" in text:  # Prüfen, ob "%" im Text vorhanden ist
                result_texts.append(text)
                result_diff.append(diff)

        return result_texts, result_diff
    #--------------------------------------------------------------------------------------------------------------------------------------#
    ### Sucht die Tabelle aus, abzählen und -1 nehmen ###

    def parse_item(self, html_page, x):
        html = HTMLParser(html_page)
        tables = html.css("table")                                         
        data = tables[x]
        if x == 28:
            result_texts, diff = crawler.Table_1(self, data.html, x)
        elif x == 29:
            result_texts, diff = crawler.Table_1(self, data.html, x)
        elif x == 31:
            result_texts, diff = crawler.Table_1(self, data.html, x) 
        elif x == 34:
            result_texts, diff = crawler.Table_1(self, data.html, x)       
        else:
            print("Keine Tabelle gefunden!")
            pass
        return result_texts, diff
    #-------------------------------------------------------------------------------------------------------------------------------------#

    def main(self):
        url = Settings.crawl_url
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=Settings.Headless)
            page = browser.new_page()
            page.set_viewport_size(
                {"width": 1280,
                "height": 1440}
                )  
            page.goto(url)
            time.sleep(0.5)
            for x in range(1, 9):
                page.mouse.wheel(0, 1750)
         
                Data0, ColData0 = crawler.parse_item(self, page.content(), Settings.x1)    
                Data1, ColData1 = crawler.parse_item(self, page.content(), Settings.x2)    
                Data2, ColData2 = crawler.parse_item(self, page.content(), Settings.x3)    
                Data3, ColData3 = crawler.parse_item(self, page.content(), Settings.x4)    
                time.sleep(0.5)

            combined_list = Data0 + Data1 + Data2 + Data3
            combined_listCol = ColData0 + ColData1 + ColData2 + ColData3
            print(f"combined list: {combined_list}")
            print(f"combined listCol: {combined_listCol}")
            return combined_list, combined_listCol


if __name__ == "__main__":
    objekt = crawler("name")
    objekt.main()
   