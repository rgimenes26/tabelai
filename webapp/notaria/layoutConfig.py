import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import html, dcc

pages = {
    'compraVenda': {
        'path': '/compra-e-venda',
        'title': 'Compra e Venda',
        'var' : 'compraVenda',
    },
    'doacaoPura': {
        'path': '/doacao-pura',
        'title': 'Doação Pura',
        'var' : 'doacaoPura',
    },
    'doacaoUsufruto': {
        'path': '/doacao-usufruto',
        'title': 'Doação com Usufruto',
        'var' : 'doacaoUsufruto',
    },
    'procuracao': {
        'path': '/procuracao',
        'title': 'Procuração',
        'var' : 'procuracao',
    }
}

def getChatMessage(type='client', content='', files=None):
    return dmc.Paper(
        children=[
            dmc.Text(content, size='xl', style={"--text-fz": "0.8em","margin": "10px"}),
            dmc.Grid(
                children=[
                    dmc.GridCol(
                        dmc.Badge(
                            size="xl",
                            color="black",
                            variant="light",
                            style={"height": "30px", "marginRight": "10px"},
                            children=[
                                DashIconify(
                                    icon="mdi:file", width=20, style={"marginRight": "5px"},
                                ),
                                f"{file}" if file else "No File"
                            ]),
                        span="content",
                    ) for file in files
                ] if files else []
            )
        ],
        shadow='md',
        p='md',
        radius='md',
        style={"width": "85%", "marginLeft": "40px"} if type == 'client' else {"width": "85%", "marginRight": "40px"},
        withBorder=False,
    )

