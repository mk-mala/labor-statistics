import plotly.express as px
import numpy as np


def create_line_chart(df, x_axis, y_axis, x_axis_title, y_axis_title, title):

    fig = px.line(
        df,
        x=x_axis,
        y=y_axis
    )

    fig.update_layout(
        xaxis_title=x_axis_title,
        yaxis_title=y_axis_title,
        title=title
    )

    fig.update_yaxes(tickformat=",")

    return fig


def create_line_chart_change_12m(df):

    # 12-month change
    df['change_12m'] = df['employment'] - df['employment'].shift(12)
    df['pct_change_12m'] = df['employment'].pct_change(periods=12)

    fig = px.line(
        df, 
        x='date', 
        y='pct_change_12m'
    )

    fig.update_layout(
        title='<b>Employment 12-Month Change</b>',
        xaxis={'title': 'Date'},
        yaxis={
            'title': 'Percent Change','tickformat': '.2%'
        },
    )

    fig.update_traces(line=dict(color="green"))

    return fig

def create_bar_chart_yoy(df):

    # Get the current month
    curr_month = df[df['date'] == df['date'].max()]['month'].iloc[0]
    curr_period = df[df['date'] == df['date'].max()]['period'].iloc[0]

    # Filter only for the current month
    df = df[df['month'] == curr_month]

    # YoY change directionality
    df['change_direction'] = np.where(
        df['change_12m'] >= 0,
        'Up',
        'Down'
    )

    fig = px.bar(
        df,
        x='date',
        y='employment',
        color='change_direction',
        color_discrete_map={
            "Up": "green",
            "Down": "red"
        }
    )

    # Axis Range Padding
    y_min = df["employment"].min()
    y_max = df["employment"].max()

    padding = 0.50 * (y_max - y_min)
    y_range = [y_min - padding, y_max + padding]

    str_bar_chart_yoy_title = f"<b>{curr_period} Employment Year Over Year</b>"

    fig.update_layout(
        title=str_bar_chart_yoy_title,
        xaxis={'title': 'Date'},
        yaxis={
            'title': 'Employment',
            'tickformat': ',',
            'range': y_range
        },
        showlegend=False
    )

    return fig
