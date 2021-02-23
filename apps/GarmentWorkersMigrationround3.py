#!/usr/bin/env python
# coding: utf-8

# In[89]:


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

data1 = pd.read_excel(DATA_PATH.joinpath('Collated_Round3_Workers.xlsx'), engine='openpyxl')
datamap = pd.read_csv(DATA_PATH.joinpath('state wise centroids_2011.csv'))
st1work=data1


def barcolour():
    return ['#000099','#0000CC','#0000FF','#009999','#0099FF','#00FFFF']

def plot_bgcolor1():
    return '#A9A9A9'
def paper_bgcolor1():
    return '#A9A9A9'

def piecolor():
    return ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']


# In[92]:


# filterpane
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


# In[93]:


def stylecss():
    return {'height': '100%', 'width': '100%' , 'font-size': '12px'}

def start():
    start=([
        html.H2("Migration",style={'text-align': 'center', 'colour':'green' } ),
        html.Button(id='TotalDataeb',style={'text-align': 'center', 'font-size': '15px', 
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
                    dbc.Col(dcc.Dropdown(id='NGOeb',options=createDroplist(getNGO(st1work) , "Source or Destination"), value='ALL',multi=True,placeholder="Source or Destination"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown'
                            ,md=dict(size=2)),
                    
                        
                    dbc.Col(dcc.Dropdown(id='Casteeb',options=createDroplist(getCastelist(st1work) , 'Caste'), value='ALL',multi=True,placeholder="Caste", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '12px' }),
                            style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Locationeb',options=createDroplist(getlocationlist(st1work),'Location'), value='ALL',multi=True,placeholder="Type of location "
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Religioneb',options=createDroplist(getReligionllist(st1work),'Religion'), value='ALL',multi=True,placeholder="Religion"
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Gendereb',options=createDroplist(getGenderlist(st1work),'Gender'), value='ALL',multi=True,placeholder="Gender",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                        
                    dbc.Col(dcc.Dropdown(id='Stateeb',options=createDroplist(getStatelist(st1work),'State'), value='ALL',multi=True,placeholder="State",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                        
                    dbc.Col(dcc.Dropdown(id='montheb',options=[ 
                                        {'label': 'July', 'value': 'July'},
                                        {'label': 'August', 'value': 'August'},
                                        {'label': 'September', 'value': 'September'},
                                      ],value='July',placeholder="Month"
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                                            
            
                        
                        
                        
                    ]
                     ,
                     
                    
                        ),
                ]),
            
    ])
    return start


# In[ ]:





# In[94]:


def pielevel2chart1(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Have you or any of the family members had to return from outside after the announcement of lockdown?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='',hole=.7 )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig
def pielevel2chart2(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Did you receive or any other faily member receive any support in form of ticket/monetary from government for the return journey?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='',hole=.7 )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig

def barMigrationLocalPanchayat(fil4):
    Bardata1=fil4['Has any migrant registration been done at local Panchayat or ward office for the members in you family who returned from outside?'].value_counts()
    
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
    ,margin={"r":0,"t":30,"l":0,"b":0}
        ,
    bargap=0.4,
    #width=[0.8, 0.8, 0.8, 0.8]
    height=300
    )
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig



def barChildAmongOutside(fil4):
    Bardata1=fil4['Have you or any of the family members had to return from outside after the announcement of lockdown?'].value_counts()
    
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
    ,margin={"r":0,"t":30,"l":0,"b":0}
        ,
    bargap=0.4,
    #width=[0.8, 0.8, 0.8, 0.8]
    height=300
    )
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig
    

    
def barWalkMoreADay(fil4):
    Bardata1=fil4['Did you or any of the family members had to walk for more than a day while returning home?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title="",)
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
               
                size=12,
                color='#7f7f7f',
                
            ),color='#ffffff'),
    plot_bgcolor='rgb(255, 255, 255)'
    ,margin={"r":0,"t":30,"l":0,"b":0}
        ,
    bargap=0.4,
    #width=[0.8, 0.8, 0.8, 0.8]
    height=300,
    

    
    )
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig


def barWhichStateReturn(fil4):
    Bardata1=fil4['You or any other family member had to return from which state?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= 'June',)
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
                size=12,
                color='#7f7f7f',
                
            ),color='#ffffff'),
    plot_bgcolor='rgb(255, 255, 255)'
    ,margin={"r":0,"t":30,"l":0,"b":0}
        ,
    bargap=0.4,
    #width=[0.8, 0.8, 0.8, 0.8]
    height=300
    
    )
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig



# In[95]:


def quick_plot1(abc):
    data=abc
    data=data["State"]
    a=data.drop_duplicates()
    data1=datamap
    df = pd.merge(a, data1, how="inner", on=["State", "State"])
    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="State", hover_name="State",size="Latitude",
                            hover_data=["State"],
                            color_discrete_sequence=['#a9a9a9'], zoom=4, height=800)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(showlegend=False)
    return fig


