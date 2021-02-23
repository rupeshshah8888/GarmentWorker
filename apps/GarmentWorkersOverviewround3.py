#!/usr/bin/env python
# coding: utf-8

# In[15]:


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



# In[48]:
import pathlib
from app import app

# Worker data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

data1 = pd.read_excel(DATA_PATH.joinpath('Collated_Round3_Workers.xlsx'), engine='openpyxl')
datamap = pd.read_csv(DATA_PATH.joinpath('state wise centroids_2011.csv'))
st1work=data1

def piecolor():
    return ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']

def barcolour():
    return ['#000099','#0000CC','#0000FF','#009999','#0099FF','#00FFFF']



def plot_bgcolor1():
    return '#a9a9a9'
def paper_bgcolor1():
    return '#a9a9a9'

def cong():
    return { 'staticPlot': False,     # True, False
      'scrollZoom': False,      # True, False
      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
      'showTips': False,       # True, False
      'displayModeBar': False,  # True, False, 'hover'
      'watermark': False,
      'displaylogo': False,
       'modeBarButtonsToRemove': [ 'hoverCompareCartesian', 'hoverClosestCartesian', 'toggleSpikelines','Pan'] 
           }


# In[17]:


def generate_card_content(card_header,card_value):
    card_head_style = {'textAlign':'center','fontSize':'12px','padding-right': '0%','padding-left':'0%'}
    card_body_style = {'textAlign':'center','fontSize':'12px','padding-right': '0%','padding-left':'0%'}
    card_header = dbc.CardHeader(card_header,style=card_head_style)
    card_body = dbc.CardBody(
        [
            html.H5(f"{int(card_value):,}", className="card-title",style=card_body_style),
        ]
        
    )
    card = [card_header,card_body]
    return card


# In[18]:


def KPI(st1vill):
    TotalDis=st1vill['District'].value_counts().count()
    Totalstate=st1vill['State'].value_counts().count()
    Totalblock=st1vill['Block'].value_counts().count()
    TotalRespondent=st1vill['Respondent Name'].count()
    TotalPanchayat=st1vill['Panchayat/ Municipal Ward'].value_counts().count()
    Totalvill=st1vill['Village/ Colony/Area'].value_counts().count()
    cards = html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(dbc.Card(generate_card_content("Village",Totalvill), color="primary", inverse=True), style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),
                    dbc.Col(dbc.Card(generate_card_content("Panchayat",TotalPanchayat), color="primary",inverse=True), style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),
                    dbc.Col(dbc.Card(generate_card_content("Block",Totalblock), color="primary", inverse=True),style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),
                    dbc.Col(dbc.Card(generate_card_content("District",TotalDis), color="primary", inverse=True),style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),
                    dbc.Col(dbc.Card(generate_card_content("State",Totalstate),color="primary", inverse=True),style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),
                    dbc.Col(dbc.Card(generate_card_content("Respondent",TotalRespondent),color="primary", inverse=True),style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),
                ],
                
            ),
        ],id='cardabchb'
    )
    return cards


# In[19]:


