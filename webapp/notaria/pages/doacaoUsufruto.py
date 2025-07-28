import dash
from dash import html, dcc, callback, Input, Output, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from webapp.notaria import layoutConfig

PAGE = 'doacaoUsufruto'

dash.register_page(
    __name__, 
    path=f"{layoutConfig.pages[PAGE]['path']}",
    title=f"{layoutConfig.pages[PAGE]['title']}",
    name=f"{layoutConfig.pages[PAGE]['title']}",
)

layout = layoutConfig.getChatPageLayout(
    page=PAGE,
)