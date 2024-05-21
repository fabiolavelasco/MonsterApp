from altair import Chart
import altair as alt


def chart(df, x, y, target) -> Chart:
    """
    Purpose:
    The chart function creates an interactive scatter plot visualization using the Altair library. The plot displays the
    relationship between two specified variables (x and y) in a DataFrame, with an additional encoding for a target
    variable.

    Parameters:
    - df (pd.DataFrame): The input DataFrame containing the data to be plotted.
    - x (str): The column name in 'df' to be used for the x-axis of the plot.
    - y (str): The column name in 'df' to be used for the y-axis of the plot.
    - target (str): The column name in 'df' to be used for coloring the scatter plot points.

    Returns:
    - Chart: An Altair chart object representing the interactive scatter plot.

    Chart Initialization:

    Creates an initial scatter plot with circles (mark_circle()) using x and y for the axes, and target for color
    encoding.
    Adds tooltips to display all columns in the DataFrame on hover.
    Sets the chart title as "{y} by {x} for {target}".

    Chart Configuration:

    Sets the background color of the chart to gray and adds padding around the chart.
    Configures the chart axes with reduced grid opacity and increased title font size.
    Sets the continuous view dimensions (width and height) to 500 pixels each, with gray fill and no stroke.
    Configures the title font size to 30 and color to black.

    Interactivity:

    Adds zoom functionality allowing users to zoom into the chart.
    Adds pan functionality, activated by holding the Alt key and dragging the mouse, allowing users to move around the
    chart.

    Return:

    Returns the fully configured and interactive Altair chart.
    """
    result = (Chart(df, title=f"{y} by {x} for {target}").mark_circle()
    .encode(x=x, y=y, tooltip=df.columns.to_list(), color=target).interactive())
    result = result.configure(background='gray', padding={"left": 50, "top": 50, "right": 50, "bottom": 50})

    zoom = alt.selection(type='interval', bind='scales')
    pan = alt.selection(type='interval', bind='scales',
                        on="[mousedown[event.altKey], window:mouseup] > window:mousemove!", encodings=['x'])
    result = result.add_params(zoom, pan)

    result = result.configure_axis(gridOpacity=0.3, titleFontSize=20)
    result = result.configure_view(continuousWidth=500, continuousHeight=500, fill='gray', stroke=None)
    result = result.configure_title(fontSize=30, color='black')
    result = result.transform_filter(zoom).transform_filter(pan)
    return result
