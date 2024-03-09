#!/usr/bin/env python3

from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.mercatoelettrico.org/it/{}"


def icon(avg: float, new_value: float):
    diff = new_value - avg
    if diff > 0:
        return "📈"
    elif diff < 0:
        return "📉"
    else:
        return "🔷"


@dataclass
class Prices:
    pun: float
    mgp: float

    def __str__(self):
        return f"""
<b>PUN</b>: {self.pun:.5f} €/kWh
<b>MGP</b>: {self.mgp:.5f} €/Smc
        """

    def str_with_diff(self, new_prices: "Prices") -> str:
        return f"""
<b>PUN</b>: {self.pun:.5f} €/kWh {icon(self.pun, new_prices.pun)}
<b>MGP</b>: {self.mgp:.5f} €/Smc {icon(self.mgp, new_prices.mgp)}
        """


def to_float(value: str) -> float:
    return float(value.strip().replace(",", "."))


def to_kwh(value: str) -> float:
    return to_float(value) / 1000


def to_smc(value: str) -> float:
    return to_float(value) * 0.0105833


def get_prices() -> Prices:
    response = requests.get(BASE_URL.format("tools/AccessoDati.aspx"))
    soup = BeautifulSoup(response.text, "html.parser")
    inputs = {i["name"]: i.get("value") for i in soup.find_all("input")}
    data = {
        "__VIEWSTATE": inputs["__VIEWSTATE"],
        "__EVENTVALIDATION": inputs["__EVENTVALIDATION"],
        "ctl00$ContentPlaceHolder1$CBAccetto1": "on",
        "ctl00$ContentPlaceHolder1$CBAccetto2": "on",
        "ctl00$ContentPlaceHolder1$Button1": "Accetto",
    }

    s = requests.Session()
    s.post(BASE_URL.format("tools/AccessoDati.aspx"), data=data)
    response = s.get(BASE_URL.format("default.aspx"))
    soup = BeautifulSoup(response.text, "html.parser")
    pun = to_kwh(soup.find("span", {"id": "ContentPlaceHolder1_lblMedia"}).text)
    mgp = to_smc(
        soup.find("table", {"id": "ContentPlaceHolder1_gvMGPGas"})
        .find_all("table")[3]
        .text
    )

    return Prices(pun=pun, mgp=mgp)


if __name__ == "__main__":
    print(get_prices())