def GeoMap(abc):
    data=abc
    data=data["State"]
    a=data.drop_duplicates()
    data1=datamap
    df = pd.merge(a, data1, how="inner", on=["State", "State"])
    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="State", hover_name="State",size="Latitude",
                            hover_data=["State"],
                            color_discrete_sequence=['#003f5c'], zoom=4, height=800)
    fig.update_layout(mapbox_style="open-street-map",showlegend=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

    
    


# In[20]:


def getNGO(st1vill):
    return st1vill["Source or Destination"].unique()

def getBlock(st1vill):
    return st1vill["Block"].unique()

def getDistrict(st1vill):
    return st1vill["District"].unique()


def getCastelist(st1vill):
    return st1vill["Caste catgeory in which the respondent's community is categorised?"].unique()

def getlocationlist(st1vill):
    return st1vill['Type of location from where the data is being collected'].unique()

def getGenderlist(st1vill):
    return st1vill['Gender of the Respondent'].unique()

def getStatelist(st1vill):
    return st1vill['State'].unique()

def getReligionlist(st1vill):
    return st1vill['Religion of the Respondent'].unique()

def createDroplist(statelist1 , name):
    statelist=[]
    for i in statelist1:
        temp_data= {'label':i,'value':i}
        statelist.append(temp_data)
    temp_data= {'label':'All '+ name,'value':'ALL'}
    statelist.append(temp_data)
    return statelist


# In[21]:


def right():
    worker=([
    
        html.H2('Overview of Individual-level data',style={'textAlign': 'center'}),
 
        html.P("The following tables provide an overview of a range of responses from workers. "
               "Further details about each aspect can be found by clicking on the relevant title on the left panel."
              ,style={'textAlign': 'left'}),
        html.Button(id='TotalDatahb',style={'text-align': 'center', 'font-size': '15px', 
                                           'background-color': '#FF8C00',
                                             'color': 'white',
                                              'text-align': 'center',
                                              'text-decoration': 'none',
                                              'display': 'inline-block',
                                             
                                              'margin': '4px 2px',
                                                } ),
        dbc.Row([ 
                dbc.Col(dcc.Dropdown(id='monthhb'
                             ,options=[   {'label': 'October', 'value': 'October'},
                                          {'label': 'November', 'value': 'November'},
                                          {'label': 'December', 'value': 'December'},
                                      ],value='October'),md=6)
                ])
        
                           
    ]
)

    return worker
      


# In[22]:


def left():
    left=([
        KPI(data1),
        html.H6("Filter the data"),
        html.P('Click on any variable from the tables below to get the correlated entitlement status of those individuals'),
        html.Div([
                dbc.Row( 
                    [
                    dbc.Col(dcc.Dropdown(id='NGOhb',options=createDroplist(getNGO(data1) , "Source or Destination"), value='ALL',multi=True,placeholder="Source or Destination"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown'
                            ,md=dict(size=3)),
                    
                        
                    dbc.Col(dcc.Dropdown(id='Statehb',options=createDroplist(getStatelist(data1),'State'), value='ALL',multi=True,placeholder="State")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=3)),

                    dbc.Col(dcc.Dropdown(id='Districthb',options=createDroplist(getDistrict(data1),'District'), value='ALL',multi=True,placeholder="District")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=3)),

                    dbc.Col(dcc.Dropdown(id='Blockhb',options=createDroplist(getBlock(data1),'Block'), value='ALL',multi=True,placeholder="Block")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=3)),

                        
                    
                    
                    dbc.Col(dcc.Dropdown(id='Castehb',options=createDroplist(getCastelist(data1) , 'Caste'), value='ALL',multi=True,placeholder="Caste"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=3)),

                    dbc.Col(dcc.Dropdown(id='Locationhb',options=createDroplist(getlocationlist(data1),'Location'), value='ALL',multi=True,placeholder="Type of location ")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=3)),

                    
                    dbc.Col(dcc.Dropdown(id='Religionhb',options=createDroplist(getReligionlist(data1),'Religion'), value='ALL',multi=True,placeholder="Religion")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=3)),
                   
                    dbc.Col(dcc.Dropdown(id='Genderhb',options=createDroplist(getGenderlist(data1),'Gender'), value='ALL',multi=True,placeholder="Gender")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=3)),
                   
                   
                    ] 
                     ,
                     
                    
                        ),
                ]),
  
            
    ])
    return left


# In[23]:


def Socialissues1(fil4):
    Bardata1=fil4['Comapred to other dominant caste/social group hamlets how would you assess the government response during covid in your hamlet?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= '',)
    fig.update_layout(plot_bgcolor='rgb(255, 255, 255)',margin={"r":0,"t":0,"l":0,"b":0},bargap=0.4,height=300)
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    fig.update_yaxes(title=None,color='#ffffff')
    fig.update_xaxes(title=None,color='#ffffff')
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig

def Socialissues2(fil4):
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
            'yaxis' : dict(title='',titlefont=dict(family='Helvetica, monospace',size=12,color='#7f7f7f'),color='#ffffff'),
            'margin':{"r":0,"t":10,"l":30,"b":60},'height':300,
            'plot_bgcolor':plot_bgcolor1(),
            'paper_bgcolor':paper_bgcolor1()
        }
        
    }
            
        
    return figure



