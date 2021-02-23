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

data1 = pd.read_excel(DATA_PATH.joinpath('Collated_Round3_Workers.xlsx'), engine='openpyxl')
datamap = pd.read_csv(DATA_PATH.joinpath('state wise centroids_2011.csv'))
st1work=data1


def plot_bgcolor1():
    return '#A9A9A9'
def paper_bgcolor1():
    return '#A9A9A9'

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


def barcolour():
    return ['#568949','#F7EC3F', '#73B761', '#ABD4A0','#43B7A0']


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
    return st1work["In case you or your family owns farm land, please specify the land size?"].unique()


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
         html.Button(id='TotalData1xb',style={'text-align': 'center', 'font-size': '15px', 
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
                    dbc.Col(dcc.Dropdown(id='NGOxb',options=createDroplist(getNGO(st1work) , "Source or Destination"), value='ALL',multi=True,placeholder="Source or Destination"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown'
                            ,md=dict(size=2)),
                        
                    dbc.Col(dcc.Dropdown(id='Statexb',options=createDroplist(getStatelist(st1work),'State'), value='ALL',multi=True,placeholder="State")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),
                    
                    dbc.Col(dcc.Dropdown(id='Districtxb',options=createDroplist(getDistrict(st1work),'District'), value='ALL',multi=True,placeholder="District")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Blockxb',options=createDroplist(getBlock(st1work),'Block'), value='ALL',multi=True,placeholder="Block")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),


                        
                    dbc.Col(dcc.Dropdown(id='agriculturexb',options=createDroplist(getagriculturelist(st1work) , 'Involved in Farmings'), value='ALL',multi=True,placeholder="Involved in Farmings"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Castexb',options=createDroplist(getCastelist(st1work) , 'Caste'), value='ALL',multi=True,placeholder="Caste"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Locationxb',options=createDroplist(getlocationlist(st1work),'Location'), value='ALL',multi=True,placeholder="Type of location ")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Religionxb',options=createDroplist(getReligionllist(st1work),'Religion'), value='ALL',multi=True,placeholder="Religion")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Genderxb',options=createDroplist(getGenderlist(st1work),'Gender'), value='ALL',multi=True,placeholder="Gender")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),
                        
                    
                        
                    dbc.Col(dcc.Dropdown(id='OwnLandxb',options=createDroplist(getOwnLandList(st1work),'Own Land'), value='ALL',multi=True,placeholder="Own Land")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2))


                    ]
                     ,
                     
                    
                        ),
                ]),
            
    ])
    return start


# In[22]:


def barchart1(fil4):
    Bardata1=fil4["Did you or any of your family members received Rs 2000 under the Kisan Samman Nidhi Yojana between October- December?"].value_counts()
    Bardata2=fil4["Have you or your family taken loan after March in this year?"].value_counts()
    Bardata3=fil4["Whether you or your family are able to access inputs such as fertilisers/seeds at subsidied rates for rabi crop cycle?"].value_counts()
    figure={
        'data': [
            {'x':Bardata1.index, 'y' :Bardata1 , 'type': 'bar', 'name': 'Family Member Recive RS 20000','text':Bardata1},
            {'x':Bardata2.index, 'y' :Bardata2 , 'type': 'bar', 'name': 'Family taken loan after March in this year?'},
            {'x':Bardata3.index, 'y' :Bardata3 , 'type': 'bar', 'name': 'Family are Able to Access Inputs Such as Fertilisers/seeds'},
                            ],
        'layout': {
            #'title': 'Did you lose you job during or after the announcement of the lockdown?',
    'xaxis' : dict(
                title='',color='#ffffff'),
            'yaxis' : dict(
                title='',color='#ffffff'),
            'width': "10px",
            'autosize': True ,
            'plot_bgcolor':plot_bgcolor1(),
            'paper_bgcolor':paper_bgcolor1()
            
            },
        
        }
    return figure


def barchart2(fil4):
    Bardata1=fil4["Are you or anyone in your family is involved in farming/agriculture?"].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=['#0000CD'],
                 title= '',)
    fig.update_layout(showlegend=False,margin={"r":0,"t":0,"l":0,"b":0} ,height=400,xaxis=dict(title='',color='#ffffff'),yaxis=dict(title='',color='#ffffff'),)
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig



# In[23]:


