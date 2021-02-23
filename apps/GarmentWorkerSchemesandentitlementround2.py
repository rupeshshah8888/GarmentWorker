#!/usr/bin/env python
# coding: utf-8

# In[70]:


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

data1 = pd.read_excel(DATA_PATH.joinpath('Round 2 Garment worker.xlsx'), engine='openpyxl')
datamap = pd.read_csv(DATA_PATH.joinpath('state wise centroids_2011.csv'))
st1work=data1

# In[72]:


def barcolour():
    return ['#000099','#0000CC','#0000FF','#009999','#0099FF','#00FFFF']

def plot_bgcolor1():
    return '#A9A9A9'
def paper_bgcolor1():
    return '#A9A9A9'

def piecolor():
    return ['#003f5c','#58508d','#bc5090','#ff6361','#ffa600']


# In[73]:


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


# In[74]:


# filterpane


def getCastelist(st1work):
    return st1work["Caste catgeory in which the respondent's community is categorised?"].unique()

def getlocationlist(st1work):
    return st1work['District'].unique()

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


# In[75]:


def stylecss():
    return {'height': '100%', 'width': '100%' , 'font-size': '12px'}

def start():
    start=([
        html.H2("Schemes and Entitlements",style={'text-align': 'center', 'colour':'green' } ),
        html.Button(id='TotalDatafa',style={'text-align': 'center', 'font-size': '15px', 
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
                        
                    dbc.Col(dcc.Dropdown(id='Castefa',options=createDroplist(getCastelist(st1work) , 'Caste'), value='ALL',multi=True,placeholder="Caste", 
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' }),
                            style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Locationfa',options=createDroplist(getlocationlist(st1work),'District'), value='ALL',multi=True,placeholder="District"
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Religionfa',options=createDroplist(getReligionllist(st1work),'Religion'), value='ALL',multi=True,placeholder="Religion"
                                        ,style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),

                    dbc.Col(dcc.Dropdown(id='Genderfa',options=createDroplist(getGenderlist(st1work),'Gender'), value='ALL',multi=True,placeholder="Gender",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                        
                    dbc.Col(dcc.Dropdown(id='Statefa',options=createDroplist(getStatelist(st1work),'State'), value='ALL',multi=True,placeholder="State",
                                        style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)),
                     dbc.Col(dcc.Dropdown(id='monthfa'
                             ,options=[ {'label': 'July', 'value': 'July'},
                                        {'label': 'August', 'value': 'August'},
                                        {'label': 'September', 'value': 'September'},
                                      ],value='July',
                                         style={'height': '100%', 'width': '100%' , 'font-size': '15px' })
                            ,style={'padding-right': '0%','padding-left':'0%'},className='dropdown',md=dict(size=2)
                             ),
                                            
            
                        
                        
                        
                    ]
                     ,
                     
                    
                        ),
                ]),
            
    ])
    return start


# In[ ]:





# In[76]:


def barJanDhanApril(fil4 , month='July'):
    month=month
    Bardata1=fil4['Do you have health insurance coverage under Rashtriya Swasthya Bima Yojana?'].value_counts()
    
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
            )),
        

    yaxis=dict(
                title='',
                titlefont=dict(
                family='Helvetica, monospace',
                size=12,
                color='#7f7f7f',
                
            )),
    plot_bgcolor='rgb(255, 255, 255)'
    ,margin={"r":0,"t":30,"l":0,"b":0}
        ,
    bargap=0.4,
    #width=[0.8, 0.8, 0.8, 0.8]
    height=300
    )
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig
    
#-------------------------------Ujjwala bar chart------------------------------------

def barUjjwalaApril(fil4 , month='July'):
    month=month
    Bardata1=fil4['Have you or any member in the family received subsidy for cyclinder for the month of '+month+' ?'].value_counts()
    
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
            )),

    yaxis=dict(
                title='',
                titlefont=dict(
                family='Helvetica, monospace',
                size=12,
                color='#7f7f7f',
                
            )),
    plot_bgcolor='rgb(255, 255, 255)'
    ,margin={"r":0,"t":30,"l":0,"b":0}
        ,
    bargap=0.4,
    #width=[0.8, 0.8, 0.8, 0.8]
    height=300
    
    )
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig
#---------------------Funnel Chart ----------------------------------





def funnelOldAgeJune(fil4 , month='July'):
    Bardata1=fil4['Has the registered old age pension beneficiary received the pension for the month of '+month+'?'].value_counts()
    
    fig = px.funnel_area(names=Bardata1.index, values=Bardata1 ,  color=Bardata1.index, color_discrete_sequence=barcolour(),
                title= 'Ex gratia under old <br> Age Pension '+ month,)
    
    fig.update_layout(showlegend=False)
    fig.update_layout( margin={"r":0,"t":60,"l":0,"b":0},plot_bgcolor='rgb(255, 255, 255)', )
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig
    
