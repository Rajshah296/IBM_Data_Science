# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites= [x for x in spacex_df['Launch Site'].unique()]
options_list=[{'label':'All Sites', 'value':'All Sites'}, *[{'label': i, 'value': i} for i in launch_sites]]
print(options_list)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                            'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                html.Div(dcc.Dropdown(id="site-dropdown",  options=options_list, value='All Sites', placeholder='Select the Site', searchable=True)),
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id = 'payload-slider',min = 0,max = 10000,step = 1000, value=[0,10000])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),Input(component_id="site-dropdown",component_property='value'))

def pie_gen(input_site):
    if input_site == 'All Sites':
        grp_site= spacex_df[spacex_df['class'] == 1]
        values_all = [len(grp_site[grp_site['Launch Site'] == site] *100)/len(grp_site) for site in launch_sites]
        pie_chart= px.pie(names= launch_sites, values= values_all, title='Total Successfull launches by All Sites')
        return pie_chart
            
    else:
        site_grp= spacex_df[spacex_df['Launch Site'] == input_site]
        values_list=[len(site_grp[site_grp['class'] == 1])* 100/ len(site_grp), 100 - (len(site_grp[site_grp['class'] == 1])* 100/ len(site_grp))]
        pie_chart = px.pie(names=['Success', 'Failure'], values= values_list, title=f'Total Successfull launches by {input_site}')
        return pie_chart



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),[Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider',component_property='value')])

def scatter_gen(input_site, payload_range):
    if input_site == 'All Sites':
        selected_recs= spacex_df[(spacex_df['Payload Mass (kg)'] >=payload_range[0]) & (spacex_df['Payload Mass (kg)'] <= payload_range[1])]

        scatter_chart= px.scatter(selected_recs,x='Payload Mass (kg)', y= 'class', color= 'Booster Version Category', title='Correlation between Success and Payload for All Sites')
        return scatter_chart

    else:
        site_data= spacex_df[spacex_df['Launch Site'] == input_site]

        selected_recs= site_data[(site_data['Payload Mass (kg)'] >=payload_range[0]) & (site_data['Payload Mass (kg)'] <= payload_range[1])]
        
        scatter_chart = px.scatter(selected_recs ,x = 'Payload Mass (kg)',y = 'class', color='Booster Version Category',title=f'Correlation between Success and Payload for {input_site}')
        return scatter_chart

# Run the app
if __name__ == '__main__':
    app.run_server()