def right():
    right=([
        dbc.Col(dcc.Graph(id='BarChart1xb',figure= barchart1(st1work),config=cong() ) ,md=12),
        dbc.Col([html.P('Your family is involved in farming/agriculture',style={'text-align': 'center' }),
            dcc.Graph(id='BarChart2xb',figure= barchart2(st1work),config=cong() )] ,md=12)
    ])
    return right


# In[24]:


def left():
    left=([
        dbc.Col(dcc.Graph(id='GeoMap1xb',figure= quick_plot1(st1work) ) ,md=12)
        
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
    Output(component_id='NGOxb', component_property='options'),
    Output(component_id='Districtxb', component_property='options'),
    Output(component_id='Blockxb', component_property='options'),
   
    Output(component_id='Castexb', component_property='options'),
    Output(component_id='Locationxb', component_property='options'),
    Output(component_id='Religionxb', component_property='options'),
    Output(component_id='Genderxb', component_property='options'),
    Output(component_id='Statexb', component_property='options'),
    Output(component_id='OwnLandxb', component_property='options'),
    Output(component_id='agriculturexb', component_property='options'),
    
    Output(component_id='BarChart1xb', component_property='figure'),
    Output(component_id='BarChart2xb', component_property='figure'),
    Output(component_id='GeoMap1xb', component_property='figure'),
    Output(component_id='TotalData1xb', component_property='children'),
    
    Input(component_id='Castexb', component_property='value'),
    Input(component_id='Locationxb', component_property='value'),
    Input(component_id='Religionxb', component_property='value'),
    Input(component_id='Genderxb', component_property='value'),
    Input(component_id='Statexb', component_property='value'),
    Input(component_id='OwnLandxb', component_property='value'),
    Input(component_id='agriculturexb', component_property='value'),
    Input(component_id='NGOxb', component_property='value'),
    Input(component_id='Districtxb', component_property='value'),
    Input(component_id='Blockxb', component_property='value'),
   
)
def update_output1(input_value,input_value1,input_value2,input_value3,input_value4,input_value5,input_value6,input_value7,input_value8,input_value9):
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
        fil6=fil5[fil5["In case you or your family owns farm land, please specify the land size?"].isin(input_value5)]
    
    if len(input_value6) == 0:
        fil7=fil6
    elif 'ALL' in input_value6:
        fil7=fil6
    else:
        fil7=fil6[fil6["Are you or anyone in your family is involved in farming/agriculture?"].isin(input_value6)]
        
    if len(input_value7) == 0:
        fil8=fil7
    elif 'ALL' in input_value7:
        fil8=fil7
    else:
        fil8=fil7[fil7["Source or Destination"].isin(input_value7)]
    
    if len(input_value8) == 0:
        fil9=fil8
    elif 'ALL' in input_value8:
        fil9=fil8
    else:
        fil9=fil8[fil8["District"].isin(input_value8)]
    
    if len(input_value9) == 0:
        fil10=fil9
    elif 'ALL' in input_value9:
        fil10=fil9
    else:
        fil10=fil9[fil9["Block"].isin(input_value9)]
    
    
    agriculturelist=optionState=createDroplist(getagriculturelist(fil10),'Involved in Farmings')
    castelist=optionState=createDroplist(getCastelist(fil10),'Caste')
    locationlist=optionState=createDroplist(getlocationlist(fil10),'Location')
    Religionllist=optionState=createDroplist(getReligionllist(fil10),'Religion')
    Genderlist=optionState=createDroplist(getGenderlist(fil10),'Gender')
    Statelist=optionState=createDroplist(getStatelist(fil10),'State')
    OwnLandList=optionState=createDroplist(getOwnLandList(fil10),'Own Land')
    
    optionNGO=createDroplist(getNGO(fil10),"Source or Destination")
    optionBlock=createDroplist(getBlock(fil10),"Block")
    optionDistrict=createDroplist(getDistrict(fil10),"District")
    
    
    return optionNGO,optionDistrict,optionBlock,castelist,locationlist,Religionllist,Genderlist,Statelist,OwnLandList,agriculturelist,barchart1(fil10),barchart2(fil10),quick_plot1(fil10),'Total Number: {}'.format(totalcount(fil10)) 


# In[ ]:


if __name__ == '__main__':
    app.run_server(host= '127.0.0.2',debug=False)


# In[ ]:





# In[ ]:





# In[ ]:




