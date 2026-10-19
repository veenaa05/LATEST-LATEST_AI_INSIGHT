from dash import html, dcc
import dash_bootstrap_components as dbc
from components.admin_layout import admin_layout


def generate_users_page(session_data=None):

    body = html.Div(

        [

            dcc.Store(id="selected-user-id"),

            html.Div(
                id="create-user-msg",
                className="mb-3"
            ),

            # =====================================================
            # CREATE USER
            # =====================================================

            dbc.Card(

                dbc.CardBody(

                    [

                        html.H4(
                            "Create User",
                            className="fw-bold mb-3"
                        ),

                        dbc.Row(

                            [

                                dbc.Col(

                                    [

                                        dbc.Label(
                                            "Username",
                                            className="fw-semibold mb-2"
                                        ),

                                        dbc.Input(
                                            id="user-username",
                                            placeholder="Enter username",
                                            type="text"
                                        )

                                    ],

                                    md=3

                                ),

                                dbc.Col(

                                    [

                                        dbc.Label(
                                            "Password",
                                            className="fw-semibold mb-2"
                                        ),

                                        dbc.Input(
                                            id="user-password",
                                            placeholder="Enter password",
                                            type="password"
                                        )

                                    ],

                                    md=3

                                ),

                                dbc.Col(

                                    [

                                        dbc.Label(
                                            "Role",
                                            className="fw-semibold mb-2"
                                        ),

                                        dbc.Select(

                                            id="user-role",

                                            options=[

                                                {
                                                    "label": "Admin",
                                                    "value": 1
                                                },

                                                {
                                                    "label": "User",
                                                    "value": 2
                                                }

                                            ],

                                            value=2

                                        )

                                    ],

                                    md=3

                                ),

                                dbc.Col(

                                    [

                                        dbc.Label(
                                            " ",
                                            className="mb-2"
                                        ),

                                        dbc.Button(

                                            "Create User",

                                            id="btn-save-user",

                                            color="primary",

                                            className="w-100"

                                        )

                                    ],

                                    md=3

                                )

                            ],

                            className="g-3"

                        )

                    ]

                ),

                className="shadow-sm rounded-4 border-0 mb-4"

            ),

            # =====================================================
            # USER LIST
            # =====================================================

            dbc.Card(

                dbc.CardBody(

                    [

                        html.H4(

                            "User List",

                            className="fw-bold mb-3"

                        ),

                        html.Div(

                            html.Table(

                                [

                                    html.Thead(

                                        html.Tr(

                                            [

                                                html.Th(

                                                    "Action",

                                                    style={
                                                        "width": "12%"
                                                    }

                                                ),

                                                html.Th(

                                                    "Username",

                                                    style={
                                                        "width": "48%"
                                                    }

                                                ),

                                                html.Th(

                                                    "Role",

                                                    style={
                                                        "width": "20%"
                                                    }

                                                ),

                                                html.Th(

                                                    "Status",

                                                    style={
                                                        "width": "20%",
                                                        "textAlign": "center"
                                                    }

                                                )

                                            ]

                                        )

                                    ),

                                    html.Tbody(

                                        id="users-list"

                                    )

                                ],

                                className="table table-hover align-middle mb-0"

                            ),

                            className="table-responsive"

                        )

                    ]

                ),

                className="shadow-sm rounded-4 border-0"

            )

        ]

    )

    return admin_layout(
        title="User Master",
        body=body,
        active="users",
        session_data=session_data

    )





# from dash import html, dcc
# import dash_bootstrap_components as dbc
# from components.admin_layout import admin_layout


# def generate_users_page():
#     print( "USERS PAGE FUNCTION CALLED" )
#     body = html.Div(

#         [

#             dcc.Store(id="selected-user-id"),

#             html.Div(
#                 id="create-user-msg",
#                 className="mb-3"
#             ),

#             dbc.Card(

#                 dbc.CardBody(

#                     [

#                         html.H5(
#                             "Create User",
#                             className="fw-bold mb-4"
#                         ),

#                         dbc.Row(

#                             [

#                                 dbc.Col(

#                                     [

#                                         dbc.Label(
#                                             "Username",
#                                             className="fw-semibold"
#                                         ),

