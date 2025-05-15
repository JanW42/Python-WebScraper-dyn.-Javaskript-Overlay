from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import time
from bs4 import BeautifulSoup
import icecream as ic
from icecream import ic

from Settings import Settings

class crawler2:

    def __init__(self, name):
        self.name = name

    def count_players_in_gang(self, gang_players, all_players):
        count = 0
        for gang, player in gang_players.items():
            if player in all_players:
                count += 1
                print (f"{gang}: {player}")
        return count
    
    def count_item_players_in_gang(self, gang_players, all_players):
        count = 0
        for player in gang_players.values():
            if player in all_players:
                count += 1
        return count

    def Player_table(self,html, nr):
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find('table') 
        # Iterieren über Zeilen und Spalten und Daten zusammenfügen
        result_texts = []
        a = len(table.find_all('tr'))
        print(f"Es sind {a} Spieler Online")
        
        player_number = 2  # Starte ab dem zweiten Dateneintrag (Überschrift überspringen)

        for i in range(2, a):  # Starte ab dem zweiten Dateneintrag (Überschrift überspringen)
            tr_tag = table.find_all('tr')[i]  # Hole das i-te tr-Tag
            a_tag = tr_tag.find('td').a  # Suche nach dem a-Tag im ersten td-Tag

            if a_tag is None or not a_tag.text.strip():  # Wenn Name leer ist oder nicht vorhanden ist
                continue
            else:
                name = a_tag.text.strip()
                #print(f"Name von Spieler {player_number}: {name}")
                result_texts.append(name)
                player_number += 1  # Inkrementiere die Spielerzahl unabhängig davon, ob der Name leer ist oder nicht

        return result_texts
    #--------------------------------------------------------------------------------------------------------------------------------------#
    ### Sucht die Tabelle aus, abzählen und -1 nehmen ###

    def parse_item(self, html_page, x):   
        html = HTMLParser(html_page)
        tables = html.css("table")    
        data = tables[x]
        if x == 0:
            result_texts = crawler2.Player_table(self, data.html, x) 
        else:
            print("Keine Tabelle gefunden!")
            pass
        return result_texts
    #-------------------------------------------------------------------------------------------------------------------------------------#
  
    def main(self):
        url = Settings.crawl2_url
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=Settings.Headless)
            page = browser.new_page()
            page.set_viewport_size(
                {"width": 1280,
                "height": 1440}
                )
            page.goto(url)

            page.wait_for_load_state('load')

            try:
                for x in range(1, 2):
                    page.mouse.wheel(0, 1750)
                        #print("scrolling key press", x)    !!!  hier einstellen was man haben möchte  !!!
                    player_list = crawler2.parse_item(self, page.content(), Settings.x5)      # Gangcount 
                    Group1_results = crawler2.count_players_in_gang(self, Settings.POLbest_player_dict ,player_list)
                    Group2_results = crawler2.count_players_in_gang(self, Settings.POLgood_player_dict ,player_list)
                    Group3_result = crawler2.count_players_in_gang(self, Settings.BB_player_dict ,player_list)
                    Group4_result = crawler2.count_players_in_gang(self, Settings.AMG_players_dict ,player_list)
                    Group5_result = crawler2.count_players_in_gang(self, Settings.cl_player_dict ,player_list)
                    Group6_result = crawler2.count_players_in_gang(self, Settings.sechser_player_dict ,player_list)
                    Group7_results = crawler2.count_players_in_gang(self, Settings.AP_player_dict ,player_list)
                    Group8_results = crawler2.count_players_in_gang(self, Settings.BF_player_dict ,player_list)
                    Group9_results = crawler2.count_players_in_gang(self, Settings.AND_player_dict ,player_list)
                    
                    data0 = f"here_shortname {Group1_results}"
                    data1 = f"here_shortname {Group2_results}"
                    data2 = f"here_shortname {Group3_result}"
                    data3 = f"here_shortname {Group4_result}"
                    data4 = f"here_shortname {Group9_results}"
                    data5 = f"here_shortname {Group6_result}"
                    data6 = f"here_shortname {Group7_results}"
                    data7 = f"here_shortname {Group8_results}"
                    data8 = f"here_shortname {Group5_result}"
                   
                    combined_list = [data0, data1, data2, data3, data4, data5, data6, data7, data8]#, data9]
                    ic("jetzt am ende update Groups")
                    ic()
                return combined_list
            except Exception as e1:
                    print(f"An error occurred: {e1}")
                    try:
                        # Warten, bis das Checkbox-Element sichtbar ist und dann darauf klicken
                        page.wait_for_selector("label.cb-lb input[type='checkbox']", timeout=10000)
                        page.click("label.cb-lb input[type='checkbox']")
                        print("Checkbox clicked successfully.")
                        
                    except Exception as e2:
                        print(f"An error occurred: {e2}")


if __name__ == "__main__":
    objekt = crawler2("name")
    objekt.main()
   