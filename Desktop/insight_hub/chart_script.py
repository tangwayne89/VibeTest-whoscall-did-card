import plotly.graph_objects as go
import numpy as np

# Define nodes with positions and translated labels (keeping under 15 char limit)
nodes = [
    {"id": "user_visit", "label": "Visit Website", "type": "user_action", "x": 1, "y": 8},
    {"id": "browse_articles", "label": "Browse Topics", "type": "user_action", "x": 1, "y": 6},
    {"id": "subscription_form", "label": "Subscribe Form", "type": "interface", "x": 1, "y": 4},
    {"id": "email_verification", "label": "Email Verify", "type": "process", "x": 1, "y": 2},
    {"id": "preference_management", "label": "User Prefs", "type": "system", "x": 3, "y": 2},
    {"id": "cms", "label": "CMS", "type": "system", "x": 5, "y": 4},
    {"id": "email_automation", "label": "Email System", "type": "system", "x": 3, "y": 0},
    {"id": "newsletter_delivery", "label": "Send Newsletter", "type": "output", "x": 1, "y": -2}
]

# Define connections
connections = [
    {"from": "user_visit", "to": "browse_articles"},
    {"from": "browse_articles", "to": "subscription_form"},
    {"from": "subscription_form", "to": "email_verification"},
    {"from": "email_verification", "to": "preference_management"},
    {"from": "cms", "to": "email_automation"},
    {"from": "preference_management", "to": "email_automation"},
    {"from": "email_automation", "to": "newsletter_delivery"}
]

# Brand colors for different node types
type_colors = {
    "user_action": "#1FB8CD",  # Strong cyan
    "interface": "#FFC185",    # Light orange
    "process": "#ECEBD5",      # Light green
    "system": "#5D878F",       # Cyan
    "output": "#D2BA4C"        # Moderate yellow
}

# Create node lookup for easy access
node_lookup = {node["id"]: node for node in nodes}

# Create figure
fig = go.Figure()

# Add connection arrows
for conn in connections:
    from_node = node_lookup[conn["from"]]
    to_node = node_lookup[conn["to"]]
    
    # Add arrow line
    fig.add_trace(go.Scatter(
        x=[from_node["x"], to_node["x"]],
        y=[from_node["y"], to_node["y"]],
        mode='lines',
        line=dict(color='#333333', width=2),
        showlegend=False,
        hoverinfo='skip',
        cliponaxis=False
    ))

# Add arrowheads using annotations
for conn in connections:
    from_node = node_lookup[conn["from"]]
    to_node = node_lookup[conn["to"]]
    
    # Calculate arrow direction
    dx = to_node["x"] - from_node["x"]
    dy = to_node["y"] - from_node["y"]
    length = np.sqrt(dx**2 + dy**2)
    
    if length > 0:
        # Normalize direction
        dx_norm = dx / length
        dy_norm = dy / length
        
        # Arrow position (slightly before the target node)
        arrow_x = to_node["x"] - 0.3 * dx_norm
        arrow_y = to_node["y"] - 0.3 * dy_norm
        
        # Add arrowhead
        fig.add_annotation(
            x=arrow_x,
            y=arrow_y,
            ax=from_node["x"],
            ay=from_node["y"],
            arrowcolor='#333333',
            arrowsize=1.5,
            arrowwidth=2,
            arrowhead=2,
            showarrow=True,
            text="",
            xref="x",
            yref="y",
            axref="x",
            ayref="y"
        )

# Add nodes as rectangles with text
for node in nodes:
    color = type_colors[node["type"]]
    
    # Add rectangle background
    fig.add_shape(
        type="rect",
        x0=node["x"]-0.6,
        y0=node["y"]-0.4,
        x1=node["x"]+0.6,
        y1=node["y"]+0.4,
        fillcolor=color,
        line=dict(color="#333333", width=1),
        opacity=0.9
    )
    
    # Add text label
    fig.add_trace(go.Scatter(
        x=[node["x"]],
        y=[node["y"]],
        mode='text',
        text=[node["label"]],
        textfont=dict(size=11, color="black", family="Arial"),
        showlegend=False,
        hoverinfo='skip',
        cliponaxis=False
    ))

# Create legend
type_labels = {
    "user_action": "User Actions",
    "interface": "Interface", 
    "process": "Process",
    "system": "System",
    "output": "Output"
}

for node_type, color in type_colors.items():
    fig.add_trace(go.Scatter(
        x=[None],
        y=[None],
        mode='markers',
        marker=dict(size=15, color=color, symbol='square'),
        name=type_labels[node_type],
        showlegend=True,
        cliponaxis=False
    ))

# Update layout
fig.update_layout(
    title="Newsletter Flow Architecture",
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-0.5, 6]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-3, 9]
    ),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='center',
        x=0.5
    ),
    plot_bgcolor='white'
)

# Save the chart
fig.write_image("newsletter_flowchart.png")