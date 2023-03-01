from dash import Dash, dcc, html
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
            html.A('Select Files')
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),
    html.Div(id='output-image-upload'),
])

def parse_contents(contents):
    img = Image.fromarray(remove_bg(readb64(contents), (192, 192, 192))).convert('RGB')

    return html.Div([
        html.Img(src=contents),
        html.Img(src=img, style={'margin': '10px'}),  
        html.Hr()
    ])

@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'))

def update_output(list_of_contents):
    if list_of_contents is not None:
        children = [parse_contents(c) for c in list_of_contents]
        
        return children
    

if __name__ == '__main__':
    app.run_server(debug=True)