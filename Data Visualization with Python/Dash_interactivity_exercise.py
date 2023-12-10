import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc
from dash import html
import pandas as pd
from dash.dependencies import Input,Output

airline_data=pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
encoding= "ISO-8859-1",
dtype={'Div1Airport':str,'Div1TailNum':str,'Div2Airport': str,'Div2TailNum':str})

app=dash.Dash(__name__)

app.layout=html.Div(children=[html.H1('Total number of flights in the destination state split by reporting airline',style={'textAligh':'center','font-size':40,'color':'#503D36'}),

html.Div(['Input Year: ',dcc.Input(type='number',id='input-yr',value='2010',style={'font-size':35,'height':'50px'}),]),

html.Br(),
html.Br(),
html.Div(dcc.Graph(id='bar-plot')),

])

@app.callback(Output(component_id='bar-plot',component_property='figure'),Input(component_id='input-yr',component_property='value'))

def generate_graph(entered_year):
    df =  airline_data[airline_data['Year']==int(entered_year)]
    bar_data=df.groupby('DestState')['Flights'].sum().reset_index()

    fig=px.bar(data_frame=bar_data,x=bar_data['DestState'],y=bar_data['Flights'],labels={'x':'Destination','y':'Number of Flights'},title='Flights to Destination State')
    return fig
if __name__=='__main__':
    app.run_server()

