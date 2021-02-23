#!/usr/bin/env python
# coding: utf-8

# In[21]:


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


def plot_bgcolor1():
    return '#a9a9a9'
def paper_bgcolor1():
    return '#a9a9a9'
def piecolor():
    return ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']

def barcolour():
    return ['#000099','#0000CC','#0000FF','#009999','#0099FF','#00FFFF']
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


# In[ ]:





# In[ ]:





# In[23]:


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

    
    


# In[24]:


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


# In[ ]:



      


# In[25]:


def left():
    left=([
        html.H2('Access to Food',style={'textAlign': 'center'}), 
        html.Button(id='TotalDataib',style={'text-align': 'center', 'font-size': '15px', 
                                           'background-color': '#FF8C00',
                                             'color': 'white',
                                              'text-align': 'center',
                                              'text-decoration': 'none',
                                              'display': 'inline-block',
                                             
                                              'margin': '4px 2px',
                                                } ),
 
        html.P('To capture an understanding of the access to food, respondents were asked about ration and the number of meals they were able to afford.'
               ,style={'textAlign': 'center'}),

               
        
        
       
        html.P('Click on any variable from the tables below to get the correlated entitlement status of those individuals'),
        html.Div([
                dbc.Row( 
                    [
                    dbc.Col(dcc.Dropdown(id='Casteib',options=createDroplist(getCastelist(data1) , 'Caste'), value='ALL',multi=True,placeholder="Caste"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},md=dict(size=3)),

                    dbc.Col(dcc.Dropdown(id='Locationib',options=createDroplist(getlocationlist(data1),'Location'), value='ALL',multi=True,placeholder="Type of location ")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},md=dict(size=3)),

                    dbc.Col(dcc.Dropdown(id='Stateib',options=createDroplist(getStatelist(data1),'State'), value='ALL',multi=True,placeholder="State")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},md=dict(size=3)),

                    dbc.Col(dcc.Dropdown(id='Religionib',options=createDroplist(getReligionlist(data1),'Religion'), value='ALL',multi=True,placeholder="Religion")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},md=dict(size=3)),
                   
                    dbc.Col(dcc.Dropdown(id='Genderib',options=createDroplist(getGenderlist(data1),'Gender'), value='ALL',multi=True,placeholder="Gender")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},md=dict(size=3)),
                            
                        
                    dbc.Col(dcc.Dropdown(id='monthib'
                             ,options=[ {'label': 'October', 'value': 'October'},
                                        {'label': 'November', 'value': 'November'},
                                        {'label': 'December', 'value': 'December'},
                                      ],value='October',style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'}),md=dict(size=3)),
                   
                   
                    
                ]),
            
  
            
    ])
        ])
    return left


# In[26]:


def Socialissues1(fil4):
    Bardata1=fil4['Were there any instances when you or anyone in your family had to go hungry during October to December?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= '',)
    fig.update_layout(showlegend=False)
    fig.update_layout(plot_bgcolor='rgb(255, 255, 255)',margin={"r":0,"t":0,"l":0,"b":0},bargap=0.4,height=300)
    fig.update_yaxes(title=None,color='#ffffff')
    fig.update_xaxes(title=None,color='#ffffff')
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig
    
def Socialissues2(fil4):
    Bardata1=fil4['Was there any day when you or any members in the family had maximum of one meal?'].value_counts()

    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= '',)
    fig.update_layout(showlegend=False)
    fig.update_layout(plot_bgcolor='rgb(255, 255, 255)',margin={"r":0,"t":0,"l":0,"b":0},bargap=0.4,height=300)
    fig.update_yaxes(title=None,color='#ffffff')
    fig.update_xaxes(title=None,color='#ffffff')
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig
def Socialissues3(fil4):
    Bardata1=fil4['Was there any day when you or any members in the family had maximum of two meals?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= '',)
    fig.update_layout(showlegend=False)
    fig.update_layout(plot_bgcolor='rgb(255, 255, 255)',margin={"r":0,"t":0,"l":0,"b":0},bargap=0.4,height=300)
    fig.update_yaxes(title=None,color='#ffffff')
    fig.update_xaxes(title=None,color='#ffffff')
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig


# In[27]:




def pielevelchart1(fil4 , month='October'):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Did you or any registered member in your family people get additional ration ( 5 kgs rice and 1Kg pulse) for the month of '+month+'?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='In '+month,hole=.7 )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig
def pielevelchart2(fil4 , month='October'):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Did as ration card holders you or any registered member also get cash support for the month of '+month+'?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='In '+month,hole=.7 )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig
def pielevelchart3(fil4 , month='October'):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Did you or any registered member in your family get dry ration as per existing quota for the month of '+month+'?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='In '+month,hole=.7 )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig
def pielevelchart4(fil4 , month='October'):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Looking at the current situation, is it likely that nutritional intake for people will come down?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='',hole=.7 )
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0},height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig



