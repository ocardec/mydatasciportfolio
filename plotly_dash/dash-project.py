#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# get data
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash 
app = dash.Dash(__name__)

# Set title for dashboard
app.title = "Automobile Statistics Dashboard"

# Define the dropdown option
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

# year list
year_list = [i for i in range(1980, 2024, 1)]

#  layout of the app
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", 
    style={'textAlign':'center', 'color':'#503D36', 'font-size': 24}),
    
    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type',
            style={'textAlign':'center', 'width':'80%', 'padding':'3px', 'font-size': '20px'}
        )
    ]),

    html.Div(dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select a year', 
            style={'textAlign':'center', 'width':'80%', 'padding':'3px', 'font-size': '20px'}
        )),

    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display':'flex'})
        ])
    ])

# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)

def update_input_container(selected_statistics):
    if selected_statistics =='Yearly Statistics': 
        return False
    else: 
        return True

# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), 
    Input(component_id='dropdown-statistics', component_property='value')])

def update_output_container(selected_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        # filtered data - recession period
        recession_data = data[data['Recession'] == 1]

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales fluctuation over Recession Period"
            )
        )
#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()                    
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales, 
                x='Vehicle_Type', 
                y='Automobile_Sales',
                title='Average Automobile Sales by Vehicle Type'
            )
        ) 
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()  
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec, 
                names='Vehicle_Type', 
                values='Advertising_Expenditure',
                title='Average Advertising Expenditure by Vehicle Type'
            )
        )

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
        unem_rate = recession_data.groupby(['Vehicle_Type', 'unemployment_rate'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unem_rate, 
                x='Vehicle_Type', 
                y='Automobile_Sales',
                color='unemployment_rate',
                barmode='group',
                title='Average Automobile Sales by Vehicle Type and Unemployment Rate'
            )
        )

        return [
            html.Div(className='chart-item', children=[html.Div(children=R_chart1),html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)])
            ]

# TASK 2.6: Create and display graphs for Yearly Report Statistics                     
    elif (selected_year is not None and selected_statistics=='Yearly Statistics') :
        yearly_data = data[data['Year'] == selected_year]
                              
#plot 1 Yearly Automobile sales using line chart for the whole period.
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas, 
                x='Year',
                y='Automobile_Sales',
                title="Yearly Automobile Sales"
            )
        )
# Plot 2 Total Monthly Automobile sales using line chart.
        Y_chart2 = dcc.Graph(
            figure=px.line(
                yearly_data, 
                x='Month',
                y='Automobile_Sales',
                title="Monthly Automobile Sales in {}".format(selected_year)
            )
        )
# Plot 3  bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata, 
                x='Vehicle_Type', 
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year)
            )
        )
# Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].mean().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data, 
                names='Vehicle_Type', 
                values='Advertising_Expenditure',
                title='Total Advertising Expenditure by Vehicle Type in the year {}'.format(selected_year)
            )
        )

        return [
                html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)]),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)])
                ]        
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
