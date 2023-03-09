from dash import Dash, dcc, html, ctx, no_update
from dash.dependencies import Input, Output
from images import ImageProcessor
from utils import str_to_io, b64_image

ids = []

bg_images = {
    'example1': './assets/forest.jpg',
    'example2': './assets/beach.jpg',
    'example3': './assets/city.jpg'
}

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
            'top': '5%',
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
        'width': '30%',
        'height': '7vh',
        'lineHeight': '60px',
        'textAlign': 'center',
        'margin': '10px',
        'borderRadius': '5px',
        'borderWidth': '1px',
        'borderStyle': 'solid',
        'backgroundColor': '#B4E4FF'
    }),
    html.Button('Save image', id='save_img', n_clicks=0, style={
        'position': 'absolute',
        'top': '80%',
        'left': '7%',
        'width': '30%',
        'height': '7vh',
        'lineHeight': '60px',
        'textAlign': 'center',
        'backgroundColor': '#B4E4FF',
        'borderRadius': '5px',
        'borderWidth': '1px',
        'borderStyle': 'solid',
        'margin': '10px'
    }),
    html.Img(id='example1', src='/assets/forest.jpg' ,style={
        'position': 'absolute',
        'top': '65%',
        'left': '8%',
        'width': '8%',
        'height': '10%',
    }),
    html.Img(id='example2', src='/assets/beach.jpg' ,style={
        'position': 'absolute',
        'top': '65%',
        'left': '18%',
        'width': '8%',
        'height': '10%',
    }),
    html.Img(id='example3', src='/assets/city.jpg' ,style={
        'position': 'absolute',
        'top': '65%',
        'left': '28%',
        'width': '8%',
        'height': '10%',
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
                id='red-slider',
                min=0,
                max=255,
                marks={0: {'label' : 'R', 'style': {'color': '#f50'}}},
                value=130,
            ),
        ], 
        style={'position': 'absolute', 
                  'bottom': '23%', 
                  'width': '40%', 
                  'right': '6%',
        }),
        html.Div([
            dcc.Slider(
                id='green-slider',
                min=0,
                max=255,
                marks={0: {'label' : 'G', 'style': {'color': '#32CD32'}}},
                value=130,
            ),
        ], 
        style={'position': 'absolute', 
                  'bottom': '18%', 
                  'width': '40%', 
                  'right': '6%',
        }),
        html.Div([
            dcc.Slider(
                id='blue-slider',
                min=0,
                max=255,
                marks={0: {'label' : 'B', 'style': {'color': '#0000ff'}}},
                value=130,
            ),
        ], 
        style={'position': 'absolute', 
                  'bottom': '13%', 
                  'width': '40%', 
                  'right': '6%',
        }),
        html.Div([
            dcc.Slider(
                id='brightness-slider',
                min=0,
                max=255,
                marks={0: {'label' : 'BRIGHT', 'style': {'color': '#ffff00'}}},
                value=130,
                vertical=True,
            ),
        ], 
        style={'position': 'absolute', 
                  'top': '10%', 
                  'width': '40%', 
                  'left': '96%',
        }),
    ], 
    style={'position': 'relative', 
              'height': '98vh', 
              'width': '100vw', 
              'max-width': '100%',
              'max-height': '100%',
              'overflow': 'hidden',
              'margin': '0',
              }
)

def parse_contents(contents, id, bg_img, slider_value):
    
    img = ImageProcessor(contents)
    slider_ids = ['red-slider', 'green-slider', 'blue-slider']
    changes = ['example1', 'example2', 'example3', 'change-bg']
    if id == 'remove-bg':
        img = img.remove_bg((192,192,192))
        return [img, html.Div([
            html.Img(src=img, style={'width': '100%', 'height': '100%',}),  
        ])]
    elif id in slider_ids:
        img = img.remove_bg(slider_value)
        return [img, html.Div([
            html.Img(src=img, style={'width': '100%', 'height': '100%',}),  
        ])]
    elif id in changes:
        img = img.change_bg(bg_img)
        return [img, html.Div([
            html.Img(src=img, style={'width': '100%', 'height': '100%',}),  
        ])]
    elif id == 'reset_img':
        return [img, html.Div([])]
    else:
        return [img, html.Div([
            html.Img(src=contents, style={'width': '100%', 'height': '100%',}),  
        ])]

@app.callback(Output('download-image', 'data'),
            Output('output-image-upload', 'children'),
            Input('upload-image', 'contents'),
            Input('change-bg', 'contents'),
            Input('save_img', 'n_clicks'),
            Input('red-slider', 'value'),
            Input('green-slider', 'value'),
            Input('blue-slider', 'value'),
            Input('brightness-slider', 'value'),
            Input('example1', 'n_clicks'),
            Input('example2', 'n_clicks'),
            Input('example3', 'n_clicks'),
            prevent_initial_call=True,)

def update_output(list_of_contents, 
                  change_bg, 
                  save_img,
                  red_slider,
                  green_slider,
                  blue_slider,
                  brightness_slider,
                  example1,
                  example2,
                  example3,):

    if list_of_contents is not None:
        if ctx.triggered_id == 'save_img':

            children = [parse_contents(c, 
                                   ids[-1], 
                                   change_bg, 
                                   (red_slider, green_slider, blue_slider),
                                   ) for c in list_of_contents]

            data = dcc.send_bytes(str_to_io(children[0][0]).getvalue(), "image.png")

            return data, no_update

        else:
            if ctx.triggered_id in bg_images.keys():
                change_bg = b64_image(bg_images[ctx.triggered_id])
            
            children = [parse_contents(c, 
                                    ctx.triggered_id, 
                                    change_bg, 
                                    (red_slider, green_slider, blue_slider),
                                    ) for c in list_of_contents]
            ids.append(ctx.triggered_id)
            
            return no_update, children[0][1]
        

if __name__ == '__main__':
    app.run_server(debug=True)