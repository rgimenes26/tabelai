import dash
from dash import (Dash,
                dash_table,
                html, dcc,
                Input, Output, State
                )
import dash_bootstrap_components as dbc
from flask_login import login_required
from datetime import date, datetime

from google import genai
client = genai.Client(api_key="AIzaSyDXfkh34h8TVCMsBkqYX706qwDjyKZr13o")

import base64
import io

from pathlib import Path
base_path = Path(__file__).parent
file_path = (base_path / "assets/layout.html").resolve()

with open(file_path, 'r', encoding='utf-8') as hFile:
    htmlIndex = hFile.read()

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css",
    "https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap",
    dcb.themes.BOOTSTRAP,
    ]


def protect_views(app):
    for view_func in app.server.view_functions:
        if view_func.startswith(app.config['url_base_pathname']):
            app.server.view_functions[view_func] = login_required(
                app.server.view_functions[view_func])
    return app

def init_dash_app(server):
    """Initialize the Dash app with the Flask server."""

    app = Dash(
        __name__,
        server=server,
        url_base_pathname='/app/',
        external_stylesheets=external_stylesheets,
        suppress_callback_exceptions=True,
    )

    app.index_string = htmlIndex

    app.layout = dcb.Container([
        dcb.Row([
            dcb.Col([
                dcb.Form([
                    dcb.Stack([
                        html.H1("Teste de API", className='text-center'),
                        dcc.Dropdown(
                            id='FundoDropdown',
                            options=[
                                {'label': 'Gemini 2.5 PRO', 'value': 'teste', 'disabled': True},
                            ],
                            value='teste',
                        ),
                        dcb.Textarea(
                            id='InputText',
                            size='lg',
                            placeholder='Digite algo...',
                            className='mb-2',
                            style={'height': '200px', 'resize': 'none'}
                        ),
                        dcc.Upload(
                            id='uploadFiles',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ]),
                            style={
                                'width': '100%',
                                'height': '80px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                # 'margin': '10px'
                            },
                            # Allow multiple files to be uploaded
                            multiple=True
                            ),
                    ],gap=4, className='mb-3'),
                    dcb.Button('Enviar', id='btnRefresh', className='btn', style={'width': '100%', 'background-color': 'rgb(255,122,138)'}),
                ])
            ], width=12, md=9,),
        ], justify='center', className='Nbox-content'),
        dcc.Loading(
            id='loadingfile',
            type='circle',
            children=[
                html.H3(id='fileNameH1'),
            ]),    
        dcc.Loading(
            id='loading',
            type='circle',
            children=[
                html.Div(
                    id='MainTabs_div', 
                    children=[
                    ],
                ),
            ])
    ], fluid=True, className='box-content')

    @app.callback(
            Output('MainTabs_div', 'children'),
            Input('btnRefresh', 'n_clicks'),
            State('InputText', 'value'),
            State('fileNameH1', 'children'),
            # State('FundoDropdown', 'value'),
            prevent_initial_call=True,
        )
    def render_master3(n_clicks, prompt, filenames):
        print(filenames)
        if filenames is not None:
            myfile = client.files.get(name=filenames)
            print(myfile) 

        print(f"Prompt: {prompt}")
        response = client.models.generate_content(
            model="gemini-2.5-pro", 
            contents=[
                prompt,
            ],
        )
        resp = [
            html.H1("Resposta", className='text-center'),
            html.Div(
                [
                    html.P("Texto:"),
                    html.Pre(response.text, style={'white-space': 'pre-wrap'}),
                    html.P("Uso de tokens:"),
                    html.Pre(str(response.usage_metadata), style={'white-space': 'pre-wrap'}),
                    html.P("Feedback do prompt:"),
                    html.Pre(str(response.prompt_feedback), style={'white-space': 'pre-wrap'}),
                ],
                className='response-container'
            ),
        ]
        return resp


    @app.callback(
            Output('fileNameH1', 'children'),
            Input('upload-data', 'contents'),
            State('upload-data', 'filename'),
            State('upload-data', 'last_modified'),
            # State('FundoDropdown', 'value'),
            prevent_initial_call=True,
        )
    def render_master3( contents, filenames, last_modified):
        if contents is not None:
            print("Trying to upload file...")
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            file = io.BytesIO(decoded)
            myfile = client.files.upload(file=file, name=filenames)
            file_name = myfile.name
            print(file_name)  # "files/*"
        else:
            file_name = None
            print("No file uploaded.")

        return file_name
    # app = layout.dev.importCallbacks(app)

    # app.enable_dev_tools(debug=True)
    dash_app = protect_views(app)
    return dash_app.server


# if __name__ == '__main__':
#     app.run(debug=True)
