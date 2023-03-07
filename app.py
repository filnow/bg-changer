from dash import Dash, dcc, html, ctx, no_update
from dash.dependencies import Input, Output
from images import ImageProcessor
import io

ids = []
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
    }),
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
        ], 
        style={'position': 'absolute', 
                  'bottom': '25%', 
                  'width': '40%', 
                  'right': '3%',
                  }),
    ], 
    style={'position': 'relative', 
              'height': '98vh', 
              'width': '100vw', 
              'max-width': '100%',
              'max-height': '100%',
              'overflow': 'hidden',
              }
)

def parse_contents(contents, id, bg_img, slider_value):
    
    img = ImageProcessor(contents)

    if id == 'my-slider' or id == 'remove-bg':
        img = img.remove_bg((slider_value, slider_value, slider_value))
        return [img, html.Div([
            html.Img(src=img, style={'width': '100%', 'height': '100%', 'margin': '10px'}),  
        ])]
    elif id == 'change-bg':
        img = img.change_bg(bg_img)
        return [img, html.Div([
            html.Img(src=img, style={'width': '100%', 'height': '100%', 'margin': '10px'}),  
        ])]
    elif id == 'reset_img':
        return [img, html.Div([])]
    else:
        return [img, html.Div([
            html.Img(src=contents, style={'width': '100%', 'height': '100%', 'margin': '10px'}),  
        ])]

@app.callback(Output('download-image', 'data'),
              Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'),
              Input('change-bg', 'contents'),
              Input('remove-bg', 'n_clicks'),
              Input('reset_img', 'n_clicks'),
              Input('save_img', 'n_clicks'),
              Input('my-slider', 'value'),
              prevent_initial_call=True,)

def update_output(list_of_contents, 
                  change_bg, 
                  remove_bg,
                  reset_img,
                  save_img,
                  slider_value):
 
    if list_of_contents is not None:

        if ctx.triggered_id == 'save_img':

            children = [parse_contents(c, 
                                   ids[-1], 
                                   change_bg, 
                                   slider_value) for c in list_of_contents]
            img = children[0][0]
            img_io = io.BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

            data = dcc.send_bytes(img_io.getvalue(), "image.png")

            return data, no_update

        children = [parse_contents(c, 
                                   ctx.triggered_id, 
                                   change_bg, 
                                   slider_value) for c in list_of_contents]
        ids.append(ctx.triggered_id)

        return no_update, children[0][1]
    

if __name__ == '__main__':
    app.run_server(debug=True)