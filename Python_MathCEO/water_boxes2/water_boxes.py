import dash
from dash.dependencies import Input, Output, State
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import random

app = dash.Dash(__name__)
server = app.server
app.title = "Water Boxes"

rows = 14

target_dict = {2250: 2.25, 2000: 2.0, 7500: 7.5, 8820: 8.82}

targets = [1800]*5 + sorted([random.choice(list(target_dict.keys())) for _ in range(rows - 5) ])



col_tups = [("Target", "Target volume in cm^3", False), ("WaterBox","Box #",False), ("Length", "Length in cm",True), ("Width", "Width in cm",True), ("Area", "Area of Square Base in cm^2",False), ("Height", "Height in cm",True), 
            ("Volume", "Volume in cm^3",False), ("Finished","Finished?",False)]

cols = [{"id": col_id, "name": name, "editable":edit, "type": "numeric"} for col_id,name,edit in col_tups]

app.layout = html.Div(children =[
    html.H1(
                    children="Water Boxes", className="header-title", style={"textAlign":"center"}
    ),
    html.P(children = [f'''Engineer Martina has received orders for boxes in a variety of sizes.  One of the boxes must hold exactly 1.8 liters of water, which is equal to 1800 cm^3.  Another
                    must hold {target_dict[targets[-1]]} liters, which is equal to {targets[-1]} cm^3.  The list goes on.''', html.Br(), html.Br(),  '''Martina wants the 
                    boxes to be ''', html.I("special"), ''': they should have a square base, and the length of each side (as measured in centimeters) should be an integer.'''
    ]),
    html.Div("",style={'height':'100px','margin':'20px','backgroundRepeat':"repeat-x",'textAlign': 'center', 'backgroundImage':"url('/assets/waterbox.png')", "backgroundSize": "100px 100px",}),
    dash_table.DataTable(
        id='table-editing-simple',
        columns=(
            cols
        ),
        data=[
            dict(Target = targets[i-1], WaterBox = i, **{c["id"]: "" for c in cols[2:]})
            for i in range(1, rows+1)
        ],
        editable=True,
        style_data_conditional=[
        {
            'if': {
                'filter_query': '({Length} != {Width}) && ({Length} != "") && ({Width} != "")',
                'column_id': ['Length', 'Width'],
            },
           'backgroundColor': 'pink',
        },
        {
            'if': {
                'filter_query': '({Volume} != {Target}) && ({Volume} != "")',
                'column_id': 'Volume',
            },
            'backgroundColor': 'pink',
        },
        {
            'if': {
                'filter_query': '({Volume} = {Target}) && ({Length} = {Width})',
            },
            'backgroundColor': 'lightgreen',
        },
        {
            'if': {
                'state': 'active'  # 'active' | 'selected'
            },
           'backgroundColor': 'rgba(256, 256, 256, 0.3)',
           'border': '1px solid rgb(0, 116, 217)',
        },
        {
            'if': {
                'filter_query': '({Volume} != {Target}) && ({Volume} != "")',
                'state': 'active',  # 'active' | 'selected'
                'column_id': 'Volume',
            },
           'backgroundColor': 'pink',
           'border': '1px solid rgb(0, 116, 217)',
        },
        {
            'if': {
                'state': 'active',  # 'active' | 'selected'
                'column_id': 'Target',
            },
           'backgroundColor': 'darkblue',
        },
        {
            'if': {
                'column_id': ['Target'],
            },
           'backgroundColor': 'darkblue',
           'color': 'white'
        },
        ],
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '30px', 'width': '90px', 'maxWidth': '90px',
            'whiteSpace': 'normal'
        }
    ),
    html.P(
        children=["How many different unique boxes can you make?"]
    ),
    html.P(id = "unique", children = "Current number of unique boxes: 0"),
    html.P(
            id = 'hintyes',
            children=["A row colored ", html.Span("green", style={'backgroundColor':'lightgreen'}), " is correct!"]
        ),
    html.P(
            id = 'hintno',
            children=["A row colored ", html.Span("pink", style={'backgroundColor':'lightpink'}), " is not correct... yet!"]
        ),
    html.Div("",style={'height':'100px','margin':'20px','backgroundRepeat':"repeat-x",'textAlign': 'center', 'backgroundImage':"url('/assets/waterbox.png')", "backgroundSize": "100px 100px",}),
], style = {"width": "80%", "maxWidth":"650px", "margin":"auto"})

@app.callback(Output('unique','children'),
                Input('table-editing-simple', 'data'))
def count_unique(rows):
    tups = [(row["Length"],row["Width"],row["Height"]) for row in rows if row["Volume"] == row["Target"]]
    u = len(set(tups))
    return f"Current number of unique boxes: {u}"

@app.callback(Output('table-editing-simple', 'data'),
                Input('table-editing-simple', 'data_timestamp'),
                State('table-editing-simple', 'data'))
def display_output(timestamp, rows):
    for row in rows:
        try:
            row["Area"] = row["Width"]*row["Length"]
        except:
            row["Area"] = ""
        try:
            row["Volume"] = row["Width"]*row["Length"]*row["Height"]
        except:
            row["Volume"] = ""
        if ("" != row["Volume"]):
            if  (row["Target"] != row["Volume"]) or (row["Width"] != row["Length"]):
                row["Finished"] = "Keep trying"
            else:
                row["Finished"] = "Good job!"
        else:
            row["Finished?"] = ""
    return rows





if __name__ == '__main__':
    app.run_server(debug=True)