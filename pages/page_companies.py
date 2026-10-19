from dash import html, dcc
import dash_bootstrap_components as dbc
from components.admin_layout import admin_layout


def generate_companies_page(session_data=None):

    body = html.Div(

        [

            html.Div(
                id="company-msg",
                className="mb-3"
            ),

            # =====================================================
            # CREATE COMPANY
            # =====================================================

            dbc.Card(

                dbc.CardBody(
                    [
                        html.H4(
                            "Create Company",
                            className="fw-bold mb-1"
                        ),
                        html.P(
                            "Register a new company in the platform.",
                            className="text-muted mb-4"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Company Name",
                                            className="fw-semibold mb-2"
                                        ),
                                        dbc.Input(
                                            id="company-name",
                                            placeholder="Enter company name"
                                        )
                                    ],
                                    lg=3
                                ),
                                dbc.Col(
                                    [
                                        dbc.Label(
                                            "Company Code",
                                            className="fw-semibold mb-2"
                                        ),
                                        dbc.Input(
                                            id="company-code",
                                            placeholder="Enter company code"
                                        )
                                    ],
                                    lg=3
                                ),
                                dbc.Col(
                                    
                                    [

                                        dbc.Label(
                                            "Status",
                                            className="fw-semibold mb-2"
                                        ),

                                        dcc.Dropdown(

                                            id="company-status",
                                            options=[
                                                {
                                                    "label": "Active",
                                                    "value": True
                                                },
                                                {
                                                    "label": "Inactive",
                                                    "value": False
                                                }
                                            ],
                                            value=True,
                                            clearable=False
                                        )
                                    ],
                                    lg=3

                                ),

                                dbc.Col(

                                    [

                                        dbc.Label(" "),

                                        dbc.Button(
                                            "Create Company",
                                            id="btn-create-company",
                                            color="primary",
                                            className="w-100"
                                        )
                                    ],
                                    lg=3,

                                    className="d-flex align-items-end"

                                )

                            ],

                            className="g-3"

                        )

                    ]

                ),

                className="shadow-sm rounded-4 border-0 mb-4",
                style={
                    "position": "relative",
                    "zIndex": 1000
                }

            ),

            # =====================================================
            # COMPANY LIST
            # =====================================================

            dbc.Card(
                dbc.CardBody(
                    [
                        html.H4(
                            "Company List",
                            className="fw-bold mb-1"
                        ),
                        html.P(
                            "Companies available in the system.",
                            className="text-muted mb-3"
                        ),
                        html.Div(
                            id="company-table",
                            className="table-responsive"
                        )
                    ]
                ),
                # className="shadow-sm rounded-4 border-0"
                className="shadow-sm rounded-4 border-0 mt-4",
                style={
                    "position": "relative",
                    "zIndex": 1
                }
            )
        ]

    )

    return admin_layout(
        title="Company Master",
        body=body,
        active="companies",
        session_data=session_data
    )






# from dash import html, dcc
# import dash_bootstrap_components as dbc
# from components.admin_layout import admin_layout


# def generate_companies_page():

#     body = html.Div(

#         [

#             html.Div(
#                 id="company-msg",
#                 className="mb-3"
#             ),

#             dbc.Card(

#                 dbc.CardBody(

#                     [

#                         html.H5(
#                             "Create Company",
#                             className="fw-bold mb-4"
#                         ),

#                         dbc.Row(

#                             [

#                                 dbc.Col(

#                                     [

#                                         dbc.Label(
#                                             "Company Name",
#                                             className="fw-semibold"
#                                         ),

#                                         dbc.Input(
#                                             id="company-name",
#                                             placeholder="Enter company name"
#                                         )

#                                     ],

#                                     md=4

#                                 ),

#                                 dbc.Col(

#                                     [

#                                         dbc.Label(
#                                             "Company Code",
#                                             className="fw-semibold"
#                                         ),

#                                         dbc.Input(
#                                             id="company-code",
#                                             placeholder="Enter company code"
#                                         )

#                                     ],

#                                     md=4

#                                 ),

#                                 dbc.Col(

#                                     [

#                                         dbc.Label(
#                                             "Status",
#                                             className="fw-semibold"
#                                         ),