def Socialissues3(fil4):
    Bardata1=fil4['What is the work you are currently involved in?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= '',)
    fig.update_layout(showlegend=False)
    fig.update_layout(plot_bgcolor='rgb(255, 255, 255)',margin={"r":0,"t":0,"l":0,"b":0},bargap=0.4,height=300)
    fig.update_yaxes(title=None,color='#ffffff')
    fig.update_xaxes(title=None,color='#ffffff')
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig
def Socialissues4(fil4):
    Bardata1=fil4['Have you or your family taken loan after March in this year?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= '',)
    fig.update_layout(showlegend=False)
    fig.update_layout(plot_bgcolor='rgb(255, 255, 255)',margin={"r":0,"t":0,"l":0,"b":0},bargap=0.4,height=300)
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    fig.update_yaxes(title=None,color='#ffffff')
    fig.update_xaxes(title=None,color='#ffffff')
    return fig


# In[24]:


def Violence(st1vill):
    Bardata1=st1vill['Post lockdown have you observed any change in incidences of caste based violence (including physical or verbal, discrimination by dominant groups)?'].value_counts()
    Bardata2=st1vill['Post lockdown have you observed any change in incidences of physical or verbal violence against women?'].value_counts()
    Bardata3=st1vill['Post lockdown have you observed any change in incidences of physical or verbal violence against children?'].value_counts()
    
    figure={
        'data': [
            {'x':Bardata1.index, 'y' :Bardata1 , 'type': 'bar', 'name': 'Caste-Based Violence'},
            {'x':Bardata2.index, 'y' :Bardata2 , 'type': 'bar','name': 'physical or verbal violence against women?'},
            {'x':Bardata2.index, 'y' :Bardata2 , 'type': 'bar','name': 'physical or verbal violence against children?'},
            
                            ],
        'layout': {
            'title': '',

        'xaxis' : dict(
                title='',
                titlefont=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
                
            ),color='#ffffff'),
            'yaxis' : dict(
                title='',
                titlefont=dict(
                family='Helvetica, monospace',
                size=12,
                color='#7f7f7f',
                textalign= 'center'
            ),color='#ffffff'),
         'margin':{"r":0,"t":10,"l":30,"b":60},
        'height':300,
        'plot_bgcolor':plot_bgcolor1(),
        'paper_bgcolor':paper_bgcolor1()
       
            }
        }
    return figure


def pielevelchart1(fil4 , month='October'):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Comapred to other dominant caste/social group hamlets how would you assess the government response during covid in your hamlet?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='',hole=.7 )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig
def pielevelchart2(fil4 , month='October'):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Have you or any member in the family received subsidy for cyclinder for the month of '+month+'?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='In '+month,hole=.7 )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig
def pielevelchart3(fil4 , month='October'):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Did you or any registered member in your family people get additional ration ( 5 kgs rice and 1Kg pulse) for the month of '+month+'?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='In '+month,hole=.7 )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1(),height=300)

    return fig
def pielevelchart4(fil4 , month='October'):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Has the registered widow pension beneficiary received the pension for the month of '+month+'?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='In '+month,hole=.7 )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1(),height=300)

    return fig
def pielevelchart5(fil4 , month='October'):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Has the registered PWD pension beneficiary received the pension for the month of '+month+'?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='In '+month,hole=.7 )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1(),height=300)

    return fig
def pielevelchart6(fil4 , month='October'):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Has the registered old age pension beneficiary received the pension for the month of '+month+'?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='In '+month,hole=.7 )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1(),height=300)

    return fig



# In[25]:


