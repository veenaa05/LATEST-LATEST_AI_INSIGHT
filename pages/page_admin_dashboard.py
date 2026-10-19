from dash import html, dcc
import dash_bootstrap_components as dbc
from components.admin_layout import admin_layout


CARD_STYLE = {
    "backgroundColor": "white",
    "border": "1px solid #E5E7EB",
    "borderRadius": "18px",
    "padding": "24px",
    "height": "220px",
    "cursor": "pointer",
    "boxShadow": "0 6px 18px rgba(0,0,0,.08)",
    "transition": "all .25s ease"
    
    # "backgroundColor": "white",
    # "border": "1px solid #E5E7EB",
    # "borderRadius": "16px",
    # "padding": "32px",
    # "height": "210px",
    # "cursor": "pointer",
    # "boxShadow": "0 3px 10px rgba(0,0,0,.08)",
    # "transition": "all .2s ease"
}


def admin_card(icon, title, description, href):

    return dbc.Col(

        dcc.Link(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div(
                            icon,
                            style={
                                "fontSize": "54px",
                                "marginBottom": "18px"
                            }
                        ),
                        html.H4(
                            title,
                            style={
                                "fontWeight": "700",
                                "fontSize": "24px",
                                "marginBottom": "10px"
                            }
                        ),

                        html.P(
                            description,
                            style={
                                "color": "#6B7280",
                                "fontSize": "14px"
                            }
                        )
                    ]
                ),
                style=CARD_STYLE
            ),

            href=href,
            style={
                "textDecoration": "none",
                "color": "inherit"
            }

        ),

        lg=6,
        xl=3,
        md=6,
        sm=12,
        className="mb-4"

    )


def layout(session_data=None):
    session_data = session_data or {}
    username = session_data.get("name") or session_data.get("username", "Administrator")
    
    body = [
    #     html.H2(
    #     f"Welcome, {username} 👋",
    #     style={
    #         "fontSize": "36px",
    #         "fontWeight": "700",
    #         "color": "#111827",
    #         "marginBottom": "8px"
    #     }
    # ),
        # html.P(
        #     "Welcome to the administration console. Select a module below.",
        #     style={
        #         "color": "#6B7280",
        #         "fontSize": "16px",
        #         "marginBottom": "35px"
        #     }
        # ),

        dbc.Row(
            [
                admin_card(
                    "👤",
                    "Users",
                    "Create and manage users.",
                    "/users"
                ),

                admin_card(
                    "🏢",
                    "Companies",
                    "Create and manage companies.",
                    "/companies"
                ),

                admin_card(
                    "🔗",
                    "Mapping",
                    "Assign companies to users.",
                    "/mapping"
                ),

                admin_card(
                    "🌐",
                    "Portal",
                    "Open company workspace.",
                    "/portal"
                )
            ],
            className="g-4"
        )
    ]

    return admin_layout(
        title=f"Welcome, {username}",
        body=body,
        active="home",
        session_data=session_data
    )










# from dash import html, dcc
# import dash_bootstrap_components as dbc
# from components.admin_layout import admin_layout


# CARD_STYLE = {
#     "backgroundColor": "white",
#     "border": "1px solid #E5E7EB",
#     "borderRadius": "12px",
#     "padding": "30px",
#     "height": "180px",
#     "cursor": "pointer",
#     "boxShadow": "0 2px 8px rgba(0,0,0,0.06)"
# }


# def admin_card(icon, title, description, href):
#     return dbc.Col(
#         dcc.Link(
#             dbc.Card(
#                 dbc.CardBody([
#                     html.Div(
#                         icon,
#                         style={
#                             "fontSize": "42px",
#                             "marginBottom": "15px"
#                         }
#                     ),

#                     html.H4(
#                         title,
#                         style={
#                             "fontWeight": "700"
#                         }
#                     ),

#                     html.P(
#                         description,
#                         style={
#                             "color": "#6B7280"
#                         }
#                     )
#                 ]),
#                 style=CARD_STYLE
#             ),
#             href=href,
#             style={
#                 "textDecoration": "none",
#                 "color": "inherit"
#             }
#         ),
#         md=4
#     )


# def layout():

#     body = html.Div(

#         [

#             html.P(
#                 "Welcome to the administration console. Select a module below.",
#                 style={
#                     "color": "#6B7280",
#                     "marginBottom": "35px"
#                 }
#             ),

#             dbc.Row(

#                 [

#                     admin_card(
#                         "👤",
#                         "Users",
#                         "Create and manage users.",
#                         "/users"
#                     ),

#                     admin_card(
#                         "🏢",
#                         "Companies",
#                         "Create and manage companies.",
#                         "/companies"
#                     ),

#                     admin_card(
#                         "🔗",
#                         "Mapping",
#                         "Assign companies to users.",
#                         "/mapping"
#                     ),

#                 ],

#                 className="g-4"

#             )

#         ]

#     )

#     return admin_layout(
#         title="Admin Dashboard",
#         body=body,
#         active="home"
#     )


# from dash import html, dcc
# import dash_bootstrap_components as dbc
# from components.admin_layout import admin_layout


# def layout():

#     card_style = {
#         "border": "1px solid #E2E8F0",
#         "borderRadius": "10px",
#         "padding": "25px",
#         "height": "160px",
#         "cursor": "pointer",
#         "transition": "0.2s",
#         "backgroundColor": "white",
#         "boxShadow": "0 2px 6px rgba(0,0,0,0.08)"
#     }

#     return dbc.Container([

#         dbc.Row(
#             dbc.Col([
#                 html.H2(
#                     "Admin Dashboard",
#                     style={"fontWeight": "700"}
#                 ),

#                 html.P(
#                     "Manage users, companies and company mappings.",
#                     style={"color": "#666"}
#                 )
#             ]),
#             className="mt-4 mb-4"
#         ),

#         dbc.Row([

#             dbc.Col(
#                 dcc.Link(

#                     dbc.Card(
#                         dbc.CardBody([
#                             html.H4("Users"),
#                             html.P("Create and manage users.")
#                         ]),
#                         style=card_style
#                     ),

#                     href="/users",
#                     style={"textDecoration": "none", "color": "inherit"}
#                 ),
#                 md=3
#             ),

#             dbc.Col(
#                 dcc.Link(

#                     dbc.Card(
#                         dbc.CardBody([
#                             html.H4("Companies"),
#                             html.P("Create and manage companies.")
#                         ]),
#                         style=card_style
#                     ),

#                     href="/companies",
#                     style={"textDecoration": "none", "color": "inherit"}
#                 ),
#                 md=3
#             ),

#             dbc.Col(
#                 dcc.Link(

#                     dbc.Card(
#                         dbc.CardBody([
#                             html.H4("User Company Mapping"),
#                             html.P("Assign companies to users.")
#                         ]),
#                         style=card_style
#                     ),

#                     href="/mapping",
#                     style={"textDecoration": "none", "color": "inherit"}
#                 ),
#                 md=3
#             ),

#             dbc.Col(
#                 dcc.Link(

#                     dbc.Card(
#                         dbc.CardBody([
#                             html.H4("Portal"),
#                             html.P("Open User Portal.")
#                         ]),
#                         style=card_style
#                     ),

#                     href="/upload",
#                     style={"textDecoration": "none", "color": "inherit"}
#                 ),
#                 md=3
#             ),

#         ])

#     ], fluid=True)