# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 12:42:58 2020

@author: Ordóñez
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates
from datetime import datetime
import requests
from io import StringIO

FRECUENCIA = 2
url='https://bots.lucasmercado.ar/json/covid-19/daily-arg.csv'
#url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-22-2020.csv'

#ae^bx
def funcion(x,a,b):
    '''Modelo exponencial'''
    return a*np.exp(b*x)

def graficar():
    archivo=pd.read_csv('data.csv')

    dias = archivo['Dia'].values
    
    # Convierte string en datetime
    xdat = [datetime.strptime(d, "%Y-%m-%d") for d in dias]

    ydat= archivo['Confirmados'].values
    
    # Dibuja
    fig, ax = plt.subplots()
    ax.plot(xdat, ydat,'ro', mew=1, linestyle='solid')
    
    # Rota los ticks
    fig.autofmt_xdate()
    
    # Formatea las fechas
    date_format = mpl_dates.DateFormatter('%d/%m')
    ax.xaxis.set_major_formatter(date_format)
    
    # Permite manipular los ticks por dia
    locator = mpl_dates.DayLocator()
    ax.xaxis.set_major_locator(locator)
    
 
    ax.set(title='COVID-19 en Argentina',
           xlabel='Dia',
           ylabel='Casos Positivos')
    
    # Agrega el cuadriculado
    ax.grid()

    # Ticks limites en las abscisas
    ax.set_xlim(xmin=xdat[0])
    ax.set_xlim(xmax=xdat[-1])
    
    # Frecuencia de dias que muestra
    ax.set_xticks(ax.get_xticks()[::FRECUENCIA])

    # Afina los bordes    
    fig.tight_layout()
    
    plt.savefig("test.png")
    
def agregar_daily():
    header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
            }
    res = requests.get(url, headers=header)
    data = pd.read_csv(StringIO(res.text),sep=",")
    data.loc[0, 'Dia'] = datetime.strptime(data['Dia'][0], ' %Y-%m-%d').strftime("%Y-%m-%d") #le saca el espacio
    data.to_csv("data.csv", mode='a', header=False, index=False)
