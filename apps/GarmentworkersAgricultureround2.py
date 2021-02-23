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


import pathlib
from app import app

# Worker data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

data1 = pd.read_excel(DATA_PATH.joinpath('Round 2 Garment worker.xlsx'), engine='openpyxl')
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


# In[18]:


def cong():
    return { 'staticPlot': False,     # True, False
      'scrollZoom': True,      # True, False
      'doubleClick': 'reset',  # 'reset', 'autosize' or 'reset+autosize', False
      'showTips': False,       # True, False
      'displayModeBar': False,  # True, False, 'hover'
      'watermark': False,
      'displaylogo': False,
       'modeBarButtonsToRemove': [ 'hoverCompareCartesian', 'hoverClosestCartesian', 'toggleSpikelines','Pan'] 
           }


# In[19]:


def quick_plot1(abc):
    data=abc
    data=data["State"]
    a=data.drop_duplicates()
    data1=datamap
    df = pd.merge(a, data1, how="inner", on=["State", "State"])
    fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude", color="State", hover_name="State",size="Latitude",
                            hover_data=["State"],
                            color_discrete_sequence=['#003f5c'], zoom=4, height=800)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},showlegend=False)
    return fig


# In[ ]:





# In[20]:



# filterpane
def getNGO(st1vill):
    return st1vill["Source or Destination"].unique()

def getBlock(st1vill):
    return st1vill["Block"].unique()

def getDistrict(st1vill):
    return st1vill["District"].unique()
def getagriculturelist(st1work):
    return st1work["Are you or anyone in your family is involved in farming/agriculture?"].unique()

def getOwnLandList(st1work):
    return st1work["Do you or your family own land?"].unique()


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


# In[21]:


def start():
    start=([
        html.H2("Agriculture",style={'text-align': 'center', 'colour':'green' } ),
        html.Button(id='TotalDataxa',style={'text-align': 'center', 'font-size': '15px', 
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
                    dbc.Col(dcc.Dropdown(id='NGOxa',options=createDroplist(getNGO(st1work) , "Source or Destination"), value='ALL',multi=True,placeholder="Source or Destination"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'12px'},className='dropdown'
                            ,md=dict(size=2)),
                    
                    dbc.Col(dcc.Dropdown(id='Statexa',options=createDroplist(getStatelist(st1work),'State'), value='ALL',multi=True,placeholder="State")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'12px'},className='dropdown',md=dict(size=2)),
                    
                    #dbc.Col(dcc.Dropdown(id='Districtxa',options=createDroplist(getDistrict(st1work),'District'), value='ALL',multi=True,placeholder="District")
                    #        ,style={'padding-right': '0%','padding-left':'0%','fontSize':'12px'},className='dropdown',md=dict(size=2)),

                    #dbc.Col(dcc.Dropdown(id='Blockxa',options=createDroplist(getBlock(st1work),'Block'), value='ALL',multi=True,placeholder="Block")
                    #        ,style={'padding-right': '0%','padding-left':'0%','fontSize':'12px'},className='dropdown',md=dict(size=2)),

                    
                    dbc.Col(dcc.Dropdown(id='agriculturexa',options=createDroplist(getagriculturelist(st1work) , 'Involved in Farmings'), value='ALL',multi=True,placeholder="Involved in Farmings"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Castexa',options=createDroplist(getCastelist(st1work) , 'Caste'), value='ALL',multi=True,placeholder="Caste"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Locationxa',options=createDroplist(getlocationlist(st1work),'Location'), value='ALL',multi=True,placeholder="Type of location ")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Religionxa',options=createDroplist(getReligionllist(st1work),'Religion'), value='ALL',multi=True,placeholder="Religion")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Genderxa',options=createDroplist(getGenderlist(st1work),'Gender'), value='ALL',multi=True,placeholder="Gender")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),
                        
                    dbc.Col(dcc.Dropdown(id='OwnLandxa',options=createDroplist(getOwnLandList(st1work),'Own Land'), value='ALL',multi=True,placeholder="Own Land")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2))


                    ]
                     ,
                     
                    
                        ),
                ]),
            
    ])
    return start


# In[22]:


def barchart1(fil4):
    Bardata1=fil4["Did you or any of your family members received Rs 2000 under the Kisan Samman Nidhi Yojana between July- September?"].value_counts()
    Bardata2=fil4["Did your family have to take loan under compulsions for taking up agriculture in the upcoming agriculture cycle?"].value_counts()
    Bardata3=fil4["Whether you or your family are able to access inputs such as fertilisers/seeds at subsidies rates for upcoming (Kharif) crop cycle?"].value_counts()
    figure={
        'data': [
            {'x':Bardata1.index, 'y' :Bardata1 , 'type': 'bar', 'name': 'Family Member Recive RS 20000','text':Bardata1},
            {'x':Bardata2.index, 'y' :Bardata2 , 'type': 'bar', 'name': 'Family have to Take Loan Under Compulsions for Taking up Agriculture'},
            {'x':Bardata3.index, 'y' :Bardata3 , 'type': 'bar', 'name': 'Family are Able to Access Inputs Such as Fertilisers/seeds'},
                            ],
        'layout': {
            #'title': 'Did you lose you job during or after the announcement of the lockdown?',
    'xaxis' : dict(
                title='',
                titlefont=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            ),color= "#FFFFFF"),
            'yaxis' : dict(
                title='',
                titlefont=dict(
                family='Helvetica, monospace',
                size=12,
                color='#7f7f7f',
                textalign= 'center'
            ),color= "#FFFFFF"),
            'width': "10px",
            'autosize': True ,
            'plot_bgcolor':plot_bgcolor1(),
            'paper_bgcolor':paper_bgcolor1()
            
            
            },
        }
    return figure