def funnelWindowPensionJune(fil4, month='July'):
    Bardata1=fil4['Has the registered widow pension beneficiary received the pension for the month of '+month+'?'].value_counts()
    
    fig = px.funnel_area(names=Bardata1.index, values=Bardata1 ,  color=Bardata1.index, color_discrete_sequence=barcolour(),
                 title= 'Ex gratia under <br> window pension '+ month,)
    
    fig.update_layout(showlegend=False)
    fig.update_layout( plot_bgcolor='rgb(255, 255, 255)',margin={"r":0,"t":60,"l":0,"b":0})
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig

def funnelDisabilityJune(fil4, month='July'):
    Bardata1=fil4['Has the registered PWD pension beneficiary received the pension for the month of '+month+'?'].value_counts()
    
    fig = px.funnel_area(names=Bardata1.index, values=Bardata1 ,  color=Bardata1.index, color_discrete_sequence=barcolour(),
                 title= 'Ex gratia under <br> Disability Pension '+ month,)
    
    fig.update_layout(showlegend=False)
    fig.update_layout( plot_bgcolor='rgb(255, 255, 255)',margin={"r":0,"t":60,"l":0,"b":0})
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig



#--------------------------Ration card bar chart--------------------





def barRationApril(fil4 , month='July'):
    month=month

    Bardata1=fil4['Did you or any registered member in your family people get additional ration ( 5 kgs rice and 1Kg pulse) for the month of '+month+'?'].value_counts()
    
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
            )),

    yaxis=dict(
                title='',
                titlefont=dict(
                size=12,
                color='#7f7f7f',
                
            )),
    plot_bgcolor='rgb(255, 255, 255)'
    ,margin={"r":0,"t":30,"l":0,"b":0}
        ,
    bargap=0.4,
    #width=[0.8, 0.8, 0.8, 0.8]
     height=300
    )
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig




def barlevel1chart1(fil4,month='July'):
    month=month
    Bardata1=fil4['Were pregnant women, lactating mothers and young children in your family were provided with supplementary nutrition by the Anganwadi in the month of '+month+'?'].value_counts()
    
    fig = px.bar(x=Bardata1.index, y =Bardata1 ,  color=Bardata1.index, text=Bardata1,color_discrete_sequence=barcolour(),
                 title= 'Were pregnant women, lactating mothers and young children in your <br> family were provided with supplementary nutrition by the Anganwadi in the month of'+month+'?',)
    fig.update_layout(showlegend=False)
    fig.update_layout(
    xaxis=dict(
                title='Data on Status',
                titlefont=dict(
                family='Courier New, monospace',
                size=12,
                color='#7f7f7f'
            )),

    yaxis=dict(
                title='# of Status',
                titlefont=dict(
                family='Helvetica, monospace',
                size=12,
                color='#7f7f7f',
            )),
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
    colors = ['rgb(234, 214, 153)', 'cyan', 'royalblue', 'darkblue']
    Bardata1=fil4['Did you or any of your family members received Rs 2000 under the Kisan Samman Nidhi Yojana between July- September?'].value_counts()          
    fig = px.pie(names=Bardata1.index, values =Bardata1 ,color_discrete_sequence=barcolour(),
                 title='',hole=.7 )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},height=300)
    fig.update_traces(hole=.7,hoverinfo='label+percent', textinfo='value', textfont_size=20, 
                  marker=dict(colors=piecolor(), line=dict(color='#ffffff', width=1)))
    fig.update_layout(plot_bgcolor=plot_bgcolor1(),paper_bgcolor=paper_bgcolor1())

    return fig


# In[77]:


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


