import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px


def create_scatter_plot(df, x_column, y_column, hover_variable):
    fig = px.scatter(df, x=x_column, y=y_column, color='element_type', hover_name=hover_variable)

    fig.update_traces(marker=dict(color='blue', size=12),
                      selector=dict(mode='markers'))
    fig.show()
    fig.write_html("fpl_plot.html")


def get_label_rotation(angle, offset):
    rotation = np.rad2deg(angle + offset)
    if angle <= np.pi:
        alignment = "right"
        rotation = rotation + 180
    else:
        alignment = "left"
    return rotation, alignment


def add_labels(angles, values, labels, offset, ax):
    # This is the space between the end of the bar and the label
    padding = 4

    # Iterate over angles, values, and labels, to add all of them.
    for angle, value, label, in zip(angles, values, labels):
        angle = angle

        # Obtain text rotation and alignment
        rotation, alignment = get_label_rotation(angle, offset)

        # And finally add the text
        ax.text(
            x=angle,
            y=value + padding,
            s=label,
            ha=alignment,
            va="center",
            rotation=rotation,
            rotation_mode="anchor"
        )


def circular_barplot(df, value, name):  # group):  # , offset):
    ANGLES = np.linspace(0, 2 * np.pi, len(df), endpoint=False)
    VALUES = df[value].values * 100.0
    LABELS = df[name].values

    # Determine the width of each bar.
    # The circumference is '2 * pi', so we divide that total width over the number of bars.
    WIDTH = 2 * np.pi / len(VALUES)

    # Determines where to place the first bar.
    # By default, matplotlib starts at 0 (the first bar is horizontal)
    # but here we say we want to start at pi/2 (90 deg)
    OFFSET = np.pi / 2

    # Initialize Figure and Axis
    fig, ax = plt.subplots(figsize=(20, 10), subplot_kw={"projection": "polar"})

    # Specify offset
    ax.set_theta_offset(OFFSET)

    # Set limits for radial (y) axis. The negative lower bound creates the whole in the middle.
    ax.set_ylim(-100, 100)

    # Remove all spines
    ax.set_frame_on(False)

    # Remove grid and tick marks
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

    # Add bars
    ax.bar(
        ANGLES, VALUES, width=WIDTH, linewidth=2,
        color="#61a4b2", edgecolor="white"
    )

    # Add labels
    add_labels(ANGLES, VALUES, LABELS, OFFSET, ax)
