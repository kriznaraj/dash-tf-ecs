# import dash
# import dash_bootstrap_components as dbc
# from dash import dcc
# from dash import html
# from dash import dash_table
# from dash import Input, Output, callback
# import flask
# import pandas as pd
# import re
# import plotly.graph_objs as go


# server = flask.Flask(__name__)
# app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.config.suppress_callback_exceptions = True

# # This function will convert the url to a download link
# def convert_gsheets_url(u):
#     try:
#         worksheet_id = u.split("#gid=")[1]
#     except:
#         # Couldn't get worksheet id. Ignore it
#         worksheet_id = None
#     u = re.findall("https://docs.google.com/spreadsheets/d/.*?/", u)[0]
#     u += "export"
#     u += "?format=csv"
#     if worksheet_id:
#         u += "&gid={}".format(worksheet_id)
#     return u


# df2 = pd.read_csv(
#     convert_gsheets_url(
#         "https://docs.google.com/spreadsheets/d/1wxhPNkZF4GNq3HKTynRdkCvrLTQo1U75l5CU8wcNqYE/edit"
#     )
# )

# customer_options = df2["Name"].unique()

# app.layout = html.Div(
#     children=[
#         html.H1(children="Hello KK!"),
#         html.Div(children="""Dash: A web application framework for Python."""),
#         html.Div(
#             [
#                 dcc.Dropdown(
#                     id="Customer",
#                     options=[{"label": i, "value": i} for i in customer_options],
#                     value="All",
#                 ),
#             ],
#             style={"width": "25%", "display": "inline-block"},
#         ),
#         # dcc.Graph(id="customer-graph"),
#         dbc.Alert(id="tbl_out"),
#         # dcc.Graph(id="customer-table"),
#         dash_table.DataTable(
#             id="customer-table",
#             columns=[{"name": i, "id": i} for i in df2.columns],
#             # data=df2.to_dict("records"),
#         ),
#     ]
# )


# @callback(Output("tbl_out", "children"), Input("table", "active_cell"))
# def update_graphs(active_cell):
#     return str(active_cell) if active_cell else "Click a cell"


# @app.callback(
#     dash.dependencies.Output("customer-table", "object"),
#     [dash.dependencies.Input("Customer", "value")],
# )
# def update_table(Customer):
#     if Customer == "All":
#         df_customers = df2.copy()
#     else:
#         df_customers = df2[df2["Name"] == Customer]

#         dash_table.DataTable(
#             id="customer-table",
#             columns=[{"name": i, "id": i} for i in df2.columns],
#             data=df2.to_dict("records"),
#         ),
#     return {"data": df_customers.to_dict("records")}


# # @app.callback(
# #     dash.dependencies.Output("customer-graph", "figure"),
# #     [dash.dependencies.Input("Customer", "value")],
# # )
# # def update_graph(Customer):
# #     if Customer == "All":
# #         df_plot = df2.copy()
# #     else:
# #         df_plot = df2[df2["Name"] == Customer]

# #     pv = pd.pivot_table(
# #         df_plot,
# #         index=["Name"],
# #         columns=["Plan"],
# #         values=["Plan ID"],
# #         aggfunc=sum,
# #         fill_value=0,
# #     )

# #     trace1 = go.Bar(x=pv.index, y=pv[("Plan", "declined")], name="Declined")
# #     trace2 = go.Bar(x=pv.index, y=pv[("Plan", "pending")], name="Pending")
# #     trace3 = go.Bar(x=pv.index, y=pv[("Plan", "presented")], name="Presented")
# #     trace4 = go.Bar(x=pv.index, y=pv[("Plan", "won")], name="Won")

# #     return {
# #         "data": [trace1, trace2, trace3, trace4],
# #         "layout": go.Layout(
# #             title="Customer Status for {}".format(Customer), barmode="stack"
# #         ),
# #     }


# if __name__ == "__main__":
#     import os

#     debug = False if os.environ["DASH_DEBUG_MODE"] == "False" else True
#     if debug:
#         app.run_server(debug=True, threaded=True)
#     else:
#         app.run_server(host="0.0.0.0", port=8050, debug=debug)



import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),
    html.Div(id='datatable-interactivity-container')
])

@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"))
def update_graphs(rows, derived_virtual_selected_rows):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": dff["country"],
                        "y": dff[column],
                        "type": "bar",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        # check if column exists - user may have deleted it
        # If `column.deletable=False`, then you don't
        # need to do this check.
        for column in ["pop", "lifeExp", "gdpPercap"] if column in dff
    ]


if __name__ == '__main__':
    app.run_server(debug=True)
