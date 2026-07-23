import plotly.graph_objects as go

def render_score_gauge(score: float, max_score: float = 100.0, label: str = "PB Equity Score"):
    ratio = score / max_score
    color = "#10B981" if ratio >= 0.8 else "#F59E0B" if ratio >= 0.6 else "#EF4444"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': label, 'font': {'size': 18, 'color': '#F3F4F6'}},
        gauge={
            'axis': {'range': [0, max_score], 'tickwidth': 1, 'tickcolor': "#4B5563"},
            'bar': {'color': color},
            'bgcolor': "#1F2937",
            'bordercolor': "#374151",
            'steps': [
                {'range': [0, max_score * 0.6], 'color': '#374151'},
                {'range': [max_score * 0.6, max_score * 0.8], 'color': '#4B5563'}
            ]
        }
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': '#F3F4F6', 'family': 'Inter'},
        height=220,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    return fig
