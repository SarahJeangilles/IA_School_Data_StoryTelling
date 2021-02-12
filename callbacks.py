#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
import plotly.io as pio
import pandas as pd
import plotly.graph_objs as go
from layouts import df_pie, df_country_tc, df ,human_format, df_first, df_first_td
import numpy as np

    
@app.callback([Output('tc_card_coun','children'),Output('td_card_coun','children')],
              [Input('choose_country','value')])
def update_cards(country_name):
    if country_name == None:
        td_but = str(' ')
        tc_but = str(' ')
    else: 
        df_pays = df[df.COUNTRY == country_name]
        td_but = human_format(df_pays.iloc[-1].TD)
        tc_but = human_format(df_pays.iloc[-1].TC)
    return tc_but, td_but


@app.callback(Output('table_first','children'),
              [Input('choose_first','value'),Input('td_tc','value')])
def update_first(num_first,td_tc):
    n= int(num_first)
    if td_tc == 'TC':
        first = df_first[:n]
    else:
        first = df_first_td[:n]
    
    table = dbc.Table.from_dataframe(first, striped=True, bordered=True, hover=True)
    return table


@app.callback([Output('pop','children'),Output('pib','children'),
               Output('idh','children'),Output('sti','children')],
              [Input('choose_country','value')])
def update_table(country_name):
    if country_name == None:
        pop = str(' ')
        pib = str(' ')
        idh = str(' ')
        sti = str(' ')
    else: 
        df_ind = df[df.COUNTRY == country_name].max()
        pop = human_format(df_ind['pop'])
        pib = human_format(df_ind['gdpcap'])
        idh = human_format(df_ind['hdi'])
        sti = human_format(df_ind['sti'])
    return pop, pib, idh, sti


@app.callback(Output('pie_chart','figure'),
               [Input('td_tc','value')])
def update_pie(td_tc):
    fig = go.Figure(data=[go.Pie(labels=df_pie.index, values=df_pie[td_tc])])
    fig.update_traces(textposition='inside', 
                   textinfo='percent+label')
    fig.update_layout(paper_bgcolor = 'rgba(0, 0, 0, 0)',
                   margin={'l': 10, 'b': 10, 't': 10, 'r': 20},
                   width=350, height=350, showlegend=False)
    return fig


@app.callback(Output('corr_mat','figure'),
               [Input('choose_country','value')])
def update_corrmat(country_name):
    pio.templates.default = "none"
    sns_colorscale = [[0.0, '#3f7f93'], #cmap = sns.diverging_palette(220, 10, as_cmap = True)
     [0.071, '#5890a1'],
     [0.143, '#72a1b0'],
     [0.214, '#8cb3bf'],
     [0.286, '#a7c5cf'],
     [0.357, '#c0d6dd'],
     [0.429, '#dae8ec'],
     [0.5, '#f2f2f2'],
     [0.571, '#f7d7d9'],
     [0.643, '#f2bcc0'],
     [0.714, '#eda3a9'],
     [0.786, '#e8888f'],
     [0.857, '#e36e76'],
     [0.929, '#de535e'],
     [1.0, '#d93a46']]
    
    if country_name == None:
        dfcor = df[['HDI','TC','TD','STI','POP','GDPCAP','COUNTRY']]

    else:
        df_= df[['HDI','TC','TD','STI','POP','GDPCAP','COUNTRY']]
        dfcor = df_[df_.COUNTRY == country_name]
       
    corr = np.array(dfcor.corr())
    X = dfcor.corr().columns.values
    hovertext = [['{},{} <br /> Corr: {}'.format(X[i], X[j],round(corr[i][j],2)) for j in range(len(X))] for i in range(len(X))]
        
    heat = go.Heatmap(z=corr,
                      x=X,
                      y=X,
                      xgap=1, ygap=1,
                      colorscale=sns_colorscale,
                      colorbar_thickness=20,
                      colorbar_ticklen=3,
                      hovertext=hovertext,
                      hoverinfo='text',)
        #                   zmid=0
        
        # title = 'Correlation Matrix'               
        
    layout = go.Layout(title_x=0.5, 
                       width=550, height=500,
                       paper_bgcolor= 'rgba(0, 0, 0, 0)',
                       margin={'l': 10, 'b': 20, 't': 10, 'r': 10},
                       xaxis_showgrid=False,
                       yaxis_showgrid=False,
                       yaxis_autorange='reversed')
           
    fig =go.Figure(data=[heat], layout=layout) 
    return fig


@app.callback(Output('evol_coun','figure'),
               [Input('choose_country','value'), Input('check_value','value')])
def update_evol(country_name, check_param):
    df_coun = df[df.COUNTRY == country_name]
    traces = []
    for i in range(len(check_param)):
        trace = go.Scatter(
                        x = df_coun.DATE,
                        y = df_coun[check_param[i]],
                        mode = "lines",
                        name = check_param[i])
        traces.append(trace)
    
    layout = dict(#title = 'Nombre de cas COVID et mortalité en fonction du temps',
                  margin = {'l': 35, 'b': 40, 't': 10, 'r': 0},
                  plot_bgcolor= 'rgba(0, 0, 0, 0)',
                  paper_bgcolor= 'rgba(0, 0, 0, 0)',
                  width=720,
                  height=400,
                  xaxis = dict(title = 'Date',ticklen = 2,zeroline= False, title_standoff= 40))
    data = traces
    fig = dict(data = data, layout = layout)
    return fig
 

