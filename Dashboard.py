# DashboardMAIN.py

import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from flask import Flask

# Import data
df = pd.read_csv(r"C:\Users\Admin\Desktop\Lake project -Alkod\Code\Data.csv")

# Initialize Flask server
server = Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Helper function for percentages
def calculate_percentages(counts):
    total = sum(counts.values)
    return {key: (value / total) * 100 for key, value in counts.items()}

# Create social survey visualizations
def create_social_survey_charts(df):
    figures = {}
    
    # Water Availability
    water_avail_counts = df["Water_Availability"].value_counts()
    water_avail_percentages = calculate_percentages(water_avail_counts)
    figures['water_availability'] = go.Figure(

                data=go.Bar(
                    x=water_avail_counts.index,
                    y=water_avail_counts.values,
                    text=[
                        f"{val} ({water_avail_percentages[key]:.1f}%)"
                        for key, val in water_avail_counts.items()
                    ],
                    textposition="auto",
                    marker_color=["#636EFA", "#EF553B"],
                    hovertemplate="Status: %{x}<br>Count: %{y}<br>Percentage: %{text}<extra></extra>",
                )
            )

    figures['water_availability'] .update_layout(
                title="Water Availability (2021-2024)",
                xaxis=dict(title="Water Availability Status", tickangle=45),
                yaxis_title="Count",
                annotations=[
                    dict(
                        x="Improved",
                        y=water_avail_counts["Improved"],
                        text="Significant improvement",
                        showarrow=True,
                        arrowhead=2,
                        ax=0,
                        ay=-40,
                    ),
                ],template="plotly_white"
            )
# Chart: Borewell Recharge
    borewell_recharge_counts = df["Borewell_Recharge"].value_counts()
    borewell_recharge_percentages = calculate_percentages(borewell_recharge_counts)

    figures['borewell_recharge'] = go.Figure(
                                    data=go.Bar(
                                        x=borewell_recharge_counts.index,
                                        y=borewell_recharge_counts.values,
                                        text=[
                                            f"{val} ({borewell_recharge_percentages[key]:.1f}%)"
                                            for key, val in borewell_recharge_counts.items()
                                        ],
                                        textposition="auto",
                                        marker_color=["#00CC96", "#AB63FA"],
                                        hovertemplate="Status: %{x}<br>Count: %{y}<br>Percentage: %{text}<extra></extra>",
                                    )
                                )

    figures['borewell_recharge'].update_layout(
                title="Borewell Recharge (2021-2024)",
                xaxis_title="Borewell Recharge Status",
                yaxis_title="Count",
                annotations=[
                    dict(
                        x="Increased",
                        y=borewell_recharge_counts["Increased "],
                        text="Rejuvenation impact",
                        showarrow=False,
                        arrowhead=0,
                        ax=0,
                        ay=0,
                    ),
                ],
                template="plotly_white",
            )


    # Chart 3: Yield Comparison (Groundnuts and Cotton)
    figures['yield_comparison'] = go.Figure()
    groundnuts_total = [df["Groundnuts_Yield_2021"].sum(), df["Groundnuts_Yield_2024"].sum()]
    cotton_total = [df["Cotton_Yield_2021"].sum(), df["Cotton_Yield_2024"].sum()]
    figures['yield_comparison'].add_trace(
        go.Bar(
            x=["2021", "2024"],
            y=groundnuts_total,
            name="Groundnuts",
            text=[f"{val} bags" for val in groundnuts_total],
            textposition="auto",
            marker_color="#FFA15A",
            hovertemplate="Year: %{x}<br>Groundnuts Yield: %{y}<extra></extra>",
        )
    )
    figures['yield_comparison'].add_trace(
        go.Bar(
            x=["2021", "2024"],
            y=cotton_total,
            name="Cotton",
            text=[f"{val} Quintals" for val in cotton_total],
            textposition="auto",
            marker_color="#19D3F3",
            hovertemplate="Year: %{x}<br>Cotton Yield: %{y}<extra></extra>",
        )
    )
    figures['yield_comparison'].update_layout(
        title="Crop Yield Comparison (2021 vs 2024)",
        xaxis_title="Year",
        yaxis_title="Yield",
        barmode="group",
        template="plotly_white"
        
    )

    # Chart 4: Views on Lake Rejuvenation
    views_counts = df["Views_on_Lake_Rejuvenation"].value_counts()
    figures['lake_rejuvenation'] = go.Figure(
        data=go.Pie(
            labels=views_counts.index,
            values=views_counts.values,
            textinfo="label+percent",
            hoverinfo="label+value+percent",
            marker=dict(colors=["#1f77b4", "#ff7f0e"]),
        )
    )
    figures['lake_rejuvenation'].update_layout(
        title="Views on Lake Rejuvenation",
        annotations=[
            dict(
                text="Positive views dominate the feedback.",
                x=0.5,
                y=-0.1,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=14, color="black"),
                align="center",
                bgcolor="#FFE6D6",
            )
        ],
    )

