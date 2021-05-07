#!/usr/bin/env python3 -*-coding: utf-8 -*- pylint: 
# disable=invalid-name,no-member
import json

import requests
from bs4 import BeautifulSoup


class UrlGen(object):

    def __init__(self, owm_url, geo_url, api_key, units='metric', lang='ja', mode='xml'):
        self._owm_url = owm_url
        self._geo_url = geo_url
        self._params = {
            'units': units,
            'lang': lang,
            'mode': mode,
            'appid': json.load(api_key.open('rb'))['api_key']
        }

    def from_zip(self, zip_code):
        params = self._params.copy()
        params['zip'] = f'{zip_code},jp'
        return self._owm_url, params

    def from_xy(self, x, y, units='metric', lang='ja', mode='xml'):
        params = self._params.copy()
        params['lon'] = x
        params['lat'] = y
        return self._owm_url, params

    def zip2xy(self, zip_code, mode='xml'):
        if '-' in zip_code:
            zip_code = zip_code.replace('-', '')

        params = {
            'method': 'searchByPostal',
            'postal': zip_code,
        }
        req = requests.get(f'{self._geo_url}{mode}', params=params)
        if req.status_code > 400:
            print(req.status_code)
            return None, None

        print_status(req.headers)
        soup = BeautifulSoup(req.text, features='html.parser')
        try:
            x = float(soup.response.location.x.string)
            y = float(soup.response.location.y.string)
        except AttributeError as e:
            print(e)
            print(soup.response.error)
            return None, None

        return x, y


def print_status(in_dict):
    for i, (key, item) in enumerate(in_dict.items()):
        print(f'{i:2} | {key}\t{item}')


def get_txt(args, fc_type):
    ug = UrlGen(
        'http://api.openweathermap.org/data/2.5/',
        'http://geoapi.heartrails.com/api/',
        args.api_key
    )
    url, params = ug.from_zip(args.zip_code)
    url = f'{url}{fc_type}'

    req = requests.get(url, params=params)
    print_status(req.headers)
    if req.status_code < 400:
        return req.text

    # openweathermapの郵便番号検索が上手く機能しなかった場合、
    # geoapiで郵便番号から緯度経度を算出して場所を特定する
    print(req.status_code)
    x, y = ug.zip2xy(args.zip_code)
    if x is None:
        return None

    print(f'geoapi:{args.zip_code} -> ({x}, {y})')
    url, params = ug.from_xy(x, y)
    url = f'{url}{fc_type}'

    req = requests.get(url, params=params)
    print_status(req.headers)
    if req.status_code < 400:
        return req.text

    # それでも見つからない場合はNoneを返す
    print(req.status_code)
    return None