@app.callback(Output('sti_plot','figure'),
               [Input('choose_country','value'), Input('check_value2','value')])
def update_evol(country_name, check_param):
    df_coun = df[df.COUNTRY == country_name]
    traces = []
    trace1 = go.Scatter(
                        x = df_coun.DATE,
                        y = df_coun.STI,
                        mode = "lines",
                        name = 'STI')
    traces.append(trace1)
    for i in range(len(check_param)):
        trace = go.Scatter(
                        x = df_coun.DATE,
                        y = df_coun[check_param[i]],
                        mode = "lines",
                        name = check_param[i])
        traces.append(trace)
    
    layout = dict(#title = 'Nombre de cas COVID et mortalité en fonction du temps',
                  margin = {'l': 35, 'b': 40, 't': 10, 'r': 0},
                  plot_bgcolor= 'rgba(0, 0, 0, 0)',
                  paper_bgcolor= 'rgba(0, 0, 0, 0)',
                  width=720,
                  height=425,
                  xaxis = dict(title = 'Date',ticklen = 2,zeroline= False, title_standoff= 40))
    
    fig = dict(data = traces, layout = layout)
    return fig


@app.callback(Output('bubble_chart','figure'),
               [Input('slide','value')])

def update_slide(slide_param):
    color = df_country_tc.GDPCAP
    df_bub = df_country_tc[:slide_param] 
    
    fig = {
            'data': [
                go.Scatter(
                    x = df_bub.TC,
                    y = df_bub.TD,
                    mode='markers',
                    opacity=0.8,
                    marker={
                        'size': df_bub.POP,
                        'color': color, 
                        'line': {'width': 0.5, 'color': 'white'},
                        'showscale': True,
                        'colorbar': {'title': str(color.name)},
                    },
                     text = df_bub.index
                )
            ],
            'layout': go.Layout(
                title = {
                    # 'text': 'Top %d des pays les plus touchés dans le monde' %n_country,
                    'y':0.95,
                    'x':0.5},
                # xaxis={'title': 'Evolution du nombre de cas '},
                yaxis={
                    'title': {'text':'Nombre de décès cumulés'},
                    'title_standoff': 20, 
                    # 'ticklen' : 30,
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
                margin={'l': 20, 'b': 50, 't': 10, 'r': 10},
                paper_bgcolor = 'rgba(0, 0, 0, 0)',
                legend={'x': 0.0, 'y': 1.0},
                width=650,
                height=425
            )}
    return fig


@app.callback(
    Output("toast", "is_open"),
    [Input("toast_toggle", "n_clicks")],
    # [State("text_button", "is_open")],
)
def open_toast(n):
    if n:
        return True
    return False


@app.callback(
    Output("toast2", "is_open"),
    [Input("toast_toggle2", "n_clicks")],
    # [State("text_button", "is_open")],
)
def open_toastt(n):
    if n:
        return True
    return False


@app.callback(
    Output("toast3", "is_open"),
    [Input("toast_toggle3", "n_clicks")],
    # [State("text_button", "is_open")],
)
def open_toasttt(n):
    if n:
        return True
    return False

@app.callback(
    Output("toast4", "is_open"),
    [Input("toast_toggle4", "n_clicks")],
    # [State("text_button", "is_open")],
)
def open_toast4(n):
    if n:
        return True
    return False

@app.callback(
    Output("toast5", "is_open"),
    [Input("toast_toggle5", "n_clicks")],
    # [State("text_button", "is_open")],
)
def open_toast4(n):
    if n:
        return True
    return False

@app.callback(
    Output("toast6", "is_open"),
    [Input("toast_toggle6", "n_clicks")],
    # [State("text_button", "is_open")],
)
def open_toast4(n):
    if n:
        return True
    return False
    # trace1 = go.Scatter(
    #                     x = df_coun.DATE,
    #                     y = df_coun.TC,
    #                     mode = "lines",
    #                     name = "TC",
    #                     marker = dict(color = 'rgba(16, 112, 2, 0.8)'))
    # #                     text = df.university_name)
    # # Création de la trame 2
    # trace2 = go.Scatter(
    #                     x = df_coun.DATE,
    #                     y = df_coun.TD,
    #                     mode = "lines+markers",
    #                     name = "TD",
    #                     marker = dict(color = 'rgba(80, 26, 80, 0.8)'))
    # #                     text = df.university_name)
    
    # data = [trace1, trace2]
    # layout = dict(#title = 'Nombre de cas COVID et mortalité en fonction du temps',
    #               margin = {'l': 35, 'b': 40, 't': 10, 'r': 0},
    #               plot_bgcolor= 'rgba(0, 0, 0, 0)',
    #               paper_bgcolor= 'rgba(0, 0, 0, 0)',
    #               width=720,
    #               height=425,
    #               xaxis = dict(title = 'Date',ticklen = 2,zeroline= False, title_standoff= 40))
                
    # fig = dict(data = data, layout = layout)

# @app.callback(
#     Output('evol_of_tc', 'children'),
#     [Input('idtc', 'value')])

# def display_value(value):
#     return 'You have selected "{}"'.format(value)


# @app.callback(
#     Output('evol_of_td', 'children'),
#     [Input('idtd', 'value')])

# def display_value(value):
#     return 'You have display"{}"'.format(value)