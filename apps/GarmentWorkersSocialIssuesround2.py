#!/usr/bin/env python
# coding: utf-8

# In[153]:


import pandas as pd
import folium
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('max_rows',20)
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import json
import plotly.graph_objects as go


import pathlib
from app import app

# Worker data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

data1 = pd.read_excel(DATA_PATH.joinpath('Round 2 Garment worker.xlsx'), engine='openpyxl')
datamap = pd.read_csv(DATA_PATH.joinpath('state wise centroids_2011.csv'))
st1work=data1


# In[155]:


def plot_bgcolor1():
    return '#a9a9a9'
def paper_bgcolor1():
    return '#a9a9a9'
def piecolor():
    return ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']

def barcolour():
    return ['#000099','#0000CC','#0000FF','#009999','#0099FF','#00FFFF']


# In[156]:


# filterpane
def getMigrantlist(st1work):
    return st1work['Have you or any of the family members had to return from outside after the announcement of lockdown?'].unique()

def getNGO(st1vill):
    return st1vill["Source or Destination"].unique()

def getCastelist(st1work):
    return st1work["Caste catgeory in which the respondent's community is categorised?"].unique()

def getlocationlist(st1work):
    return st1work['Type of location from where the data is being collected'].unique()

def getReligionllist(st1work):
    return st1work['Religion of the Respondent'].unique()

def getGenderlist(st1work):
    return st1work['Gender of the Respondent'].unique()

def getStatelist(st1work):
    return st1work['State'].unique()

def createDroplist(statelist1 , name):
    statelist=[]
    for i in statelist1:
        temp_data= {'label':i,'value':i}
        statelist.append(temp_data)
    temp_data= {'label':'All '+ name,'value':'ALL'}
    statelist.append(temp_data)
    return statelist


# In[ ]:





# In[157]:


def stylecss():
    return {'height': '100%', 'width': '100%' , 'font-size': '12px'}

