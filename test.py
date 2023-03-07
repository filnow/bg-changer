import dash
import dash_core_components as dcc
import dash_html_components as html
import base64

app = dash.Dash(__name__)

image_filename = './static/images/bg.jpg'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

@app.callback(
    dash.dependencies.Output('download-image', 'data'),
    [dash.dependencies.Input('btn-download', 'n_clicks')]
)
def download_image(n_clicks):
    if n_clicks is not None:
        return dcc.send_file(
            'image.png',
            mimetype='image/png',
            attachment_filename='image.png',
            download=True
        )

app.layout = html.Div([
    html.Button('Download Image', id='btn-download'),
    dcc.Download(id='download-image')
])

if __name__ == '__main__':
    app.run_server(debug=True)