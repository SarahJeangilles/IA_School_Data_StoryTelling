#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from app import app
from app import server
from layouts import fig0, fig2, fig3, but1, but2, df, df_country_tc, df_first

# import plotly.express as px
# from dash.dependencies import Input, Output
import callbacks

pays = df['COUNTRY'].unique()
check_value = ['tc','td','HDI','POP','GDPCAP']
td_tc=['TC','TD']

n_country = 25

url_bar_and_content_div = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# =============================================================================
# barre de navigation
# =============================================================================
navbar = dbc.NavbarSimple(
    children=[
        dbc.Row([
            dbc.Col(
                dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Page 1", "Internal link", href="/"),
                    dbc.DropdownMenuItem("Page 2","Internal link", href="/page-2"),
                    # dbc.DropdownMenuItem("Page 3","Internal link", href="/page-3"),
                    ],
            nav=True,
            in_navbar=True,
            label="Menu",
        )),
    ])],
    brand='Dash - Impact de la COVID-19 sur l\'économie mondiale',
    brand_href="#",
    # style = {'navbar-brand':{'font_size':'80px'}},
    color="Brown",
    dark=True,
)

# =============================================================================
# cards 
# =============================================================================
card1= dbc.Card([
    dbc.CardBody([
        dbc.Row([html.H2(str(but1), className="card-title"),
        html.P("cas cumulés dans le monde",style={'font-size':'15px', 'margin-top':'0', 'text-align':'center'},className="card-text")]
                ,justify='center'),
        ])
    ],color="secondary", inverse = True, id = 'tc_card')

card2= dbc.Card([
    dbc.CardBody([
        dbc.Row([html.H2(str(but2), className="card-title"),
        html.P("décès cumulés dans le monde",style={'font-size':'15px','margin-left':'0px','margin-top':'0', 'text-align':'center'}, className="card-text")]
                ,justify='center')
        ])
    ], color="secondary", inverse = True, id = 'td_card')


card3= dbc.Card([
    dbc.CardBody([
        html.H2(className="card-title", id = 'tc_card_coun',style={'text-align':'center'}),
        html.P("cas cumulés",style={'font-size':'16px','margin-left':'0px','margin-top':'0', 'text-align':'center'}, className="card-text"),
        ])
    ],color="secondary", inverse = True)

card4= dbc.Card([
    dbc.CardBody([
        html.H2(className="card-title", id = 'td_card_coun',style={'text-align':'center'}),
        html.P("décès cumulés",style={'font-size':'16px','margin-left':'0px','margin-top':'0', 'text-align':'center'}, className="card-text"),
        ])
    ],color="secondary", inverse = True)

cards = dbc.Row([dbc.Col(card1, width=6), dbc.Col(card2, width=6)], justify = 'center')
cards_coun = dbc.Row([dbc.Col(card3), dbc.Col(card4)], justify = 'center')

# =============================================================================
# dropdown & radioitems
# =============================================================================
coun_choice = dcc.Dropdown(
    id='choose_country',
    options=[{'label': i, 'value': i} for i in pays],
    placeholder = 'Sélectionnez un pays',
    # value='France'
    )

first_choice = dcc.Dropdown(
    id='choose_first',
    options=[{'label': i, 'value': i} for i in list(range(1,11))],
    #placeholder = 'Sélectionnez un pays',
    value='3'
    )

cov_choice = dcc.RadioItems(
    id='td_tc',
    options=[{'label': i, 'value': i} for i in td_tc],
    value='TC',
    labelStyle={'display': 'inline-block', 'margin-right':'10px','margin-left':'10px'},
    inputStyle={'margin-left':'0px','padding': '0 0 0 0','margin-right':'0px'})

# =============================================================================
# tables
# =============================================================================

row1 = html.Tr([html.Td("Poulation: "), html.Td(id= 'pop')])
row2 = html.Tr([html.Td("PIB: "), html.Td(id= 'pib')])
row3 = html.Tr([html.Td("IDH: "), html.Td(id= 'idh')])
row4 = html.Tr([html.Td("STI: "), html.Td(id= 'sti')])

table1 = html.Div(id='table_first')

table = dbc.Table([html.Tbody([row1,row2,row3,row4])], 
                  dark= True, 
                  responsive= True,
                  # className = 'active',
                  # style={'background-color':'Teal'},
                  bordered=True,
                  hover=True)