# In[96]:


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
                    
                    
                ],
                style={'height': "100%"},
                align="center",
            ),
            html.Br(),
            dbc.Row([
            dbc.Col([   
                dbc.Row([
                    
                            html.P("Have you or any of the Family members had to return from outside after the announcement of lockdown?",style={'text-align': 'center', 'colour':'green' } ),
                            dbc.Col(dcc.Graph(id='pielevel2chart1eb',figure= pielevel2chart1(st1work)) ,md=12),
                ],justify="center", align="center"
                )
            
            ],md=4),
            
            dbc.Col([   
                dbc.Row([
                    
                            html.P("Has any migrant registration been done at local Panchayat or ward office for the members in you family who returned from outside?",style={'text-align': 'center', 'colour':'green' } ),
                            dbc.Col(dcc.Graph(id='barMigrationLocalPanchayateb',figure= barMigrationLocalPanchayat(st1work)) ,md=12),
                ],justify="center", align="center"
                )
            
            ],md=4),
            
           
            dbc.Col([   
                dbc.Row([
                    
                           html.P("Did you or any of the family members had to walk for more than a day while returning home?",style={'text-align': 'center', 'colour':'green' } ),
                            dbc.Col(dcc.Graph(id='barWalkMoreADayeb',figure= barWalkMoreADay(st1work)),md=12),
                            ],justify="center", align="center"
                )
            
            ],md=3),
            dbc.Col([   
                dbc.Row([
                    
                            html.P("Was there any child among the members who had gone outside for work and had to return?",style={'text-align': 'center', 'colour':'green' } ),
                            dbc.Col(dcc.Graph(id='barChildAmongOutsideeb',figure= barChildAmongOutside(st1work)),md=12),
                  ],justify="center", align="center"
                )
            
            ],md=6),
                 
               
            
            ]),
            html.Br(),
            
             
        ],style={'padding-right': '0%','padding-left': '0%'}),
    ],
    fluid=True,
)



# In[97]:


def totalcount(file):
    
    return len(file.index)


# In[98]:


@app.callback( 
    Output(component_id='NGOeb', component_property='options'),
    Output(component_id='Casteeb', component_property='options'),
    Output(component_id='Locationeb', component_property='options'),
    Output(component_id='Religioneb', component_property='options'),
    Output(component_id='Gendereb', component_property='options'),
    Output(component_id='Stateeb', component_property='options'),
   
    Output(component_id='barMigrationLocalPanchayateb', component_property='figure'),
    Output(component_id='barChildAmongOutsideeb', component_property='figure'),
    Output(component_id='barWalkMoreADayeb', component_property='figure'),
    
    
    Output(component_id='pielevel2chart1eb', component_property='figure'),
    
    
    Output(component_id='TotalDataeb', component_property='children'),
    #Output(component_id='barWhichStateReturneb', component_property='figure'),
    #Output(component_id='pielevel2chart2eb', component_property='figure'),
   
    Input(component_id='Casteeb', component_property='value'),
    Input(component_id='Locationeb', component_property='value'),
    Input(component_id='Religioneb', component_property='value'),
    Input(component_id='Gendereb', component_property='value'),
    Input(component_id='Stateeb', component_property='value'),
    Input(component_id='montheb', component_property='value'),
    Input(component_id='NGOeb', component_property='value'),
    
   # Input(component_id='stageselection', component_property='value'),
)
def update_output1(input_value1,input_value2,input_value3,input_value4,input_value5,month,input_value7):  
        
        
    if len(input_value1) == 0:
        fil2=st1work
    elif 'ALL' in input_value1:
        fil2=st1work
    else:
        fil2=st1work[st1work["Caste catgeory in which the respondent's community is categorised?"].isin(input_value1)]
    
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
        fil8=fil6
    elif 'ALL' in input_value7:
        fil8=fil6
    else:
        fil8=fil6[fil6["Source or Destination"].isin(input_value7)]
    
        
    Castelist=optionState=createDroplist(getCastelist(fil8),'Caste')
    locationlist=optionState=createDroplist(getlocationlist(fil8),'Location')
    Religionllist=optionState=createDroplist(getReligionllist(fil8),'Religion')
    Genderlist=optionState=createDroplist(getGenderlist(fil8),'Gender')
    Statelist=optionState=createDroplist(getStatelist(fil8),'State')
    optionNGO=createDroplist(getNGO(fil8),"Source or Destination")
    
    return optionNGO,Castelist, locationlist, Religionllist, Genderlist, Statelist, barMigrationLocalPanchayat(fil8), barChildAmongOutside(fil8), barWalkMoreADay(fil8),pielevel2chart1(fil8),'Total Number: {}'.format(totalcount(fil8))#,barWhichStateReturn(fil6),pielevel2chart2(fil6)


# In[ ]:


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