# In[28]:

layout = dbc.Container(
    [    
        
            dbc.Row(
                [
                   # dbc.Col(right(),md=6),
                    dbc.Col(left(),   md=12),
                ],
                style={'height': "100%"},
                align="center",
            ),
            
           
            html.Div(html.H5('Social Issues',style={'textAlign': 'center'})), 
            dbc.Row(
                [
                    dbc.Col([dbc.Row([html.P('Atleast one day your family had to go hungry'),
                        dbc.Col(dcc.Graph(id='Entitlements1ib',figure= Socialissues1(data1),config=cong()),md=12)])], md=4 ),
                    dbc.Col([dbc.Row([html.P('A day when your family had maximum of one meal'),
                        dbc.Col(dcc.Graph(id='Entitlements2ib',figure= Socialissues2(data1),config=cong()),md=12)]),], md=4 ),
                    dbc.Col([dbc.Row([html.P('A day when your family had a maximum of two meals'),
                        dbc.Col(dcc.Graph(id='Entitlements3ib',figure= Socialissues3(data1),config=cong()),md=12)]),], md=4 ),
                    ]        ,
                style={'height': "100%"},
                align="center",
            ),
       
        dbc.Row(
                [
                    dbc.Col([dbc.Row([
                        dbc.Col(dcc.Graph(id='graphib',figure= GeoMap(data1),config=cong()),md=12)])], md=6 ),
                    dbc.Col([dbc.Row([
                            dbc.Col([html.P("Did you get additional ration for the month"),
                                dcc.Graph(id='pension3ib',figure= pielevelchart1(data1),config=cong())],md=6),
                        dbc.Col([html.P("As ration card holders did you also get cash support for the month"),
                                dcc.Graph(id='pension4ib',figure= pielevelchart2(data1),config=cong())],md=6),
                        dbc.Col([html.P("Did you get dry ration as per existing quota for the month"),
                                dcc.Graph(id='pension5ib',figure= pielevelchart3(data1),config=cong())],md=6),
                        dbc.Col([html.P("Looking at the current situation, is it likely that nutritional intake for people will come down?"),
                                dcc.Graph(id='pension6ib',figure= pielevelchart4(data1),config=cong())],md=6)
                    
                    ]
                        
                        )], md=6 )
                   
                    
                ]        ,
                style={'height': "100%"},
                align="center",
            ),
        
        
 

        
    ],
    fluid=True,
)


# In[29]:


def totalcount(file):
    
    return len(file.index)


# In[30]:


#call Back Bar Graph1
@app.callback(
    
    
    Output(component_id='Casteib', component_property='options'),
    Output(component_id='Locationib', component_property='options'),
    Output(component_id='Stateib', component_property='options'),
    Output(component_id='Religionib', component_property='options'),
    Output(component_id='Genderib', component_property='options'),
              
    Output('graphib', 'figure'),
              
    Output('Entitlements1ib', 'figure'),
    Output('Entitlements2ib', 'figure'),
    Output('Entitlements3ib', 'figure'),
   
    
  
    Output('pension3ib', 'figure'),
    Output('pension4ib', 'figure'),
    Output('pension5ib', 'figure'),
    Output('pension6ib', 'figure'),
    Output(component_id='TotalDataib', component_property='children'),
    
    
          
    Input(component_id='Casteib', component_property='value'),
    Input(component_id='Locationib', component_property='value'),
    Input(component_id='Stateib', component_property='value'),
    Input(component_id='Religionib', component_property='value'),
    Input(component_id='Genderib', component_property='value'),
    Input(component_id='monthib', component_property='value'),
   # Input(component_id='stageselection', component_property='value'), 
)
def update_output1(input_value,input_value1,input_value2,input_value3,input_value4,month):
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
    optionCaste=createDroplist(getCastelist(fil5),'Caste')
    optionLocation=createDroplist(getlocationlist(fil5) , 'Location')
    optionState=createDroplist(getStatelist(fil5),'State')
    optionReligion=createDroplist(getReligionlist(fil5),'Religion')
    optionGender=createDroplist(getGenderlist(fil5),'Gender')
    
    
    
    
    return optionCaste,optionLocation,optionState,optionReligion,optionGender,GeoMap(fil5),Socialissues1(fil5),Socialissues2(fil5),Socialissues3(fil5),pielevelchart1(fil5,month),pielevelchart2(fil5,month),pielevelchart3(fil5,month),pielevelchart4(fil5,month),'Total Number: {}'.format(totalcount(fil5))


# In[ ]:





# In[31]:


if __name__ == '__main__':
    app.run_server(host= '127.0.0.1',debug=False)


# In[ ]:



                    

