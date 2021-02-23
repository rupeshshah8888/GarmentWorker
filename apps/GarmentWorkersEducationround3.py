#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
def piecolor():
    return ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']


# In[3]:


def barcolour():
    return ['#000099','#0000CC','#0000FF','#009999','#0099FF','#00FFFF']
#color_discrete_sequence=barcolour()


# In[4]:


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


# In[5]:


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
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(showlegend=False)
    return fig


# In[6]:


# filterpane


def getNGO(st1vill):
    return st1vill["Source or Destination"].unique()

def getBlock(st1vill):
    return st1vill["Block"].unique()

def getDistrict(st1vill):
    return st1vill["District"].unique()


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


# In[7]:


def stylecss():
    return {'height': '100%', 'width': '100%' , 'font-size': '12px'}

def start():
    start=([
        html.H2("EDUCATION",style={'text-align': 'center', 'colour':'green' } ),
        html.Button(id='TotalDatabb',style={'text-align': 'center', 'font-size': '15px', 
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
                    dbc.Col(dcc.Dropdown(id='NGObb',options=createDroplist(getNGO(st1work) , "Source or Destination"), value='ALL',multi=True,placeholder="Source or Destination"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown'
                            ,md=dict(size=2)),
                    
                    dbc.Col(dcc.Dropdown(id='Statebb',options=createDroplist(getStatelist(st1work),'State'), value='ALL',multi=True,placeholder="State",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                    
                    
                        
                    dbc.Col(dcc.Dropdown(id='Castebb',options=createDroplist(getCastelist(st1work) , 'Caste'), value='ALL',multi=True,placeholder="Caste", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '12px' }),
                            style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Locationbb',options=createDroplist(getlocationlist(st1work),'Location'), value='ALL',multi=True,placeholder="Type of location "
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Religionbb',options=createDroplist(getReligionllist(st1work),'Religion'), value='ALL',multi=True,placeholder="Religion"
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Genderbb',options=createDroplist(getGenderlist(st1work),'Gender'), value='ALL',multi=True,placeholder="Gender",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                        
                        
                    dbc.Col(dcc.Dropdown(id='monthbb',options= [{'label': 'October', 'value': 'October'},
                                                    {'label': 'November', 'value': 'November'},
                                                    {'label': 'December', 'value': 'December'},
                                      ],value='October',
                                                                    placeholder="Month",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '12px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                        
                    ]
                     ,
                     
                    
                        ),
                ]),
            
    ])
    return start


# In[8]:


def barlevel1chart1(fil4,month='October'):
    month=month
    Bardata1=fil4['Whether school going children (6 to 14 years) received dry ration in lieu of mid-day meal for the month of '+month+'?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= 'In '+month,)
    fig.update_layout(showlegend=False)
    fig.update_layout(
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
    ,margin={"r":0,"t":40,"l":0,"b":0}
        ,height=300)
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig

def pielevel2chart1(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Are children in your family facing difficulty in accessing education through TV channels or online system?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title=' ',hole=.7 ,height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig


def barlevel2chart1(fil4):
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
            'margin':{"r":0,"t":10,"l":30,"b":30},'height':300,
            'plot_bgcolor':plot_bgcolor1(),
            'paper_bgcolor':paper_bgcolor1()
        }
    }
            
        
    return figure


# In[9]:


def bar1(fil4,month='October'):
    month=month
    Bardata1=fil4['Have children in your family registered for any private online platform education?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= ' ',)
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis=dict(title='',color='#ffffff'),yaxis=dict(title='',color='#ffffff'),plot_bgcolor='rgb(255, 255, 255)',
                      margin={"r":0,"t":0,"l":0,"b":0},height=300)
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig
def bar2(fil4,month='October'):
    month=month
    Bardata1=fil4['Have children been provided free text books in government schools?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= '',)
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis=dict(title='',color='#ffffff'),yaxis=dict(title='',color='#ffffff'),plot_bgcolor='rgb(255, 255, 255)',
                      margin={"r":0,"t":0,"l":0,"b":0},height=300)
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig
def bar3(fil4,month='October'):
    month=month
    Bardata1=fil4['Have children in your family been able to access any form of offline education? (Coaching/Tuition Centres)'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= '',)
    fig.update_layout(showlegend=False)
    fig.update_layout(xaxis=dict(title='',color='#ffffff'),yaxis=dict(title='',color='#ffffff'),plot_bgcolor='rgb(255, 255, 255)',
                      margin={"r":0,"t":0,"l":0,"b":0},height=300)
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig
def piel(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['What was/were the purpose for taking the loan? (Multiple options possible)/Buy digital device for children education'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='',hole=.7 ,height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig


# In[10]:


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
              dbc.Row(
                [
                    dbc.Col([html.P('Whether School Going Children (6 to 14 years) received Dry Ration <br>In lieu of Mid-Day Meal For The Month of'),
                             dcc.Graph(id='barlevel1chart1bb',figure= barlevel1chart1(st1work),config=cong())],md=6),
                    dbc.Col([html.P("What was/were the purpose for taking the loan during the lockdown? (Multiple options possible)/Buy digital device for children education"),
                             dcc.Graph(id='pie1bb',figure= piel(st1work),config=cong())],md=6),
                    
                ],
                style={'height': "100%"},
                align="center",
            ),
            html.Br(),
              dbc.Row(
                [
                    dbc.Col([html.P("Have children in your family registered for any private online platform education?"),
                        dcc.Graph(id='bar1bb',figure= bar1(st1work),config=cong())],md=4),
                    dbc.Col([html.P("Have children been provided free text books in government schools?"),
                        dcc.Graph(id='bar2bb',figure= bar2(st1work),config=cong())],md=4),
                    dbc.Col([html.P("Have children in your family been able to access any form of offline education? (Coaching/Tuition Centres)"),
                        dcc.Graph(id='bar3bb',figure= bar3(st1work),config=cong())],md=4),
                    
                ],
                style={'height': "100%"},
                align="center",
            ),
            html.Br(),
             dbc.Row(
                [
                    dbc.Col(dcc.Graph(id='graphbb',figure= quick_plot1(st1work),config=cong() ),md=6),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([html.P('Are children in your family facing difficulty in accessing education through TV channels or online system?'),
                                dcc.Graph(id='pielevel2chart1bb',figure= pielevel2chart1(st1work),config=cong() )],md=12),
                            dbc.Col([html.P("Looking at the current situation, is it likely that Boys-Girls will dropout from school?")
                                ,dcc.Graph(id='barlevel2chart1bb',figure= barlevel2chart1(st1work),config=cong() )],md=12),
                            
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


# In[11]:



def totalcount(file):
    
    return len(file.index)


# In[12]:


@app.callback( 
    Output(component_id='pie1bb', component_property='figure'),
    Output(component_id='bar1bb', component_property='figure'), 
    Output(component_id='bar2bb', component_property='figure'),
    Output(component_id='bar3bb', component_property='figure'),
   
    Output(component_id='Castebb', component_property='options'),
    Output(component_id='Locationbb', component_property='options'),
    Output(component_id='Religionbb', component_property='options'),
    Output(component_id='Genderbb', component_property='options'),
    Output(component_id='Statebb', component_property='options'),
   
    
    Output(component_id='barlevel1chart1bb', component_property='figure'),
    Output(component_id='pielevel2chart1bb', component_property='figure'), 
    Output(component_id='barlevel2chart1bb', component_property='figure'),
    Output(component_id='TotalDatabb', component_property='children'),
    Output(component_id='graphbb', component_property='figure'),
   
    Input(component_id='Castebb', component_property='value'),
    Input(component_id='Locationbb', component_property='value'),
    Input(component_id='Religionbb', component_property='value'),
    Input(component_id='Genderbb', component_property='value'),
    Input(component_id='Statebb', component_property='value'),
    Input(component_id='monthbb', component_property='value'),
    Input(component_id='NGObb', component_property='value'),
    
    
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
    
    return piel(fil8),bar1(fil8),bar2(fil8),bar3(fil8),Castelist,locationlist,Religionllist,Genderlist,Statelist,barlevel1chart1(fil8,month),pielevel2chart1(fil8),barlevel2chart1(fil8),'Total Number: {}'.format(totalcount(fil8)),quick_plot1(fil8)


# In[ ]:


if __name__ == '__main__':
    app.run_server(host= '127.0.0.2',debug=False)


# In[ ]:





# In[ ]:





# In[ ]:




