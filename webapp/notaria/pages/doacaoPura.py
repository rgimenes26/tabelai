import dash
from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from webapp.notaria import layoutConfig

PAGE = 'doacaoPura'
files = [
    "cnh.pdf",
    "Escritura.pdf"
    "ImagemExemplo.png",
    "Contrato.pdf",
]

dash.register_page(
    __name__, 
    path=f"{layoutConfig.pages[PAGE]['path']}",
    title=f"{layoutConfig.pages[PAGE]['title']}",
    name=f"{layoutConfig.pages[PAGE]['title']}",
)

layout = layoutConfig.getChatPageLayout(
    page=PAGE,
)

@callback(
    Output(f"flexChatContent_{PAGE}", 'children'),
    Input(f"sendButton_{PAGE}", 'n_clicks'),
    State(f"flexChatContent_{PAGE}", 'children'),
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