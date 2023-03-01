from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output, State
from images import remove_bg
from PIL import Image
from utils import readb64

app = Dash(__name__)

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')],),
        style={
            'width': '30%',
            'height': '30vh',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'position': 'fixed',
            'top': '30%',
            'left': '5%',
            'backgroundColor': '#B4E4FF'
        },
        multiple=True
    ),
    html.Div(id='output-image-upload',  style={
        'position': 'fixed',
        'top': '30%',
        'right': '5%',
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center',
        'alignItems': 'center'
    }),
    html.Button('Change Background', id='change-bg', n_clicks=0, style={
        'position': 'fixed',
        'top': '70%',
        'right': '22%',
        'width': '10%',
        'height': '7vh',
        'lineHeight': '60px',
        'textAlign': 'center',
        'margin': '10px',

    }),
    html.Button('Remove Background', id='remove-bg', n_clicks=0, style={
        'position': 'fixed',
        'top': '70%',
        'right': '10%',
        'width': '10%',
        'height': '7vh',
        'lineHeight': '60px',
        'textAlign': 'center',
        'margin': '10px',
 
    }),
])

def parse_contents(contents, id):
    if id == 'remove-bg':
        img = Image.fromarray(remove_bg(readb64(contents), (192, 192, 192))).convert('RGB')
        return html.Div([
            html.Img(src=img, style={'width': '50%', 'height': '50%', 'margin': '10px'}),  
        ])
    elif id == 'change-bg':
        img = Image.fromarray(remove_bg(readb64(contents), (192, 192, 192))).convert('RGB')
        return html.Div([
            html.Img(src=img, style={'width': '50%', 'height': '50%', 'margin': '10px'}),  
        ])
    else:
        return html.Div([
            html.Img(src=contents, style={'width': '50%', 'height': '50%', 'margin': '10px'}),  
        ])

@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              Input('change-bg', 'n_clicks'),
              Input('remove-bg', 'n_clicks')
              )

def update_output(list_of_contents, change_bg, remove_bg):
    if list_of_contents is not None:
        children = [parse_contents(c, ctx.triggered_id) for c in list_of_contents]
        
        return children
    

if __name__ == '__main__':
    app.run_server(debug=True)