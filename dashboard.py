from argparse import Action
from bdb import effective
from typing import final

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from seaborn import heatmap


#Download dataset
df = pd.read_csv("student_academic_performance_1000.csv")

# Remove Missisng Values 
df = df.dropna(
    subset=[
        "Program",
        "Gender",
        "Attendance_Percent",
        "Final_Score",
        "Internet_Access",
        "Academic_Performance",
        "Previous_GPA",
        "Study_Hours_Per_Week",
        "Assignment_Score",
        "Midterm_Score"
    ]
)


app = dash.Dash(__name__)

program_options = [
    {"label":"All Programs", "value":"All"}
]

program_options += [
    {
        "label":i,
        "value":i
    }
    for i in df["Program"].unique()
]

gender_options = [
    {"label":"All Genders", "value":"All"}
]


gender_options += [
    {
        "label":i,
        "value":i
    }
    for i in df["Gender"].unique()
]



app.layout = html.Div(

    style={
        "padding":"20px",
        "backgroundColor":"#F5F7FB",
        "fontFamily":"Arial"
    },


children=[


html.H1(
    "Student Academic Performance Dashboard",
    style={
        "textAlign":"center",
        "color":"#FE0019"
    }
),



html.Div([


html.Div([

html.Label("Select Program", style={"fontWeight":"bold","color":"#FE0019"}),

dcc.Dropdown(
    id="program_filter",
    options=program_options,
    value="All",

)

],
style={"width":"48%"}),




html.Div([

html.Label("Select Gender", style={"fontWeight":"bold","color":"#FE0019"}),

dcc.Dropdown(
    id="gender_filter",
    options=gender_options,
    value="All",
    
)

],
style={"width":"48%"})


],
style={
    "display":"flex",
    "justifyContent":"space-between",
    "marginBottom":"25px"
}),





# Charts Layout

html.Div([


html.Div(
    dcc.Graph(id="bar_chart"),
    style={
        "width":"50%",
        "background":"black",
        "padding":"2px",
        "borderRadius":"10px"
    }
),


html.Div(
    dcc.Graph(id="waterfall_chart"),
    style={
        "width":"50%",
        "background":"black",
        "padding":"2px",
        "borderRadius":"10px"
    }
)

],
style={
    "display":"flex",
    "gap":"20px"
}),

html.Br(),
html.Div([
html.Div(
    dcc.Graph(id="bubble_chart"),
    style={
        "width":"50%",
        "background":"black",
        "padding":"2px",
        "borderRadius":"10px"
    }
),
html.Div(
    dcc.Graph(id="heatmap_chart"),
    style={
        "width":"50%",
        "background":"black",
        "padding":"2px",
        "borderRadius":"10px"
    }
)
],
style={
    "display":"flex",
    "gap":"20px"
})
])


# Dashboard Callback
@app.callback(


[
Output("bar_chart","figure"),
Output("waterfall_chart","figure"),
Output("bubble_chart","figure"),
Output("heatmap_chart","figure")

],

[
Input("program_filter","value"),
Input("gender_filter","value")
]


)

def update_dashboard(program, gender):
    filtered_df = df.copy()
    # Program Filter
    if program != "All":

        filtered_df = filtered_df[
            filtered_df["Program"] == program
        ]
    # Gender Filter
    if gender != "All":
        filtered_df = filtered_df[
            filtered_df["Gender"] == gender
        ]

    # 1. BAR CHART
    program_score = (

        filtered_df
        .groupby("Program")
        ["Final_Score"]
        .mean()
        .reset_index()

    )



    fig1 = px.bar(

        program_score,

        x="Program",

        y="Final_Score",

        title="Average Final Score by Program",

        text_auto=".2f",

        template="plotly_white"

    )

    # 2. WATERFALL CHART

    assignment = filtered_df[
        "Assignment_Score"
    ].mean()


    midterm = filtered_df[
        "Midterm_Score"
    ].mean()


    final = filtered_df[
        "Final_Score"
    ].mean()



    fig2 = go.Figure(

        go.Waterfall(

            name="Academic Score",
            orientation="v",
            measure=[
                "absolute",
                "relative",
                "relative",
                "total"
            ],

            x=[
                "Base Score",
                "Assignment",
                "Midterm",
                "Final Score"
            ],
            y=[
                50,
                assignment-50,
                midterm-assignment,
                final
            ]
        )

    )

    fig2.update_layout(
        title="Academic Score Contribution",
        template="plotly_white"
    )

    # 3. BUBBLE CHART
    fig3 = px.scatter(
        filtered_df,
        x="Attendance_Percent",
        y="Final_Score",
        size="Previous_GPA",
        color="Program",
        hover_data=[
            "Gender",
            "Previous_GPA"
        ],
        title="Attendance vs Final Score (Bubble Size = GPA)",
        template="plotly_white"
    )

    # 4. HEATMAP
    correlation_columns=[
        "Study_Hours_Per_Week",
        "Attendance_Percent",
        "Assignment_Score",
        "Midterm_Score",
        "Final_Score",
        "Previous_GPA"
    ]

    corr = filtered_df[
        correlation_columns
    ].corr()

    fig4 = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu",
        title="Academic Variables Correlation Heatmap",
        template="plotly_white"
    )

    return (
        fig1,
        fig2,
        fig3,
        fig4
    )

# Run Application


if __name__ == "__main__":

    app.run(debug=True)