def start():
    start=([
        html.H2("Social Issues",style={'text-align': 'center', 'colour':'green' } ),
         html.Button(id='TotalDataga',style={'text-align': 'center', 'font-size': '15px', 
                                           'background-color': '#FF8C00',
                                             'color': 'white',
                                              'text-align': 'center',
                                              'text-decoration': 'none',
                                              'display': 'inline-block',
                                             
                                              'margin': '4px 2px',
                                                } ),
        html.P(''),
        html.Div([
                dbc.Row(
                    [
                    dbc.Col(dcc.Dropdown(id='NGOga',options=createDroplist(getNGO(st1work) , "Source or Destination"), value='ALL',multi=True,placeholder="Source or Destination"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'12px'},className='dropdown'
                            ,md=dict(size=2)),
                        
                    dbc.Col(dcc.Dropdown(id='Migrantga',options=createDroplist(getMigrantlist(st1work) , 'Migrant'), value='ALL',multi=True,placeholder="Migrant", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '12px' }),
                            style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    
                        
                    dbc.Col(dcc.Dropdown(id='Castega',options=createDroplist(getCastelist(st1work) , 'Caste'), value='ALL',multi=True,placeholder="Caste", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '12px' }),
                            style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Locationga',options=createDroplist(getlocationlist(st1work),'Location'), value='ALL',multi=True,placeholder="Type of location "
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Religionga',options=createDroplist(getReligionllist(st1work),'Religion'), value='ALL',multi=True,placeholder="Religion"
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Genderga',options=createDroplist(getGenderlist(st1work),'Gender'), value='ALL',multi=True,placeholder="Gender",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                        
                    dbc.Col(dcc.Dropdown(id='Statega',options=createDroplist(getStatelist(st1work),'State'), value='ALL',multi=True,placeholder="State",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                    ]
                     ,
                     
                    
                        ),
                ]),
            
    ])
    return start


# In[158]:


# Chart 1st level

def barlevel1chart1(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Post lockdown have you observed any change in incidences of caste based violence (including physical or verbal, discrimination by dominant groups)?'].value_counts()
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour()
                 )
   
    fig.update_layout(
    title=' ',
    
    xaxis=dict(
                title='Data on Status',
                titlefont=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            ),color='#ffffff'),
    yaxis=dict(
                title='# of Status',
                titlefont=dict(
                family='Helvetica, monospace',
                size=12,
                color='#7f7f7f',
                
            ),color='#ffffff'),
    plot_bgcolor='rgb(255, 255, 255)'
    ,margin={"r":0,"t":0,"l":0,"b":0},)
    fig.update_layout(showlegend=False,plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig

def barlevel1chart2(fil4):
    Bardata1=fil4['Post lockdown have you observed any change in incidences of physical or verbal violence against children?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1 ,color_discrete_sequence=barcolour(),
                 title= '',)
    fig.update_layout(showlegend=False)
    fig.update_layout(
    title= ' ',
    xaxis=dict(
                title='Data on Status',
                titlefont=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            ),color='#ffffff'),
    yaxis=dict(
                title='# of Status',
                titlefont=dict(
                family='Helvetica, monospace',
                size=12,
                color='#7f7f7f',
                
            ),color='#ffffff'),
    plot_bgcolor='rgb(255, 255, 255)'
    ,margin={"r":0,"t":0,"l":0,"b":0}
        ,)
    fig.update_layout(showlegend=False,plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig

def barlevel1chart3(fil4):
    Bardata1=fil4['Post lockdown have you observed any change in incidences of physical or verbal violence against women?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= ' ',)
    fig.update_layout(showlegend=False)
    fig.update_layout(
    title= ' ',
    xaxis=dict(
                title='',
                titlefont=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            ),color='#ffffff'),
    yaxis=dict(
                title='',
                titlefont=dict(
                family='Helvetica, monospace',
                size=12,
                color='#7f7f7f',
                
            ),color='#ffffff'),
    plot_bgcolor='rgb(255, 255, 255)'
    ,margin={"r":0,"t":0,"l":0,"b":0}
        ,)
    fig.update_layout(showlegend=False,plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig


# In[159]:


#map state wise
import plotly.express as px
def map(st1work):
    data=st1work
    data=data["State"]
    a=data.drop_duplicates()
    data1=datamap
    df = pd.merge(a, data1, how="inner", on=["State", "State"])
    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="State", hover_name="State",size="Latitude",
                            hover_data=["State"],
                            color_discrete_sequence=['#003f5c'], zoom=4, height=800)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(showlegend=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


# In[160]:


def pielevel2chart1(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Did your family have to take loan under compulsions for taking up agriculture in the upcoming agriculture cycle?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,  title=' ',hole=.7 )
    #fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig

def barlevel2chart2(fil4):
    Bardata1=fil4['Looking at the current situation, is it likely that Girls will dropout from school?'].value_counts()
    Bardata2=fil4['Looking at the current situation, is it likely that Boys will dropout from school?'].value_counts()
    
    figure={
        'data': [
            {'x':Bardata1.index, 'y' :Bardata1 , 'type': 'bar', 'name': 'Girls'},
            {'x':Bardata2.index, 'y' :Bardata2 , 'type': 'bar','name': 'Boys'},
            ],
        'layout': {
            'title': '',
            'xaxis' : dict(title='',titlefont=dict(family='Courier New, monospace',size=12,color='#7f7f7f'),color='#ffffff'),
            'yaxis' : dict(title='',titlefont=dict(family='Helvetica, monospace',size=12,color='#7f7f7f',textalign= 'center'),color='#ffffff'),
            'margin':{"r":0,"t":10,"l":20,"b":60},'height':300,
            'plot_bgcolor':plot_bgcolor1(),
            'paper_bgcolor':paper_bgcolor1()
        }
    }
        
        
    return figure

def barlevel2chart1(fil4):
    Bardata1=fil4['Have you or your family taken loan during the lockdown period?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= '',)
    fig.update_layout(showlegend=False)
    fig.update_layout(
    xaxis=dict(
                title='',
                titlefont=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            ),color='#ffffff'),
    yaxis=dict(
                title='',
                titlefont=dict(
                family='Helvetica, monospace',
                size=12,
                color='#7f7f7f',
                
            ),color='#ffffff'),
    plot_bgcolor='rgb(255, 255, 255)'
    ,margin={"r":0,"t":0,"l":0,"b":0}
        ,height=300
    )
    fig.update_layout(showlegend=False,plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig


# In[161]:


#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
layout = dbc.Container(
    [    
        html.Div([
            dbc.Row(
                [
                    dbc.Col(start(),md=12),
                   
                ],
                style={'height': "100%"},
                align="center",
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([html.P('Changes in Caste-based Violence'),
                             dcc.Graph(id='barlevel1chart1ga',figure= barlevel1chart1(st1work))],md=4),
                    dbc.Col([html.P('instances of child abuse'),
                             dcc.Graph(id='barlevel1chart2ga',figure= barlevel1chart2(st1work) )],md=4),
                    dbc.Col([html.P('physical or verbal violence against women'),
                             dcc.Graph(id='barlevel1chart3ga',figure= barlevel1chart3(st1work) )],md=4),
    
                ],
                style={'height': "100%"},
                align="center",
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id='graphga',figure= map(st1work) ),md=6),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([html.P('Have to take loan under compulsions for taking up agriculture in the upcoming agriculture cycle'),
                                     dcc.Graph(id='pielevel2chart1ga',figure= pielevel2chart1(st1work) )],md=12),
                            dbc.Col([html.P('Have you or your family taken loan after March in this year?'),
                                     dcc.Graph(id='barlevel2chart1ga',figure= barlevel2chart1(st1work) )],md=6),
                            dbc.Col([html.P('Looking at the current situation, is it likely that Boys-Girls will dropout from school?'),
                                     dcc.Graph(id='barlevel2chart2ga',figure= barlevel2chart2(st1work) )],md=6),
                            
                        ])
                        
                    ],md=6),
                    
    
                ],
                style={'height': "100%"},
                align="center",
            ),
            html.Br(),
             
        ],style={'padding-right': '0%','padding-left': '0%'}),
    ],
    fluid=True,
)


