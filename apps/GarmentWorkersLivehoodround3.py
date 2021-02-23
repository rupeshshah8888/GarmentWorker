#!/usr/bin/env python
# coding: utf-8

# In[47]:


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
    return '#A9A9A9'
def paper_bgcolor1():
    return '#A9A9A9'

def piecolor():
    return ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']


# In[49]:


def barcolour():
    return ['#000099','#0000CC','#0000FF','#009999','#0099FF','#00FFFF']
#color_discrete_sequence=barcolour()


# In[50]:


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


# In[51]:


# filterpane
def getNGO(st1vill):
    return st1vill["Source or Destination"].unique()

def getDebtBeforelist(st1work):
    return st1work['Does your family have access to smart phones with internet facilities?'].unique()

def getOccupationlist(st1work):
    return st1work['What is the work you are currently involved in?'].unique()

def getMigrantlist(st1work):
    return st1work['Have you or any of the family members had to return from outside after the announcement of lockdown?'].unique()

def getWageslist(st1work):
    return st1work['Did you get wages paid for the month of October ?'].unique()


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





# In[52]:


def stylecss():
    return {'height': '100%', 'width': '100%' , 'font-size': '12px'}

def start():
    start=([
        html.H2("Livelihood",style={'text-align': 'center', 'colour':'green' } ),
        html.P(''),
        html.Button(id='TotalDatadb', style={'text-align': 'center', 'font-size': '15px',
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
                    dbc.Col(dcc.Dropdown(id='NGOdb',options=createDroplist(getNGO(st1work) , "Source or Destination"), value='ALL',multi=True,placeholder="Source or Destination"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown'
                            ,md=dict(size=2)),
                    
                        
                    dbc.Col(dcc.Dropdown(id='Wagesdb',options=createDroplist(getWageslist(st1work) , 'Wages'), value='ALL',multi=True,placeholder="Wages", 
                                        style=stylecss()),
                            style={'padding-right': '0%','padding-left':'0%', 'font-size': '15px'},className='dropdown',md=dict(size=2)),

                        
                    dbc.Col(dcc.Dropdown(id='Migrantdb',options=createDroplist(getMigrantlist(st1work) , 'Migrant'), value='ALL',multi=True,placeholder="Migrant", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' }),
                            style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    
                        
                    dbc.Col(dcc.Dropdown(id='Occupationdb',options=createDroplist(getOccupationlist(st1work) , 'Occupation'), value='ALL',multi=True,placeholder="Occupation", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px', }),
                            style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                        
                    dbc.Col(dcc.Dropdown(id='DebtBeforedb',options=createDroplist(getDebtBeforelist(st1work) , 'DebtBefore'), value='ALL',multi=True,placeholder="Debt Before", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' }),
                            style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                        
                    dbc.Col(dcc.Dropdown(id='Castedb',options=createDroplist(getCastelist(st1work) , 'Caste'), value='ALL',multi=True,placeholder="Caste", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' }),
                            style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Locationdb',options=createDroplist(getlocationlist(st1work),'Location'), value='ALL',multi=True,placeholder="Type of location "
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Religiondb',options=createDroplist(getReligionllist(st1work),'Religion'), value='ALL',multi=True,placeholder="Religion"
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Genderdb',options=createDroplist(getGenderlist(st1work),'Gender'), value='ALL',multi=True,placeholder="Gender",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                        
                    dbc.Col(dcc.Dropdown(id='Statedb',options=createDroplist(getStatelist(st1work),'State'), value='ALL',multi=True,placeholder="State",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                        
                     dbc.Col(dcc.Dropdown(id='monthdb' ,options=[{'label': 'October', 'value': 'October'},
                                                    {'label': 'November', 'value': 'November'},
                                                    {'label': 'December', 'value': 'December'},
                                      ],value='October'
                                          ,placeholder="Month",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                        
                    
                    ]
                     ,
                    
                    
                        ),
                ]),
            
    ])
    return start


# In[53]:


# Chart 1st level
#Loan During Lockdown                                                              
#st1work['Have you or your family taken loan during the lockdown period?']          

#DiD you lose your job after lockdown
#st1work['Was anyone in your family provided with work under MGNREGA in the month of April?']

def barlevel1chart1(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Have you or your family taken loan after March in this year?'].value_counts()
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1
                 )
    fig.update_layout(showlegend=False)
    fig.update_layout(
    title='',
    xaxis=dict(title='',color='#ffffff'),yaxis=dict(title='',color='#ffffff'),
    plot_bgcolor='rgb(255, 255, 255)'
    ,margin={"r":0,"t":0,"l":0,"b":0},
    height=400
    
   
    )
    
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    
    return fig

def barlevel1chart2(fil4):
    Bardata1=fil4['What is the work you are currently involved in?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1, text=Bardata1,
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


# In[54]:


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
def barlevel2chart1(fil4, month='October'):
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

def bar1evel2chart2(fil4 , month='October'):
    
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


# In[55]:


def pielevel3chart1(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Has there been any change in wages and working condition at the place of migration compared to earlier times?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,  title='',hole=.7,height=400 )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig
def pielevel3chart2(fil4):
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    
    Bardata1=fil4['Have any of your family members migrated for work post the relaxation of lockdown?'].value_counts()
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,   title='',height=400)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0} )
    fig.update_traces(hole=.7,hoverinfo='label+percent+name', textinfo='value', textfont_size=20,
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig


# In[56]:


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
                    dbc.Col([html.P('Looking at the Current Situation, is it likely that children will be Engaged in Work'),
                        dcc.Graph(id='pielevel2chart1db',figure= pielevel2chart1(st1work),config=cong() ),
                            ],md=4),
                    dbc.Col([ html.P('Have you or your family taken loan during the lockdown period?'),
                        dcc.Graph(id='barlevel1chart1db',figure= barlevel1chart1(st1work),config=cong() ),
                             ],md=4),
                           
                    dbc.Col([html.P('When did you lose your job?'),
                        dcc.Graph(id='barlevel1chart2db',figure= barlevel1chart2(st1work),config=cong() ),
                            ],md=4),
    
                ],
                style={'height': "100%"},
                align="center",
            ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([html.P('Work Provided under MNREGA '),
                            dcc.Graph(id='barlevel2chart1db',figure= barlevel2chart1(st1work),config=cong() ),],md=3),
                    dbc.Col([html.P('Wages for'),
                            dcc.Graph(id='bar1evel2chart2db',figure= bar1evel2chart2(st1work),config=cong() ),],md=3),
                    dbc.Col([html.P('Any change in wages and working condition at the place of migration compared to earlier times'),
                             dcc.Graph(id='pielevel3chart1db',figure= pielevel3chart1(st1work),config=cong() ),],md=3),
                    dbc.Col([html.P('Have any of your family members migrated for work post the relaxation of lockdown?'),
                             dcc.Graph(id='pielevel3chart2db',figure= pielevel3chart2(st1work),config=cong() ),
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
    
    Output(component_id='Wagesdb', component_property='options'),
    Output(component_id='Migrantdb', component_property='options'),
    Output(component_id='Occupationdb', component_property='options'),
    Output(component_id='DebtBeforedb', component_property='options'),
    Output(component_id='Castedb', component_property='options'),
    Output(component_id='Locationdb', component_property='options'),
    Output(component_id='Religiondb', component_property='options'),
    Output(component_id='Genderdb', component_property='options'),
    Output(component_id='Statedb', component_property='options'),
    
    Output(component_id='pielevel3chart1db', component_property='figure'),
    Output(component_id='pielevel3chart2db', component_property='figure'),
    Output(component_id='pielevel2chart1db', component_property='figure'),
    Output(component_id='barlevel2chart1db', component_property='figure'), 
    Output(component_id='bar1evel2chart2db', component_property='figure'),
    Output(component_id='barlevel1chart1db', component_property='figure'),
    Output(component_id='barlevel1chart2db', component_property='figure'),
    Output(component_id='TotalDatadb', component_property='children'),
    
    Input(component_id='Wagesdb', component_property='value'),
    Input(component_id='Migrantdb', component_property='value'),
    Input(component_id='Occupationdb', component_property='value'),
    Input(component_id='DebtBeforedb', component_property='value'),
    Input(component_id='Castedb', component_property='value'),
    Input(component_id='Locationdb', component_property='value'),
    Input(component_id='Religiondb', component_property='value'),
    Input(component_id='Genderdb', component_property='value'),
    Input(component_id='Statedb', component_property='value'),
    Input(component_id='monthdb', component_property='value'),
    
    Input(component_id='NGOdb', component_property='value'),
    
   # Input(component_id='stageselection', component_property='value'),
)
def update_output1(input_value,input_value1,input_value2,input_value3,input_value4,input_value5,input_value6,input_value7,input_value8,month,input_value9):
    month=month
    if len(input_value) == 0:
        fil1=st1work
    elif 'ALL' in input_value:
        fil1=st1work
    else:
        fil1=st1work[st1work['Did you get wages paid for the month of October ?'].isin(input_value)]
        
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
        fil3=fil2[fil2['What is the work you are currently involved in?'].isin(input_value2)]
        
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
        
    if len(input_value8) == 0:
        fil10=fil9
    elif 'ALL' in input_value8:
        fil10=fil9
    else:
        fil10=fil9[fil9["Source or Destination"].isin(input_value8)]
    
        
 
    
    DebtBeforelist=optionState=createDroplist(getDebtBeforelist(fil10),'DebtBefore')
    Occupationlist=optionState=createDroplist(getOccupationlist(fil10),'Occupation')
    Migrantlist=optionState=createDroplist(getMigrantlist(fil10),'Migrant')
    Wageslist=optionState=createDroplist(getWageslist(fil10),'Wages')
    
    Castelist=optionState=createDroplist(getCastelist(fil10),'Caste')
    locationlist=optionState=createDroplist(getlocationlist(fil10),'Location')
    Religionllist=optionState=createDroplist(getReligionllist(fil10),'Religion')
    Genderlist=optionState=createDroplist(getGenderlist(fil10),'Gender')
    Statelist=optionState=createDroplist(getStatelist(fil10),'State')
    
    
    
    
    return Wageslist ,Migrantlist,Occupationlist,DebtBeforelist, Castelist, locationlist, Religionllist, Genderlist, Statelist, pielevel3chart1(fil10),pielevel3chart2(fil10),pielevel2chart1(fil10),barlevel2chart1(fil10,month),bar1evel2chart2(fil10,month),barlevel1chart1(fil10),barlevel1chart2(fil10),'Total Number: {}'.format(totalcount(fil10))


# In[ ]:





# In[58]:


if __name__ == '__main__':
    app.run_server(host= '127.0.0.1',debug=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