#                                         dbc.Input(

#                                             id="user-username",

#                                             placeholder="Enter username",

#                                             type="text"

#                                         )

#                                     ],

#                                     md=3

#                                 ),

#                                 dbc.Col(

#                                     [

#                                         dbc.Label(
#                                             "Password",
#                                             className="fw-semibold"
#                                         ),

#                                         dbc.Input(

#                                             id="user-password",

#                                             placeholder="Enter password",

#                                             type="password"

#                                         )

#                                     ],

#                                     md=3

#                                 ),

#                                 dbc.Col(

#                                     [

#                                         dbc.Label(
#                                             "Role",
#                                             className="fw-semibold"
#                                         ),

#                                         dbc.Select(

#                                             id="user-role",

#                                             options=[
#                                                 {
#                                                     "label": "Admin",
#                                                     "value": 1
#                                                 },
#                                                 {
#                                                     "label": "User",
#                                                     "value": 2
#                                                 }
#                                             ],

#                                             value=2

#                                         )

#                                     ],

#                                     md=3

#                                 ),

#                                 dbc.Col(

#                                     dbc.Button(

#                                         "Create User",

#                                         id="btn-save-user",

#                                         color="primary",

#                                         className="w-100"

#                                     ),

#                                     md=3,

#                                     className="d-flex align-items-end"

#                                 )

#                             ],

#                             className="g-3"

#                         )

#                     ]

#                 ),

#                 className="shadow-sm border-0 rounded-4 mb-4"

#             ),

#             dbc.Card(

#                 dbc.CardBody(

#                     [

#                         html.H5(

#                             "User List",

#                             className="fw-bold mb-3"

#                         ),

#                         html.Table(

#                             [

#                                 html.Thead(

#                                     html.Tr(

#                                         [

#                                             html.Th("Action"),

#                                             html.Th("Username"),

#                                             html.Th("Role"),

#                                             html.Th("Toggle Status")

#                                         ]

#                                     )

#                                 ),

#                                 html.Tbody(

#                                     id="users-list"

#                                 )

#                             ],

#                             className="table"

#                         )

#                     ]

#                 ),

#                 className="shadow-sm border-0 rounded-4"
#             )
#         ]
#     )
#     print(type(body))
#     print(body)
#     return admin_layout(
#         title="User Master",
#         body=body,
#         active="users"
#     )












# from dash import html, dcc
# import dash_bootstrap_components as dbc


# def generate_users_page():

#     return dbc.Container(