# In[78]:

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
                    
                            dbc.Col([
                            html.H6("Swasthya Bima Yojana",style={'text-align': 'center', 'colour':'green' } ),
                            html.P("You have health insurance coverage under Rashtriya Swasthya Bima Yojana?",style={'text-align': 'center', 'colour':'green' } ),
                            dcc.Graph(id='barJanDhanAprilfa',figure= barJanDhanApril(st1work),config=cong())] ,md=6),
                            dbc.Col([
                            html.H6("Addtional Rations",  style={'text-align': 'center', 'colour':'green' } ),
                            html.P("The Central Government announced 5 Kg free food grain and 1 kg pulses to those with ration cards for April-June",style={'text-align': 'center', 'colour':'green' } ),
                            dcc.Graph(id='barRationAprilfa',figure= barRationApril(st1work),config=cong())],md=6),
                            
                ],justify="center", align="center"
                )
            
            ],md=6),
                
                 
               
            
            dbc.Col([  
                dbc.Row([
                            dbc.Col([
                            html.H6(" Ujjwala Scheme",style={'text-align': 'center', 'colour':'green' } ),
                            html.P("Ujjwala Yojana Beneficiaries will Receive 3 Gas cylinders for free over 3 Month (April, May, June)"
                                   ,style={'text-align': 'center', 'colour':'green' } ),
                            dcc.Graph(id='barUjjwalaAprilfa',figure= barUjjwalaApril(st1work),config=cong())],md=6),
                    
                            dbc.Col([
                            html.H6("Kisan Samman Nidhi",style={'text-align': 'center', 'colour':'green' } ),
                            html.P("under Pradhan Mantri Kisan Samman Yojana will be provided Ts 2000 in the first week of April 2020",style={'text-align': 'center', 'colour':'green' } ),
                            dcc.Graph(id='pielevel2chart1fa',figure= pielevel2chart1(st1work),config=cong() )
                            ],md=6),
                            
                           ],justify="center", align="center"
                )
                
            ],md=6)
            ]),
            
            dbc.Row(
                [
                    dbc.Col(dcc.Graph(id='graphfa',figure= quick_plot1(st1work),config=cong() ),md=6),
                    dbc.Col([
                        dbc.Row([
                                   
                        ],justify="center", align="center"
                        ),
                        dbc.Row([
                            dbc.Col(html.H6("Social pensions ",  style={'text-align': 'center', 'colour':'green' } ),md=12),
                            dbc.Col(html.H6("In Addtion to the regular pension a benefit of Rs 1000 was announced",  style={'text-align': 'center', 'colour':'green' } ),md=12),
                           
                            dbc.Col(dcc.Graph(id='funnelOldAgeJunefa',figure= funnelOldAgeJune(st1work),config=cong()),md=4),
                            dbc.Col(dcc.Graph(id='funnelWindowPensionJunefa',figure= funnelWindowPensionJune(st1work),config=cong()),md=4),
                            dbc.Col(dcc.Graph(id='funnelDisabilityJunefa',figure= funnelDisabilityJune(st1work),config=cong()),md=4),
                        ],justify="center", align="center"
                        )
                        
                    ],md=6),
                ],
                style={'height': "100%"},
                align="center",
            ),
           
             
        ],style={'padding-right': '0%','padding-left': '0%'}),
    ],
    fluid=True,
)



# In[79]:



def totalcount(file):
    
    return len(file.index)


# In[80]:


@app.callback( 
    
    Output(component_id='Castefa', component_property='options'),
    Output(component_id='Locationfa', component_property='options'),
    Output(component_id='Religionfa', component_property='options'),
    Output(component_id='Genderfa', component_property='options'),
    Output(component_id='Statefa', component_property='options'),
    
    Output(component_id='barJanDhanAprilfa', component_property='figure'),
    
    Output(component_id='barRationAprilfa', component_property='figure'),
    
    Output(component_id='barUjjwalaAprilfa', component_property='figure'),
    
    Output(component_id='funnelOldAgeJunefa', component_property='figure'),
    Output(component_id='funnelWindowPensionJunefa', component_property='figure'),
    Output(component_id='funnelDisabilityJunefa', component_property='figure'),
                             
    Output(component_id='pielevel2chart1fa', component_property='figure'),
    
    Output(component_id='graphfa', component_property='figure'),
    
    Output(component_id='TotalDatafa', component_property='children'),
    #Output(component_id='barlevel1chart2', component_property='figure'),
   
    Input(component_id='Castefa', component_property='value'),
    Input(component_id='Locationfa', component_property='value'),
    Input(component_id='Religionfa', component_property='value'),
    Input(component_id='Genderfa', component_property='value'),
    Input(component_id='Statefa', component_property='value'),
    Input(component_id='monthfa', component_property='value'),
    
   # Input(component_id='stageselection', component_property='value'),
)
def update_output1(input_value1,input_value2,input_value3,input_value4,input_value5,month):  
        
        
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
        fil3=fil2[fil2["District"].isin(input_value2)]
    
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
    Castelist=optionState=createDroplist(getCastelist(fil6),'Caste')
    locationlist=optionState=createDroplist(getlocationlist(fil6),'District')
    Religionllist=optionState=createDroplist(getReligionllist(fil6),'Religion')
    Genderlist=optionState=createDroplist(getGenderlist(fil6),'Gender')
    Statelist=optionState=createDroplist(getStatelist(fil6),'State')
    
    return Castelist, locationlist, Religionllist, Genderlist, Statelist , barJanDhanApril(fil6,month), barRationApril(fil6,month),barUjjwalaApril(fil6,month),funnelOldAgeJune(fil6),funnelWindowPensionJune(fil6),funnelDisabilityJune(fil6),pielevel2chart1(fil6),quick_plot1(fil6),'Total Number: {}'.format(totalcount(fil6))


# In[81]:


if __name__ == '__main__':
    app.run_server(host= '127.0.0.3',debug=False)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




