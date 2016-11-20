from bs4 import BeautifulSoup
import requests


response = requests.get('http://www.bjmb.gov.cn/')
bs = BeautifulSoup(response.content, 'lxml')

win_div = bs.find('div', attrs={'class': 'win_div'})
date = win_div.find('h6').find('span').string
cond = win_div.find('div', attrs={'class': 'ri_div'}).find('label').string
print(cond)