#!/usr/bin/env python
# coding: utf-8

# In[13]:


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


# In[14]:


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


# In[16]:


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


# In[17]:


# filterpane


def getDebtBeforelist(st1work):
    return st1work['Does your family have access to smart phones with internet facilities?'].unique()

def getOccupationlist(st1work):
    return st1work['What is the work you are currently involved in?'].unique()

def getMigrantlist(st1work):
    return st1work['Have you or any of the family members had to return from outside after the announcement of lockdown?'].unique()

def getWageslist(st1work):
    return st1work['Did you get wages paid for the month of September ?'].unique()


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





# In[18]:


def stylecss():
    return {'height': '100%', 'width': '100%' , 'font-size': '12px'}

def start():
    start=([
        html.H2("Livelihood",style={'text-align': 'center', 'colour':'green' } ),
        html.P(''),
        html.Button(id='TotalDatada', style={'text-align': 'center', 'font-size': '15px',
                                             'background-color': '#FF8C00',
                                             'color': 'white',
                                             'text-align': 'center',
                                             'text-decoration': 'none',
                                             'display': 'inline-block',

                                             'margin': '4px 2px',
                                             }),
        html.Div([
                dbc.Row(
                    [
                        
                    dbc.Col(dcc.Dropdown(id='Wagesda',options=createDroplist(getWageslist(st1work) , 'Wages'), value='ALL',multi=True,placeholder="Wages", 
                                        style=stylecss()),
                            style={'padding-right': '0%','padding-left':'0%', 'font-size': '15px'},md=dict(size=2)),

                        
                    dbc.Col(dcc.Dropdown(id='Migrantda',options=createDroplist(getMigrantlist(st1work) , 'Migrant'), value='ALL',multi=True,placeholder="Migrant", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' }),
                            style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),

                    
                        
                    dbc.Col(dcc.Dropdown(id='Occupationda',options=createDroplist(getOccupationlist(st1work) , 'Occupation'), value='ALL',multi=True,placeholder="Occupation", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px', }),
                            style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),

                        
                    dbc.Col(dcc.Dropdown(id='DebtBeforeda',options=createDroplist(getDebtBeforelist(st1work) , 'DebtBefore'), value='ALL',multi=True,placeholder="Debt Before", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' }),
                            style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),

                        
                    dbc.Col(dcc.Dropdown(id='Casteda',options=createDroplist(getCastelist(st1work) , 'Caste'), value='ALL',multi=True,placeholder="Caste", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' }),
                            style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Locationda',options=createDroplist(getlocationlist(st1work),'Location'), value='ALL',multi=True,placeholder="Type of location "
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Religionda',options=createDroplist(getReligionllist(st1work),'Religion'), value='ALL',multi=True,placeholder="Religion"
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Genderda',options=createDroplist(getGenderlist(st1work),'Gender'), value='ALL',multi=True,placeholder="Gender",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),
                        
                    dbc.Col(dcc.Dropdown(id='Stateda',options=createDroplist(getStatelist(st1work),'State'), value='ALL',multi=True,placeholder="State",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),
                        
                     dbc.Col(dcc.Dropdown(id='monthda' ,options=[ 
                                        {'label': 'July', 'value': 'July'},
                                        {'label': 'August', 'value': 'August'},
                                        {'label': 'September', 'value': 'September'},
                                      ],value='July'
                                          ,placeholder="Month",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},md=dict(size=2)),

                        
                    
                    ]
                     ,
                    
                    
                        ),
                ]),
            
    ])
    return start


# In[19]:


# Chart 1st level
#Loan During Lockdown                                                              
#st1work['Have you or your family taken loan during the lockdown period?']          

#DiD you lose your job after lockdown
#st1work['Was anyone in your family provided with work under MGNREGA in the month of April?']

def barlevel1chart1(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Have you or your family taken loan during the lockdown period?'].value_counts()
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1)
    fig.update_layout(showlegend=False)
    fig.update_layout(
    title='',
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
    ,margin={"r":0,"t":0,"l":0,"b":0},
    height=400
    
   
    )
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    
    
    
    
    return fig

def barlevel1chart2(fil4):
    Bardata1=fil4['When did you lose your job?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= '',)
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
        ,height=400)
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig


# In[20]:


def pielevel2chart1(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4["Looking at the current situation, is it likely that children will be engaged in work?"].value_counts()
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,  #color=Bardata1,
                 title='',height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig
def barlevel2chart1(fil4, month='July'):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Was anyone in your family provided with work under MGNREGA in the month of '+month+'?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1, text=Bardata1,
                 title= 'In '+month,)
    fig.update_layout(showlegend=False)
    fig.update_layout(
    title= 'In '+month+'',
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
        ,height=400)
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    
    return fig

def bar1evel2chart2(fil4 , month='July'):
    
    Bardata1=fil4['Did you get wages paid for the month of '+month+' ?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1, text=Bardata1,
                 title= '',)
    fig.update_layout(showlegend=False)
    fig.update_layout(
    title= month,
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
        ,height=400)
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig


# In[21]:


def pielevel3chart1(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Has there been any change in wages and working condition?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,  title='',hole=.7,height=400 )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    
    return fig
def pielevel3chart2(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    
    Bardata1=fil4['Are you or any of your family members planning to migrate back for work?'].value_counts()
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,   title='',height=400)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0} )
    fig.update_traces(hole=.7,hoverinfo='label+percent+name', textinfo='value', textfont_size=20,
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig


# In[22]:

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
                    dbc.Col([html.P('Looking at the Current Situation, is it likely that children will be Engaged in Work'),
                        dcc.Graph(id='pielevel2chart1da',figure= pielevel2chart1(st1work),config=cong() ),
                            ],md=4),
                    dbc.Col([ html.P('Have you or your family taken loan during the lockdown period?'),
                        dcc.Graph(id='barlevel1chart1da',figure= barlevel1chart1(st1work),config=cong() ),
                             ],md=4),
                           
                    dbc.Col([html.P('When did you lose your job?'),
                        dcc.Graph(id='barlevel1chart2da',figure= barlevel1chart2(st1work),config=cong() ),
                            ],md=4),
    
                ],
                style={'height': "100%"},
                align="center",
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([html.P('Work Provided under MNREGA '),
                            dcc.Graph(id='barlevel2chart1da',figure= barlevel2chart1(st1work),config=cong() ),],md=3),
                    dbc.Col([html.P('Wages for'),
                            dcc.Graph(id='bar1evel2chart2da',figure= bar1evel2chart2(st1work),config=cong() ),],md=3),
                    dbc.Col([html.P('Any change in wages and working condition at the place of migration compared to earlier times'),
                             dcc.Graph(id='pielevel3chart1da',figure= pielevel3chart1(st1work),config=cong() ),],md=3),
                    dbc.Col([html.P('Are you or any of your family members planning to migrate back for work'),
                             dcc.Graph(id='pielevel3chart2da',figure= pielevel3chart2(st1work),config=cong() ),
                            ],md=3),
                    
    
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
             
        ],style={'padding-right': '0%','padding-left': '0%'}),
    ],
    fluid=True,
)