# In[162]:


def totalcount(file):
    
    return len(file.index)


# In[163]:


@app.callback( 
    Output(component_id='NGOga', component_property='options'),
    Output(component_id='Migrantga', component_property='options'),
    Output(component_id='Castega', component_property='options'),
    Output(component_id='Locationga', component_property='options'),
    Output(component_id='Religionga', component_property='options'),
    Output(component_id='Genderga', component_property='options'),
    Output(component_id='Statega', component_property='options'),
    
    
    Output(component_id='barlevel1chart1ga', component_property='figure'),
    Output(component_id='barlevel1chart2ga', component_property='figure'),
    Output(component_id='barlevel1chart3ga', component_property='figure'),
    Output(component_id='pielevel2chart1ga', component_property='figure'), 
    Output(component_id='barlevel2chart1ga', component_property='figure'),
    Output(component_id='barlevel2chart2ga', component_property='figure'),
    Output(component_id='graphga', component_property='figure'),
    Output(component_id='TotalDataga', component_property='children'),

    
    Input(component_id='Migrantga', component_property='value'),
    Input(component_id='Castega', component_property='value'),
    Input(component_id='Locationga', component_property='value'),
    Input(component_id='Religionga', component_property='value'),
    Input(component_id='Genderga', component_property='value'),
    Input(component_id='Statega', component_property='value'),
    Input(component_id='NGOga', component_property='value'),
    
   # Input(component_id='stageselection', component_property='value'),
)
def update_output1(input_value,input_value1,input_value2,input_value3,input_value4,input_value5,input_value7):  
    if len(input_value) == 0:
        fil1=st1work
    elif 'ALL' in input_value:
        fil1=st1work
    else: 
        fil1=st1work[st1work['Have you or any of the family members had to return from outside after the announcement of lockdown?'].isin(input_value)]
        
        
    if len(input_value1) == 0:
        fil2=fil1
    elif 'ALL' in input_value1:
        fil2=fil1
    else:
        fil2=fil1[fil1["Caste catgeory in which the respondent's community is categorised?"].isin(input_value1)]
    
    if len(input_value2) == 0:
        fil3=fil2
    elif 'ALL' in input_value2:
        fil3=fil2
    else:
        fil3=fil2[fil2["Type of location from where the data is being collected"].isin(input_value2)]
    
    if len(input_value3) == 0:
        fil4=fil3
    elif 'ALL' in input_value3:
        fil4=fil3
    else:    
        fil4=fil3[fil3["Religion of the Respondent"].isin(input_value3)]
        
    if len(input_value4) == 0:
        fil5=fil4
    elif 'ALL' in input_value4:
        fil5=fil4
    else:
        fil5=fil4[fil4['Gender of the Respondent'].isin(input_value4)]
    
    if len(input_value5) == 0:
        fil6=fil5
    elif 'ALL' in input_value5:
        fil6=fil5
    else:
        fil6=fil5[fil5['State'].isin(input_value5)]
    if len(input_value7) == 0:
        fil7=fil6
    elif 'ALL' in input_value7:
        fil7=fil6
    else:
        fil7=fil6[fil6["Source or Destination"].isin(input_value7)]
    
    
    Castelist=createDroplist(getCastelist(fil7),'Caste')
    locationlist=createDroplist(getlocationlist(fil7),'Location')
    Religionllist=createDroplist(getReligionllist(fil7),'Religion')
    Genderlist=createDroplist(getGenderlist(fil7),'Gender')
    Statelist=createDroplist(getStatelist(fil7),'State')
    Migrantlist=createDroplist(getMigrantlist(fil7) , 'Migrant')
    optionNGO=createDroplist(getNGO(fil7),"Source or Destination")
    
    return optionNGO,Migrantlist ,Castelist, locationlist, Religionllist, Genderlist, Statelist , barlevel1chart1(fil7),barlevel1chart2(fil7),barlevel1chart3(fil7),pielevel2chart1(fil7),barlevel2chart1(fil7),barlevel2chart2(fil7),map(fil7),'Total Number: {}'.format(totalcount(fil7))


# In[164]:


if __name__ == '__main__':
    app.run_server(host= '127.0.0.2',debug=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