def barchart2(fil4):
    Bardata1=fil4["Do you think there is any change in the labour rates for the labour engaged in agriculture?"].value_counts()
    fig = px.bar(x=Bardata1.index, y=Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=['#0000CD'],
                 title= '',)
    
    fig.update_layout(showlegend=False,plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    fig.update_yaxes(title=None,color= "#FFFFFF")
    fig.update_xaxes(title=None,color= "#FFFFFF")
    return fig



# In[23]:


def right():
    right=([
        dbc.Col(dcc.Graph(id='BarChart1xa',figure= barchart1(st1work),config=cong() ) ,md=12),
        dbc.Col([html.P('any change in the labour rates for the labour engaged in agriculture' ),
            dcc.Graph(id='BarChart2xa',figure= barchart2(st1work),config=cong() ) ],md=12)
    ])
    return right


# In[24]:


def left():
    left=([
        dbc.Col(dcc.Graph(id='GeoMap1xa',figure= quick_plot1(st1work) ) ,md=12)
        
    ])
    return left


# In[25]:


layout = dbc.Container(
    [    
        html.Div([
            dbc.Row(
                [
                    dbc.Col(start(),md=12),
                    dbc.Col(left(),md=6),
                    dbc.Col(right(), md=6),
                ],
                style={'height': "100%"},
                align="center",
            ),
        ],style={'padding-right': '0%','padding-left': '0%'}),
    ],
    fluid=True,
)

    


# In[26]:


def totalcount(file):
    
    return len(file.index)


# In[27]:


#call Back Bar Graph1
@app.callback( 
    Output(component_id='NGOxa', component_property='options'),
    #Output(component_id='Districtxa', component_property='options'),
    #Output(component_id='Blockxa', component_property='options'),
    Output(component_id='Castexa', component_property='options'),
    Output(component_id='Locationxa', component_property='options'),
    Output(component_id='Religionxa', component_property='options'),
    Output(component_id='Genderxa', component_property='options'),
    Output(component_id='Statexa', component_property='options'),
    Output(component_id='OwnLandxa', component_property='options'),
    Output(component_id='agriculturexa', component_property='options'),
    
    Output(component_id='BarChart1xa', component_property='figure'),
    Output(component_id='BarChart2xa', component_property='figure'),
    Output(component_id='GeoMap1xa', component_property='figure'),
    Output(component_id='TotalDataxa', component_property='children'),

    
    Input(component_id='Castexa', component_property='value'),
    Input(component_id='Locationxa', component_property='value'),
    Input(component_id='Religionxa', component_property='value'),
    Input(component_id='Genderxa', component_property='value'),
    Input(component_id='Statexa', component_property='value'),
    Input(component_id='OwnLandxa', component_property='value'),
    Input(component_id='agriculturexa', component_property='value'),
    Input(component_id='NGOxa', component_property='value'),
    
    
   # Input(component_id='stageselection', component_property='value'),
)
def update_output1(input_value,input_value1,input_value2,input_value3,input_value4,input_value5,input_value6,input_value7):
    if len(input_value) == 0:
        fil1=st1work
    elif 'ALL' in input_value:
        fil1=st1work
    else:
        fil1=st1work[st1work["Caste catgeory in which the respondent's community is categorised?" ].isin(input_value)]
        
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
        fil3=fil2[fil2["Religion of the Respondent"].isin(input_value2)]
        
    if len(input_value3) == 0:
        fil4=fil3
    elif 'ALL' in input_value3:
        fil4=fil3
    else:
        fil4=fil3[fil3["Gender of the Respondent"].isin(input_value3)]
        
    if len(input_value4) == 0:
        fil5=fil4
    elif 'ALL' in input_value4:
        fil5=fil4
    else:
        fil5=fil4[fil4["State"].isin(input_value4)]
    
    if len(input_value5) == 0:
        fil6=fil5
    elif 'ALL' in input_value5:
        fil6=fil5
    else:
        fil6=fil5[fil5["Do you or your family own land?"].isin(input_value5)]
    
    if len(input_value6) == 0:
        fil7=fil6
    elif 'ALL' in input_value6:
        fil7=fil6
    else:
        fil7=fil6[fil6["Are you or anyone in your family is involved in farming/agriculture?"].isin(input_value6)]
        
        
    if len(input_value7) == 0:
        fil10=fil7
    elif 'ALL' in input_value7:
        fil10=fil7
    else:
        fil10=fil7[fil7["Source or Destination"].isin(input_value7)]
    
    
    
        
    agriculturelist=optionState=createDroplist(getagriculturelist(fil10),'Involved in Farmings')
    castelist=optionState=createDroplist(getCastelist(fil10),'Caste')
    locationlist=optionState=createDroplist(getlocationlist(fil10),'Location')
    Religionllist=optionState=createDroplist(getReligionllist(fil10),'Religion')
    Statelist=optionState=createDroplist(getStatelist(fil10),'State')
    Genderlist=optionState=createDroplist(getGenderlist(fil10),'Gender')
    OwnLandList=optionState=createDroplist(getOwnLandList(fil10),'Own Land')
    optionNGO=createDroplist(getNGO(fil10),"Source or Destination")
    #optionBlock=createDroplist(getBlock(fil10),"Block")
    #optionDistrict=createDroplist(getDistrict(fil10),"District")
    
    return optionNGO,castelist,locationlist,Religionllist,Genderlist,Statelist,OwnLandList,agriculturelist,barchart1(fil10),barchart2(fil10),quick_plot1(fil10),'Total Number: {}'.format(totalcount(fil10)) # ,GEOMAP1(fil6)


# In[ ]:


if __name__ == '__main__':
    app.run_server(host= '127.0.0.2',debug=False)


# In[ ]:





# In[ ]:





# In[ ]:




