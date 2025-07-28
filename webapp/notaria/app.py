import dash
import dash_mantine_components as dmc
from dash import (Dash,
                dash_table,
                html, dcc,
                Input, Output, State
                )
from dash_iconify import DashIconify
# import dash_bootstrap_components as dbc
from flask_login import login_required
from datetime import date, datetime
from . import layoutConfig

from google import genai
client = genai.Client(api_key="AIzaSyDXfkh34h8TVCMsBkqYX706qwDjyKZr13o")

import base64
import io


external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css",
    "https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap",
    # dbc.themes.BOOTSTRAP,
    ]
theme = {
    "fontFamily": "Montserrat, sans-serif",
    "defaultRadius": "md",    
}


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
        use_pages=True,
    )

    app.layout = dmc.MantineProvider(
        children=[
            dmc.AppShell([
                dmc.AppShellHeader(
                    dmc.Group(
                        [
                            dmc.Group(
                                [
                                    dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False),
                                    # dmc.Image(src=logo, h=40, flex=0),
                                    dmc.Title("escreventes.ai", c="blue", style={"marginLeft": "20px"}),
                                ],
                                h="100%",
                                px="md",
                            ),
                            dmc.Group(
                                [
                                    dmc.Button(
                                        DashIconify(icon="mdi:home", width=20),
                                        variant="subtle",
                                        color="blue",
                                        # href="/",
                                    ),
                                    dmc.Button(
                                        DashIconify(icon="mdi:account-cog", width=20),
                                        variant="subtle",
                                        color="blue",
                                        # href="/profile",
                                    ),
                                    dmc.Button(
                                        DashIconify(icon="mdi:logout", width=20),
                                        variant="subtle",
                                        color="blue",
                                        # href="/logout",
                                    ),
                                ],
                                justify="flex-end",
                                gap="xs",
                                h="100%",
                                style={"marginRight": "15px"},
                            ),
                        ],
                        gap="md",
                        justify="space-around",
                        grow=True,
                        style={"height": "100%"},
                    ),
                ),
                dmc.AppShellNavbar(
                    id="navbar",
                    children=[
                        dmc.Divider(
                            label=[
                                DashIconify(icon='hugeicons:ai-brain-04', width=30, style={"marginRight": "10px"}), 
                                dmc.Title("Modelos", order=3)
                            ], 
                            labelPosition="left", 
                            size='lg', 
                            style={"marginBottom": "20px"},
                        ),
                        *[dmc.NavLink(
                            label=layoutConfig.pages[page]['title'],
                            href=f"/app{layoutConfig.pages[page]['path']}",
                            styles={"label": {"fontSize": "1.5em"}},
                        ) for page in layoutConfig.pages],
                        # dmc.NavLink(
                        #     label="Compra e Venda",
                        #     href="/app/compra-e-venda",
                        #     styles={"label": {"fontSize": "1.5em"}},
                        # ),
                        # dmc.NavLink(
                        #     label="Doação Pura",
                        #     href="/app/doaPura",
                        #     styles={"label": {"fontSize": "1.5em"}},
                        # ),
                        # dmc.NavLink(
                        #     label="Doação Res. Usufruto",
                        #     href="/app/DoaUsufruto",
                        #     styles={"label": {"fontSize": "1.5em"}},
                        # ),
                        # dmc.NavLink(
                        #     label="Procurações",
                        #     href="/app/procuracoes",
                        #     styles={"label": {"fontSize": "1.5em"}},
                        # ),
                        # dmc.NavLink(
                        #     label="Analista Matrícula",
                        #     href="/app/matricula",
                        #     styles={"label": {"fontSize": "1.5em"}},
                        # ),
                        # dmc.NavLink(
                        #     label="Conferente - Doação",
                        #     href="/app/confereDoa",
                        #     styles={"label": {"fontSize": "1.5em"}},
                        # ),
                        # "Navbar",
                        # *[dmc.Skeleton(height=28, mt="sm", animate=False) for _ in range(15)],
                    ],
                    p="md",
                ),
                dmc.AppShellMain(
                    id='mainShell',
                    children=[
                        # html.H1("Teste de API", className='text-center'),
                        dash.page_container,
                        layoutConfig.getHelpDrawer(),
                        html.Div(id='pseudo-output', style={'display': 'none'}),
                    ],
                ),
                # dmc.AppShellFooter("Footer", p="md"),
            ],
            header={"height": 80},
            padding="md",
            navbar={
                "width": 350,
                "breakpoint": "sm",
                "collapsed": {"mobile": True},
            },
            # footer={"height": 60},
            id="appshell",
            ),  
        ],
        theme=theme,
    )

    @app.callback(
        Output("appshell", "navbar"),
        Input("burger", "opened"),
        State("appshell", "navbar"),
    )
    def navbar_is_open(opened, navbar):
        navbar["collapsed"] = {"mobile": not opened}
        return navbar

    #         dbc.Container([
    #             dbc.Row([
    #                 dbc.Col([
    #                     dbc.Form([
    #                         dbc.Stack([
    #                             html.H1("Teste de API", className='text-center'),
    #                             dcc.Dropdown(
    #                                 id='FundoDropdown',
    #                                 options=[
    #                                     {'label': 'Gemini 2.5 PRO', 'value': 'teste', 'disabled': True},
    #                                 ],
    #                                 value='teste',
    #                             ),
    #                             dbc.Textarea(
    #                                 id='InputText',
    #                                 size='lg',
    #                                 placeholder='Digite algo...',
    #                                 className='mb-2',
    #                                 style={'height': '200px', 'resize': 'none'}
    #                             ),
    #                             dcc.Upload(
    #                                 id='uploadFiles',
    #                                 children=html.Div([
    #                                     'Drag and Drop or ',
    #                                     html.A('Select Files')
    #                                 ]),
    #                                 style={
    #                                     'width': '100%',
    #                                     'height': '80px',
    #                                     'lineHeight': '60px',
    #                                     'borderWidth': '1px',
    #                                     'borderStyle': 'dashed',
    #                                     'borderRadius': '5px',
    #                                     'textAlign': 'center',
    #                                     # 'margin': '10px'
    #                                 },
    #                                 # Allow multiple files to be uploaded
    #                                 multiple=True
    #                                 ),
    #                         ],gap=4, className='mb-3'),
    #                         dbc.Button('Enviar', id='btnRefresh', className='btn', style={'width': '100%', 'background-color': 'rgb(255,122,138)'}),
    #                     ])
    #                 ], width=12, md=9,),
    #             ], justify='center', className='Nbox-content'),
    #             dcc.Loading(
    #                 id='loadingfile',
    #                 type='circle',
    #                 children=[
    #                     html.H3(id='fileNameH1'),
    #                 ]),    
    #             dcc.Loading(
    #                 id='loading',
    #                 type='circle',
    #                 children=[
    #                     html.Div(
    #                         id='MainTabs_div', 
    #                         children=[
    #                         ],
    #                     ),
    #                 ])
    #         ], fluid=True, className='box-content'),
    #     ],
    #     theme=theme,
    # )

    # @app.callback(
    #         Output('MainTabs_div', 'children'),
    #         Input('btnRefresh', 'n_clicks'),
    #         State('InputText', 'value'),
    #         State('fileNameH1', 'children'),
    #         # State('FundoDropdown', 'value'),
    #         prevent_initial_call=True,
    #     )
    # def render_master3(n_clicks, prompt, filenames):
    #     print(filenames)
    #     if filenames is not None:
    #         myfile = client.files.get(name=filenames)
    #         print(myfile) 

    #     print(f"Prompt: {prompt}")
    #     response = client.models.generate_content(
    #         model="gemini-2.5-pro", 
    #         contents=[
    #             prompt,
    #         ],
    #     )
    #     resp = [
    #         html.H1("Resposta", className='text-center'),
    #         html.Div(
    #             [
    #                 html.P("Texto:"),
    #                 html.Pre(response.text, style={'white-space': 'pre-wrap'}),
    #                 html.P("Uso de tokens:"),
    #                 html.Pre(str(response.usage_metadata), style={'white-space': 'pre-wrap'}),
    #                 html.P("Feedback do prompt:"),
    #                 html.Pre(str(response.prompt_feedback), style={'white-space': 'pre-wrap'}),
    #             ],
    #             className='response-container'
    #         ),
    #     ]
    #     return resp


    # @app.callback(
    #         Output('fileNameH1', 'children'),
    #         Input('upload-data', 'contents'),
    #         State('upload-data', 'filename'),
    #         State('upload-data', 'last_modified'),
    #         # State('FundoDropdown', 'value'),
    #         prevent_initial_call=True,
    #     )
    # def render_master3( contents, filenames, last_modified):
    #     if contents is not None:
    #         print("Trying to upload file...")
    #         content_type, content_string = contents.split(',')
    #         decoded = base64.b64decode(content_string)
    #         file = io.BytesIO(decoded)
    #         myfile = client.files.upload(file=file, name=filenames)
    #         file_name = myfile.name
    #         print(file_name)  # "files/*"
    #     else:
    #         file_name = None
    #         print("No file uploaded.")

    #     return file_name

    
    
    # app = layout.dev.importCallbacks(app)
    app.clientside_callback(
        """
        function(hash) {
            if (hash) {
                const targetElement = document.getElementById(hash.replace('#', ''));
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            }
            return window.dash_clientside.no_update; // No actual output needed
        }
        """,
        Output('pseudo-output', 'children'),
        Input('url_CompraVenda', 'hash')
    )
    app.enable_dev_tools(debug=True)
    dash_app = protect_views(app)
    return dash_app.server


# if __name__ == '__main__':
#     app.run(debug=True)
