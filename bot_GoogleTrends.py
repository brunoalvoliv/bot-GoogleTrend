#Importando bibliotecas

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pytrends.request import TrendReq

plt.style.use('ggplot')

#Buscando dados

pytrends = TrendReq(hl='en-US', tz=360)

all_keywords = ['Bitcoin', 'Magazine Luiza', 'Wege']

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

'''for kw in all_keywords:
    keywords.append(kw)
    check_trends()
    keywords.pop()'''

def comparacao():
    plt.figure(figsize=(12, 6))
    x_pos = np.arange(len(all_keywords))

    #Last 5-years
    pytrends.build_payload(all_keywords, cat, timeframes[0], geo, gprop)

    data =  pytrends.interest_over_time()
    media = data.mean()
    media = round(media / media.max() * 100, 2)
    ax1 = plt.subplot2grid((3, 2), (0, 0), rowspan=1, colspan=1)
    ax2 = plt.subplot2grid((3, 2), (0, 1), rowspan=1, colspan=1)
    for kw in all_keywords:
        ax1.plot(data[kw], label=kw)
    ax2.bar(x_pos, media, align='center')
    plt.xticks(x_pos, all_keywords)

    #Last 12-months
    pytrends.build_payload(all_keywords, cat, timeframes[1], geo, gprop)

    data =  pytrends.interest_over_time()
    media = data.mean()
    media = round(media / media.max() * 100, 2)
    ax3 = plt.subplot2grid((3, 2), (1, 0), rowspan=1, colspan=1)
    ax4 = plt.subplot2grid((3, 2), (1, 1), rowspan=1, colspan=1)
    for kw in all_keywords:
        ax3.plot(data[kw], label=kw)
    ax4.bar(x_pos, media, align='center')
    plt.xticks(x_pos, all_keywords)

    #Last 3-months
    pytrends.build_payload(all_keywords, cat, timeframes[2], geo, gprop)

    data =  pytrends.interest_over_time()
    media = data.mean()
    media = round(media / media.max() * 100, 2)
    ax5 = plt.subplot2grid((3, 2), (2, 0), rowspan=1, colspan=1)
    ax6 = plt.subplot2grid((3, 2), (2, 1), rowspan=1, colspan=1)
    for kw in all_keywords:
        ax5.plot(data[kw], label=kw)
    ax6.bar(x_pos, media[0: len(all_keywords)], align='center')
    plt.xticks(x_pos, all_keywords)

    ax1.set_ylabel('Últimos 5 anos')
    ax3.set_ylabel('Último ano')
    ax5.set_ylabel('Últimos 3 meses')
    ax1.set_title('Interesse por todo tempo', fontsize=14)
    ax2.set_title('Interesse por período', fontsize=14)
    ax5.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m'))
    ax1.legend()
    ax3.legend()
    ax5.legend()
    plt.show()

for kw in all_keywords:
    keywords.append(kw)
    check_trends()
    keywords.pop()

comparacao()

# SCRIPT FINALIZADO!