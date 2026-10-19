
from dash import html, dcc
import dash_bootstrap_components as dbc
from components.admin_layout import admin_layout


def generate_mapping_page(session_data=None):
    
    body = html.Div(

        [

            html.Div(
                id="mapping-msg",
                className="mb-3"
            ),

            dbc.Card(

                dbc.CardBody(

                    [

                        html.H4(
                            "Assign Companies",
                            className="fw-bold mb-1"
                        ),

                        html.P(
                            "Map one or more companies to a user.",
                            className="text-muted mb-4"
                        ),

                        dbc.Row(

                            [

                                dbc.Col(

                                    [

                                        dbc.Label(
                                            "User",
                                            className="fw-semibold mb-2"
                                        ),

                                        dcc.Dropdown(
                                            id="mapping-user-dropdown",
                                            placeholder="Select User"
                                        )

                                    ],

                                    md=4

                                ),

                                dbc.Col(

                                    [

                                        dbc.Label(
                                            "Companies",
                                            className="fw-semibold mb-2"
                                        ),

                                        dcc.Dropdown(
                                            id="mapping-company-dropdown",
                                            multi=True,
                                            placeholder="Select Companies",
                                            optionHeight=40,
                                            maxHeight=220
                                        )
                                    ],
                                    md=5
                                ),
                                
                                dbc.Col(
                                    dbc.Button(
                                        "Assign",
                                        id="btn-assign-company",
                                        color="primary",
                                        className="w-100"
                                    ),
                                    md=3,
                                    className="d-flex align-items-end"

                                )
                            ],
                            className="g-3 mb-5"
                        )
                    ]
                ),
                className="shadow-sm border-0 rounded-4 mb-5",
                style={
                    "position": "relative",
                    "zIndex": 1000
                }
            ),

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(
                            "Mapped Companies",
                            className="fw-bold mb-1"
                        ),
                        html.P(
                            "Users and their assigned companies.",
                            className="text-muted mb-4"
                        ),
                        html.Div(
                            id="mapping-table",
                            className="table-responsive"
                        )
                    ] 
                ),
                className="shadow-sm border-0 rounded-4 mt-4",
                style={
                    "position": "relative",
                    "zIndex": 1
                }
            )
        ]
    )
    
    return admin_layout(
        title="Company Mapping",
        body=body,
        active="mapping",
        session_data=session_data
    )

    # body = html.Div(

    #     [

    #         html.Div(
    #             id="mapping-msg",
    #             className="mb-3"
    #         ),

    #         dbc.Card(

    #             dbc.CardBody(

    #                 [

    #                     html.H5(
    #                         "Assign Companies",
    #                         className="fw-bold mb-4"
    #                     ),

    #                     dbc.Row(

    #                         [

    #                             dbc.Col(

    #                                 [

    #                                     dbc.Label(
    #                                         "User",
    #                                         className="fw-semibold"
    #                                     ),

    #                                     dcc.Dropdown(
    #                                         id="mapping-user-dropdown",
    #                                         placeholder="Select User"
    #                                     )

    #                                 ],

    #                                 md=6

    #                             ),

    #                             dbc.Col(

    #                                 [

    #                                     dbc.Label(
    #                                         "Companies",
    #                                         className="fw-semibold"
    #                                     ),

    #                                     dcc.Dropdown(

    #                                         id="mapping-company-dropdown",

    #                                         multi=True,

    #                                         placeholder="Select Companies"

    #                                     )

    #                                 ],

    #                                 md=6

    #                             )

    #                         ],

    #                         className="g-3"

    #                     ),

    #                     html.Br(),

    #                     dbc.Button(

    #                         "Assign Companies",

    #                         id="btn-assign-company",

    #                         color="primary"

    #                     )

    #                 ]

    #             ),

    #             className="shadow-sm border-0 rounded-4 mb-4"

    #         ),

    #         dbc.Card(

    #             dbc.CardBody(

    #                 [

    #                     html.H5(

    #                         "Mapped Companies",

    #                         className="fw-bold mb-3"

    #                     ),

    #                     html.Div(
    #                         id="mapping-table"
    #                     )

    #                 ]

    #             ),

    #             className="shadow-sm border-0 rounded-4"

    #         )

    #     ]

    # )

    # return admin_layout(

    #     title="Company Mapping",

    #     body=body,

    #     active="mapping"

    # )






# from dash import html, dcc
# import dash_bootstrap_components as dbc

# def generate_mapping_page():

#     return html.Div([

#         html.H2("User Company Mapping", style={'marginBottom': '20px'}),

#         dbc.Card([
#             dbc.CardBody([

#                 html.Label("Select User"),
#                 dcc.Dropdown(id='mapping-user-dropdown'),

#                 html.Br(),

#                 html.Label("Select Companies"),
#                 dcc.Dropdown(id='mapping-company-dropdown', multi=True),

#                 html.Br(),

#                 dbc.Button("Assign Companies", id='btn-assign-company', color='primary'),

#                 html.Div(id='mapping-msg', style={'marginTop': '10px'})

#             ])
#         ], className="mb-4"),

#         dbc.Card([
#             dbc.CardBody([
#                 html.H5("Mappings"),
#                 html.Div(id='mapping-table')
#             ])
#         ])

#     ], style={'padding': '20px'})