layout = dbc.Container(
    [    
        
            dbc.Row(
                [
                    dbc.Col(right(),md=6),
                    dbc.Col(left(),   md=6),
                ],
                style={'height': "100%"},
                align="center",
            ),
            
           
            html.Div(html.H5('Social Issues',style={'textAlign': 'center'})), 
            dbc.Row(
                [
                    dbc.Col([dbc.Row([html.P('Comapred to other dominant caste/social group hamlets how would you assess the government response during covid in your hamlet?',style={'textAlign': 'center'}),
                        dbc.Col(dcc.Graph(id='Entitlements1hb',figure= Socialissues1(data1),config=cong()),md=12)])], md=3 ),
                    dbc.Col([dbc.Row([html.P('Looking at the current situation, is it likely that Boys-Girls will dropout from school?',style={'textAlign': 'center'}),
                        dbc.Col(dcc.Graph(id='Entitlements2hb',figure= Socialissues2(data1),config=cong()),md=12)]),], md=3 ),
                    dbc.Col([dbc.Row([html.P('What is the work you are currently involved in?',style={'textAlign': 'center'}),
                        dbc.Col(dcc.Graph(id='Entitlements3hb',figure= Socialissues3(data1),config=cong()),md=12)]),], md=3 ),
                    dbc.Col([dbc.Row([html.P('Have you or your family taken loan after March in this year?',style={'textAlign': 'center'}),
                        dbc.Col(dcc.Graph(id='Entitlements4hb',figure= Socialissues4(data1),config=cong()),md=12)]),], md=3 ),
            ]        ,
                style={'height': "100%"},
                align="center",
            ),
        dbc.Row(
                [
                    dbc.Col([dbc.Row([
                        dbc.Col(dcc.Graph(id='Violencehb',figure= Violence(data1),config=cong()),md=12)])], md=6 ),
                    dbc.Col([dbc.Row([html.P("Comapred to other dominant caste/social group hamlets how would you assess the government response",style={'textAlign': 'center'}),
                     dbc.Col(dcc.Graph(id='pension1hb',figure= pielevelchart1(data1),config=cong()),md=12)])], md=3 ),
                     dbc.Col([dbc.Row([html.P("Free cylinder under Ujjwala scheme",style={'textAlign': 'center'}),
                        dbc.Col(dcc.Graph(id='pension2hb',figure= pielevelchart2(data1),config=cong()),md=12)])], md=3 ),
                   
                    
                ]        ,
                style={'height': "100%"},
                align="center",
            ),
        dbc.Row(
                [
                    dbc.Col([dbc.Row([
                        dbc.Col(dcc.Graph(id='graphhb',figure= GeoMap(data1)),md=12)])], md=6 ),
                    dbc.Col([dbc.Row([
                            dbc.Col([html.P(" Additional Ration",style={'textAlign': 'center'}),
                                dcc.Graph(id='pension3hb',figure= pielevelchart3(data1),config=cong())],md=6),
                        dbc.Col([html.P("Ex gratia under Widow pension",style={'textAlign': 'center'}),
                                dcc.Graph(id='pension4hb',figure= pielevelchart4(data1),config=cong())],md=6),
                        dbc.Col([html.P("Ex gratia - Disability pension",style={'textAlign': 'center'}),
                                dcc.Graph(id='pension5hb',figure= pielevelchart5(data1),config=cong())],md=6),
                        dbc.Col([html.P("Ex gratia under Old age pension",style={'textAlign': 'center'}),
                                dcc.Graph(id='pension6hb',figure= pielevelchart6(data1),config=cong())],md=6)
                    
                    ]
                        
                        )], md=6 )
                   
                    
                ]        ,
                style={'height': "100%"},
                align="center",
            ),
        
        
 

        
    ],
    fluid=True,
)


# In[26]:


def totalcount(file):
    
    return len(file.index)


# In[27]:


