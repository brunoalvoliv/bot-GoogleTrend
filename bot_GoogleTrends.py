#Importando bibliotecas

import pandas as pd
import numpy as np
from pytrends.request import TrendReq

#Buscando dados

pytrends = TrendReq(hl='en-US', tz=360)

all_keywords = ['Política', 'Bolsonaro']

keywords = []

timeframes = ['today 5-y', 'today 12-m', 'today 3-m', 'today 1-m']
geo = 'BR'
cat = 0
gprop = ''

def check_trends():
    pytrends.build_payload(keywords, cat, timeframes[0], geo, gprop)

    data =  pytrends.interest_over_time()
    mean = round(data.mean(), 2)
    avg = round(data[kw][-52:].mean(), 2) #último ano
    avg2 = round(data[kw][:52].mean(), 2) #primeiro ano 
    trend = round(((avg / mean[kw]) - 1) * 100, 2)
    trend2 = round(((avg / mean[kw]) - 1) * 100, 2)
    print('A média dos 5 anos por ' + kw + ' foi ' + str(mean[kw]) + '.')
    print('O interesse por ' + kw + ', comparado aos últimos 5 anos, teve uma mudança de ' + str(trend) + '%.')
    print('')

    #Tendência estável 
    if mean[kw] > 75 and abs(trend) <= 5:
        print('O interesse por ' + kw + ' está estável comparado aos últimos 5 anos.') 
    elif mean[kw] > 75 and trend > 5:
        print('O interesse por ' + kw + ' está estável e crescendo comparado aos últimos 5 anos.')
    elif mean[kw] > 75 and trend < -5:
        print('O interesse por ' + kw + ' está estável e decrescendo comparado aos últimos 5 anos.')

    #Tendência relativamente estável
    elif mean[kw] > 60 and abs(trend) < 15:
        print('O interesse por ' + kw + ' está relativamente estável comparado aos últimos 5 anos.') 
    elif mean[kw] > 60 and trend > 15:
        print('O interesse por ' + kw + ' está relativamente estável e crescendo comparado aos últimos 5 anos.')
    elif mean[kw] > 60 and trend < -15:
        print('O interesse por ' + kw + ' está relativamente estável e decrescendo comparado aos últimos 5 anos.')
    
    #Sazonalidade
    elif mean[kw] > 20 and abs(trend) <= 15:
        print('O interesse por ' + kw + ' é sazonal.')

    #Palavra nova
    elif mean[kw] > 20 and trend > 15:
        print('O interesse por ' + kw + ' é novo.')

    #Declínio pelo interesse pela palavra
    elif mean[kw] > 20 and trend < -15:
        print('O interesse por ' + kw + ' está decrescendo.')

    #Interesse cíclico
    elif mean[kw] > 5 and abs(trend) <= 15:
        print('O interesse por ' + kw + ' é cíclico.')
    
    #Novo
    elif mean[kw] > 0 and trend > 15:
        print('O interesse por ' + kw + ' é novo e possui tendência.')

    #Decaindo
    elif mean[kw] > 0 and trend < -15:
        print('O interesse por ' + kw + ' está declinando e não possui pico.')

    #Outros:
    else:
        print('Checar!')

    print('')

for kw in all_keywords:
    keywords.append(kw)
    check_trends()
    keywords.pop()