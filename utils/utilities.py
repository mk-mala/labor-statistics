import plotly.express as px


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
