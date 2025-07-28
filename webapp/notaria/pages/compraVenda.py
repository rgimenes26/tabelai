import dash
from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from webapp.notaria import layoutConfig

PAGE = 'compraVenda'

dash.register_page(
    __name__, 
    path="/compra-e-venda",
    title="Compra e Venda",
    name="Compra e Venda",
)

files = [
    "cnh.pdf",
    "Escritura.pdf"
    "ImagemExemplo.png",
    "Contrato.pdf",
]

layout = html.Div([
    dcc.Location(id='url_compraVenda', refresh=False),
    html.A("To the end of the chat", href="#endOfChat", style={"display": "none"}),
    html.Div(
        dmc.Grid(
            children=[
                dmc.GridCol(
                    html.H1("Compra e Venda", className='text-left', style={"fontSize": "3rem", 'marginTop': "10px", "marginBottom": "10px", "fontWeight": "bold", 'marginLeft': "20px"}),
                    span=11, 
                    style={"textAlign": "left"},
                ),
                dmc.GridCol(
                    dmc.Center(
                        dmc.ActionIcon(
                            id='helpButton',
                            variant="light",
                            color="blue",
                            size="lg",
                            children=[
                                DashIconify(icon="ic:baseline-help", width=20),
                            ],
                        )
                    ),
                    span=1,
                    style={"height": "100%"},
                )
            ],
            grow=True,
        ),
        style={"position": "sticky", 'top' : 50, "zIndex": 100, "backgroundColor": 'white'},
    ),
    dmc.ScrollArea(
        id='scrollArea_compraVenda',
        type="auto",
        scrollbarSize=10,
        scrollHideDelay=1000,
        offsetScrollbars=True,
        w="100%",
        h="calc(100vh - 330px)",
        children=[
            dmc.Flex(
                id='flexChatContent',
                children = [
                ],
                gap="md",
                justify="center",
                align="center",
                direction="column",
                wrap="wrap",
            ),
            dmc.Divider(variant="solid", id='endOfChat_compraVenda', style={"marginTop": "20px", "marginBottom": "10px"}),
        ],
        style={"fontSize": "1.5em"},
    ),
    dmc.Grid(
        justify="center",
        align="stretch",
        children=[
            dmc.GridCol([
                dmc.Textarea(
                    id='inputText_compraVenda',
                    placeholder="Escreva aqui...",
                    w='100%',
                    autosize=True,
                    minRows=3,
                    maxRows=3,
                    radius="md",
                    styles={'input': {"fontSize": "1em"}},
                    style={"marginTop": "10px", "marginBottom": "20px"},
                    className='inputConfig',
                ),
            ], span={'base': 12, 'md': 9}),
    ]),
    dmc.Grid([
        dmc.GridCol([
            dcc.Upload(
                id='uploadFiles_compraVenda',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                },
                # Allow multiple files to be uploaded
                multiple=True,
            ),
        ], span={'base': 12, 'md': 6}),
        dmc.GridCol([
            dmc.Button(
                "Enviar",
                id='sendButton_compraVenda',
                variant="filled",
                color="blue",
                radius="md",
                w="100%",
                style={
                    "height" : "100%", 
                    'minHeight' : '50px',
                },
            ),
        ], span={'base': 12, 'md': 3}),
    ],
    justify="center",
    align="stretch",
    style={"marginTop": "10px", "marginBottom": "20px"},
    ),
])


@callback(
    Output('helpDrawer', 'opened'),
    Input('helpButton', 'n_clicks'),
    State('helpDrawer', 'opened'),
    prevent_initial_call=True
)
def open_helper_compra_venda(n_clicks, opened):
    if n_clicks is not None:
        return True
    
@callback(
    Output('flexChatContent', 'children'),
    Input('sendButton_compraVenda', 'n_clicks'),
    State('flexChatContent', 'children'),
    prevent_initial_call=True
)
def send_chat_data(n_clicks, chatLlist):
    chatLlist.append(
        layoutConfig.getChatMessage(
            type='client',
            files=files
            # files=[file for file in dcc.Upload(id='uploadFiles_compraVenda', children=html.Div()).contents]
        )
    )
    return chatLlist

@callback(
    Output('url_compraVenda', 'hash'),
    Input('flexChatContent', 'children'),
    prevent_initial_call=True
)
def open_helper_compra_venda(flexChatContent):
    return '#endOfChat_compraVenda'

# @callback(
#     Output('url_compraVenda', 'hash'),
#     Input('flexChatContent', 'children'),
#     prevent_initial_call=True
# )
# def open_helper_compra_venda(flexChatContent):
#     return '#endOfChat_compraVenda'