#call Back Bar Graph1
@app.callback(
    Output(component_id='cardabchb', component_property='children'),
    Output(component_id='NGOhb', component_property='options'),
    Output(component_id='Districthb', component_property='options'),
    Output(component_id='Blockhb', component_property='options'),
    
    Output(component_id='Castehb', component_property='options'),
    Output(component_id='Locationhb', component_property='options'),
    Output(component_id='Statehb', component_property='options'),
    Output(component_id='Religionhb', component_property='options'),
    Output(component_id='Genderhb', component_property='options'),
              
    Output('graphhb', 'figure'),
              
    Output('Entitlements1hb', 'figure'),
    Output('Entitlements2hb', 'figure'),
    Output('Entitlements3hb', 'figure'),
    Output('Entitlements4hb', 'figure'),
    
    Output('pension1hb', 'figure'),
    Output('pension2hb', 'figure'),
    Output('pension3hb', 'figure'),
    Output('pension4hb', 'figure'),
    Output('pension5hb', 'figure'),
    Output('pension6hb', 'figure'),
    
    Output('Violencehb', 'figure'),
    
    Output(component_id='TotalDatahb', component_property='children'),
    
   
    
          
    Input(component_id='Castehb', component_property='value'),
    Input(component_id='Locationhb', component_property='value'),
    Input(component_id='Statehb', component_property='value'),
    Input(component_id='Religionhb', component_property='value'),
    Input(component_id='Genderhb', component_property='value'),
    
    Input(component_id='monthhb', component_property='value'),
    Input(component_id='NGOhb', component_property='value'),
    Input(component_id='Districthb', component_property='value'),
    Input(component_id='Blockhb', component_property='value'),
   
   # Input(component_id='stageselection', component_property='value'), 
)
def update_output1(input_value,input_value1,input_value2,input_value3,input_value4,month,input_value5,input_value6,input_value7):
    month=month
    
    st1vill=data1
    if len(input_value) == 0:
        fil1=st1vill
    elif 'ALL' in input_value:
        fil1=st1vill
    else:
        fil1=st1vill[st1vill["Caste catgeory in which the respondent's community is categorised?"].isin(input_value)]
        
    if len(input_value1) == 0:
        fil2=fil1
    elif 'ALL' in input_value1:
        fil2=fil1
    else:
        fil2=fil1[fil1["Type of location from where the data is being collected"].isin(input_value1)]
        
    if len(input_value2) == 0:
        fil3=fil2
    elif 'ALL' in input_value2:
        fil3=fil2
    else:
        fil3=fil2[fil2["State"].isin(input_value2)]
        
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
        fil5=fil4[fil4["Gender of the Respondent"].isin(input_value4)]
    if len(input_value5) == 0:
        fil6=fil5
    elif 'ALL' in input_value5:
        fil6=fil5
    else:
        fil6=fil5[fil5["Source or Destination"].isin(input_value5)]
    
    if len(input_value7) == 0:
        fil7=fil6
    elif 'ALL' in input_value7:
        fil7=fil6
    else:
        fil7=fil6[fil6["Block"].isin(input_value7)]
    
    if len(input_value6) == 0:
        fil8=fil7
    elif 'ALL' in input_value6:
        fil8=fil7
    else:
        fil8=fil7[fil7["District"].isin(input_value6)]
        
    
    optionCaste=createDroplist(getCastelist(fil8),'Caste')
    optionLocation=createDroplist(getlocationlist(fil8) , 'Location')
    optionState=createDroplist(getStatelist(fil8),'State')
    optionReligion=createDroplist(getReligionlist(fil8),'Religion')
    optionGender=createDroplist(getGenderlist(fil8),'Gender')
    optionNGO=createDroplist(getNGO(fil8),"Source or Destination")
    optionBlock=createDroplist(getBlock(fil8),"Block")
    optionDistrict=createDroplist(getDistrict(fil8),"District")
    
    
    
    
    
    return KPI(fil8),optionNGO,optionDistrict,optionBlock,optionCaste,optionLocation,optionState,optionReligion,optionGender,GeoMap(fil8),Socialissues1(fil8),Socialissues2(fil8),Socialissues3(fil8),Socialissues4(fil8),pielevelchart1(fil8,month),pielevelchart2(fil8,month),pielevelchart3(fil8,month),pielevelchart4(fil8,month),pielevelchart5(fil8,month),pielevelchart6(fil8,month),Violence(fil8),'Total Number: {}'.format(totalcount(fil8))


# In[ ]:





# In[28]:


if __name__ == '__main__':
    app.run_server(host= '127.0.0.1',debug=False)


# In[ ]:



                    