def getChatPageLayout(page='compraVenda'):
    return (
        html.Div([
            dcc.Location(id=f"url_{pages[page]['var']}", refresh=False),
            html.Div(
                dmc.Grid(
                    children=[
                        dmc.GridCol(
                            html.H1(f"{pages[page]['title']}", className='text-left', style={"fontSize": "3rem", 'marginTop': "10px", "marginBottom": "10px", "fontWeight": "bold", 'marginLeft': "20px"}),
                            span=11, 
                            style={"textAlign": "left"},
                        ),
                        dmc.GridCol(
                            dmc.Center(
                                dmc.ActionIcon(
                                    # id=f"helpButton_{pages[page]['var']}",
                                    id=f"helpButton",
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
                id=f"scrollArea_{pages[page]['var']}",
                type="auto",
                scrollbarSize=10,
                scrollHideDelay=1000,
                offsetScrollbars=True,
                w="100%",
                h="calc(100vh - 330px)",
                children=[
                    dmc.Flex(
                        id=f"flexChatContent_{pages[page]['var']}",
                        children = [
                            getChatMessage(type='client', content="Ato hibrido. Dispensa de apresentação das certidões dos distribuidores. Joao vendedor e Marcos Rogerio comprador assinam eletronicamente. Imóvel rural."),
                            getChatMessage(type='server', content="""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed sagittis libero et purus molestie, eget rhoncus diam imperdiet. Curabitur in molestie mauris, vel hendrerit tortor.
                                                        Aliquam faucibus nulla eu dolor viverra hendrerit. Phasellus consequat purus lobortis, hendrerit diam ac, tempus massa. Aenean et pulvinar nunc. Donec fermentum ut ipsum eget imperdiet. Nunc sollicitudin elit est, quis tincidunt metus consequat vitae. Ut suscipit urna id mauris tristique, at lobortis magna iaculis. Pellentesque et ullamcorper neque, eu posuere arcu. Suspendisse non scelerisque mauris, a fermentum felis. Etiam in sem rhoncus, aliquet leo non, ornare diam. Maecenas nec urna sed orci malesuada lobortis. Fusce arcu erat, elementum eget lacinia a, molestie at orci. Aenean aliquam quam ac eros lacinia efficitur sed vel mauris. Donec quis ex porttitor, congue tellus ac, sollicitudin dolor. Curabitur pulvinar sem dolor, quis sagittis felis blandit eu. Aliquam venenatis risus vitae magna pulvinar faucibus sed ut orci. Praesent elementum eget mauris consequat molestie.

                        #         Cras accumsan felis sed lectus posuere placerat. Donec vitae tempor sapien. Maecenas fringilla, elit id pulvinar eleifend, tortor nisl suscipit augue, ut tincidunt est ante quis orci. Curabitur a mauris massa. Integer nec justo massa. Donec at fringilla risus. Nullam aliquam, orci ut auctor tempor, tellus mi varius velit, eu finibus massa felis vel sem. Etiam suscipit ultrices purus, ac faucibus est placerat id. Phasellus scelerisque tellus sed risus feugiat lobortis. Nam vitae magna rutrum, commodo velit ac, bibendum sem. Nullam tincidunt ac erat non iaculis. In hac habitasse platea dictumst. Sed sit amet nunc id nunc tristique posuere vel sagittis magna. In hac habitasse platea dictumst. Nunc volutpat eros a ultrices volutpat. Phasellus sed mauris euismod, rutrum augue eget, rutrum nibh.

                        #         Phasellus finibus erat in sollicitudin tincidunt. Integer sollicitudin commodo eros quis commodo. Vestibulum ac sem aliquet, faucibus neque sed, porta elit. Duis pretium nibh ante, ac molestie enim luctus eget. Nulla sed justo mauris. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Morbi dignissim velit ac urna congue, eu hendrerit tellus dictum. Fusce dictum, eros vitae lacinia fermentum, eros lorem consectetur arcu, at pharetra mauris dolor dictum nunc. Fusce pellentesque ligula maximus consectetur placerat. Vestibulum tristique porta nisl, eu bibendum tortor pretium quis. Sed sed neque dui. Maecenas finibus mauris eu dolor ultricies, sed lobortis ipsum scelerisque. Ut eu scelerisque leo. Vestibulum malesuada id urna non pharetra.

                        #         Sed ac urna eu orci tempor ultrices. Duis rutrum sem sit amet ligula tristique, placerat fringilla augue mattis. Nulla mauris ipsum, ornare non ultrices nec, hendrerit ac dui. Proin vitae eros finibus, tincidunt dolor eu, ultricies purus. Cras sagittis consectetur nulla bibendum semper. In in ultrices augue. Curabitur porta purus eget magna vulputate, eget lobortis diam commodo. Vivamus a imperdiet dolor, vel hendrerit nulla. Nam finibus tempus turpis a egestas. Mauris nec semper massa, sit amet placerat nulla. In tempus ante a blandit accumsan. Nam quis orci felis. Suspendisse fringilla eu nunc sit amet ornare. Integer aliquam ac magna a eleifend. Proin lobortis nisi ut est suscipit euismod."""),
                        
                        ],
                        gap="md",
                        justify="center",
                        align="center",
                        direction="column",
                        wrap="wrap",
                    ),
                    dmc.Divider(variant="solid", id=f"endOfChat_{pages[page]['var']}", style={"marginTop": "20px", "marginBottom": "10px"}),
                ],
                style={"fontSize": "1.5em"},
            ),
            dmc.Grid(
                justify="center",
                align="stretch",
                children=[
                    dmc.GridCol([
                        dmc.Textarea(
                            id=f"inputText_{pages[page]['var']}",
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
            html.A("To the end of the chat", href=f"#endOfChat_{pages[page]['var']}", style={"display": "none"}),
            dmc.Grid([
                dmc.GridCol([
                    dcc.Upload(
                        id=f"uploadFiles_{pages[page]['var']}",
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
                        multiple=True,
                    ),
                ], span={'base': 12, 'md': 6}),
                dmc.GridCol([
                    dmc.Button(
                        "Enviar",
                        id=f"sendButton_{pages[page]['var']}",
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
        ]),
    )




# def getMantineTheme():
#     return dmc.Theme(
#         colorScheme='light',
#         primaryColor='blue',
#         fontFamily='Poppins, sans-serif",
#         headingsFontFamily='Poppin", sans-serif',
#         defaultRadius='md',
#         colors={
#             'blue': ['#E3F2FD', '#BBDEFB', '#90CAF9', '#64B5F6', '#42A5F5', '#2196F3', '#1E88E5', '#1976D2', '#1565C0', '#0D47A1'],
#             'red': ['#FFEBEE', '#FFCDD2', '#EF9A9A', '#E57373', '#EF5350', '#F44336', '#E53935', '#D32F2F', '#C62828', '#B71C1C'],
#         }
#     )



def getHelpDrawer():
    return dmc.Drawer(
        id='helpDrawer',
        title="Ajuda",
        opened=False,
        size="md",
        children=[
            dmc.Text("Aqui você pode encontrar informações sobre como usar a página de Compra e Venda."),
            dmc.Text("Para enviar uma mensagem, digite seu texto na caixa de entrada e clique no botão 'Enviar'."),
            dmc.Text("Você também pode fazer upload de arquivos relevantes para a conversa."),
            dmc.Text("Use o botão de ajuda para abrir este guia."),
        ],
        padding="xl",
        position="right",
    )