import os
import random
import base64
import numpy as np

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import dash_cytoscape as cyto
from dash_html_components.I import I

# Remove the following if not using it in the cytoscape layouts
# Load extra layouts
# cyto.load_extra_layouts()

image_filename = 'assets/Euler.jpeg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


asset_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', 'assets'
)

app = dash.Dash(__name__, assets_folder=asset_path, title='Bridges of Königsberg')
server = app.server

random.seed(2019)

rng = np.random.default_rng()

n = 5


found = False
while not found:
    try:
        degs = rng.choice([2,4,6],size=n,p=(0.67,0.22,0.11),replace=True)
        edge_dict = {i:[] for i in range(1,n+1)}
        for i in range(1,n+1):
            try:
                neighbors = rng.choice([j for j in range(i+1,n+1) if j not in edge_dict[i]],size = degs[i-1]-len(edge_dict[i]),replace=False)
            except ValueError:
                if (len(edge_dict[i]) > 0) and (len(edge_dict[i])%2 == 0):
                    neighbors = []
                elif len(edge_dict[i]) == 0:
                    raise
                else:
                    neighbors = [rng.choice([j for j in range(i+1,n+1) if j not in edge_dict[i]])]
            for v in neighbors:
                edge_dict[i].append(v)
                edge_dict[v].append(i)
        odd1 = rng.choice(list(edge_dict.keys()))
        odd2 = rng.choice([x for x in edge_dict.keys() if ((x != odd1) and (x not in edge_dict[odd1]))])
        edge_dict[odd1].append(odd2)
        edge_dict[odd2].append(odd1)
        found = True
    except:
        pass


nodes = [
    {'data': {'id': str(i), 'label': f'Node {i}'}, 'selectable': False}
    for i in range(1,n+1)
]

#node_ids = [n['data']['id'] for n in nodes]

chosen_nodes = []

edge_tuples = [[str(a),str(b)] for a in edge_dict.keys() for b in edge_dict[a] if a < b]

#edge_tuples = []

edges = [
    {'data': {'id': f'{i}_{j}','source': i, 'target': j}, 'selectable': False}
    for i,j in edge_tuples
]

#edge_ids = [e['data']['id'] for e in edges]

chosen_edges = []

default_stylesheet = [{
        "selector": 'node',
        "style": {
            'opacity': 0.9,
            'label': 'data(label)'
        }
    },
]


default_elements = nodes + edges

options = [{'label': x, 'value': x} for x in range(5,100)]

nonhint = "(Try moving the nodes around if the edges are difficult to understand, or zooming.)"

name_options = [{'label':'Randomly', 'value':'random'}, {'label':'In a circle', 'value':'circle'},{'label':'In concentric circles', 'value':'concentric'},
                {'label':'In a grid', 'value':'grid'},{'label':'Like a tree', 'value':'breadthfirst'},{'label':'Use AI and physics', 'value':'cose'}]

app.layout = html.Div(children=[
        html.H1("The Bridges of Königsberg"),
        html.P('''Can you cross every bridge without crossing the same bridge twice?
            Click on the nodes, one at a time, to move through the historic city of Königsberg!'''),
        html.Div([
            html.Label(children=["Choose how many nodes you want in your graph:"]),
        dcc.Dropdown(
            id='node-dropdown',
            options=options,
            value=5,
            ),
        ]),
        html.Div([
            html.Label(children=["Choose how the graph should be displayed:"]),
        dcc.Dropdown(
            id='name-dropdown',
            options=name_options,
            value='random',
            ),
        ], style={"padding":"15px 0"}),
        html.Table(html.Tr(children=[
            html.Td(html.Button('Clear all nodes', id='reset',style={"float":"left"})),
            html.Td(html.Button('I want a hint', id='hint',style={"float":"left"})),
            html.Td(html.P(nonhint, id="hint_location",style={"float":"left"}))
        ], style={"padding":"30px", "width":"100%"})),
        html.Div(id="image_holder",children=[]),
        dcc.Store(id="chosen_nodes",data=[]),
        dcc.Store(id="chosen_edges",data=[]),
        dcc.Store(id="edge_tuples",data=edge_tuples),
        dcc.Store(id="odd",data=odd1),
        html.Div(children = [
        cyto.Cytoscape(
            id='cytoscape',
            elements=default_elements,
            layout={
                'name': 'random'
            },
            stylesheet = [x for x in default_stylesheet],
            style={
                'height':  '40vh',
                'width': '40wh'
            }
        ),], style={"border":"2px black solid", 'background-color': 'lightblue', 'width': '80%', 'max-width': '100vw', 'height': '80%', 'max-height': '80vh'},
        ),
        html.P("Caution: Especially in the Grid and Tree views, it may look like there is an edge from Node A to Node B to Node C, when secretly it is just an edge from Node A to Node C passing over Node B.  Try dragging the nodes around to get a better view.",style={"padding":"10px"}),
        
    ])

@app.callback(Output('cytoscape', 'layout'),
                Input('name-dropdown','value'),
                State('cytoscape','layout'))
def set_layout(value,layout):
    ctx = dash.callback_context
    if not ctx:
        return layout
    elif ctx.triggered[0]['prop_id'] != 'name-dropdown.value':
        return layout
    return {'name': value}

