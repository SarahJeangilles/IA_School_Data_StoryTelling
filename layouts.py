#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np


df = pd.read_csv('data2.csv', sep=';')
df_raw = pd.read_csv('raw_data.csv')

df[['HDI','STI','POP','GDPCAP']] = df[['HDI','STI','POP','GDPCAP']].stack().str.replace(',','.').unstack().astype(float)
df[['tc','td']]= df[['TC','TD']].stack().str.replace(',','.').unstack().astype(float)
df[['TC','TD']] = df_raw[['total_cases','total_deaths']]
df['DATE']= pd.to_datetime(df['DATE'])

df[['pop','hdi','gdpcap','sti']] = df_raw[['population','human_development_index','gdp_per_capita','stringency_index']]



df_geo = df.fillna(0).groupby('COUNTRY').last()
df_geo['COUNTRY']=df_geo.index
# df_geo['tc_taux']= [(df_geo['TC'][i]/df_geo['pop'][i])*100 for i in range(len(df_geo['TC']))]

def human_format(num):
    num = float('{:.4g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

df_evol = df.groupby(pd.Grouper(key='DATE', freq='W')).sum()
df_but = df_evol.iloc[-1]
but1 = human_format(int(df_evol.iloc[-1].TC))
but2 = human_format(int(df_evol.iloc[-1].TD))

def first_countries(n, feat):
    return df.groupby('COUNTRY').last().nlargest(n, columns = feat)

n_country = 25
df_country_tc = first_countries(n_country, 'tc')
df_country_td = first_countries(n_country, 'td')

df_pie = first_countries(30, 'TC')

df_first = pd.DataFrame(
    {
        "Rang": list(range(1,11)),
        "Pays": df_country_tc[:10].index,
        "Total de cas cumulés (TC)": [human_format(i) for i in df_country_tc[:10].TC],
    }
)
df_first_td = pd.DataFrame(
    {
        "Rang": list(range(1,11)),
        "Pays": df_country_td[:10].index,
        "Total de décès cumulés (TD)": [human_format(i) for i in df_country_td[:10].TC],
    }
)

# scatter Tc vs TD vs PIB
fig = px.scatter_geo(df_geo, locations= 'CODE', hover_name='COUNTRY', size= "TD", width=760, height=500)
fig_ = px.choropleth(df_geo, color="TC", locations="CODE", width=720, height=425)
fig0 = fig_.add_trace(fig.data[0])
fig0.update_layout({
    'margin': {'l': 50, 'b': 8, 't': 5, 'r': 5},    #b = marge du bas ; l= marges left ;  
    'autosize':True,
    # 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

color = df_country_tc.HDI
fig2 = {
        'data': [
            go.Scatter(
                x = df_country_tc.TC,
                y = df_country_tc.TD,
                mode='markers',
                opacity=0.8,
                marker={
                    'size': df_country_tc.POP,
                    'color': color, 
                    'line': {'width': 0.5, 'color': 'white'},
                    'showscale': True,
                    'colorbar': {'title': str(color.name)},
                },
                 text = df_country_tc.index
            )
        ],
        'layout': go.Layout(
            title = {
                # 'text': 'Top %d des pays les plus touchés dans le monde' %n_country,
                'y':0.95,
                'x':0.5},
            # xaxis={'title': 'Evolution du nombre de cas '},
            yaxis={
                'title': 'Nombre de décès cumulés',
                'title_standoff': 5, 
                'ticklen' : 10,
                'tickcolor' :'rgba(0,0,0,0)',
                'titlefont': dict(color = 'LightSlateGrey'), 
                'tickfont': dict(color = 'LightSlateGrey'),
                'zeroline':False},
            xaxis = {
                'title': 'Nombre de cas cumulés', 
                'autorange':'reversed',
                'zeroline':False,
                'title_standoff': 20, 
                'ticklen' : 10,
                'tickcolor' :'rgba(0,0,0,0)',
                'titlefont': dict(color = 'LightSlateGrey'), 
                'tickfont': dict(color = 'LightSlateGrey')},
            margin={'l': 80, 'b': 50, 't': 10, 'r': 10},
            paper_bgcolor = 'rgba(0, 0, 0, 0)',
            legend={'x': 0.0, 'y': 1.0},
            width=720,
            height=425
            # hovermode='closest'
        )}
 
trace1 = go.Bar(
                x = df_evol.index,
                y = df_evol.td,
                name = "Mortalité",
                marker = dict(color = 'rgba(255, 174, 255, 0.5)',
                             line = dict(color ='rgb(0,0,0)',width =0.25)))
#                 text = df_first_TD.index)

# Création de la deuxième trace 
trace2 = go.Bar(
                x = df_evol.index,
                y = df_evol.tc,
                name = "Nb de cas",
                marker = dict(color = 'rgba(255, 255, 128, 0.5)',
                              line = dict(color = 'rgb(0,0,0)',width = 0.25)))
#                 text = df_first_TD.index)

data = [trace1, trace2]
layout = go.Layout(barmode = "group")
fig3 = go.Figure(data = data, layout = layout)
fig3.update_layout({
    'autosize':True,
    'width':720, 
    'height':425,
    # 'xaxis':{'title_standoff': 40},
    # 'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    # 'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'margin':{'l': 35, 'b': 50, 't': 10, 'r': 0}
    })
      
# fig.show() 

# data.sort_values("Date", inplace=True)
#data = data.query("type == 'conventional' and region == 'Albany'")


