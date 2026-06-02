import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.offline import plot

# Create output directories
os.makedirs("visuals", exist_ok=True)

# ---------------------------------------------------------
# 1. Load Data with Pandas
# ---------------------------------------------------------
df = pd.read_csv("sales_data_consolidated.csv")

# Compute grand totals and summary metrics
totals = {
    'FY_23_24': df['FY_23_24'].sum(),
    'FY_24_25': df['FY_24_25'].sum(),
    'FY_25_26': df['FY_25_26'].sum(),
    'Cumulative': df['Total_Sales'].sum()
}

counts = {
    'total_clients': len(df),
    'retained': len(df[df['Status'] == 'Retained']),
    'new': len(df[df['Status'] == 'New']),
    'lost': len(df[df['Status'] == 'Lost']),
    'inactive': len(df[df['Status'] == 'Inactive'])
}

# ---------------------------------------------------------
# Helper: Format Rupees in Indian Numbering System
# ---------------------------------------------------------
def format_currency_in(val):
    s = f"{val:,.2f}"
    # Convert standard US format to Indian currency grouping
    parts = s.split('.')
    num = parts[0].replace(',', '')
    if len(num) > 3:
        last_three = num[-3:]
        remaining = num[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        groups.append(last_three)
        formatted_num = ",".join(groups)
    else:
        formatted_num = num
    return f"₹{formatted_num}.{parts[1]}"

# ---------------------------------------------------------
# 2. Matplotlib Static High-Res Graphs (saved to disk)
# ---------------------------------------------------------
# Set global style
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['text.color'] = '#f3f4f6'
plt.rcParams['axes.labelcolor'] = '#9ca3af'
plt.rcParams['xtick.color'] = '#9ca3af'
plt.rcParams['ytick.color'] = '#9ca3af'
plt.rcParams['grid.color'] = '#1f2937'

# Theme palette
primary_color = '#6366f1'  # Indigo
secondary_color = '#8b5cf6'  # Violet
pink_color = '#ec4899'  # Pink
success_color = '#10b981'  # Emerald
danger_color = '#ef4444'  # Red
warning_color = '#f59e0b'  # Amber

# GRAPH 1: YoY Trajectory Line Chart
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
years = ['FY 23-24', 'FY 24-25', 'FY 25-26']
sales_trajectory = [totals['FY_23_24'], totals['FY_24_25'], totals['FY_25_26']]

ax.plot(years, sales_trajectory, marker='o', linewidth=3, color=primary_color, markersize=8, markerfacecolor=secondary_color)
ax.fill_between(years, sales_trajectory, alpha=0.15, color=primary_color)
ax.grid(True, linestyle='--', alpha=0.3)
ax.set_title("Overall Sales Trajectory (3 Years)", fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel("Sales volume (in Millions)")
# Fix tick warning
ticks = ax.get_yticks()
ax.set_yticks(ticks)
ax.set_yticklabels([f"₹{(y/1000000):.1f}M" for y in ticks])
fig.tight_layout()
plt.savefig("visuals/yearly_trajectory.png", facecolor='#0b0f19', edgecolor='none')
plt.close()

# GRAPH 2: Customer Status Distribution
fig, ax = plt.subplots(figsize=(6, 5), dpi=300)
status_counts = df['Status'].value_counts()
colors = [success_color, primary_color, danger_color, warning_color]
ax.pie(status_counts, labels=status_counts.index, autopct='%1.1f%%', startangle=140, colors=colors, 
       textprops={'fontsize': 9}, wedgeprops={'edgecolor': '#0b0f19', 'linewidth': 2, 'antialiased': True})
# Draw circle to convert to doughnut
centre_circle = plt.Circle((0,0),0.60,fc='#0b0f19')
fig.gca().add_artist(centre_circle)
ax.set_title("Customer Segments Share", fontsize=13, fontweight='bold', pad=15)
fig.tight_layout()
plt.savefig("visuals/customer_segments.png", facecolor='#0b0f19', edgecolor='none')
plt.close()

# GRAPH 3: Top 15 Particulars Stacked Bar Plot
top_15 = df.nlargest(15, 'Total_Sales')
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

y_indices = np.arange(len(top_15))
height = 0.55

# Draw stacked segments horizontally
p1 = ax.barh(y_indices, top_15['FY_23_24'], height, label='FY 23-24', color=secondary_color)
p2 = ax.barh(y_indices, top_15['FY_24_25'], height, left=top_15['FY_23_24'], label='FY 24-25', color=pink_color)
p3 = ax.barh(y_indices, top_15['FY_25_26'], height, left=top_15['FY_23_24']+top_15['FY_24_25'], label='FY 25-26', color=success_color)

ax.set_yticks(y_indices)
ax.set_yticklabels(top_15['Particulars'], fontsize=8)
ax.invert_yaxis()  # top-down ranking
ax.set_xlabel("Sales Volume (Rupees)")
# Fix tick warning
ticks = ax.get_xticks()
ax.set_xticks(ticks)
ax.set_xticklabels([f"₹{(x/100000):.1f}L" for x in ticks])
ax.set_title("Top 15 Clients: Stacked Annual Breakdown", fontsize=13, fontweight='bold', pad=15)
ax.grid(True, axis='x', linestyle='--', alpha=0.2)
ax.legend(loc='lower right', framealpha=0.1)
fig.tight_layout()
plt.savefig("visuals/top_15_particulars.png", facecolor='#0b0f19', edgecolor='none')
plt.close()

print("[Matplotlib] Static graphics saved to 'visuals/' folder.")

# ---------------------------------------------------------
# 3. Interactive Plotly Charts
# ---------------------------------------------------------
# Dark plot layout dictionary
dark_plotly_layout = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#e5e7eb', family='Inter, sans-serif'),
    xaxis=dict(
        gridcolor='rgba(255,255,255,0.06)',
        linecolor='rgba(255,255,255,0.1)',
        tickfont=dict(color='#9ca3af')
    ),
    yaxis=dict(
        gridcolor='rgba(255,255,255,0.06)',
        linecolor='rgba(255,255,255,0.1)',
        tickfont=dict(color='#9ca3af')
    ),
    margin=dict(l=40, r=20, t=40, b=40)
)

# Plotly Chart 1: Trajectory
fig_traj = go.Figure()
fig_traj.add_trace(go.Scatter(
    x=['FY 23-24', 'FY 24-25', 'FY 25-26'],
    y=[totals['FY_23_24'], totals['FY_24_25'], totals['FY_25_26']],
    mode='lines+markers',
    name='Outward Sales',
    line=dict(color='#6366f1', width=4),
    marker=dict(color='#8b5cf6', size=10, line=dict(color='#fff', width=1.5)),
    fill='tozeroy',
    fillcolor='rgba(99, 102, 241, 0.08)',
    hovertemplate="<b>%{x}</b><br>Sales: ₹%{y:,.2f}<extra></extra>"
))
fig_traj.update_layout(
    **dark_plotly_layout,
    title=dict(text="Outward Revenue YoY Trend", font=dict(family='Outfit', size=16)),
    height=320
)
div_traj = plot(fig_traj, include_plotlyjs=False, output_type='div')

# Plotly Chart 2: Customer Status Distribution Doughnut
fig_dist = go.Figure()
fig_dist.add_trace(go.Pie(
    labels=['Retained Accounts', 'New clients', 'Lost (Missed)', 'Inactive'],
    values=[counts['retained'], counts['new'], counts['lost'], counts['inactive']],
    hole=0.55,
    marker=dict(colors=[success_color, primary_color, danger_color, warning_color]),
    textinfo='percent',
    hoverinfo='label+value+percent',
    textposition='outside'
))
fig_dist.update_layout(
    **dark_plotly_layout,
    title=dict(text="Customer Distribution by Status", font=dict(family='Outfit', size=16)),
    height=320,
    legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
)
div_dist = plot(fig_dist, include_plotlyjs=False, output_type='div')

# Plotly Chart 3: Top 15 Stacked Bar
fig_top = go.Figure()
fig_top.add_trace(go.Bar(
    y=top_15['Particulars'], x=top_15['FY_23_24'], name='FY 23-24', orientation='h', marker_color='#8b5cf6'
))
fig_top.add_trace(go.Bar(
    y=top_15['Particulars'], x=top_15['FY_24_25'], name='FY 24-25', orientation='h', marker_color='#ec4899'
))
fig_top.add_trace(go.Bar(
    y=top_15['Particulars'], x=top_15['FY_25_26'], name='FY 25-26', orientation='h', marker_color='#10b981'
))
fig_top.update_layout(**dark_plotly_layout)
fig_top.update_layout(
    barmode='stack',
    title=dict(text="Top 15 Selling Particulars", font=dict(family='Outfit', size=16)),
    height=400,
    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
)
fig_top.update_yaxes(autorange="reversed")
div_top = plot(fig_top, include_plotlyjs=False, output_type='div')

# Plotly Chart 4: YoY Growth vs Sales Bubble Plot (Executive Analytics)
# Filter clients with significant sales to prevent bubble size explosion
bubble_df = df.copy()
# Bubble sizes scale
size_vals = np.sqrt(bubble_df['Total_Sales']) / 10
size_vals = np.clip(size_vals, 5, 50)  # limit bounds

color_map = {
    'Retained': success_color,
    'New': primary_color,
    'Lost': danger_color,
    'Inactive': warning_color
}
bubble_colors = bubble_df['Status'].map(color_map)

fig_bubble = go.Figure()
fig_bubble.add_trace(go.Scatter(
    x=bubble_df['Total_Sales'],
    y=bubble_df['Growth_24_25_to_25_26'],
    mode='markers',
    marker=dict(
        size=size_vals,
        color=bubble_colors,
        opacity=0.7,
        line=dict(width=1, color='rgba(255,255,255,0.2)')
    ),
    text=bubble_df['Particulars'],
    customdata=np.stack((bubble_df['Status'], bubble_df['FY_25_26']), axis=-1),
    hovertemplate="<b>%{text}</b><br>Lifetime Sales: ₹%{x:,.2f}<br>FY 25-26 Growth: %{y:.1f}%<br>Status: %{customdata[0]}<br>FY 25-26 Sales: ₹%{customdata[1]:,.2f}<extra></extra>"
))
fig_bubble.update_layout(**dark_plotly_layout)
fig_bubble.update_layout(
    title=dict(text="Growth Trajectory vs Lifetime Volume (Bubble Plot)", font=dict(family='Outfit', size=16)),
    height=400
)
fig_bubble.update_xaxes(type='log', title='Total Cumulative Sales (Rupees - Log Scale)')
fig_bubble.update_yaxes(title='YoY Growth Rate (FY 25-26) in %', range=[-120, 500])  # crop bounds
div_bubble = plot(fig_bubble, include_plotlyjs=False, output_type='div')

# Plotly Chart 5: Opportunity Lost (Win-Back Pipeline)
lost_df = df[df['Status'] == 'Lost'].sort_values(by='FY_24_25', ascending=False).head(15)
fig_lost = go.Figure()
fig_lost.add_trace(go.Bar(
    x=lost_df['FY_24_25'],
    y=lost_df['Particulars'],
    orientation='h',
    marker=dict(
        color='rgba(239, 68, 68, 0.2)',
        line=dict(color=danger_color, width=1.5)
    ),
    hovertemplate="<b>%{y}</b><br>Recapturable Value: ₹%{x:,.2f}<extra></extra>"
))
fig_lost.update_layout(**dark_plotly_layout)
fig_lost.update_layout(
    title=dict(text="High-Value Win-back Opportunity Pipeline", font=dict(family='Outfit', size=16)),
    height=400
)
fig_lost.update_yaxes(autorange="reversed")
fig_lost.update_xaxes(title='Recapturable Annual Sales Volume (FY 24-25 Sales)')
div_lost = plot(fig_lost, include_plotlyjs=False, output_type='div')

# Calculate KPI labels
total_lost_val = df[df['Status'] == 'Lost']['FY_24_25'].sum()

# Plotly Chart 6: Slipping Revenue Leakage Pipeline (Ordering Less YoY)
slipping_df = df[(df['Status'] == 'Retained') & (df['FY_25_26'] < df['FY_24_25']) & (df['FY_24_25'] > 0)].copy()
slipping_df['Revenue_Drop'] = slipping_df['FY_24_25'] - slipping_df['FY_25_26']
slipping_df = slipping_df.sort_values(by='Revenue_Drop', ascending=False).head(15)

fig_slipping = go.Figure()
fig_slipping.add_trace(go.Bar(
    x=slipping_df['Revenue_Drop'],
    y=slipping_df['Particulars'],
    orientation='h',
    marker=dict(
        color='rgba(249, 115, 22, 0.2)',
        line=dict(color='#f97316', width=1.5)
    ),
    hovertemplate="<b>%{y}</b><br>Revenue Drop: ₹%{x:,.2f}<br>FY 24-25: ₹%{customdata[0]:,.2f}<br>FY 25-26: ₹%{customdata[1]:,.2f}<extra></extra>",
    customdata=np.stack((slipping_df['FY_24_25'], slipping_df['FY_25_26']), axis=-1)
))
fig_slipping.update_layout(**dark_plotly_layout)
fig_slipping.update_layout(
    title=dict(text="Top 15 Active Slipping Customer Accounts", font=dict(family='Outfit', size=16)),
    height=400
)
fig_slipping.update_yaxes(autorange="reversed")
fig_slipping.update_xaxes(title='Year-over-Year Revenue Decelerated (FY 24-25 to FY 25-26 Drop)')
div_slipping = plot(fig_slipping, include_plotlyjs=False, output_type='div')

# Calculate KPI labels for Slipping
total_slipping_val = df[(df['Status'] == 'Retained') & (df['FY_25_26'] < df['FY_24_25']) & (df['FY_24_25'] > 0)].copy()
total_slipping_val['Revenue_Drop'] = total_slipping_val['FY_24_25'] - total_slipping_val['FY_25_26']
slipping_revenue_leakage = total_slipping_val['Revenue_Drop'].sum()
slipping_accounts_count = len(total_slipping_val)

print("[Plotly] Interactive components generated successfully.")

# ---------------------------------------------------------
# 4. Generate Premium HTML Dashboard
# ---------------------------------------------------------
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Plotly Executive Dashboard</title>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Plotly CDN JS -->
    <script src="https://cdn.plot.ly/plotly-2.24.1.min.js"></script>
    
    <style>
        :root {{
            --bg-base: #080c14;
            --bg-card: rgba(15, 23, 42, 0.55);
            --border-color: rgba(255, 255, 255, 0.08);
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.15);
            --violet: #8b5cf6;
            --pink: #ec4899;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }}

        body {{
            background-color: var(--bg-base);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 5% 5%, rgba(99, 102, 241, 0.06) 0%, transparent 40%),
                radial-gradient(circle at 95% 95%, rgba(236, 72, 153, 0.06) 0%, transparent 40%);
            background-attachment: fixed;
            padding-bottom: 3rem;
        }}

        header {{
            background: rgba(8, 12, 20, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 1.5rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo-section h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.6rem;
            font-weight: 800;
            background: linear-gradient(135deg, #a5b4fc 0%, var(--primary) 50%, var(--violet) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.5px;
        }}

        .logo-section p {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 2px;
            letter-spacing: 1.2px;
            text-transform: uppercase;
            font-weight: 500;
        }}

        .header-action-badge {{
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid rgba(99, 102, 241, 0.2);
            color: #a5b4fc;
            padding: 0.5rem 1rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        main {{
            max-width: 1440px;
            margin: 0 auto;
            padding: 2rem;
        }}

        /* KPI grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        .kpi-card {{
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: rgba(99, 102, 241, 0.3);
            box-shadow: 0 10px 25px -10px rgba(0, 0, 0, 0.5);
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 4px;
            height: 100%;
            background: var(--primary);
        }}

        .kpi-card.violet::before {{ background: var(--violet); }}
        .kpi-card.emerald::before {{ background: var(--success); }}
        .kpi-card.coral::before {{ background: var(--danger); }}
        .kpi-card.orange::before {{ background: #f97316; }}

        .kpi-label {{
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }}

        .kpi-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 0.25rem;
        }}

        .kpi-subtext {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        /* Layout Grids */
        .grid-half {{
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        .grid-equal {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}

        @media (max-width: 1024px) {{
            .grid-half, .grid-equal {{
                grid-template-columns: 1fr;
            }}
        }}

        .chart-card {{
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1.5rem;
            position: relative;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }}

        .chart-card-full {{
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        }}

        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .card-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: #fff;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .card-desc {{
            font-size: 0.75rem;
            color: var(--text-secondary);
        }}

        .badge {{
            padding: 0.25rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }}
        .badge-primary {{
            background: rgba(99, 102, 241, 0.1);
            color: var(--primary);
            border: 1px solid rgba(99, 102, 241, 0.2);
        }}
        .badge-danger {{
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.2);
        }}

        .insight-text {{
            font-size: 0.85rem;
            line-height: 1.5;
            color: var(--text-secondary);
            margin-top: 1rem;
            padding-top: 0.75rem;
            border-top: 1px solid rgba(255, 255, 255, 0.03);
        }}

        .highlight {{
            color: #fff;
            font-weight: 500;
        }}
    </style>
</head>
<body>

    <header>
        <div class="logo-section">
            <h1>Sales Intelligence Center</h1>
            <p>Interactive Plotly Engine (3 Years consolidated)</p>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
            <a href="dashboard.html" style="text-decoration: none; color: #fff; background: var(--primary); padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.8rem; font-weight: 600; box-shadow: 0 4px 10px rgba(99, 102, 241, 0.2); transition: all 0.3s ease;">
                Go to Interactive Ledger Explorer & Uploader &rarr;
            </a>
            <div class="header-action-badge">
                <span style="display:inline-block; width: 8px; height: 8px; background: var(--success); border-radius: 50%; box-shadow: 0 0 8px var(--success);"></span>
                Plotly Engine Active
            </div>
        </div>
    </header>

    <main>
        <!-- KPI Cards -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Cumulative Sales volume</div>
                <div class="kpi-value">{format_currency_in(totals['Cumulative'])}</div>
                <div class="kpi-subtext">Unified Outward Turnover</div>
            </div>
            <div class="kpi-card violet">
                <div class="kpi-label">FY 25-26 Sales</div>
                <div class="kpi-value">{format_currency_in(totals['FY_25_26'])}</div>
                <div class="kpi-subtext">Latest Year Total Sales</div>
            </div>
            <div class="kpi-card emerald">
                <div class="kpi-label">Total Unique Accounts</div>
                <div class="kpi-value">{counts['total_clients']}</div>
                <div class="kpi-subtext">{counts['retained']} Retained repeat clients</div>
            </div>
            <div class="kpi-card coral">
                <div class="kpi-label">Opportunity Lost Pipeline</div>
                <div class="kpi-value">{format_currency_in(total_lost_val)}</div>
                <div class="kpi-subtext">{counts['lost']} Churned dropouts</div>
            </div>
            <div class="kpi-card orange">
                <div class="kpi-label">Slipping Revenue Leakage</div>
                <div class="kpi-value">{format_currency_in(slipping_revenue_leakage)}</div>
                <div class="kpi-subtext">{slipping_accounts_count} Slipping active repeat accounts</div>
            </div>
        </div>

        <!-- Row 1: Line Trajectory and Segment Doughnut -->
        <div class="grid-half">
            <div class="chart-card">
                <div class="card-header">
                    <div class="card-title">📉 Annual Sales Trajectory</div>
                    <span class="badge badge-primary">Interactive Zoom</span>
                </div>
                {div_traj}
                <div class="insight-text">
                    Sales rose steadily from <span class="highlight">{format_currency_in(totals['FY_23_24'])}</span> in FY 23-24 to <span class="highlight">{format_currency_in(totals['FY_24_25'])}</span> in FY 24-25 (+14.5%), maintaining a positive growth trajectory of <span class="highlight">+1.7%</span> into FY 25-26 to reach <span class="highlight">{format_currency_in(totals['FY_25_26'])}</span>.
                </div>
            </div>
            <div class="chart-card">
                <div class="card-header">
                    <div class="card-title">🍰 Client Segment Share</div>
                    <span class="badge badge-primary">Interactive Legend</span>
                </div>
                {div_dist}
                <div class="insight-text">
                    Out of {counts['total_clients']} accounts, <span class="highlight">{(counts['retained']/counts['total_clients']*100):.1f}%</span> are successfully retained. <span class="highlight">{(counts['lost']/counts['total_clients']*100):.1f}%</span> are churned accounts representing lost pipeline revenue that can be actively targeted for win-back campaigns.
                </div>
            </div>
        </div>

        <!-- Row 2: Top 15 Stacked and bubble charts -->
        <div class="grid-equal">
            <div class="chart-card">
                <div class="card-header">
                    <div class="card-title">🏆 Top 15 Customer Outward Contribution</div>
                    <span class="badge badge-primary">Hover segments</span>
                </div>
                {div_top}
                <div class="insight-text">
                    The biggest buyer is <span class="highlight">{top_15.iloc[0]['Particulars']}</span> contributing <span class="highlight">{format_currency_in(top_15.iloc[0]['Total_Sales'])}</span> lifetime sales, followed by <span class="highlight">{top_15.iloc[1]['Particulars']}</span>. Plotly's stacked view lets you hover to see the exact annual split of each client account.
                </div>
            </div>
            <div class="chart-card">
                <div class="card-header">
                    <div class="card-title">📊 YoY Growth Rate vs. Cumulative Customer Sales Volume</div>
                    <span class="badge badge-primary">Box Zoom Enabled</span>
                </div>
                {div_bubble}
                <div class="insight-text">
                    <strong style="color: #fff;">How to read this bubble plot:</strong> larger right-side bubbles are higher lifetime revenue clients. The Y-Axis represents latest year growth rate: bubbles above 0% are growing repeat clients, while bubbles below 0% are slipping repeat clients. Bubble sizes scale with FY 25-26 volume.
                </div>
            </div>
        </div>

        <!-- Row 3: Revenue Leakage and Win-Back Opportunity Pipelines -->
        <div class="grid-equal">
            <div class="chart-card">
                <div class="card-header">
                    <div class="card-title">Opportunity Lost Win-Back Pipeline</div>
                    <span class="badge badge-danger">High opportunity</span>
                </div>
                {div_lost}
                <div class="insight-text">
                    These are your highest value lost opportunity accounts. Recovering even the top 3 (e.g. <span class="highlight">{lost_df.iloc[0]['Particulars']}</span>, <span class="highlight">{lost_df.iloc[1]['Particulars']}</span>, and <span class="highlight">{lost_df.iloc[2]['Particulars']}</span>) would instantly inject over <span class="highlight">₹7.5 Lakhs</span> back into latest fiscal year sales.
                </div>
            </div>
            <div class="chart-card">
                <div class="card-header">
                    <div class="card-title">⚠️ Slipping Revenue Leakage Pipeline</div>
                    <span class="badge badge-warning" style="background: rgba(249, 115, 22, 0.1); color: #f97316; border: 1px solid rgba(249, 115, 22, 0.2);">Slipping Revenue</span>
                </div>
                {div_slipping}
                <div class="insight-text">
                    These active repeat accounts have the largest year-over-year sales volume decline. Re-engaging the top slipping accounts (e.g. <span class="highlight">{slipping_df.iloc[0]['Particulars'] if len(slipping_df) > 0 else 'N/A'}</span>, <span class="highlight">{slipping_df.iloc[1]['Particulars'] if len(slipping_df) > 1 else 'N/A'}</span>) can quickly recover up to <span class="highlight">₹27.04 Lakhs</span> in decel sales.
                </div>
            </div>
        </div>
    </main>

</body>
</html>
"""

# Write HTML file
with open("plotly_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("[Plotly] standalone dashboard 'plotly_dashboard.html' generated successfully.")
