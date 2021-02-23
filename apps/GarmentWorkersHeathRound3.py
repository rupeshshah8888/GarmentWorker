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


# In[2]:
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




# In[3]:


def piecolor():
    return ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']

def barcolour():
    return ['#000099','#0000CC','#0000FF','#009999','#0099FF','#00FFFF']


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
    fig.update_layout(showlegend=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig


# In[6]:


# filterpane

def getNGO(st1vill):
    return st1vill["Source or Destination"].unique()

def getDistrict(st1vill):
    return st1vill["District"].unique()

def getBlock(st1vill):
    return st1vill["Block"].unique()

    


def getLoanlist(st1work):
    return st1work["Have you or your family taken loan after March in this year?"].unique()


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
        html.H2("Health",style={'text-align': 'center', 'color':'#ffffff' } ),
        html.Button(id='TotalDatacb',style={'text-align': 'center', 'font-size': '15px',
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
                    dbc.Col(dcc.Dropdown(id='NGOcb',options=createDroplist(getNGO(st1work) , "Source or Destination"), value='ALL',multi=True,placeholder="Source or Destination"),
                            style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown'
                            ,md=dict(size=2)),
                    dbc.Col(dcc.Dropdown(id='Statecb',options=createDroplist(getStatelist(st1work),'State'), value='ALL',multi=True,placeholder="State",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                    
                    dbc.Col(dcc.Dropdown(id='Districtcb',options=createDroplist(getDistrict(st1work),'District'), value='ALL',multi=True,placeholder="District")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Blockcb',options=createDroplist(getBlock(st1work),'Block'), value='ALL',multi=True,placeholder="Block")
                            ,style={'padding-right': '0%','padding-left':'0%','fontSize':'15px'},className='dropdown',md=dict(size=2)),

                    
                        
                    dbc.Col(dcc.Dropdown(id='Castecb',options=createDroplist(getCastelist(st1work) , 'Caste'), value='ALL',multi=True,placeholder="Caste", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' }),
                            style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Locationcb',options=createDroplist(getlocationlist(st1work),'Location'), value='ALL',multi=True,placeholder="Type of location "
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Religioncb',options=createDroplist(getReligionllist(st1work),'Religion'), value='ALL',multi=True,placeholder="Religion"
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Gendercb',options=createDroplist(getGenderlist(st1work),'Gender'), value='ALL',multi=True,placeholder="Gender",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                        
                        
                    dbc.Col(dcc.Dropdown(id='monthcb'
                                         ,options=[   {'label': 'October', 'value': 'October'},
                                                    {'label': 'November', 'value': 'November'},
                                                    {'label': 'December', 'value': 'December'},
                                      ],value='October'
                                         ,placeholder="Month",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                                            
                    dbc.Col(dcc.Dropdown(id='LoanLoackdowncb',options=createDroplist(getLoanlist(st1work),'Loan During Lockdown'), value='ALL',multi=True,placeholder="Loan During Lockdown",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                        
                        
                        
                    ]
                     ,
                     
                    
                        ),
                ]),
            
    ])
    return start


# In[ ]:





# In[8]:


def barlevel1chart1(fil4,month='October'):
    monthb=month
    Bardata1=fil4['Were pregnant women, lactating mothers and young children in your family provided with supplementary nutrition by the Anganwadi in the month of '+monthb+'?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= 'In '+month,)
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
    ,margin={"r":0,"t":80,"l":0,"b":0}
        ,
    bargap=0.4,
    height=300
    #width=[0.8, 0.8, 0.8, 0.8]
    
    )
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig

def pielevel2chart1(fil4):
    colors = ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']
    Bardata1=fil4['Are children and adult in your family able to access mental health support services at government facility?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=piecolor(),
                 title='',hole=.7,height=400 )
    #fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0},)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig

def pielevel2chart2(fil4):
    colors = ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']
    Bardata1=fil4['Are you or any of the family members able to get treatment and medicines at the Sub Health Centres, Public Health Centres?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=piecolor(),height=400,
                 title='',hole=.7 )
    #fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors,
                              line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())
    return fig




# In[9]:


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
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id='graphcb',figure= quick_plot1(st1work) ,config=cong()),md=6),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([html.P('Were pregnant women, lactating mothers and young children in your family were provided with supplementary nutrition by the Anganwadi in the month of')
                                     ,dcc.Graph(id='barlevel1chart1cb',figure= barlevel1chart1(st1work),config=cong())],md=12),
                            dbc.Col([html.P('Are children and adult in your family able to access mental health support services at government facility?')
                                     ,dcc.Graph(id='pielevel2chart1cb',figure= pielevel2chart1(st1work) ,config=cong())],md=6),
                            dbc.Col([html.P('Are you or any of the family members able to get treatment and medicines at the govt. health facilities available at the location or close to it?')
                                     ,dcc.Graph(id='pielevel2chart2cb',figure= pielevel2chart2(st1work) ,config=cong())],md=6),
                            
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


# In[10]:


def totalcount(file):
    
    return len(file.index)


# In[11]:


@app.callback( 
    Output(component_id='NGOcb', component_property='options'),
    Output(component_id='Districtcb', component_property='options'),
    Output(component_id='Blockcb', component_property='options'),
    Output(component_id='Castecb', component_property='options'),
    Output(component_id='Locationcb', component_property='options'),
    Output(component_id='Religioncb', component_property='options'),
    Output(component_id='Gendercb', component_property='options'),
    Output(component_id='Statecb', component_property='options'),
    Output(component_id='LoanLoackdowncb', component_property='options'),
    
    
    
    Output(component_id='barlevel1chart1cb', component_property='figure'),
    Output(component_id='pielevel2chart1cb', component_property='figure'), 
    Output(component_id='pielevel2chart2cb', component_property='figure'),
    Output(component_id='TotalDatacb', component_property='children'),
    Output(component_id='graphcb', component_property='figure'),
   
    Input(component_id='Castecb', component_property='value'),
    Input(component_id='Locationcb', component_property='value'),
    Input(component_id='Religioncb', component_property='value'),
    Input(component_id='Gendercb', component_property='value'),
    Input(component_id='Statecb', component_property='value'),
    Input(component_id='monthcb', component_property='value'),
    Input(component_id='LoanLoackdowncb', component_property='value'),
    Input(component_id='NGOcb', component_property='value'),
    Input(component_id='Districtcb', component_property='value'),
    Input(component_id='Blockcb', component_property='value'),
    
    
   # Input(component_id='stageselection', component_property='value'),
)
def update_output1(input_value1,input_value2,input_value3,input_value4,input_value5,month,input_value6,input_value7,input_value8,input_value9):  
        
        
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
        
    if len(input_value6) == 0:
        fil7=fil6
    elif 'ALL' in input_value6:
        fil7=fil6
    else:
        fil7=fil6[fil6["Have you or your family taken loan after March in this year?"].isin(input_value6)]
    
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
        
    
    
        
    Castelist=optionState=createDroplist(getCastelist(fil10),'Caste')
    locationlist=optionState=createDroplist(getlocationlist(fil10),'Location')
    Religionllist=optionState=createDroplist(getReligionllist(fil10),'Religion')
    Genderlist=optionState=createDroplist(getGenderlist(fil10),'Gender')
    Statelist=optionState=createDroplist(getStatelist(fil10),'State')
    Loanlist=createDroplist(getLoanlist(fil10),'Loan During Lockdown')
    optionNGO=createDroplist(getNGO(fil10),"Source or Destination")
    optionBlock=createDroplist(getBlock(fil10),"Block")
    optionDistrict=createDroplist(getDistrict(fil10),"District")
    
    
        
   
    return optionNGO,optionDistrict,optionBlock,Castelist, locationlist, Religionllist, Genderlist, Statelist, Loanlist,barlevel1chart1(fil10,month),pielevel2chart1(fil10),pielevel2chart2(fil10),'Total Number: {}'.format(totalcount(fil10)),quick_plot1(fil10)


# In[ ]:


if __name__ == '__main__':
    app.run_server(host= '127.0.0.2',debug=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




