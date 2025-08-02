import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Data from the JSON
data = {
    "platforms": [
        {
            "name": "Custom Development\n(Next.js + Email Service)",
            "customization": "High",
            "technical_complexity": "High",
            "cost": "High",
            "scalability": "High",
            "time_to_launch": "Long"
        },
        {
            "name": "WordPress + Email Plugin",
            "customization": "Medium",
            "technical_complexity": "Medium",
            "cost": "Medium",
            "scalability": "Medium",
            "time_to_launch": "Medium"
        },
        {
            "name": "Dedicated Newsletter Platforms\n(Mailchimp, Beehiiv, ConvertKit)",
            "customization": "Medium",
            "technical_complexity": "Low",
            "cost": "Medium",
            "scalability": "High",
            "time_to_launch": "Short"
        },
        {
            "name": "All-in-One Solutions\n(Substack)",
            "customization": "Low",
            "technical_complexity": "Low",
            "cost": "Low",
            "scalability": "Medium",
            "time_to_launch": "Short"
        }
    ]
}

# Create matrix data
platforms = ["Custom Dev", "WordPress", "Newsletter", "All-in-One"]
metrics = ["Custom", "Tech", "Cost", "Scale", "Time"]

# Create color mapping for categories
color_map = {
    "High": "#B4413C",    # Red for High
    "Medium": "#FFC185",  # Orange for Medium 
    "Low": "#5D878F",     # Blue-gray for Low
    "Long": "#B4413C",    # Red for Long (same as High)
    "Short": "#5D878F"    # Blue-gray for Short (same as Low)
}

# Extract data and create the table
table_data = []
colors = []
for platform in data["platforms"]:
    row_data = [
        platform["customization"],
        platform["technical_complexity"], 
        platform["cost"],
        platform["scalability"],
        platform["time_to_launch"]
    ]
    table_data.append(row_data)
    colors.append([color_map[val] for val in row_data])

# Create the table
fig = go.Figure(data=go.Table(
    header=dict(
        values=["Platform"] + metrics,
        fill_color='#1FB8CD',
        font=dict(color='white', size=14),
        align='center',
        height=40
    ),
    cells=dict(
        values=[platforms] + [[row[i] for row in table_data] for i in range(5)],
        fill_color=[['white'] * len(platforms)] + [[colors[j][i] for j in range(len(platforms))] for i in range(5)],
        font=dict(color=['black'] + [['white'] * len(platforms)] * 5, size=12),
        align='center',
        height=35
    )
))

fig.update_layout(
    title="Newsletter Platform Comparison",
    font=dict(size=12)
)

# Save the chart
fig.write_image("newsletter_platform_comparison.png")