def totalcount(file):
    return len(file.index)


@app.callback( 
    
    Output(component_id='Wagesda', component_property='options'),
    Output(component_id='Migrantda', component_property='options'),
    Output(component_id='Occupationda', component_property='options'),
    Output(component_id='DebtBeforeda', component_property='options'),
    Output(component_id='Casteda', component_property='options'),
    Output(component_id='Locationda', component_property='options'),
    Output(component_id='Religionda', component_property='options'),
    Output(component_id='Genderda', component_property='options'),
    Output(component_id='Stateda', component_property='options'),
    
    Output(component_id='pielevel3chart1da', component_property='figure'),
    Output(component_id='pielevel3chart2da', component_property='figure'),
    Output(component_id='pielevel2chart1da', component_property='figure'),
    Output(component_id='barlevel2chart1da', component_property='figure'), 
    Output(component_id='bar1evel2chart2da', component_property='figure'),
    Output(component_id='barlevel1chart1da', component_property='figure'),
    Output(component_id='barlevel1chart2da', component_property='figure'),
    Output(component_id='TotalDatada', component_property='children'),
    
    Input(component_id='Wagesda', component_property='value'),
    Input(component_id='Migrantda', component_property='value'),
    Input(component_id='Occupationda', component_property='value'),
    Input(component_id='DebtBeforeda', component_property='value'),
    Input(component_id='Casteda', component_property='value'),
    Input(component_id='Locationda', component_property='value'),
    Input(component_id='Religionda', component_property='value'),
    Input(component_id='Genderda', component_property='value'),
    Input(component_id='Stateda', component_property='value'),
    Input(component_id='monthda', component_property='value'),
    
   # Input(component_id='stageselection', component_property='value'),
)
def update_output1(input_value,input_value1,input_value2,input_value3,input_value4,input_value5,input_value6,input_value7,input_value8,month):
    month=month
    if len(input_value) == 0:
        fil1=st1work
    elif 'ALL' in input_value:
        fil1=st1work
    else:
        fil1=st1work[st1work['Did you get wages paid for the month of September ?'].isin(input_value)]
        
    if len(input_value1) == 0:
        fil2=fil1
    elif 'ALL' in input_value1:
        fil2=fil1
    else:
        fil2=fil1[fil1['Have you or any of the family members had to return from outside after the announcement of lockdown?'].isin(input_value1)]
        
    if len(input_value2) == 0:
        fil3=fil2
    elif 'ALL' in input_value2:
        fil3=fil2
    else:
        fil3=fil2[fil2['What was the work you were involved in right before the lockdown or are currently involved in?'].isin(input_value2)]
        
    if len(input_value3) == 0:
        fil4=fil3
    elif 'ALL' in input_value3:
        fil4=fil3
    else:
        fil4=fil3[fil3["Does your family have access to smart phones with internet facilities?"].isin(input_value3)]
        
    if len(input_value4) == 0:
        fil5=fil4
    elif 'ALL' in input_value4:
        fil5=fil4
    else:
        fil5=fil4[fil4["Caste catgeory in which the respondent's community is categorised?"].isin(input_value4)]
    
    if len(input_value5) == 0:
        fil6=fil5
    elif 'ALL' in input_value5:
        fil6=fil5
    else:
        fil6=fil5[fil5["Type of location from where the data is being collected"].isin(input_value5)]
    
    if len(input_value6) == 0:
        fil7=fil6
    elif 'ALL' in input_value6:
        fil7=fil6
    else:    
        fil7=fil6[fil6["Religion of the Respondent"].isin(input_value6)]
        
    if len(input_value7) == 0:
        fil8=fil7
    elif 'ALL' in input_value7:
        fil8=fil7
    else:
        fil8=fil7[fil7['Gender of the Respondent'].isin(input_value7)]
    
    if len(input_value8) == 0:
        fil9=fil8
    elif 'ALL' in input_value8:
        fil9=fil8
    else:
        fil9=fil8[fil8['State'].isin(input_value8)]
        
 
    
    DebtBeforelist=optionState=createDroplist(getDebtBeforelist(fil9),'DebtBefore')
    Occupationlist=optionState=createDroplist(getOccupationlist(fil9),'Occupation')
    Migrantlist=optionState=createDroplist(getMigrantlist(fil9),'Migrant')
    Wageslist=optionState=createDroplist(getWageslist(fil9),'Wages')
    
    Castelist=optionState=createDroplist(getCastelist(fil9),'Caste')
    locationlist=optionState=createDroplist(getlocationlist(fil9),'Location')
    Religionllist=optionState=createDroplist(getReligionllist(fil9),'Religion')
    Genderlist=optionState=createDroplist(getGenderlist(fil9),'Gender')
    Statelist=optionState=createDroplist(getStatelist(fil9),'State')
    
    
    
    
    return Wageslist ,Migrantlist,Occupationlist,DebtBeforelist, Castelist, locationlist, Religionllist, Genderlist, Statelist, pielevel3chart1(fil9),pielevel3chart2(fil9),pielevel2chart1(fil9),barlevel2chart1(fil9,month),bar1evel2chart2(fil9,month),barlevel1chart1(fil9),barlevel1chart2(fil9),'Total Number: {}'.format(totalcount(fil9))


# In[ ]:





# In[24]:


if __name__ == '__main__':
    app.run_server(host= '127.0.0.1',debug=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