@app.callback(Output('hint_location', 'children'),
                Input('hint','n_clicks'),
                Input('reset', 'n_clicks'),
                Input('node-dropdown','value'),
                State('odd','data'))
def show_hint(btn,btn_reset, drop, odd1):
    ctx = dash.callback_context
    if not ctx:
        return nonhint
    elif ctx.triggered[0]['prop_id'] != "hint.n_clicks":
        return nonhint
    return f"Hint: Try starting at Node {odd1}"
    

@app.callback([Output('chosen_nodes', 'data'),
                Output('chosen_edges','data')],
              [Input('reset', 'n_clicks'),
              Input('cytoscape', 'tapNode'),
              Input('cytoscape','elements'),
              State('chosen_nodes', 'data'),
              State('chosen_edges', 'data'),
              State('edge_tuples', 'data')])
def remember_node(btn, node, elements, chosen_nodes,chosen_edges,edge_tuples):
    ctx = dash.callback_context

    if not ctx:
        return [],[]
    elif ctx.triggered[0]['prop_id'].split(".")[0] == "reset":
        return [],[]
    elif (ctx.triggered[0]['prop_id'] == "cytoscape.elements"):
        return [],[]


    try:
        d = node['data']['id']
    except:
        return [],[]

    if len(chosen_nodes) == 0:
        return [d],[]

    if (([chosen_nodes[-1],d] in edge_tuples) and (chosen_nodes[-1]+"_"+d not in chosen_edges)):
        return chosen_nodes+[d], chosen_edges + [chosen_nodes[-1]+"_"+d]
    elif (([d,chosen_nodes[-1]] in edge_tuples) and (d+"_"+chosen_nodes[-1] not in chosen_edges)):
        return chosen_nodes+[d], chosen_edges+[d+"_"+chosen_nodes[-1]]

    return chosen_nodes, chosen_edges
    


@app.callback(Output('cytoscape', 'stylesheet'),
            Input('chosen_nodes', 'data'),
            Input('chosen_edges', 'data'),
            State('cytoscape','stylesheet'))
def generate_stylesheet(chosen_nodes,chosen_edges,stylesheet):

    if len(chosen_nodes) == 0:
        return default_stylesheet
    
    try:
        stylesheet.append({
            "selector": f'node[id = "{chosen_nodes[-1]}"]',
            "style": {
                'background-color': "green",
                'opacity': 0.9,
            }
        })
    except:
        pass

    try:
        stylesheet.append({
            "selector": f'edge[id= "{chosen_edges[-1]}"]',
            "style": {
                "line-color": "green",
                'opacity': 0.9,
                'z-index': 5000
            }
        })
    except:
        pass

    return stylesheet



@app.callback(Output('image_holder', 'children'),
              Input('cytoscape', 'stylesheet'),
              State('chosen_nodes', 'data'),
              State('chosen_edges', 'data'),
              State('edge_tuples', 'data'))
def set_image(sty,chosen_nodes,chosen_edges,edge_tuples):
    if len(chosen_edges) == len(edge_tuples):
        return [html.H3("Hooray, says Euler"), html.Img(src=f'data:image/jpeg;base64,{encoded_image.decode()}',height=300)]
    else:
        return [] #[html.P(chosen_nodes),html.P(chosen_edges)]



@app.callback([Output('cytoscape','elements'),
               Output('edge_tuples','data'),
               Output('odd','data')],
                Input('node-dropdown','value'))
def reset_everything(n):
    found = False
    while not found:
        try:
            degs = rng.choice([2,4,6],size=n,p=(0.67,0.22,0.11),replace=True)
            edge_dict = {i:[] for i in range(1,n+1)}
            for i in range(1,n+1):
                try:
                    neighbors = rng.choice([j for j in range(i+1,n+1) if j not in edge_dict[i]],size = degs[i-1]-len(edge_dict[i]),replace=False)
                except ValueError:
                    if (len(edge_dict[i]) > 0) and (len(edge_dict[i])%2 == 0):
                        neighbors = []
                    elif len(edge_dict[i]) == 0:
                        raise
                    else:
                        neighbors = [rng.choice([j for j in range(i+1,n+1) if j not in edge_dict[i]])]
                for v in neighbors:
                    edge_dict[i].append(v)
                    edge_dict[v].append(i)
            odd1 = rng.choice(list(edge_dict.keys()))
            odd2 = rng.choice([x for x in edge_dict.keys() if ((x != odd1) and (x not in edge_dict[odd1]))])
            edge_dict[odd1].append(odd2)
            edge_dict[odd2].append(odd1)
            found = True
        except:
            pass


    nodes = [
        {'data': {'id': str(i), 'label': f'Node {i}'}, 'selectable': False}
        for i in range(1,n+1)
    ]


    edge_tuples = [[str(a),str(b)] for a in edge_dict.keys() for b in edge_dict[a] if a < b]

    edges = [
        {'data': {'id': f'{i}_{j}','source': i, 'target': j}, 'selectable': False}
        for i,j in edge_tuples
    ]

    return (nodes + edges, edge_tuples, odd1)


if __name__ == '__main__':
    app.run_server(debug=True)