#                                         dcc.Dropdown(

#                                             id="company-status",

#                                             options=[
#                                                 {
#                                                     "label": "Active",
#                                                     "value": True
#                                                 },
#                                                 {
#                                                     "label": "Inactive",
#                                                     "value": False
#                                                 }
#                                             ],

#                                             value=True,

#                                             clearable=False

#                                         )

#                                     ],

#                                     md=4

#                                 )

#                             ],

#                             className="g-3"

#                         ),

#                         html.Br(),

#                         dbc.Button(

#                             "Create Company",

#                             id="btn-create-company",

#                             color="primary"

#                         )

#                     ]

#                 ),

#                 className="shadow-sm border-0 rounded-4 mb-4"

#             ),

#             dbc.Card(

#                 dbc.CardBody(

#                     [

#                         html.H5(

#                             "Company List",

#                             className="fw-bold mb-3"

#                         ),

#                         html.Div(
#                             id="company-table"
#                         )

#                     ]

#                 ),

#                 className="shadow-sm border-0 rounded-4"

#             )

#         ]

#     )

#     return admin_layout(

#         title="Company Master",

#         body=body,

#         active="companies"

#     )





# from dash import html, dcc
# import dash_bootstrap_components as dbc
# from components.admin_layout import admin_layout


# def generate_companies_page():

#     body = html.Div([

#         dbc.Card([
#             dbc.CardBody([

#                 html.H5("Create Company"),

#                 dbc.Row([

#                     dbc.Col([
#                         html.Label("Company Name"),
#                         dcc.Input(
#                             id="company-name",
#                             className="form-control"
#                         )
#                     ], width=4),

#                     dbc.Col([
#                         html.Label("Company Code"),
#                         dcc.Input(
#                             id="company-code",
#                             className="form-control"
#                         )
#                     ], width=4),

#                     dbc.Col([
#                         html.Label("Status"),
#                         dcc.Dropdown(
#                             id="company-status",
#                             options=[
#                                 {"label": "Active", "value": True},
#                                 {"label": "Inactive", "value": False},
#                             ],
#                             value=True
#                         )
#                     ], width=4),

#                 ], className="mb-3"),

#                 dbc.Button(
#                     "Create Company",
#                     id="btn-create-company",
#                     color="primary"
#                 ),

#                 html.Div(
#                     id="company-msg",
#                     style={"marginTop": "10px"}
#                 )

#             ])
#         ], className="mb-4"),

#         dbc.Card([
#             dbc.CardBody([
#                 html.H5("Company List"),
#                 html.Div(id="company-table")
#             ])
#         ])

#     ])

#     return admin_layout(
#         title="Company Master",
#         body=body,
#         active="companies"
#     )






# from dash import html, dcc
# import dash_bootstrap_components as dbc
# from components.admin_layout import admin_layout

# def generate_companies_page():

#     return html.Div([

#         html.H2("Company Master", style={'marginBottom': '20px'}),

#         # ✅ FORM
#         dbc.Card([
#             dbc.CardBody([

#                 html.H5("Create Company"),

#                 dbc.Row([
#                     dbc.Col([
#                         html.Label("Company Name"),
#                         dcc.Input(id='company-name', className='form-control')
#                     ], width=4),

#                     dbc.Col([
#                         html.Label("Company Code"),
#                         dcc.Input(id='company-code', className='form-control')
#                     ], width=4),

#                     dbc.Col([
#                         html.Label("Status"),
#                         dcc.Dropdown(
#                             id='company-status',
#                             options=[
#                                 {"label": "Active", "value": True},
#                                 {"label": "Inactive", "value": False},
#                             ],
#                             value=True
#                         )
#                     ], width=4),
#                 ], className="mb-3"),

#                 dbc.Button("Create Company", id='btn-create-company', color='primary'),

#                 html.Div(id='company-msg', style={'marginTop': '10px'})

#             ])
#         ], className="mb-4"),

#         # ✅ TABLE
#         dbc.Card([
#             dbc.CardBody([
#                 html.H5("Company List"),
#                 html.Div(id='company-table')
#             ])
#         ])

#     ], style={'padding': '20px'})
