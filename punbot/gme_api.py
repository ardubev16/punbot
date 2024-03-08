#!/usr/bin/env python3

from dataclasses import dataclass
import requests
from punbot.util import icon
from bs4 import BeautifulSoup

BASE_URL = "https://www.mercatoelettrico.org/it/{}"


@dataclass
class Indexes:
    pun: float
    mgp_gas: float

    def __str__(self):
        return f"""
<b>PUN</b>: {self.pun:.5f} €/kWh
<b>MGP Gas</b>: {self.mgp_gas:.5f} €/Smc
        """

    def str_avg(self, avg):
        return f"""
<b>PUN</b>: {self.pun:.5f} €/kWh {icon(self.pun, avg)}
<b>MGP Gas</b>: {self.mgp_gas:.5f} €/Smc {icon(self.mgp_gas, avg)}
        """


def to_float(value: str) -> float:
    return float(value.strip().replace(",", "."))


def to_kwh(value: str) -> float:
    return to_float(value) / 1000


def to_smc(value: str) -> float:
    return to_float(value) * 0.0105833


def get_indexes() -> Indexes:
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
    pun_avg = to_kwh(soup.find("span", {"id": "ContentPlaceHolder1_lblMedia"}).text)
    mgp_gas = to_smc(
        soup.find("table", {"id": "ContentPlaceHolder1_gvMGPGas"})
        .find_all("table")[3]
        .text
    )

    return Indexes(pun=pun_avg, mgp_gas=mgp_gas)


if __name__ == "__main__":
    print(get_indexes())