# Chart 5: Willingness to Be a Committee Member
    willingness_counts = df["Willing_to_Be_Committee_Member"].value_counts()
    figures['committee_member'] = go.Figure(
        data=go.Pie(
            labels=["Willing", "Not Willing"],
            values=willingness_counts.values,
            textinfo="label+percent",
            hoverinfo="label+value+percent",
            marker=dict(colors=["#2ca02c", "#d62728"]),
        )
    )
    figures['committee_member'].update_layout(
        title="Willingness to Be a Committee Member",
        annotations=[
            dict(
                text="Majority of respondents are willing to participate.",
                x=0.5,
                y=-0.1,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=14, color="black"),
                align="center",
                bgcolor="#E6FFEB",
            )
        ],
    )

    return figures


# Example placeholder figures for other sections
sample_fig = px.bar(x=["A", "B", "C"], y=[1, 3, 2], title="Placeholder Graph")

# Create content sections
sections_content = {
    "Social Survey": "dashboard",  # Special flag for full dashboard view
    "Hydro Geology Study": {
        "Percolation Test": sample_fig,
        "Pump Test": sample_fig,
        "Land Use and Land Cover": sample_fig,
        "Yield Test": sample_fig,
        "Ground water Level and TDS": sample_fig,
        "Geophysical Survey": sample_fig,
        "Biomass": sample_fig,
        "Water Budget": sample_fig,
    },
    "Community Interactions": {
        "Focus Group Discussions": sample_fig,
        "Focus Interviews": sample_fig,
        "Additional Community Feedback": sample_fig,
    },
    "Impact Assessment": {
        "Water Quality Improvement": sample_fig,
        "Access Enhancement": sample_fig,
        "Health Metrics": sample_fig,
    },
}

# Generate Sidebar Layout
sidebar = html.Div(
    [
        html.H2("Alkod Lake Dashboard", style={"color": "white", "text-align": "center"}),
        html.Hr(style={"border": "1px solid #ccc"}),
        html.Div(
            [
                html.Div(
                    [
                        html.Button(
                            section,
                            id=f"{section}-btn",
                            n_clicks=0,
                            className="sidebar-button",
                        ),
                        dbc.Collapse(
                            id=f"{section}-collapse",
                            is_open=False,
                            children=[
                                html.Div(
                                    [
                                        html.Button(
                                            f"- {subsection}",
                                            id=f"{section}-{subsection}-btn",
                                            n_clicks=0,
                                            className="sidebar-sub-button",
                                        )
                                        for subsection in (subsections.keys() if isinstance(subsections, dict) else [])
                                    ],
                                    style={"margin-left": "10px"},
                                )
                            ] if isinstance(subsections, dict) else [],
                        ),
                    ],
                    style={"margin-bottom": "10px"},
                )
                for section, subsections in sections_content.items()
            ]
        ),
    ],
    id="sidebar",
    style={
        "width": "20%",
        "height": "100%",
        "position": "fixed",
        "top": "0",
        "left": "0",
        "background-color": "#2c3e50",
        "padding": "20px",
        "color": "white",
        "overflow-y": "auto",
    },
)

# Define the Layout of the App and Content of dashboard
app.layout = html.Div(
    [
        sidebar,
        html.Div(
            id="content",
            style={
                "flex-grow": "1",
                "margin-left": "20%", 
                "padding": "20px", 
                "background-color": "#ecf0f1"
            },
        ),
    ],
    style={"display": "flex","flex-direction": "row"},
)

