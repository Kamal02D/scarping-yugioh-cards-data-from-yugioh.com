# special thanks to https://www.yugioh.com

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

df = None


def scrape_card_info(link):
    global df # use the global version of the
    index = len(df.index) - 1
    page_html = requests.get(link,).text
    # creating our soup
    soup = BeautifulSoup(page_html, "lxml")
    # getting the attributes
    atrs = soup.find("div", {"class": "text-holder"}).find_all("li")
    atrs = [atr.text for atr in atrs]
    for atr in atrs:
        if re.match("^level", atr, re.IGNORECASE):
            # modify the last row
            df.iloc[index, 5] = atr[atr.index(":") + 1:].strip()
        if re.match("^type", atr, re.IGNORECASE):
            df.iloc[index, 6] = atr[atr.index(":") + 1:].strip()
        if re.match("^Card Type", atr, re.IGNORECASE):
            df.iloc[index, 4] = atr[atr.index(":") + 1:].strip()
        if re.match("^def", atr, re.IGNORECASE):
            df.iloc[index, 3] = atr[atr.index(":") + 1:].strip()
        if re.match("^atk", atr, re.IGNORECASE):
            df.iloc[index, 2] = atr[atr.index(":") + 1:].strip()


def initDf():
    """ initiates a dataframe"""
    global df
    df = pd.DataFrame(columns=["card_name", "image", "attack", "defence", "card_type", "level", "type"])


def run():
    global df
    link = "https://www.yugioh.com/cards.yu-gi-oh!?page={}"
    # there are a total of 143 page
    for i in range(143):
        print(f"scraping page {(i+1)} ...")
        page_html =requests.get(link.format(i+1)).text
        # creating our soup
        soup = BeautifulSoup(page_html, "lxml")
        # the cards are in div called main
        cards = soup.find("div", {"id": "main"})
        cards_list = cards.find("ul", {"class": "cards-list"}).find_all("li")
        for indx ,oneCard in enumerate(cards_list):
            name = oneCard.a.strong.text
            image = oneCard.a.img["src"]
            card_info_link = "https://www.yugioh.com{}".format(oneCard.a["href"])
            df_temp = pd.DataFrame({"card_name": [name],
                                    "image": [image]
                                    })
            df = pd.concat([df, df_temp], ignore_index=True)
            df.reset_index()
            scrape_card_info(card_info_link)

    print("done")
    df.to_csv("yugioh_data.csv", index=False)


if __name__ == '__main__':
    initDf()
    run()
