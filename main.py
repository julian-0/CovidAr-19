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
import os

FRECUENCIA = 2
url='https://bots.lucasmercado.ar/json/covid-19/daily-arg.csv'
#url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/01-22-2020.csv'

script_dir = os.path.dirname(__file__)
rel_path = "data.csv"
abs_path_data = os.path.join(script_dir, rel_path)

formatoImg = ".png"

#ae^bx
def funcion(x,a,b):
    '''Modelo exponencial'''
    return a*np.exp(b*x)

def graficar():
    archivo=pd.read_csv(abs_path_data)

    dias = archivo['Dia'].values
    
    # Convierte string en datetime
    xdat = [datetime.strptime(d, "%Y-%m-%d") for d in dias]

    ydat= archivo['Delta_Confirmados'].values
    
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
    
    hoy = datetime.today().strftime("%Y-%m-%d")
    nombre = os.path.join(script_dir, hoy+"infectados"+formatoImg)
    
    plt.savefig(nombre)
    
    
def obtener_daily():
    header = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
            }
    res = requests.get(url, headers=header)
    data = pd.read_csv(StringIO(res.text),sep=",")

    data.loc[0, 'Dia'] = datetime.strptime(data['Dia'][0], ' %Y-%m-%d').strftime("%Y-%m-%d") #le saca el espacio
    return data
    

def actualizar_datos(data):
    historico = pd.read_csv(abs_path_data)
    
    if data['Dia'][0]!=historico['Dia'][len(historico)-1]:
    
        mover = [('Delta_Confirmados','Confirmados'),
                 ('Delta_Muertos','Muertos'),
                 ('Delta_Recuperados','Recuperados')]
        
        data.insert(len(data.columns),'Activos',0)
    
        for (delta,categoria) in mover:
            data.insert(len(data.columns),delta,data[categoria][0])
    
        sumar = ['Confirmados','Muertos','Recuperados']
        ult_pos = len(historico)-1
        
        for categoria in sumar:
            data.loc[0,categoria] = historico[categoria][ult_pos]+data[categoria][0]
    
        data.loc[0,'Activos'] = historico['Confirmados'][ult_pos]-data['Muertos'][0]-data['Recuperados'][0]
        
        data.to_csv(abs_path_data, mode='a', header=False, index=False)
    
    else:
        print("Los datos del dia "+ data['Dia'][0] + " ya estan almacenados")



data = obtener_daily()
actualizar_datos(data)
graficar()
print("Script finalizado")