# Callbacks
@app.callback(
    [Output(f"{section}-collapse", "is_open") for section in sections_content.keys()],
    [Input(f"{section}-btn", "n_clicks") for section in sections_content.keys()],
    [State(f"{section}-collapse", "is_open") for section in sections_content.keys()],
)
def toggle_subsections(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [False] * len(sections_content)

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    section_name = button_id.replace("-btn", "")
    
    return [
        not is_open if f"{section}-btn" == button_id and isinstance(sections_content[section], dict) else is_open
        for section, is_open in zip(sections_content.keys(), args[len(sections_content):])
    ]

# Modified callback for content display

@app.callback(
    Output("content", "children"),
    [Input(f"{section}-btn", "n_clicks") for section in sections_content.keys()] +
    [Input(f"{section}-{subsection}-btn", "n_clicks") 
     for section, subsections in sections_content.items() 
     if isinstance(subsections, dict)
     for subsection in subsections.keys()]
)
def update_content(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.Div([
            html.H2("Welcome to Alkod Lake Dashboard"),
            html.P("Select a section from the sidebar to view detailed analysis.")
        ])

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        # Handle main section buttons
    for section in sections_content.keys():
        if button_id == f"{section}-btn":
            if section == "Social Survey":
                figures = create_social_survey_charts(df)
                return html.Div([
                    html.H2("Social Survey Analysis"),
                    dbc.Row([
            dbc.Col(dcc.Graph(figure=figures['water_availability']), md=6),
            dbc.Col(dcc.Graph(figure=figures['borewell_recharge']), md=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(figure=figures['yield_comparison']), md=12),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col(dcc.Graph(figure=figures['committee_member']), md=6),
            dbc.Col(dcc.Graph(figure=figures['lake_rejuvenation']), md=6),
        ], className="mb-4"),
                ])
    # Handle subsection buttons
    for section, subsections in sections_content.items():
        if isinstance(subsections, dict):
            for subsection in subsections.keys():
                if button_id == f"{section}-{subsection}-btn":
                    if section == "Community Interactions":
                        if subsection == "Focus Group Discussions":
                            return html.Div([
                                html.H3("Community Interactions - Focus Group Discussions"),
                                html.Div([
                                    html.Video(src=r"C:\Users\Admin\Desktop\Lake project -Alkod\Code\assests\Video 1.mp4", controls=True, style={"width": "100%"}),
                                    html.P("The Village President shares heartfelt appreciation for the ICICI Foundation's initiatives in their village. By removing 3-4 feet of silt, the Foundation revived the village lake and borewells, providing water essential for agriculture and livestock."),
                                ], style={"margin-bottom": "20px"}),
                                html.Div([
                                    html.Video(src="/assets/video2.mp4", controls=True, style={"width": "100%"}),
                                    html.P("During a Gram Panchayat meeting, committee members and ICICI officers exchanged gratitude. The villagers celebrated the successful completion of the project, recognizing its profound impact on their lives."),
                                ], style={"margin-bottom": "20px"}),
                            ])
                        elif subsection == "Focus Interviews":
                            return html.Div([
                                html.H3("Community Interactions - Focus Interviews"),
                                html.Div([
                                    html.Video(src="/assets/video3.mp4", controls=True, style={"width": "100%"}),
                                    html.P("A farmer from Alkoda Village recounts how ICICI Foundation alleviated the financial burden of desilting the village tank."),
                                ], style={"margin-bottom": "20px"}),
                                html.Div([
                                    html.Video(src="/assets/video4.mp4", controls=True, style={"width": "100%"}),
                                    html.P("Lakshmi, a local resident, speaks of her daily struggle to fetch water for her livestock, highlighting the critical need for water resources."),
                                ], style={"margin-bottom": "20px"}),
                            ])
                        elif subsection == "Additional Community Feedback":
                            return html.Div([
                                html.H3("Community Interactions - Additional Community Feedback"),
                                html.Div([
                                    html.Video(src="/assets/video5.mp4", controls=True, style={"width": "100%"}),
                                    html.P("Mr. Narayana describes the ICICI Foundation’s efforts in silt removal and water conservation at Gimigena Panchayat."),
                                ], style={"margin-bottom": "20px"}),
                                html.Div([
                                    html.Video(src="/assets/video6.mp4", controls=True, style={"width": "100%"}),
                                    html.P("In Alkoda Village, the ICICI Foundation revived a lake in Raichur district over three years."),
                                ], style={"margin-bottom": "20px"}),
                                html.Div([
                                    html.Video(src="/assets/video7.mp4", controls=True, style={"width": "100%"}),
                                    html.P("The villagers celebrate the ICICI Foundation's two-year effort to rebuild water resources and provide livestock and poultry to families."),
                                ], style={"margin-bottom": "20px"}),
                            ])

    return html.Div(["Please select a section to view"])


# Custom CSS remains the same...
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Alkod Lake Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #f8f9fa;
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .sidebar-button {
                width: 100%;
                padding: 10px;
                margin: 5px 0;
                background: none;
                border: 1px solid #ffffff3d;
                color: white;
                text-align: left;
                cursor: pointer;
                border-radius: 4px;
            }
            
            .sidebar-button:hover {
                background-color: #34495e;
            }
            
            .sidebar-sub-button {
                width: 100%;
                padding: 8px;
                margin: 2px 0;
                background: none;
                border: none;
                color: white;
                text-align: left;
                cursor: pointer;
                font-size: 0.9em;
            }
            
            .sidebar-sub-button:hover {
                background-color: #34495e;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == "__main__":
    app.run_server(debug=True)