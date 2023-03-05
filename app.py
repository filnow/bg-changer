from dash import Dash, dcc, html, ctx
from dash.dependencies import Input, Output, State
from images import remove_bg, change_bg
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
            'position': 'absolute',
            'top': '10%',
            'left': '7%',
            'backgroundColor': '#B4E4FF'
        },
        multiple=True
    ),
    html.Div(id='output-image-upload',  style={
        'position': 'absolute',
        'top': '10%',
        'right': '10%',
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'center',
        'alignItems': 'center'
    }),
    dcc.Upload('Change Background', id='change-bg', style={
        'position': 'absolute',
        'top': '50%',
        'left': '7%',
        'width': '10%',
        'height': '7vh',
        'lineHeight': '60px',
        'textAlign': 'center',
        'margin': '10px',
        'borderRadius': '5px',
        'borderWidth': '1px',
        'borderStyle': 'solid',
        'backgroundColor': '#B4E4FF'
    },
        multiple=True
    ),
    html.Button('Remove Background', id='remove-bg', n_clicks=0, style={
        'position': 'absolute',
        'top': '50%',
        'left': '27%',
        'width': '10%',
        'height': '7vh',
        'lineHeight': '60px',
        'textAlign': 'center',
        'backgroundColor': '#B4E4FF',
        'borderRadius': '5px',
        'borderWidth': '1px',
        'borderStyle': 'solid',
        'margin': '10px'
    }),
    html.Button('Reset', id='reset_img', n_clicks=0, style={
        'position': 'absolute',
        'top': '70%',
        'left': '27%',
        'width': '10%',
        'height': '7vh',
        'lineHeight': '60px',
        'textAlign': 'center',
        'backgroundColor': '#B4E4FF',
        'borderRadius': '5px',
        'borderWidth': '1px',
        'borderStyle': 'solid',
        'margin': '10px'
    }),
    html.Button('Save image', id='save_img', n_clicks=0, style={
        'position': 'absolute',
        'top': '70%',
        'left': '7%',
        'width': '10%',
        'height': '7vh',
        'lineHeight': '60px',
        'textAlign': 'center',
        'backgroundColor': '#B4E4FF',
        'borderRadius': '5px',
        'borderWidth': '1px',
        'borderStyle': 'solid',
        'margin': '10px'
    }),
    dcc.Download(id="download-image"),
    html.Div(id='vertical_line', style={
        'position': 'absolute',
        'top': '0%',
        'left': '50%',
        'width': '1px',
        'height': '100%',
        'backgroundColor': 'black'
        }),
    
        html.Div([
            dcc.Slider(
                id='my-slider',
                min=0,
                max=255,
                step=10,
                value=192,
            ),
        ], style={'position': 'absolute', 
                  'bottom': '25%', 
                  'width': '40%', 
                  'right': '3%',
                  }),
    ], style={'position': 'relative', 
              'height': '98vh', 
              'width': '100vw', 
              'max-width': '100%',
              'max-height': '100%',
              'overflow': 'hidden',
              }
)
  

def parse_contents(contents, id, bg_img, slider_value):
    
    img = contents

    if id == 'my-slider' or id == 'remove-bg':
        img = Image.fromarray(remove_bg(readb64(contents), (slider_value, slider_value, slider_value))).convert('RGB')
        return html.Div([
            html.Img(src=img, style={'width': '100%', 'height': '100%', 'margin': '10px'}),  
        ])
    elif id == 'change-bg':
        img = Image.fromarray(change_bg(readb64(contents), readb64(bg_img))).convert('RGB')
        return html.Div([
            html.Img(src=img, style={'width': '100%', 'height': '100%', 'margin': '10px'}),  
        ])
    elif id == 'reset_img':
        return html.Div([])
    else:
        return html.Div([
            html.Img(src=contents, style={'width': '100%', 'height': '100%', 'margin': '10px'}),  
        ])

@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              Input('change-bg', 'contents'),
              Input('remove-bg', 'n_clicks'),
              Input('reset_img', 'n_clicks'),
              Input('my-slider', 'value'))

def update_output(list_of_contents, 
                  change_bg, 
                  remove_bg,
                  reset_img,
                  slider_value):
    
    if list_of_contents is not None:
        children = [parse_contents(c, 
                                   ctx.triggered_id, 
                                   change_bg, 
                                   slider_value) for c in list_of_contents]
        
        return children
    
@app.callback(Output("download-image", "data"),
              Input("save_img", "n_clicks"),
              State("output-image-upload", "children"))

def download_image(n_clicks, children):
    print(children[0])
    if n_clicks > 0:
        return dcc.send_data_frame(children, "image.png")
    
            


if __name__ == '__main__':
    app.run_server(debug=True)