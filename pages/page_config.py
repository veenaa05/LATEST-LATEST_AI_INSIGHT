"""Page 2: Configuration - User selects KPIs, filters, and aggregations"""
from io import StringIO
from dash.exceptions import PreventUpdate
import pandas as pd
from dash import html, dcc, Input, Output, State, callback, ALL, ctx
from dashboard import llm_analyzer   # ✅ import global analyzer
import dash
from dash import dcc
import dash_bootstrap_components as dbc
from core.config import PRIMARY_BG, CARD_BG, TEXT, TEXT_LIGHT, BORDER, PRIMARY, SUCCESS, WARNING
from core.session_state import KPISelection, FilterSelection
import uuid

def generate_config_page(df: pd.DataFrame, profiles: dict, confirmed_dtypes: dict) -> html.Div:
    """
    Generate the configuration page layout
    User selects KPIs, filters, and aggregation types
    """

    # Handle both dict and object formats for confirmed_dtypes
    # If confirmed_dtypes is empty, use profiles
    if not confirmed_dtypes:
        confirmed_dtypes = {}
        for col, profile in profiles.items():
            if isinstance(profile, dict):
                confirmed_dtypes[col] = profile.get('dtype', 'categorical')
            else:
                confirmed_dtypes[col] = profile.dtype

    # Get numeric and categorical columns based on confirmed types
    # numeric_cols = [col for col, dtype in confirmed_dtypes.items() if dtype == 'numeric']
    # categorical_cols = [col for col, dtype in confirmed_dtypes.items() if dtype == 'categorical']
    # temporal_cols = [col for col, dtype in confirmed_dtypes.items() if dtype == 'temporal']

    numeric_cols = [col for col, dtype in confirmed_dtypes.items() if dtype == 'numeric']

    # All columns except columns explicitly marked as ignore
    kpi_cols = [
        col for col, dtype in confirmed_dtypes.items()
        if dtype != 'ignore'
    ]
    filter_cols = [
        col for col, dtype in confirmed_dtypes.items()
        if dtype != 'ignore'
    ]
    categorical_cols = [
        col for col, dtype in confirmed_dtypes.items()
        if dtype == 'categorical'
    ]
    temporal_cols = [
        col for col, dtype in confirmed_dtypes.items()
        if dtype == 'temporal'
    ]
    
    # Create layout
    layout = html.Div([
        # Header
        html.Div([
            html.H1("Configure Your Dashboard", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': TEXT}),
            html.P(
                "Select KPIs, aggregation types, and filters. You can add multiple of each.",
                style={'color': TEXT_LIGHT, 'marginBottom': '20px'}
            ),
        ], style={'marginBottom': '30px'}),

        # KPI Configuration Section
        html.Div([
            html.H3("KPI Metrics", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': TEXT, 'marginBottom': '15px'}),

            # KPI selection guide
            # html.Div(
            #     f"Select from {len(numeric_cols)} numeric column{'s' if len(numeric_cols) != 1 else ''}",
            #     style={'color': TEXT_LIGHT, 'fontSize': '12px', 'marginBottom': '10px'}
            # ),
            html.Div(
                    f"Select from {len(kpi_cols)} available column{'s' if len(numeric_cols) != 1 else ''}",
                    style={'color': TEXT_LIGHT, 'fontSize': '12px', 'marginBottom': '10px'}
            ),

            # Multi-select for KPI columns
            # dcc.Dropdown(
            #     id='kpi-column-selector',
            #     options=[{'label': col, 'value': col} for col in numeric_cols],
            #     multi=True,
            #     placeholder="Select columns to add as KPIs...",
            #     className='config-kpi-dropdown',
            #     style={'width': '100%', 'marginBottom': '20px'}
            # ),
            dcc.Dropdown(
            id='kpi-column-selector',
            options=[{'label': col, 'value': col} for col in kpi_cols],
            multi=True,
            placeholder="Select columns to add as KPIs...",
            className='config-kpi-dropdown',
            maxHeight=300,
            style={'width': '100%', 'marginBottom': '20px'}
            ),

            # Container for selected KPIs
            html.Div(id='kpi-items-container', children=[]),

            # Add KPI button (appears after selection)
            dbc.Button("+ Add Selected as KPI", id='btn-add-kpi', outline=True, color="info",
                       size="sm", style={'marginTop': '15px', 'display': 'none'}),

        ],  className='config-kpi-selection',
            style={'background': CARD_BG, 'padding': '20px', 'borderRadius': '8px', 'marginBottom': '30px',
                  'border': f'1px solid {BORDER}'}),

        # Filter Configuration Section
        html.Div([
            html.H3("Filters", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': TEXT, 'marginBottom': '15px'}),

            # Filter selection guide
            html.Div(
                f"Select from {len(filter_cols)} available column{'s' if len(filter_cols) != 1 else ''}",
                style={'color': TEXT_LIGHT, 'fontSize': '12px', 'marginBottom': '10px'}
            ),

            # Multi-select for Filter columns
            dcc.Dropdown(
                id='filter-column-selector',
                options=[{'label': col, 'value': col} for col in filter_cols],
                multi=True,
                placeholder="Select columns to add as filters...",
                className='config-filter-dropdown',
                maxHeight=300,
                style={'width': '100%', 'marginBottom': '20px'}
            ),

            # Container for selected Filters
            html.Div(id='filter-items-container', children=[]),

            # Add Filter button (appears after selection)
            dbc.Button("+ Add Selected as Filter", id='btn-add-filter', outline=True, color="info",
                       size="sm", style={'marginTop': '15px', 'display': 'none'}),

        ],  className='config-filter-selection',
            style={'background': CARD_BG, 'padding': '20px', 'borderRadius': '8px', 'marginBottom': '30px',
                  'border': f'1px solid {BORDER}'}),

        # LLM Analysis Section
        html.Div([
            html.Div([
                html.H3("AI Suggestions", style={'fontSize': '18px', 'fontWeight': 'bold', 'color': TEXT}),
                dbc.Button("Get AI Suggestions", id='btn-analyze-ai', color="success", size="sm"),
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center', 'marginBottom': '15px'}),

            html.Div(
                "Get AI-powered recommendations for additional charts and analysis",
                style={'color': TEXT_LIGHT, 'fontSize': '12px', 'marginBottom': '15px'}
            ),

            # Objective input
            html.Div([
                html.Div("ANALYSIS OBJECTIVE", style={
                    'fontSize': '10px', 'fontWeight': '700', 'letterSpacing': '0.08em',
                    'color': '#2B6CB0', 'marginBottom': '6px',
                }),
                dcc.Textarea(
                    id='objective-input',
                    placeholder='e.g. Check monthly trend of expense and performance of the posters...',
                    maxLength=500,
                    rows=3,
                    style={
                        'width': '100%', 'padding': '8px 12px', 'fontSize': '13px',
                        'borderRadius': '6px', 'border': f'1px solid {BORDER}',
                        'resize': 'vertical', 'fontFamily': 'inherit',
                        'backgroundColor': '#F8FBFF',
                    }
                ),
                html.Div(
                    "Optional — steers AI chart and KPI recommendations toward your goal (max 500 chars)",
                    style={'fontSize': '11px', 'color': TEXT_LIGHT, 'marginTop': '4px'}
                ),
            ], style={
                'backgroundColor': '#EBF4FF', 'border': '1px solid #90CDF4',
                'borderLeft': '4px solid #2B6CB0', 'borderRadius': '6px',
                'padding': '12px 16px', 'marginBottom': '16px',
            }),

            # AI Analysis Results (no Loading wrapper — avoids double-spinner with page-level loader)
            # html.Div(id='ai-analysis-results', children=[], style={'marginTop': '15px'}),
            dcc.Loading(
                id="loading-ai-analysis",
                type="circle",
                children=[
                    html.Div(
                        id="ai-analysis-results",
                        children=[],
                        style={
                            'background': CARD_BG,
                            'padding': '20px'
                        }
                    )
                ]
            )

        ], style={'background': CARD_BG, 'padding': '20px', 'borderRadius': '8px', 'marginBottom': '30px',
                  'border': f'1px solid {BORDER}'}),

        # Hidden stores (note: store-kpi-selections and store-filter-selections are defined in main app.layout)
        dcc.Store(id='store-confirmed-dtypes-from-review', data=confirmed_dtypes),

        # Navigation Buttons
        html.Div([
            dcc.Link(
                dbc.Button("← Back to Data Review", outline=True, color="secondary",
                           style={'padding': '10px 20px', 'fontSize': '14px'}),
                href='/data-review',
                style={'textDecoration': 'none'}
            ),
            dcc.Link(
                dbc.Button("Generate Dashboard →", color="primary",
                           style={'padding': '10px 20px', 'fontSize': '14px'}),
                href='/dashboard',
                style={'textDecoration': 'none'}
            ),
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'marginTop': '30px'}),

    ], style={'padding': '30px', 'maxWidth': '1200px', 'margin': '0 auto', 'background': PRIMARY_BG, 'minHeight': '100vh'})

    return layout


def create_kpi_item(kpi_id: str, column: str, aggregation: str = 'sum', label: str = None, z_index: int = 1, dtype: str = 'numeric') -> html.Div:
    """Create a KPI configuration card"""
    if dtype == 'numeric':
        aggregation_options = [
            {'label': 'Sum', 'value': 'sum'},
            {'label': 'Average', 'value': 'mean'},
            {'label': 'Count', 'value': 'count'},
            {'label': 'Max', 'value': 'max'},
            {'label': 'Min', 'value': 'min'},
        ]
    else:
        aggregation_options = [
            {'label': 'Count', 'value': 'count'}
        ]
        aggregation = 'count'

    if label is None:
        label = f"{aggregation.capitalize()} of {column}"
        
    return html.Div([
        html.Div([
            html.Div([
                html.Div("Column:", style={'fontWeight': 'bold', 'fontSize': '12px', 'color': TEXT_LIGHT}),
                html.Div(column, style={'fontSize': '14px', 'color': TEXT}),
            ], style={'flex': '1'}),

            html.Div([
                html.Div("Aggregation:", style={'fontWeight': 'bold', 'fontSize': '12px', 'color': TEXT_LIGHT}),
                dcc.Dropdown(
                    id={'type': 'kpi-aggregation', 'index': kpi_id},
                    # options=[
                    #     {'label': 'Sum', 'value': 'sum'},
                    #     {'label': 'Average', 'value': 'mean'},
                    #     {'label': 'Count', 'value': 'count'},
                    #     {'label': 'Max', 'value': 'max'},
                    #     {'label': 'Min', 'value': 'min'},
                    # ],
                    options=aggregation_options,
                    value=aggregation,
                    clearable=False,
                    maxHeight=300,
                    style={'width': '100%'}
                ),
            ], style={'flex': '1', 'marginLeft': '15px'}),

            html.Div([
                html.Div("Label:", style={'fontWeight': 'bold', 'fontSize': '12px', 'color': TEXT_LIGHT}),
                dcc.Input(
                    id={'type': 'kpi-label', 'index': kpi_id},
                    type='text',
                    value=label,
                    placeholder='e.g., Total Revenue',
                    style={'width': '100%', 'padding': '8px', 'borderRadius': '4px',
                        'border': f'1px solid {BORDER}'}
                ),
            ], style={'flex': '1', 'marginLeft': '15px'}),

            dbc.Button("Remove", id={'type': 'kpi-remove', 'index': kpi_id}, outline=True,
                    color="danger", size="sm", style={'marginTop': '18px', 'marginLeft': '15px'}),
        ], style={'display': 'flex', 'gap': '10px', 'alignItems': 'flex-start'}),
    ], 
        id=f'kpi-{kpi_id}',   # ✅ FIXED (moved here)           
        style={'background': '#F9FAFB', 'padding': '15px', 'borderRadius': '6px', 'marginBottom': '10px',
            'border': f'1px solid {BORDER}', 'position': 'relative', 'zIndex': z_index}
    )


def create_filter_item(filter_id: str, column: str, filter_type: str = 'dropdown', label: str = None, dtype: str = 'categorical') -> html.Div:
    """Create a filter configuration card"""

    if dtype == 'numeric':
            filter_options = [
                {'label': 'Numeric Range', 'value': 'numeric_range'}
            ]
            filter_type = 'numeric_range'

    elif dtype == 'temporal':
            filter_options = [
                {'label': 'Date Range', 'value': 'date_range'}
            ]
            filter_type = 'date_range'

    else:
            # categorical / alphanumeric / text
            filter_options = [
                {'label': 'Dropdown', 'value': 'dropdown'}
            ]
            filter_type = 'dropdown'

    if label is None:
            label = column

    return html.Div([
        html.Div([
            html.Div([
                html.Div("Column:", style={'fontWeight': 'bold', 'fontSize': '12px', 'color': TEXT_LIGHT}),
                html.Div(column, style={'fontSize': '14px', 'color': TEXT}),
            ], style={'flex': '1'}),

            html.Div([
                html.Div("Type:", style={'fontWeight': 'bold', 'fontSize': '12px', 'color': TEXT_LIGHT}),
                dcc.Dropdown(
                    id={'type': 'filter-type', 'index': filter_id},
                    options=filter_options,
                    value=filter_type,
                    clearable=False,
                    style={'width': '100%'}
                ),
            ], style={'flex': '1', 'marginLeft': '15px'}),

            html.Div([
                html.Div("Label:", style={'fontWeight': 'bold', 'fontSize': '12px', 'color': TEXT_LIGHT}),
                dcc.Input(
                    id={'type': 'filter-label', 'index': filter_id},
                    type='text',
                    value=label,
                    placeholder='e.g., Select Status',
                    style={'width': '100%', 'padding': '8px', 'borderRadius': '4px',
                        'border': f'1px solid {BORDER}'}
                ),
            ], style={'flex': '1', 'marginLeft': '15px'}),

            dbc.Button("Remove", id={'type': 'filter-remove', 'index': filter_id}, outline=True,
                    color="danger", size="sm", style={'marginTop': '18px', 'marginLeft': '15px'}),
        ], style={'display': 'flex', 'gap': '10px', 'alignItems': 'flex-start'}),
    ],
        id=f'filter-{filter_id}',   # ✅ FIXED (moved here)            
        style={'background': '#F9FAFB', 'padding': '15px', 'borderRadius': '6px', 'marginBottom': '10px',
            'border': f'1px solid {BORDER}'}
    )
    

# Callback to handle Filter selection and rendering

@callback(
    [
        Output('kpi-items-container', 'children'),
        Output('btn-add-kpi', 'style'),
        Output('store-kpi-selections', 'data')
    ],
    [   
        Input('kpi-column-selector', 'value'),
        Input('btn-add-kpi', 'n_clicks'),
        Input({'type': 'kpi-remove', 'index': ALL}, 'n_clicks'),
        Input({'type': 'kpi-aggregation', 'index': ALL}, 'value'),
        Input({'type': 'kpi-label', 'index': ALL}, 'value')
    ],
    [
        State('store-kpi-selections', 'data'),
        State('store-confirmed-dtypes-from-review', 'data')
    ],
    prevent_initial_call=True
)
def update_kpi_items(
    selected_columns,
    add_clicks,
    remove_clicks,
    agg_values,
    label_values,
    stored_kpis,
    confirmed_dtypes
):
    """Add, remove and update KPI configurations."""

    stored_kpis = stored_kpis or []
    selected_columns = selected_columns or []
    confirmed_dtypes = confirmed_dtypes or {}

    triggered = ctx.triggered_id

    # --------------------------------------------------
    # ADD SELECTED KPIs
    # --------------------------------------------------
    if triggered == 'btn-add-kpi':

        existing_columns = {
            item.get('column')
            for item in stored_kpis
        }
        for col in selected_columns:
            if col not in existing_columns:

                dtype = confirmed_dtypes.get(col, 'categorical')

                if dtype == 'numeric':
                    aggregation = 'sum'
                    label = f'Sum of {col}'
                else:
                    aggregation = 'count'
                    label = f'Count of {col}'

                stored_kpis.append({
                    'column': col,
                    'aggregation': aggregation,
                    'label': label
                })
        # for col in selected_columns:
        #     if col not in existing_columns:
        #         stored_kpis.append({
        #             'column': col,
        #             'aggregation': 'sum',
        #             'label': f'Sum of {col}'
        #         })

    # --------------------------------------------------
    # REMOVE KPI
    # --------------------------------------------------
    elif isinstance(triggered, dict) and triggered.get('type') == 'kpi-remove':

        remove_id = triggered.get('index')

        stored_kpis = [
            item for item in stored_kpis
            if item.get('column', '').replace(' ', '_') != remove_id
        ]

    # --------------------------------------------------
    # UPDATE AGGREGATION / LABEL
    # --------------------------------------------------
    elif isinstance(triggered, dict) and triggered.get('type') in (
        'kpi-aggregation',
        'kpi-label'
    ):

        for i, item in enumerate(stored_kpis):

            if i < len(agg_values or []):
                item['aggregation'] = agg_values[i]

            if i < len(label_values or []):
                item['label'] = label_values[i]

    # --------------------------------------------------
    # BUILD KPI CARDS
    # --------------------------------------------------
    kpi_items = []

    for i, item in enumerate(stored_kpis):

        column = item.get('column')
        dtype = confirmed_dtypes.get(column, 'categorical')

        aggregation = item.get('aggregation', 'sum')
        label = item.get('label')

        if dtype != 'numeric':
            aggregation = 'count'

            if not label or label.startswith('Sum of'):
                label = f'Count of {column}'

        kpi_id = column.replace(' ', '_')
        kpi_items.append(
            create_kpi_item(
                kpi_id,
                column,
                aggregation,
                label,
                z_index=1000 - i,
                dtype=dtype
            )
        )

    # --------------------------------------------------
    # ADD BUTTON VISIBILITY
    # --------------------------------------------------
    already_added = {
        item.get('column')
        for item in stored_kpis
    }

    available_to_add = [
        col for col in selected_columns
        if col not in already_added
    ]

    btn_style = {
        'marginTop': '15px',
        'display': 'block' if available_to_add else 'none'
    }

    return kpi_items, btn_style, stored_kpis

# @callback(
#     [Output('kpi-items-container', 'children'),
#     Output('btn-add-kpi', 'style'),
#     Output('store-kpi-selections', 'data')],
#     [Input('kpi-column-selector', 'value'),
#     Input({'type': 'kpi-remove', 'index': ALL}, 'n_clicks'),
#     Input({'type': 'kpi-aggregation', 'index': ALL}, 'value'),
#     Input({'type': 'kpi-label', 'index': ALL}, 'value')],
#     [State('store-kpi-selections', 'data')],
#     allow_duplicate=True
# )
# def update_kpi_items(selected_columns, remove_clicks, agg_values, label_values, stored_kpis):
#     """Update KPI items when columns are selected or aggregations/labels change"""
#     if not selected_columns:
#         selected_columns = []

#     # Create cards for each selected column
#     kpi_items = []
#     kpi_list = []

#     for i, col in enumerate(selected_columns):
#         kpi_id = col.replace(' ', '_')

#         # Get aggregation and label from inputs if available, otherwise use defaults
#         agg = agg_values[i] if agg_values and i < len(agg_values) else 'sum'
#         label = label_values[i] if label_values and i < len(label_values) else f"Sum of {col}"

#         kpi_item = create_kpi_item(kpi_id, col, agg, label)
#         kpi_items.append(kpi_item)
#         kpi_list.append({'column': col, 'aggregation': agg, 'label': label})

#     # Hide button if no selections
#     btn_style = {'marginTop': '15px', 'display': 'block' if selected_columns else 'none'}

#     return kpi_items, btn_style, kpi_list

#Updated callback for filter items to handle add, remove, and update actions

@callback(
    [
        Output('filter-items-container', 'children'),
        Output('btn-add-filter', 'style'),
        Output('store-filter-selections', 'data')
    ],
    [
        Input('filter-column-selector', 'value'),
        Input('btn-add-filter', 'n_clicks'),
        Input({'type': 'filter-remove', 'index': ALL}, 'n_clicks'),
        Input({'type': 'filter-type', 'index': ALL}, 'value'),
        Input({'type': 'filter-label', 'index': ALL}, 'value')
    ],
    [
        State('store-filter-selections', 'data'),
        State('store-confirmed-dtypes-from-review', 'data')
    ],
    prevent_initial_call=True
)
def update_filter_items(
    selected_columns,
    add_clicks,
    remove_clicks,
    type_values,
    label_values,
    stored_filters,
    confirmed_dtypes
):
    """Add, remove and update filter configurations."""

    stored_filters = stored_filters or []
    selected_columns = selected_columns or []
    confirmed_dtypes = confirmed_dtypes or {}

    triggered = ctx.triggered_id

    # --------------------------------------------------
    # ADD SELECTED FILTERS
    # --------------------------------------------------
    if triggered == 'btn-add-filter':

        existing_columns = {
            item.get('column')
            for item in stored_filters
        }

        for col in selected_columns:

            if col not in existing_columns:
                stored_filters.append({
                    'column': col,
                    'filter_type': 'dropdown',
                    'label': col
                })

    # --------------------------------------------------
    # REMOVE FILTER
    # --------------------------------------------------
    elif isinstance(triggered, dict) and triggered.get('type') == 'filter-remove':

        remove_id = triggered.get('index')

        stored_filters = [
            item for item in stored_filters
            if item.get('column', '').replace(' ', '_') != remove_id
        ]

    # --------------------------------------------------
    # UPDATE FILTER TYPE / LABEL
    # --------------------------------------------------
    elif isinstance(triggered, dict) and triggered.get('type') in (
        'filter-type',
        'filter-label'
    ):

        for i, item in enumerate(stored_filters):

            if i < len(type_values or []):
                item['filter_type'] = type_values[i]

            if i < len(label_values or []):
                item['label'] = label_values[i]

    # --------------------------------------------------
    # BUILD FILTER CARDS
    # --------------------------------------------------
    filter_items = []

    for item in stored_filters:

        column = item.get("column", '')
        filter_type = item.get("filter_type", "dropdown")
        label = item.get('label', column)

        filter_id = column.replace(' ', '_')

        filter_items.append(
            create_filter_item(
                filter_id,
                column,
                filter_type,
                label,
                dtype=confirmed_dtypes.get(column, 'categorical')
            )
        )

    # --------------------------------------------------
    # ADD BUTTON VISIBILITY
    # --------------------------------------------------
    already_added = {
        item.get('column')
        for item in stored_filters
    }

    available_to_add = [
        col for col in selected_columns
        if col not in already_added
    ]

    btn_style = {
        'marginTop': '15px',
        'display': 'block' if available_to_add else 'none'
    }

    return filter_items, btn_style, stored_filters


# @callback(
#     [Output('filter-items-container', 'children'),
#      Output('btn-add-filter', 'style'),
#      Output('store-filter-selections', 'data')],
#     [Input('filter-column-selector', 'value'),
#      Input({'type': 'filter-remove', 'index': ALL}, 'n_clicks'),
#      Input({'type': 'filter-type', 'index': ALL}, 'value'),
#      Input({'type': 'filter-label', 'index': ALL}, 'value')],
#     [State('store-filter-selections', 'data')],
#     allow_duplicate=True
# )
# def update_filter_items(selected_columns, remove_clicks, type_values, label_values, stored_filters):
#     """Update filter items when columns are selected or filter types/labels change"""
#     if not selected_columns:
#         selected_columns = []

#     # Create cards for each selected column
#     filter_items = []
#     filter_list = []

#     for i, col in enumerate(selected_columns):
#         filter_id = col.replace(' ', '_')

#         # Get filter type and label from inputs if available, otherwise use defaults
#         f_type = type_values[i] if type_values and i < len(type_values) else 'dropdown'
#         label = label_values[i] if label_values and i < len(label_values) else col

#         filter_item = create_filter_item(filter_id, col, f_type, label)
#         filter_items.append(filter_item)
#         filter_list.append({'column': col, 'filter_type': f_type, 'label': label})

#     # Hide button if no selections
#     btn_style = {'marginTop': '15px', 'display': 'block' if selected_columns else 'none'}

#     return filter_items, btn_style, filter_list


@callback(
    Output('store-objective', 'data'),
    Input('objective-input', 'value'),
    prevent_initial_call=True
)
def sync_objective(value):
    return (value or '').strip()

print("PAGE_CONFIG LOADED")
@callback(
    Output('ai-analysis-results', 'children'),
    Output('store-ai-suggestions', 'data'),
    Input('btn-analyze-ai', 'n_clicks'),
    State('store-global-dataframe', 'data'),
    State('store-global-profiles', 'data'),
    State('store-objective', 'data'),
    prevent_initial_call=True
)

def run_ai_analysis(n_clicks, df_json, profiles, objective):
    if not n_clicks:
        print("SKIPPING INITIAL LOAD")
        raise PreventUpdate
    
    import time
    print("=" * 80)
    print("AI CALLBACK FIRED")
    print("N_CLICKS:", n_clicks)
    print("TIME:", time.time())
    print("=" *80)
    
    print("STEP 1- CALLBACK STARTED")
    if not df_json:
        print("STEP 2- NO DF JSON")
        return dbc.Alert("No data available", color="warning"), None
    print("DF_JSON IS NONE:", df_json is None)
    print("DF_JSON LENGTH:", len(df_json) if df_json else 0)
    print("STEP 3- BEFORE READ_JSON")   
    try:
        print("DF_JSON TYPE:", type(df_json))
        print("DF_JSON PREVIEW:", str(df_json)[:200])  # Print the first 200 chars to avoid overload
        
        # df = pd.read_json(df_json, orient='split')
        from io import StringIO
        df = pd.read_json(StringIO(df_json), orient='split')
        print("STEP 4- AFTER READ_JSON")
        print(df.shape)
        # ============================================================
        # STEP 5 - BUILD DATA-DRIVEN DATASET SUMMARY
        # ============================================================

        summary = {
            "row_count": int(len(df)),
            "column_count": int(len(df.columns)),
            "columns": list(df.columns),
            "column_details": {}
        }

        # Use the profiler / confirmed data types as the source of truth.
        # This avoids mistakes such as Invoice Date being interpreted
        # as numeric by pandas.

        for col in df.columns:

            # Get profile information if available
            profile = profiles.get(col, {}) if isinstance(profiles, dict) else {}

            if isinstance(profile, dict):
                dtype = profile.get("dtype", "categorical")
            else:
                dtype = getattr(profile, "dtype", "categorical")

            series = df[col]

            # Basic information for every column
            col_info = {
                "dtype": dtype,
                "missing_count": int(series.isna().sum()),
                "missing_pct": round(float(series.isna().mean() * 100), 2),
                "unique_count": int(series.nunique(dropna=True)),
            }

            # --------------------------------------------------------
            # NUMERIC COLUMN
            # --------------------------------------------------------
            if dtype == "numeric":

                numeric_series = pd.to_numeric(series, errors="coerce").dropna()

                if len(numeric_series) > 0:

                    col_info.update({
                        "min": float(numeric_series.min()),
                        "max": float(numeric_series.max()),
                        "mean": round(float(numeric_series.mean()), 2),
                        "median": float(numeric_series.median()),
                        "sum": float(numeric_series.sum()),
                        "zero_pct": round(
                            float((numeric_series == 0).mean() * 100), 2
                        ),
                        "negative_pct": round(
                            float((numeric_series < 0).mean() * 100), 2
                        )
                    })

            # --------------------------------------------------------
            # TEMPORAL COLUMN
            # --------------------------------------------------------
            elif dtype == "temporal":

                date_series = pd.to_datetime(
                    series,
                    errors="coerce"
                ).dropna()

                if len(date_series) > 0:

                    col_info.update({
                        "min_date": str(date_series.min().date()),
                        "max_date": str(date_series.max().date()),
                        "date_span_days": int(
                            (date_series.max() - date_series.min()).days
                        )
                    })

            # --------------------------------------------------------
            # CATEGORICAL COLUMN
            # --------------------------------------------------------
            elif dtype == "categorical":

                # Avoid sending thousands of category values to the LLM.
                # Only send the top 5.
                top_values = (
                    series
                    .dropna()
                    .astype(str)
                    .value_counts()
                    .head(5)
                )

                col_info["top_values"] = [
                    {
                        "value": str(value),
                        "count": int(count),
                        "percentage": round(
                            float(count / len(series.dropna()) * 100), 2
                        )
                    }
                    for value, count in top_values.items()
                ]

            summary["column_details"][col] = col_info


        print("STEP 5 - DATASET SUMMARY CREATED")
        print("ROWS:", summary["row_count"])
        print("COLUMNS:", summary["column_count"])

        for col, info in summary["column_details"].items():
            print(
                f"{col} -> "
                f"dtype={info.get('dtype')}, "
                f"missing={info.get('missing_pct')}%, "
                f"unique={info.get('unique_count')}"
            )
        # # Build a compact summary from the complete uploaded dataset.
        # # The full dataframe is NOT sent to the LLM.
        # # This allows AI suggestions to be based on the actual dataset
        # # while keeping the LLM request small.
        # summary = {
        #     "row_count": len(df),
        #     "column_count": len(df.columns),
        #     "columns": list(df.columns),
        #     "numeric_columns": df.select_dtypes(include="number").columns.tolist(),
        #     "categorical_columns": df.select_dtypes(include=["object", "string"]).columns.tolist(),
        #     "datetime_columns": df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist(),
        # }
        # # # ✅ LIMIT DATA (CRITICAL)
        # # df_sample = df.head(50)
        # # summary = {
        # #     "columns": list(df.columns),
        # #     "row_count": len(df),
        # #     "numeric_columns": df.select_dtypes(include='number').columns.tolist(),
        # #     "categorical_columns": df.select_dtypes(include='object').columns.tolist()
        # # }
        # print("STEP 5 - DATASET SUMMARY CREATED")
        # print(summary)
        
        if llm_analyzer:
            print("STEP 6 - BEFORE ANALYZE")
            result = llm_analyzer.analyze(df, profiles, objective or "", dataset_summary=summary)
            print("STEP 7 - AFTER ANALYZE")
            print(type(result))
            print(result)
            
            if result is None:
                print("LLM ANALYZER RETURNED NONE")
                print("STOPPING BEFORE to_dict()")
                
                return(
                    dbc.Alert(
                        "AI analysis failed. Please try again or check the logs for details.",
                        color="danger"
                    ),
                    {}
                )
            
            print("RESULT DIR")
            print(dir(result))
            
            # print("TO DICT")
            # print(result.to_dict())
            
            # ============================================================
            # STEP 7 - BUILD STRUCTURED AI SUGGESTIONS UI
            # ============================================================

            print("STEP 7 - BUILDING STRUCTURED AI SUGGESTIONS UI")
            ai_analysis = getattr(result, "ai_analysis", {}) or {}
            store_data = result.to_dict()
            
            # print("=" * 80)
            # print("STORE DATA DETAILED TYPE CHECK")

            # if isinstance(store_data, dict):
            #     for key, value in store_data.items():
            #         print(
            #             f"STORE [{key}] -> "
            #             f"type={type(value)}, "
            #             f"value={str(value)[:300]}"
            #         )

            print("=" * 80)
            print("AI ANALYSIS AVAILABLE:", bool(ai_analysis))
            print("AI ANALYSIS TYPE:", type(ai_analysis))
            if isinstance(ai_analysis, dict):
                print("AI ANALYSIS KEYS:", list(ai_analysis.keys()))
            print("STORE DATA TYPE:", type(store_data))
            
            if isinstance(store_data, dict):
                print("STORE DATA KEYS:", list(store_data.keys()))

                # --------------------------------------------------------
                # Helper function for bullet lists
                # --------------------------------------------------------
                def make_bullet_list(items):
                    if not items:
                        return html.Div(
                            "No information available.",
                            style={"color": "#718096"}
                        )

                    return html.Ul(
                        [
                            html.Li(
                                str(item),
                                style={
                                    "marginBottom": "8px",
                                    "lineHeight": "1.5"
                                }
                            )
                            for item in items
                        ],
                        style={
                            "paddingLeft": "20px",
                            "marginBottom": "0"
                        }
                    )

                # --------------------------------------------------------
                # EXECUTIVE SUMMARY
                # --------------------------------------------------------
                executive_summary = ai_analysis.get(
                    "executive_summary", {}
                ) or {}

                key_findings = executive_summary.get(
                    "key_findings", []
                )

                # --------------------------------------------------------
                # DATA QUALITY
                # --------------------------------------------------------
                data_quality = ai_analysis.get(
                    "data_quality", {}
                ) or {}

                # --------------------------------------------------------
                # INSIGHTS
                # --------------------------------------------------------
                insights = ai_analysis.get(
                    "insights", []
                )

                # --------------------------------------------------------
                # RECOMMENDATIONS
                # --------------------------------------------------------
                recommendations = ai_analysis.get(
                    "recommendations", []
                )

                # --------------------------------------------------------
                # FILTERS
                # --------------------------------------------------------
                filters = ai_analysis.get(
                    "filters", []
                )

                # --------------------------------------------------------
                # KPIs
                # --------------------------------------------------------
                kpis = ai_analysis.get(
                    "kpis", []
                )

                # --------------------------------------------------------
                # CHARTS
                # --------------------------------------------------------
                charts = ai_analysis.get(
                    "charts", []
                )

                # ========================================================
                # BUILD FILTER CARDS
                # ========================================================
                filter_components = []

                for item in filters:
                    if isinstance(item, dict):
                        column = str(item.get("column", "") or "")
                        label = str(item.get("label", column) or column)

                        filter_components.append(
                            dbc.Badge(
                                label,
                                color="light",
                                text_color="dark",
                                className="me-2 mb-2",
                                style={
                                    "border": "1px solid #CBD5E0",
                                    "padding": "8px 12px",
                                    "fontSize": "13px"
                                }
                            )
                        )


                # ========================================================
                # BUILD KPI CARDS
                # ========================================================
                kpi_components = []

                for item in kpis:
                    if isinstance(item, dict):
                        metric = str(item.get("metric", "") or "")
                        label = str(item.get("label", metric) or metric)
                        aggregation = str(item.get("aggregation", "") or "")

                        kpi_components.append(
                            dbc.Card(
                                dbc.CardBody([
                                    html.Div(
                                        label,
                                        style={
                                            "fontWeight": "600",
                                            "fontSize": "14px",
                                            "color": "#2D3748"
                                        }
                                    ),
                                    html.Div(
                                        f"{metric} ({aggregation})",
                                        style={
                                            "fontSize": "12px",
                                            "color": "#718096",
                                            "marginTop": "4px"
                                        }
                                    )
                                ]),
                                style={
                                    "marginBottom": "8px",
                                    "border": "1px solid #E2E8F0"
                                }
                            )
                        )

                # ========================================================
                # BUILD CHART RECOMMENDATIONS
                # ========================================================
                chart_components = []

                for item in charts:
                    if isinstance(item, dict):

                        chart_type = item.get("type", "")
                        x_column = item.get("x", "")
                        y_column = item.get("y")
                        title = item.get("title", "")

                        chart_text = title

                        if x_column:
                            chart_text += f" | Dimension: {x_column}"

                        if y_column:
                            chart_text += f" | Measure: {y_column}"

                        if chart_type:
                            chart_text += f" | Type: {chart_type}"

                        chart_components.append(
                            dbc.Card(
                                dbc.CardBody(
                                    html.Div(
                                        chart_text,
                                        style={
                                            "fontSize": "13px",
                                            "lineHeight": "1.5"
                                        }
                                    )
                                ),
                                style={
                                    "marginBottom": "8px",
                                    "border": "1px solid #E2E8F0"
                                }
                            )
                        )

                # ========================================================
                # FINAL AI SUGGESTIONS UI
                # ========================================================
                print("=" * 80)
                print("AI UI DATA TYPE CHECK")
                print("key_findings:", type(key_findings), key_findings)
                print("data_quality:", type(data_quality), data_quality)
                print("insights:", type(insights), insights)
                print("recommendations:", type(recommendations), recommendations)
                print("filters:", type(filters), filters)
                print("kpis:", type(kpis), kpis)
                print("charts:", type(charts), charts)
                print("=" * 80)
                # ----------------------------------------------------
                 # DEBUG STATEMENTS FOR DETAILED TYPE CHECKING
                # ----------------------------------------------------
                
                print("=" * 80)
                print("DETAILED AI UI TYPE CHECK")

                def debug_types(name, value):
                    print(f"{name}: type={type(value)}")

                    if isinstance(value, list):
                        for i, item in enumerate(value):
                            print(f"  {name}[{i}]: type={type(item)}")
                            if isinstance(item, dict):
                                for k, v in item.items():
                                    print(f"      {k}: type={type(v)}, value={str(v)[:150]}")

                    elif isinstance(value, dict):
                        for k, v in value.items():
                            print(f"  {name}.{k}: type={type(v)}, value={str(v)[:150]}")


                debug_types("key_findings", key_findings)
                debug_types("data_quality", data_quality)
                debug_types("insights", insights)
                debug_types("recommendations", recommendations)
                debug_types("filters", filters)
                debug_types("kpis", kpis)
                debug_types("charts", charts)
                print("=" * 80)
                ai_ui = html.Div([

                    # ----------------------------------------------------
                    # TITLE
                    # ----------------------------------------------------
                    html.H5(
                        "AI Suggestions",
                        style={
                            "fontWeight": "700",
                            "marginBottom": "15px",
                            "color": "#1A365D"
                        }
                    ),

                    # ----------------------------------------------------
                    # EXECUTIVE SUMMARY
                    # ----------------------------------------------------
                    html.Div([
                        html.H6(
                            "Executive Summary",
                            style={
                                "fontWeight": "700",
                                "color": "#2D3748",
                                "marginBottom": "10px"
                            }
                        ),

                        make_bullet_list(key_findings)

                    ], style={
                        "background": "#F7FAFC",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "marginBottom": "15px"
                    }),

                    # ----------------------------------------------------
                    # DATA QUALITY
                    # ----------------------------------------------------
                    html.Div([
                        html.H6(
                            "Data Quality",
                            style={
                                "fontWeight": "700",
                                "color": "#2D3748",
                                "marginBottom": "10px"
                            }
                        ),

                        html.Div([
                            html.Strong("Health: "),
                            str(
                                executive_summary.get(
                                    "overall_health",
                                    "Not available"
                                )
                            )
                        ]),

                        html.Div([
                            html.Strong("Reliability: "),
                            str(
                                executive_summary.get(
                                    "reliability",
                                    "Not available"
                                )
                            ),
                            html.Br(),

                            html.Strong("Data Completeness: "),
                            str(
                                data_quality.get(
                                    "data_completeness",
                                    "Not available"
                                )
                            )
                        ]),

                        html.Div(
                            str(
                                data_quality.get(
                                    "recommendation",
                                    ""
                                )
                            ),
                            style={
                                "marginTop": "8px",
                                "color": "#4A5568"
                            }
                        )

                    ], style={
                        "background": "#FFFFFF",
                        "border": "1px solid #E2E8F0",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "marginBottom": "15px"
                    }),

                    # ----------------------------------------------------
                    # KEY INSIGHTS
                    # ----------------------------------------------------
                    html.Div([
                        html.H6(
                            "Key Insights",
                            style={
                                "fontWeight": "700",
                                "color": "#2D3748",
                                "marginBottom": "10px"
                            }
                        ),

                        make_bullet_list(insights)

                    ], style={
                        "background": "#FFFFFF",
                        "border": "1px solid #E2E8F0",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "marginBottom": "15px"
                    }),

                    # ----------------------------------------------------
                    # RECOMMENDATIONS
                    # ----------------------------------------------------
                    html.Div([
                        html.H6(
                            "Recommendations",
                            style={
                                "fontWeight": "700",
                                "color": "#2D3748",
                                "marginBottom": "10px"
                            }
                        ),

                        make_bullet_list(recommendations)

                    ], style={
                        "background": "#FFFFFF",
                        "border": "1px solid #E2E8F0",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "marginBottom": "15px"
                    }),

                    # ----------------------------------------------------
                    # RECOMMENDED FILTERS
                    # ----------------------------------------------------
                    html.Div([
                        html.H6(
                            "Recommended Filters",
                            style={
                                "fontWeight": "700",
                                "color": "#2D3748",
                                "marginBottom": "10px"
                            }
                        ),

                        html.Div(
                            filter_components
                            if filter_components
                            else html.Div(
                                "No filters recommended.",
                                style={"color": "#718096"}
                            )
                        )

                    ], style={
                        "background": "#FFFFFF",
                        "border": "1px solid #E2E8F0",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "marginBottom": "15px"
                    }),

                    # ----------------------------------------------------
                    # RECOMMENDED KPIs
                    # ----------------------------------------------------
                    html.Div([
                        html.H6(
                            "Recommended KPIs",
                            style={
                                "fontWeight": "700",
                                "color": "#2D3748",
                                "marginBottom": "10px"
                            }
                        ),

                        html.Div(
                            kpi_components
                            if kpi_components
                            else [
                                html.Div(
                                    "No KPIs recommended.",
                                    style={"color": "#718096"}
                                )
                            ]
                        )

                    ], style={
                        "background": "#FFFFFF",
                        "border": "1px solid #E2E8F0",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "marginBottom": "15px"
                    }),

                    # ----------------------------------------------------
                    # RECOMMENDED CHARTS
                    # ----------------------------------------------------
                    html.Div([
                        html.H6(
                            "Recommended Charts",
                            style={
                                "fontWeight": "700",
                                "color": "#2D3748",
                                "marginBottom": "10px"
                            }
                        ),

                        html.Div(
                            chart_components
                            if chart_components
                            else [
                                html.Div(
                                    "No charts recommended.",
                                    style={"color": "#718096"}
                                )
                            ]
                        )

                    ], style={
                        "background": "#FFFFFF",
                        "border": "1px solid #E2E8F0",
                        "padding": "15px",
                        "borderRadius": "8px",
                        "marginBottom": "15px"
                    })
                ])

                print("STEP 8 - STRUCTURED AI UI CREATED")

                return (
                    ai_ui,
                    store_data
                )

            else:
                print("STEP 7 - NO AI RESULT")

                return (
                    dbc.Alert(
                        "No suggestions generated",
                        color="warning"
                    ),
                    {}
                )
                        
            # print("RETURNING TO STORE:")
            # print(type(result.reasoning if result else " "))
            # print(result.reasoning if result else " ")
            
            # print("RETURN TYPE:", type(result.to_dict()))
            # print("STORE DATA", result.to_dict())
            
            # return( html.Div([
            #         html.H5("AI Suggestions"),
            #         html.Div(result.reasoning if result else "No suggestions generated", 
            #             style={
            #             'whiteSpace': 'pre-wrap',
            #             'background': '#F7FAFC',
            #             'padding': '10px',
            #             'borderRadius': '6px'
            #         })
            #     ]), 
            #         result.to_dict() if result else {}
            # )           
        else:
            print("STEP X - LLM IS NONE")
            return dbc.Alert("LLM not initialized", color="danger"), None
        
    except Exception as e:
        print("READ_JSON ERROR")
        print(type(e).__name__)
        print(str(e))
        return dbc.Alert(f"AI Error: {type(e).__name__}: {str(e)}", color="danger"), None