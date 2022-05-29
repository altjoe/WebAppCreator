import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

class WebApp():
    def __init__(self):
        self.app = Dash(__name__)
    
        self.call_back_list = []
        self.input_ids = []
        self.output_ids = []
    
    def add_cell(self, objects, widthp=100, heightp=100): 
        if type(objects) != list:
            raise Exception('WebApp:add_cell -> List input only')
        return html.Div(objects, style={'width' : f'{widthp}%', 'height' : f'{heightp}%', 'border' : '2px black solid'})

    def add_graph(self, id, widthp=100, heightp=100):
        self.call_back_list.insert(0, Output(id, 'figure'))
        self.output_ids.append(id)
        return self.add_cell([dcc.Graph(id=id)], widthp, heightp)

    def add_dropdown(self, id, options, value, widthp=100, heightp=100, multi=False):
        self.call_back_list.append(Input(id, 'value'))
        self.input_ids.append(id)
        return self.add_cell([dcc.Dropdown(id=id, options=options, value=value, multi=multi)], widthp, heightp)
        
    def add_row(self, objects, widthp=100, heightp=100, flex=True, center=True): # rows are for putting cells side by side
        if type(objects) != list:
            raise Exception('WebApp:add_cell -> List input only')
        if flex:
            if center:
                return html.Center(html.Div(children=objects, style={'width' : f'{widthp}%', 'height' : f'{heightp}%', 'display': 'flex', 'border' : '2px black solid'}))
            return html.Div(children=objects, style={'width' : f'{widthp}%', 'height' : f'{heightp}%', 'display': 'flex', 'border' : '2px black solid'})
        else:
            if center:
                return html.Center(html.Div(children=objects, style={'width' : f'{widthp}%', 'height' : f'{heightp}%', 'border' : '2px black solid'}))
            return html.Div(children=objects, style={'width' : f'{widthp}%', 'height' : f'{heightp}%', 'border' : '2px black solid'})
    
    def add_column(self, objects, widthp=100, heightp=100, center=False): # this holds rows and columns
        if type(objects) != list:
            raise Exception('WebApp:add_cell -> List input only')
        if center:
            return html.Center(html.Div(children=objects, style={'width' : f'{widthp}%', 'height' : f'{heightp}%', 'border' : '2px red solid'}))
        return html.Div(children=objects, style={'width' : f'{widthp}%', 'height' : f'{heightp}%', 'border' : '2px red solid'})

    def set_layout(self, html_returns):
        self.app.layout = html_returns
    
    def add_input(self, input_id, output_id, value):
        if input_id in self.input_ids and output_id in self.output_ids:
            print(f'all good: {value}')
        else:
            print('not good')

    def return_call_back(self):
        return self.call_back_list

    def run_server(self):
        self.app.run_server(debug=True)
    
    def return_output():
        pass

def main():
    web_app = WebApp()
    web_app.set_layout(
                web_app.add_row([
                    web_app.add_dropdown(id='drop1', options=['test', 'hi', 'hello', 'there'], value='hi', multi=True, widthp=10),
                    web_app.add_dropdown(id='drop2', options=['test', 'hi', 'hello', 'there'], value='test', multi=False, widthp=10),
                    web_app.add_graph(id='graph1', widthp=90, heightp=100)
                ], 90, 100)
        )

    print(web_app.return_call_back())
    @web_app.app.callback(web_app.return_call_back())

    def figure(*arguments):

        web_app.add_input('drop1', 'graph1', arguments[0])

        # print(arguments)
        fig = go.Figure()
        # fig.add_scatter(x=list(range(15)), y=list(range(15)))
        return [fig]

    web_app.run_server()


main()