# =============================================================================
# checklist & slider
# =============================================================================
check = dcc.Checklist(
    id = 'check_value',
    options=[{'label': i, 'value': i} for i in check_value],
    value=['tc', 'GDPCAP'],
    labelStyle={'display': 'inline-block','margin-right':'20px','margin-left':'20px'}
) 

check1 = dcc.Checklist(
    id = 'check_value2',
    options=[
        {'label': 'TC', 'value': 'tc'},
        {'label': 'TD', 'value': 'td'}],
    value=['tc'],
    labelStyle={'display': 'inline-block','margin-right':'20px','margin-left':'20px'}
)
slider = dcc.Slider(
    id = 'slide',
    min=4,
    max=30,
    vertical = True,
    #step=None,
    marks={
        5: '5',
        10: '10',
        15: '15',
        20: '20',
        25: '25'
    },
    value=25
) 
# =============================================================================
# TOASTS
# =============================================================================
toast5 = html.Div([
            html.H1(
                    dbc.Button(
                        "Analyse des données (1)",
                        color="link",
                        id="toast_toggle6",
                    )
                ),
            dbc.Toast([
                    dcc.Markdown('''Pour observer la matrice de corrélation des indicateurs pour tous les pays, cliquer sur l'onglet "Corrélation" sans sélectionner de pays. 
On s'aperçoit qu'aucun lien ne ressort entre les mesures de sécurité sanitaires(STI) et les indicateurs COVID (TC, TD) ni les indicateurs COVID et les indicateurs économiques (HDI,GDPCAP). Par contre, on observe logiquement une corrélation positive entre l'indice de développement humain et le PIB, également entre le total de cas et décès cumulés. Cette dernière observation laisse supposer que la matrice est bien cohérente. ''')],
            id="toast6",
            header="Corrélation entre les indicateurs économiques et covid",
            is_open=False,
            dismissable=True,
            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", 'overflowX':'hidden', 'height':300, "top": 66, "right": 10, "width": 400},)
])


toast6 = html.Div([
            html.H1(
                    dbc.Button(
                        "Analyse des données (3)",
                        color="link",
                        id="toast_toggle5",
                    )
                ),
            dbc.Toast([
                    dcc.Markdown('''Comme la figure précédente, les effets bénéfiques des mesures de restrictions ne sont pas visibles à court-terme. La normalisation des données ne permet pas de mettre en évidence que certains pays ont des indices STI plus faibles (par exemple l'Inde) que d'autres et d'observer par conséquent les effets sur la gestion de la crise. Il aurait fallu réaliser cette analyse sur une plus grande période. ''')],
            id="toast5",
            header="Effets des mesures de restrictions sanitaires",
            is_open=False,
            dismissable=True,
            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", 'overflowX':'hidden', 'height':300, "top": 66, "right": 10, "width": 400},)
])
            
            
toast4 = html.Div([
            html.H1(
                    dbc.Button(
                        "Analyse des données (2)",
                        color="link",
                        id="toast_toggle4",
                    )
                ),
            dbc.Toast([
                    dcc.Markdown('''Cette figure montre l'évolution des indicateurs économiques en fonction du temps. Les données utilisées sont des données transformées probablement standardisées pour mettre les données à la même échelle et les rendre "comparables". On observe que les indicateurs économiques restent constant dans le temps malgré la pandémie; les données disponibles ne permettent donc pas de démontrer les effets de la pandémie sur l'économie des pays. Sans doute parce que ce type de données (HDI, PIB) sont calculées une fois par an et les effets sur l'économie ne seront visibles que des années plus tard. Je pense qu'il faudrait alors étudier les effets de la COVID-19 sur l'économie mondiale sur une plus longue période (effets à long terme).''')],
            id="toast4",
            header="Impact de la COVID-19 sur l'économie mondiale",
            is_open=False,
            dismissable=True,
            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", 'overflowX':'hidden', 'height':500, "top": 66, "right": 10, "width": 400},)
])
            

toast3 = html.Div([
            html.H1(
                    dbc.Button(
                        "Analyse des données (3)",
                        color="link",
                        id="toast_toggle3",
                    )
                ),
            dbc.Toast([
                    dcc.Markdown('''Cette figure met en évidence l\'évolution de la maladie dans le monde. On observe une bond au cours du mois de Mars 2020. Cette évolution tend à se stabiliser (pente de moins en moins importante), ceci pourrait s'expliquer par les différentes mesures prises afin de contrôler l\'épidémie. Une figure de ce type est un bon indicateur pour évaluer l\'évolution de la crise dans le temps.
                            ''')],
            id="toast3",
            header="Evolution de l'épidémie",
            is_open=False,
            dismissable=True,
            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", 'overflowX':'hidden', 'height':300, "top": 66, "right": 10, "width": 400},)
])

toast2 = html.Div([
            html.H1(
                    dbc.Button(
                        "Analyse des données (2)",
                        color="link",
                        id="toast_toggle2",
                    )
                ),
            dbc.Toast([
                    dcc.Markdown('''L\' analyse globale des données (à l\'échelle mondiale) ne suffit pas pour mettre en évidence un lien entre le PIB et l\'incidence/mortalité. Un pays ne sera pas plus ou moins affecté suivant son niveau économique. Il est difficile d'apprécier rééllement cette figure car les données utilisées ont été transformées (jeu de données "data_transformed"), sans doute normalisées pour être à la même échelle. Ne sachant pas quel type de traitement leur a été appliqué, il est difficile d'en tirer des conclusions''')],
            id="toast2",
            header="Top 25 des pays les plus touchés",
            is_open=False,
            dismissable=True,
            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", 'overflowX':'hidden', 'height':300, "top": 66, "right": 10, "width": 400},)
])

toast1 = html.Div([
            html.H1(
                    dbc.Button(
                        "Analyse des données (1)",
                        color="link",
                        id="toast_toggle",
                    )
                ),
            dbc.Toast([
                    dcc.Markdown('''Cette figure permet de mettre en évidence la répartition de la pandémie dans le monde. On peut avoir une vision globale de l\'incidence et la mortalité de la COVID-19 dans le monde. Il en ressort que les pays les plus touchés sont les Etats-Unis, l\'Inde et le Brésil. Cette observation s\'explique notamment par la gestion cahotique de la crise sanitaire notamment par l\'ancien président des USA, Donald Trump et son confrère Jair Bolsonaro opposés à la mise en place d\'un confinement total généralisé et au port du masque. Les deux dirigeants préférant en effet préserver l\'économie de leur pays au détriments de leurs compatriotes. Par ailleurs, les soins aux USA étant très chers, les personnes atteintes ne peuvent bénéficier de soins décents ce qui explique le nombre important de décès. Concernant l\'Inde, j\'explique ce chiffre par rapport à la forte proportion d\'habitants vivant sous le seuil de pauvreté. Cette hypothèse est soutenue par le faible indice de développement humain (HDI) de ce pays comparé aux autres. \n Bien entendu ces observations sont discutables à plusieurs niveaux. Premièrement d\'un point de vue démographique, puisque les USA, l\'Inde et le Brésil sont des pays à forte densité de population donc le nombre de cas/décès évolue logiquement dans ce sens (même si ceci n\'est pas visible avec la matrice de corrélation). En contradiction avec ce premier point on observe qu\'en Russie, il y a très peu de cas (seraient-ils truqués?  "haha"). D\'autre part, j\'ai réalisé la même figure avec le nombre de cas cumulés(TC)/population, il n\'y avait pas de différence notable mais cet un argument à considérer. ''')],
            id="toast",
            header="L'épidémie à l'échelle modiale",
            is_open=False,
            dismissable=True,
            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed",'overflow': 'scroll','overflowX':'hidden', 'height':500, "top": 66, "right": 10, "width": 400},),
])
# =============================================================================
# tabs
# =============================================================================
tab1_content = html.Div([dbc.Card(
    dbc.CardBody([
        html.H5("La COVID-19 dans le monde", style={'font-style':'italic'}),
        dbc.Row([
            dcc.Graph(id = 'planet', figure = fig0)])]),
    className="mt-3",color = 'white'),
    toast1
    # html.Hr(),
  ])

tab2_content = html.Div([
    dbc.Card(
    dbc.CardBody(
        [
            # html.P("Top 25", className="card-text"),
            html.H5('Top %d des pays les plus touchés dans le monde' %n_country, style={'font-style':'italic'}),
            dbc.Row([dbc.Col(slider,width=1),
            dbc.Col(dbc.Row([dcc.Graph(id = 'bubble_chart')],justify='center'), width = 11)]), 
                    # justify='center'),
        ]
    ),
    className="mt-3",color = 'white'), 
    toast2
    ])


tab3_content = html.Div([
    dbc.Card(
    dbc.CardBody(
        [
            html.H5("Evolution de l'épidémie dans le monde", style={'font-style':'italic'}),
            dbc.Row([
                    dcc.Graph(id = 'evol_of_tc', figure = fig3)]),
        ]
    ),
    className="mt-3",color = 'white'),
    toast3
  ])


tab4_content = html.Div([
    dbc.Card([
        dbc.CardBody(
            [
                html.H5("Evolution des indicateurs dans le temps", style={'font-style':'italic'}),
                dbc.Row([
                    dbc.Row([check],justify = 'start', style = {'margin-left':'25px','margin-top':'10px' }),
                    dcc.Graph(id = 'evol_coun', figure = fig3),
                        ]),
            ]
        )], 
        className="mt-3", color = 'white'
        ),
    toast4,
    ])

tab5_content = html.Div([
    dbc.Card(
    dbc.CardBody(
        [
            html.H5("Matrice de corrélation", style={'font-style':'italic'}),
            dbc.Row([
                    dcc.Graph(id = 'corr_mat')],
                    justify='center'),
        ]
    ),
    className="mt-3",color = 'white'),
    toast5
    ])

tab6_content = html.Div([
    dbc.Card(
    dbc.CardBody(
        [
            html.H5("Effet des restrictions sanitaires sur l'épidémie", style={'font-style':'italic'}),
            dbc.Row([
                    dbc.Row([check1],justify = 'start', style = {'margin-left':'25px','margin-top':'10px' }),
                    dcc.Graph(id = 'sti_plot')]),
        ]
    ),
    className="mt-3",color = 'white'),
    toast6
    ])



tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="World Map"),
        dbc.Tab(tab2_content, label="Top 25"),
        dbc.Tab(tab3_content, label="Progression"),
    ]
)

tabs_1 = dbc.Tabs(
    [
     dbc.Tab(tab5_content, label="Corrélation"),   
     dbc.Tab(tab4_content, label="Evolution"),
        dbc.Tab(tab6_content, label="Restrictions")
        # dbc.Tab(tab3_content, label="Progression"),
    ]
)

indic= html.Div([
    dcc.Markdown(''' **PIB (Produit Intérieur Brut) ou GDPCAP (GDP per Capita):** Il correspond à la valeur de l'ensemble des biens et services produits dans un pays donné au cours d'une période donnée (généralement une année).
Cet indicateur économique permet de mesurer la production économique annuelle, c’est-à-dire le revenu provenant de la production à l’intérieur d’un territoire national pour une année donnée. La variation du PIB est l'indicateur le plus utilisé pour mesurer la croissance économique.
Le PIB a été inventé par l’économiste et statisticien américain Simon Kuznets (1901-1985) en 1934. C’est un indicateur très utile, mais qui a ses limites. On lui reproche notamment de ne pas refléter les effets de l’activité économique sur l'environnement et la société.(source: https://www.infinance.fr/articles/bourse/formation-conseil/)''',style={'text-align':'justify'}),
    dcc.Markdown('''**STI (Stringency Index):** Il fait partie des paramètres utilisés par l'Oxford COVID-19 Government Response Tracker.
Le Tracker implique une équipe de 100 membres de la communauté d'Oxford qui ont continuellement mis à jour une base de données de 17 indicateurs de réponse du gouvernement.
Ces indicateurs examinent les politiques de confinement telles que les fermetures d'écoles et de lieux de travail, les événements publics, les transports publics, les politiques de maintien à la maison.
L'indice de stringence est un nombre compris entre 0 et 100 qui reflète ces indicateurs. Un score d'indice plus élevé indique un niveau de rigueur plus élevé (source: https://www.civilsdaily.com/news/what-is-stringency-index/)''',style={'text-align':'justify'}),
    dcc.Markdown('''**IDH ou HDI (Indice de Développement Humain):** L'IDH est un système de mesure utilisé par les Nations Unies pour évaluer le niveau de développement humain individuel dans chaque pays. Cet indicateur utilise des éléments tels que le revenu annuel moyen et les attentes en matière d'éducation pour classer et comparer les pays. Il a été critiqué par les défenseurs sociaux pour ne pas représenter une mesure suffisamment large de la qualité de vie et par les économistes pour fournir peu d'informations utiles supplémentaires au-delà des mesures plus simples du niveau de vie économique.(source: https://www.investopedia.com/terms/h/human-development-index-hdi.asp)''',style={'text-align':'justify'})
    ])

 
##############################################################################
# =============================================================================
# page layout
# =============================================================================
app.layout = url_bar_and_content_div

page_1_layout = html.Div([
    # dbc.Row([html.H1(children= 'Dash - Impact de la COVID-19 sur l\'économie mondiale')]),
    navbar,
    dbc.Row([
        dbc.Col(
            html.Div(children=[
                html.Hr(),
                html.H5('Situation épidémiologique à l\'échelle mondiale',className='text-success'),
                html.Hr(style = {'border-top': '0.25px solid LightSlateGray'}),
                cards,
                html.Hr(), #style = {'border-top': '0.25px solid LightSlateGray'},
                html.H5('Les pays les plus touchés', className='text-success'),
                html.Hr(style = {'border-top': '0.25px solid LightSlateGray'}),
                dbc.Row([cov_choice],justify = 'center'),
                first_choice,
                table1,
                html.Hr(),
                html.H5('Répartition dans le monde',className='text-success'),
                html.Hr(style = {'border-top': '0.25px solid LightSlateGray'}),
                dbc.Row([
                    dcc.Graph(id = 'pie_chart')], 
                    justify='center'),
                html.P("Ce graphique permet de mieux évaluer la proportion de chaque pays par rapport aux données mondiales. On voit par exemple que la France, pourtant de faible densité de population comparée à des pays comme la Russie, l'Inde ou les Etats-Unis se trouve parmis les 10 pays les plus touchés par l'épidémie. Pas très rassurant tout ça! snif ", style={'text-align':'justify'}),
                ])
            ,width=4, style={'overflow': 'scroll', 'height': 610, 'overflowX':'hidden'}), 
            #style={'background-color':'LightSlateGrey','color':'DarkCyan'},
        dbc.Col(
            tabs,
            # html.Div(children=[
            #     dbc.Row([
            #         dcc.Graph(id = 'planet', figure = fig0),
            #         html.P('Sur ce graphique nous pouvons voir ...')],
            #         justify='end'),
            #     dbc.Row([
            #         dcc.Graph(id = 'evol_of_tc', figure = fig3), 
            #         html.P('Sur ce graphique nous pouvons voir ...')],
            #         justify='end')
            #     ]),
            width=8)
        ])
    ])

page_2_layout = html.Div(children=[
    navbar,
    dbc.Row([
        dbc.Col(
            html.Div(children=[
                html.Hr(),
                html.H5('Etude de l\'impact de la COVID-19 sur l\'économie mondiale',className='text-success'),
                html.Hr(style = {'border-top': '0.25px solid LightSlateGray'}),
                coun_choice,
                cards_coun,
                html.Hr(style = {'border-top': '0.25px solid LightSlateGray'}),
                html.H5('Indicateurs économiques',className='text-success'),
                table,
                html.P('PIB: Produit Intérieur Brut, IDH: Indice de développement humain, STI: Stringency Index', style={'font-size':'smaller','text-align':'justify'}),
                html.Hr(style = {'border-top': '0.25px solid LightSlateGray'}),
                html.H5('Définition des indicateurs',className='text-success'),
                indic])
                # dbc.Row([
                #     dcc.Graph(id = 'corr_mat', figure = fig5)], 
                #     justify='start')
                # ])
            ,width=4, style={'overflow': 'scroll', 'height': 640, 'overflowX':'hidden'}), 
            #style={'background-color':'LightSlateGrey','color':'DarkCyan'},
        dbc.Col(
            tabs_1,
            width=8)
        ])
    ])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    # elif pathname == '/page-3':
    #     return page_3_layout

if __name__ == '__main__':
    app.run_server(debug=True)

# @app.callback(Output('page-content', 'children'),
#               [Input('url', 'pathname')])
# def display_page(pathname):
#     if pathname == '/apps/TC':
#         return layout1
#     elif pathname == '/apps/TD':
#         return layout2
#     else:
#         return '404'