#         [
#             dcc.Store(id="selected-user-id"),
#             html.H2(
#                 "User Master",
#                 className="fw-bold mb-4"
#             ),
#             html.Div(
#                 id="create-user-msg",
#                 className="mb-3"
#             ),
#             dbc.Card(
#                 dbc.CardBody(
#                     [
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     [
#                                         dbc.Label(
#                                             "Username",
#                                             className="fw-semibold"
#                                         ),
#                                         dbc.Input(
#                                             id="user-username",
#                                             placeholder="Enter username",
#                                             type="text",
#                                             className="user-input"
#                                         )
#                                     ],
#                                     md=3
#                                 ),
#                                 dbc.Col(
#                                     [
#                                         dbc.Label(
#                                             "Password",
#                                             className="fw-semibold"
#                                         ),
#                                         dbc.Input(
#                                             id="user-password",
#                                             placeholder="Enter password",
#                                             type="password",
#                                             className="user-input"
#                                         )
#                                     ],
#                                     md=3
#                                 ),
#                                 dbc.Col(
#                                     [
#                                         dbc.Label(
#                                             "Role",
#                                             className="fw-semibold"
#                                         ),
#                                         dbc.Select(
#                                             id="user-role",
#                                             options=[
#                                                 {
#                                                     "label": "Admin",
#                                                     "value": 1
#                                                 },
#                                                 {
#                                                     "label": "User",
#                                                     "value": 2
#                                                 }
#                                             ],
#                                             value=2,
#                                             className="user-input"
#                                         )
#                                     ],
#                                     md=3
#                                 ),
#                                 dbc.Col(
#                                     dbc.Button(
#                                         "Create User",
#                                         id="btn-save-user",
#                                         color="primary",
#                                         className="create-user-btn"
#                                     ),
#                                     md=3,
#                                     className="d-flex align-items-end"
#                                 )
#                             ],
#                             className="g-3"
#                         )
#                     ]
#                 ),
#                 className="shadow-sm rounded-3"
#             ),
#             dbc.Card(
#                 dbc.CardBody(
#                     [
#                         html.H5(
#     "User List",
#     className="fw-bold mb-3"
# ),

# html.Table(

#     [

#         html.Thead(

#             html.Tr(

#                 [

#                     html.Th("Action"),
#                     html.Th("Username"),
#                     html.Th("Role"),
#                     html.Th("Toggle Status")

#                 ]

#             )

#         ),

#         html.Tbody(

#             id="users-list"

#         )

#     ],

#     className="table user-master-table"

# )
#                     ]
#                 ),
#                 className="shadow-sm border-0 rounded-4"
#             )
#         ],
#         fluid=True,
#         className="p-4"
#     )




# from dash import html, dcc
# import dash_bootstrap_components as dbc
# from dash.dash_table import DataTable

# def generate_users_page():

#     return dbc.Container(
#         [
#             dcc.Store(
#                 id="selected-user-id",
#             ),
#             html.H2(
#                 "User Master",
#                 style={
#                     "fontWeight": "700",
#                     "marginBottom": "25px"
#                 }
#             ),

#             dbc.Card(
#                 dbc.CardBody(
#                     [
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     [
#                                         dbc.Label("Username"),
#                                         dbc.Input(
#                                             id="user-username",
#                                             placeholder="Username",
#                                             type="text"
#                                         )
#                                     ],
#                                     md=4
#                                 ),
#                                 dbc.Col(
#                                     [
#                                         dbc.Label("Password"),
#                                         dbc.Input(
#                                             id="user-password",
#                                             placeholder="Password",
#                                             type="password"
#                                         )
#                                     ],
#                                     md=4
#                                 ),
#                                 dbc.Col(
#                                     [
#                                         dbc.Label("Role"),
#                                         dbc.Select(
#                                             id="user-role",
#                                             options=[
#                                                 {
#                                                     "label": "User",
#                                                     "value": 2
#                                                 },

#                                                 {
#                                                     "label": "Admin",
#                                                     "value": 1
#                                                 }
#                                             ],
#                                             value=2
#                                         )
#                                     ],
#                                     md=3
#                                 ),
#                                 dbc.Col(
#                                     [
#                                         dbc.Button(
#                                             "Create User",
#                                             id="btn-save-user",
#                                             color="primary",
#                                             style={
#                                                 "marginTop": "32px",
#                                                 "width": "100%"
#                                             }
#                                         )
#                                     ],
#                                     md=1
#                                 )
#                             ]
#                         )
#                     ]
#                 )
#             ),

#             html.Br(),
#             dbc.Card(
#                 dbc.CardBody(
#                     [
#                         html.H4("User List"),
#                         html.Div(
#                             id="users-list",
#                             className="mt-3",
#                         #     columns=[
#                         #         {
#                         #             "name": "Action",
#                         #             "id": "action",
#                         #             "presentation": "markdown"
#                         #         },

#                         #         {
#                         #             "name": "Username",
#                         #             "id": "username"
#                         #         },

#                         #         {
#                         #             "name": "Role",
#                         #             "id": "role"
#                         #         },

#                         #         {
#                         #             "name": "Toggle Status",
#                         #             "id": "status",
#                         #             "presentation": "markdown"
#                         #         }

#                         #     ],

#                         #     data=[],

#                         #     style_table={
#                         #         "overflowX": "auto"
#                         #     },
#                         #     style_cell={
#                         #         "textAlign": "left",
#                         #         "padding": "12px"
#                         #     },

#                         #     style_header={
#                         #         "fontWeight": "bold",
#                         #         "backgroundColor": "#f8f9fa"
#                         #     }
#                         # )
#                         )
#                     ]
#                 )
#             )
#         ],

#         fluid=True,
#         style={
#             "padding": "25px"
#         }
#     )