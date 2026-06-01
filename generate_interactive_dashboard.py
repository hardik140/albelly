import json
import os

json_path = r"e:\albelly\sales_data_consolidated.json"
html_path = r"e:\albelly\dashboard.html"

print("Generating premium interactive sales dashboard...")

# Load the consolidated JSON data
with open(json_path, "r") as f:
    sales_data = json.load(f)

# Convert to a JS object
js_data = json.dumps(sales_data)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Performance Dashboard</title>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <style>
        :root {{
            --bg-base: #0b0f19;
            --bg-card: rgba(17, 24, 39, 0.7);
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
            scrollbar-width: thin;
            scrollbar-color: var(--border-color) transparent;
        }}

        body {{
            background-color: var(--bg-base);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(99, 102, 241, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(236, 72, 153, 0.05) 0%, transparent 40%);
            background-attachment: fixed;
        }}

        header {{
            background: rgba(11, 15, 25, 0.8);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            padding: 1.25rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .logo-section h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
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
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .nav-tabs {{
            display: flex;
            gap: 0.5rem;
        }}

        .tab-btn {{
            background: transparent;
            border: 1px solid transparent;
            color: var(--text-secondary);
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            font-size: 0.875rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .tab-btn:hover {{
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.03);
            border-color: var(--border-color);
        }}

        .tab-btn.active {{
            color: #fff;
            background: var(--primary);
            border-color: var(--primary);
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
        }}

        main {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }}

        /* KPI grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
            cursor: pointer;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.3s ease, box-shadow 0.3s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-4px) scale(1.02);
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 12px 24px rgba(99, 102, 241, 0.15);
        }}

        .kpi-card::after {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--primary);
        }}

        .kpi-card.purple::after {{ background: var(--violet); }}
        .kpi-card.pink::after {{ background: var(--pink); }}
        .kpi-card.success::after {{ background: var(--success); }}

        .kpi-label {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            font-weight: 500;
        }}

        .kpi-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.85rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
            color: #fff;
        }}

        .kpi-growth {{
            font-size: 0.75rem;
            display: flex;
            align-items: center;
            gap: 4px;
            font-weight: 600;
        }}

        .kpi-growth.up {{ color: var(--success); }}
        .kpi-growth.down {{ color: var(--danger); }}
        .kpi-growth.neutral {{ color: var(--text-secondary); }}

        /* Interactive banner for Filtered Sales */
        .filtered-stats-banner {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            animation: fadeIn 0.4s ease forwards;
        }}

        .filtered-stats-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .filtered-stats-value {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 700;
            color: #fff;
            background: linear-gradient(135deg, #a5b4fc 0%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        /* Dashboard Section Layout */
        .dashboard-section {{
            display: none;
            animation: fadeIn 0.4s ease forwards;
        }}

        .dashboard-section.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Grid for main charts */
        .chart-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        @media (max-width: 1024px) {{
            .chart-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .chart-card {{
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            min-height: 380px;
        }}

        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 0.75rem;
        }}

        .chart-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: #fff;
        }}

        .chart-subtitle {{
            font-size: 0.8125rem;
            color: var(--text-secondary);
            margin-bottom: 1.25rem;
        }}

        /* Table & Data Explorer */
        .table-card {{
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
        }}

        .table-controls {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 1.25rem;
        }}

        .search-wrapper {{
            position: relative;
            flex-grow: 1;
            max-width: 400px;
        }}

        .search-input {{
            width: 100%;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 0.65rem 1rem 0.65rem 2.5rem;
            color: #fff;
            font-size: 0.875rem;
            outline: none;
            transition: all 0.3s ease;
        }}

        .search-input:focus {{
            border-color: var(--primary);
            background: rgba(99, 102, 241, 0.03);
            box-shadow: 0 0 10px rgba(99, 102, 241, 0.1);
        }}

        .search-icon {{
            position: absolute;
            left: 0.85rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-secondary);
            pointer-events: none;
        }}

        .filters-wrapper {{
            display: flex;
            gap: 0.75rem;
        }}

        .select-filter {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 0.65rem 1.25rem;
            color: #fff;
            font-size: 0.875rem;
            outline: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .select-filter:focus {{
            border-color: var(--primary);
        }}

        .select-filter option {{
            background: #0f172a;
            color: #fff;
        }}

        .action-btn {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            color: var(--text-primary);
            padding: 0.65rem 1.25rem;
            font-size: 0.875rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .action-btn:hover {{
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--text-secondary);
        }}

        .table-responsive {{
            width: 100%;
            overflow-x: auto;
            margin-bottom: 1rem;
            border-radius: 12px;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}

        th {{
            background: rgba(255, 255, 255, 0.02);
            color: var(--text-secondary);
            font-size: 0.75rem;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.5px;
            padding: 1rem;
            border-bottom: 1px solid var(--border-color);
            cursor: pointer;
            user-select: none;
        }}

        th:hover {{
            color: #fff;
            background: rgba(255, 255, 255, 0.04);
        }}

        td {{
            padding: 1rem;
            font-size: 0.875rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            color: var(--text-primary);
            max-width: 250px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        tr {{
            cursor: pointer;
            transition: background 0.2s ease;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.015);
            color: #fff;
        }}

        .badge {{
            padding: 0.25rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
        }}

        .badge-retained {{
            background: rgba(16, 185, 129, 0.1);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }}

        .badge-new {{
            background: rgba(99, 102, 241, 0.1);
            color: var(--primary);
            border: 1px solid rgba(99, 102, 241, 0.2);
        }}

        .badge-lost {{
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.2);
        }}

        .badge-inactive {{
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning);
            border: 1px solid rgba(245, 158, 11, 0.2);
        }}

        /* Pagination */
        .pagination {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 1rem;
            border-top: 1px solid rgba(255, 255, 255, 0.04);
        }}

        .pagination-info {{
            font-size: 0.8125rem;
            color: var(--text-secondary);
        }}

        .pagination-buttons {{
            display: flex;
            gap: 0.5rem;
        }}

        .page-btn {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.875rem;
        }}

        .page-btn:hover:not(:disabled) {{
            background: rgba(255, 255, 255, 0.08);
            border-color: var(--text-secondary);
        }}

        .page-btn:disabled {{
            opacity: 0.4;
            cursor: not-allowed;
        }}

        .page-btn.active {{
            background: var(--primary);
            border-color: var(--primary);
            color: #fff;
        }}

        /* Missed opportunities panel */
        .missed-opportunities-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}

        @media (max-width: 900px) {{
            .missed-opportunities-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .missed-list-card {{
            background: var(--bg-card);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
        }}

        .missed-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.04);
            transition: all 0.2s ease;
        }}

        .missed-item:hover {{
            background: rgba(255, 255, 255, 0.015);
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            border-radius: 8px;
        }}

        .missed-item:last-child {{
            border-bottom: none;
        }}

        .missed-client-name {{
            font-weight: 500;
            color: #fff;
        }}

        .missed-lost-value {{
            font-family: 'Outfit', sans-serif;
            font-weight: 600;
            color: var(--danger);
        }}

        .missed-sub {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-top: 2px;
        }}

        /* Modal styling */
        .modal {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(8px);
            z-index: 1000;
            justify-content: center;
            align-items: center;
            animation: fadeIn 0.2s ease forwards;
        }}

        .modal-content {{
            background: #0f172a;
            border: 1px solid var(--border-color);
            border-radius: 20px;
            width: 90%;
            max-width: 600px;
            padding: 2rem;
            position: relative;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}

        @keyframes slideUp {{
            from {{ transform: translateY(20px) scale(0.95); opacity: 0; }}
            to {{ transform: translateY(0) scale(1); opacity: 1; }}
        }}

        .close-modal {{
            position: absolute;
            top: 1.25rem;
            right: 1.25rem;
            font-size: 1.5rem;
            color: var(--text-secondary);
            cursor: pointer;
            transition: color 0.3s ease;
        }}

        .close-modal:hover {{
            color: #fff;
        }}

        .modal-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.35rem;
            font-weight: 700;
            color: #fff;
            margin-bottom: 0.5rem;
        }}

        .modal-subtitle {{
            font-size: 0.8125rem;
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .client-metric-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}

        .client-metric-card {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 0.85rem;
            text-align: center;
        }}

        .client-metric-lbl {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-bottom: 0.25rem;
        }}

        .client-metric-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.15rem;
            font-weight: 600;
            color: #fff;
        }}

        .client-metric-growth {{
            font-size: 0.7rem;
            font-weight: 700;
            margin-top: 4px;
        }}
    </style>
</head>
<body>

    <header>
        <div class="logo-section">
            <h1>Sales Performance Hub</h1>
            <p>Unified Ledger Analysis (3 Years)</p>
        </div>
        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('dashboard', this)">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2H6a2 2 0 01-2-2v-4zM14 16a2 2 0 012-2h2a2 2 0 012 2v4a2 2 0 01-2 2h-2a2 2 0 01-2-2v-4z"></path></svg>
                Dashboard
            </button>
            <button class="tab-btn" onclick="switchTab('ledger', this)">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path></svg>
                Client Ledger
            </button>
            <button class="tab-btn" onclick="switchTab('missed', this)">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                Missed Opportunities
            </button>
        </div>
    </header>

    <main>
        <!-- KPI Cards Grid -->
        <div class="kpi-grid">
            <div class="kpi-card" onclick="handleKpiClick('ALL', 'Total_Sales')">
                <div class="kpi-label">Cumulative Sales (All Years)</div>
                <div class="kpi-value" id="kpi-cumulative">₹0.00</div>
                <div class="kpi-growth neutral">Click to view Ledger</div>
            </div>
            <div class="kpi-card purple" onclick="handleKpiClick('ALL', 'FY_23_24')">
                <div class="kpi-label">FY 23-24 Total Sales</div>
                <div class="kpi-value" id="kpi-y1">₹0.00</div>
                <div class="kpi-growth neutral">Click to sort by 23-24</div>
            </div>
            <div class="kpi-card pink" onclick="handleKpiClick('ALL', 'FY_24_25')">
                <div class="kpi-label">FY 24-25 Total Sales</div>
                <div class="kpi-value" id="kpi-y2">₹0.00</div>
                <div class="kpi-growth up" id="kpi-growth-y2">
                    <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 10l7-7 7 7M12 3v18"></path></svg>
                    0.0% vs FY 23-24
                </div>
            </div>
            <div class="kpi-card success" onclick="handleKpiClick('ALL', 'FY_25_26')">
                <div class="kpi-label">FY 25-26 Total Sales</div>
                <div class="kpi-value" id="kpi-y3">₹0.00</div>
                <div class="kpi-growth up" id="kpi-growth-y3">
                    <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M5 10l7-7 7 7M12 3v18"></path></svg>
                    0.0% vs FY 24-25
                </div>
            </div>
        </div>

        <!-- TAB 1: EXECUTIVE DASHBOARD -->
        <div id="section-dashboard" class="dashboard-section active">
            <div class="chart-grid">
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Year-over-Year Growth Trajectory</div>
                    </div>
                    <div class="chart-subtitle">Overall annual outward sales volume trends</div>
                    <div style="height: 300px; position: relative;">
                        <canvas id="trajectoryChart"></canvas>
                    </div>
                </div>
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Customer Distribution</div>
                    </div>
                    <div class="chart-subtitle">Click slices to filter client ledger</div>
                    <div style="height: 300px; position: relative; display: flex; align-items: center; justify-content: center;">
                        <canvas id="distributionChart" style="max-height: 260px; max-width: 260px; cursor: pointer;"></canvas>
                    </div>
                </div>
            </div>

            <div class="chart-card" style="margin-bottom: 2rem; min-height: auto;">
                <div class="chart-header">
                    <div class="chart-title">Top 15 Selling Particulars (Lifetime Revenue)</div>
                </div>
                <div class="chart-subtitle">Click on any bar to open deep-dive client metrics</div>
                <div style="height: 380px; position: relative;">
                    <canvas id="topParticularsChart" style="cursor: pointer;"></canvas>
                </div>
            </div>
        </div>

        <!-- TAB 2: CLIENT LEDGER EXPLORER -->
        <div id="section-ledger" class="dashboard-section">
            <!-- Interactivity Feature: Filtered Sales Banner -->
            <div class="filtered-stats-banner">
                <div class="filtered-stats-title" id="filtered-stats-label">Filtered Accounts Summary</div>
                <div class="filtered-stats-value" id="filtered-sales-sum">₹0.00</div>
            </div>

            <div class="table-card">
                <div class="table-controls">
                    <div class="search-wrapper">
                        <span class="search-icon">
                            <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                        </span>
                        <input type="text" class="search-input" id="search-bar" placeholder="Search by Particulars name..." oninput="handleSearch()">
                    </div>
                    <div class="filters-wrapper">
                        <select class="select-filter" id="status-filter" onchange="handleFilter()">
                            <option value="ALL">All Accounts</option>
                            <option value="Retained">Retained Accounts</option>
                            <option value="New">New Accounts (FY 25-26)</option>
                            <option value="Lost">Lost Accounts (FY 25-26 Churn)</option>
                            <option value="Inactive">Inactive Accounts (Historical)</option>
                        </select>
                        <button class="action-btn" onclick="exportCSV()">
                            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                            Export CSV
                        </button>
                    </div>
                </div>

                <div class="table-responsive">
                    <table>
                        <thead>
                            <tr>
                                <th onclick="handleSort('Particulars')">Particulars</th>
                                <th onclick="handleSort('Status')" style="text-align: center;">Status</th>
                                <th onclick="handleSort('FY_23_24')" style="text-align: right;">FY 23-24</th>
                                <th onclick="handleSort('FY_24_25')" style="text-align: right;">FY 24-25</th>
                                <th onclick="handleSort('FY_25_26')" style="text-align: right;">FY 25-26</th>
                                <th onclick="handleSort('Total_Sales')" style="text-align: right;">Total Sales</th>
                            </tr>
                        </thead>
                        <tbody id="ledger-table-body">
                            <!-- Injected dynamically -->
                        </tbody>
                    </table>
                </div>

                <div class="pagination">
                    <div class="pagination-info" id="pagination-info">Showing 0-0 of 0 accounts</div>
                    <div class="pagination-buttons" id="pagination-buttons">
                        <!-- Buttons injected dynamically -->
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 3: MISSED OPPORTUNITIES -->
        <div id="section-missed" class="dashboard-section">
            <div style="background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.15); border-radius: 12px; padding: 1.25rem; margin-bottom: 2rem; display: flex; align-items: flex-start; gap: 1rem;">
                <span style="color: var(--danger); font-size: 1.5rem; margin-top: 2px;">⚠️</span>
                <div>
                    <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 600; color: #fff; margin-bottom: 0.25rem;">Missed Opportunities Analysis</h3>
                    <p style="font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5;">This tab isolates accounts that had sales volumes historically in <strong>FY 23-24</strong> or <strong>FY 24-25</strong>, but recorded <strong>₹0.00 sales in FY 25-26</strong>. Re-engaging these customers could reclaim lost revenue quickly.</p>
                </div>
            </div>

            <div class="missed-opportunities-grid">
                <div class="missed-list-card">
                    <h3 class="chart-title" style="margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem; color: var(--danger);">
                        🔴 Recent High-Value Dropouts (Active in 24-25, Lost in 25-26)
                    </h3>
                    <div id="lost-list-container" style="max-height: 480px; overflow-y: auto; padding-right: 0.5rem;">
                        <!-- Injected dynamically -->
                    </div>
                </div>

                <div class="missed-list-card">
                    <h3 class="chart-title" style="margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem; color: var(--warning);">
                        🟠 Older Historical Dropouts (Active in 23-24, Inactive since)
                    </h3>
                    <div id="inactive-list-container" style="max-height: 480px; overflow-y: auto; padding-right: 0.5rem;">
                        <!-- Injected dynamically -->
                    </div>
                </div>
            </div>
        </div>
    </main>

    <!-- Client Detail Modal -->
    <div class="modal" id="client-modal" onclick="closeModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <span class="close-modal" onclick="closeModal(null)">&times;</span>
            <div class="modal-title" id="modal-client-name">CLIENT NAME</div>
            <div class="modal-subtitle" id="modal-client-status">STATUS</div>
            
            <div class="client-metric-grid">
                <div class="client-metric-card">
                    <div class="client-metric-lbl">FY 23-24</div>
                    <div class="client-metric-val" id="modal-metric-y1">₹0.00</div>
                    <div class="client-metric-growth neutral" style="color: var(--text-secondary);">Base Year</div>
                </div>
                <div class="client-metric-card">
                    <div class="client-metric-lbl">FY 24-25</div>
                    <div class="client-metric-val" id="modal-metric-y2">₹0.00</div>
                    <div class="client-metric-growth" id="modal-metric-growth-y2">0.0%</div>
                </div>
                <div class="client-metric-card">
                    <div class="client-metric-lbl">FY 25-26</div>
                    <div class="client-metric-val" id="modal-metric-y3">₹0.00</div>
                    <div class="client-metric-growth" id="modal-metric-growth-y3">0.0%</div>
                </div>
            </div>

            <div style="height: 250px; position: relative;">
                <canvas id="clientTrendChart"></canvas>
            </div>
        </div>
    </div>

    <!-- Data Injection -->
    <script>
        const salesData = {js_data};
        const records = salesData.records;
        
        // Global State
        let currentPage = 1;
        const rowsPerPage = 12;
        let filteredRecords = [...records];
        let currentSearchQuery = "";
        let currentStatusFilter = "ALL";
        let currentSortColumn = "Total_Sales";
        let currentSortDirection = "desc";
        
        let trajectoryChartInst = null;
        let distributionChartInst = null;
        let topParticularsChartInst = null;
        let clientTrendChartInst = null;

        // Initialize App
        window.addEventListener('DOMContentLoaded', () => {{
            updateKPIs();
            renderDashboardCharts();
            applyFilters(); // Trigger filters rendering table & subsets
            renderMissedOpportunities();
        }});

        function formatCurrency(val) {{
            return new Intl.NumberFormat('en-IN', {{
                style: 'currency',
                currency: 'INR',
                maximumFractionDigits: 2
            }}).format(val);
        }}

        function updateKPIs() {{
            const totals = salesData.totals;
            document.getElementById('kpi-cumulative').innerText = formatCurrency(totals.Cumulative);
            document.getElementById('kpi-y1').innerText = formatCurrency(totals.FY_23_24);
            document.getElementById('kpi-y2').innerText = formatCurrency(totals.FY_24_25);
            document.getElementById('kpi-y3').innerText = formatCurrency(totals.FY_25_26);

            // YoY growth rates
            const g_y2 = ((totals.FY_24_25 - totals.FY_23_24) / totals.FY_23_24) * 100;
            const g_y3 = ((totals.FY_25_26 - totals.FY_24_25) / totals.FY_24_25) * 100;

            const growthY2El = document.getElementById('kpi-growth-y2');
            growthY2El.className = g_y2 >= 0 ? "kpi-growth up" : "kpi-growth down";
            growthY2El.innerHTML = (g_y2 >= 0 ? '▲' : '▼') + ` ${{Math.abs(g_y2).toFixed(1)}}% vs FY 23-24`;

            const growthY3El = document.getElementById('kpi-growth-y3');
            growthY3El.className = g_y3 >= 0 ? "kpi-growth up" : "kpi-growth down";
            growthY3El.innerHTML = (g_y3 >= 0 ? '▲' : '▼') + ` ${{Math.abs(g_y3).toFixed(1)}}% vs FY 24-25`;
        }}

        // Interactive KPI Click logic
        function handleKpiClick(statusFilter, sortCol) {{
            // Switch to ledger tab
            const btn = document.querySelector('button[onclick*="ledger"]');
            switchTab('ledger', btn);
            
            // Set filter dropdown and filter value
            document.getElementById('status-filter').value = statusFilter;
            currentStatusFilter = statusFilter;
            
            // Set sort details
            currentSortColumn = sortCol;
            currentSortDirection = "desc";
            
            // Apply
            applyFilters();
        }}

        function renderDashboardCharts() {{
            const totals = salesData.totals;
            const counts = salesData.counts;

            // 1. Line Trajectory
            const ctx1 = document.getElementById('trajectoryChart').getContext('2d');
            trajectoryChartInst = new Chart(ctx1, {{
                type: 'line',
                data: {{
                    labels: ['FY 23-24', 'FY 24-25', 'FY 25-26'],
                    datasets: [{{
                        label: 'Annual Outward Sales',
                        data: [totals.FY_23_24, totals.FY_24_25, totals.FY_25_26],
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.1)',
                        fill: true,
                        tension: 0.3,
                        borderWidth: 3,
                        pointBackgroundColor: '#8b5cf6',
                        pointRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return 'Sales: ' + formatCurrency(context.raw);
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{ color: '#9ca3af', callback: function(value) {{ return '₹' + (value/100000).toFixed(0) + 'L'; }} }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}
                        }},
                        x: {{
                            ticks: {{ color: '#9ca3af' }},
                            grid: {{ display: false }}
                        }}
                    }}
                }}
            }});

            // 2. Doughnut Distribution (Interactive segment click)
            const ctx2 = document.getElementById('distributionChart').getContext('2d');
            distributionChartInst = new Chart(ctx2, {{
                type: 'doughnut',
                data: {{
                    labels: ['Retained', 'New clients', 'Lost (Missed)', 'Inactive'],
                    datasets: [{{
                        data: [counts.retained_active, counts.new_active, counts.lost_active, counts.inactive_active],
                        backgroundColor: ['#10b981', '#6366f1', '#ef4444', '#f59e0b'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    onClick: (event, activeElements) => {{
                        if (activeElements.length > 0) {{
                            const index = activeElements[0].index;
                            const label = distributionChartInst.data.labels[index];
                            
                            let filterValue = "ALL";
                            if (label === 'Retained') filterValue = 'Retained';
                            else if (label === 'New clients') filterValue = 'New';
                            else if (label === 'Lost (Missed)') filterValue = 'Lost';
                            else if (label === 'Inactive') filterValue = 'Inactive';
                            
                            handleKpiClick(filterValue, 'Total_Sales');
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            position: 'right',
                            labels: {{ color: '#e5e7eb', boxWidth: 12, font: {{ size: 11 }} }}
                        }}
                    }}
                }}
            }});

            // 3. Top Particulars Bar Chart (Interactive bar click)
            const topRecords = [...records].slice(0, 15);
            const ctx3 = document.getElementById('topParticularsChart').getContext('2d');
            topParticularsChartInst = new Chart(ctx3, {{
                type: 'bar',
                data: {{
                    labels: topRecords.map(r => r.Particulars),
                    datasets: [
                        {{
                            label: 'FY 23-24',
                            data: topRecords.map(r => r.FY_23_24),
                            backgroundColor: '#8b5cf6'
                        }},
                        {{
                            label: 'FY 24-25',
                            data: topRecords.map(r => r.FY_24_25),
                            backgroundColor: '#ec4899'
                        }},
                        {{
                            label: 'FY 25-26',
                            data: topRecords.map(r => r.FY_25_26),
                            backgroundColor: '#10b981'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    onClick: (event, activeElements) => {{
                        if (activeElements.length > 0) {{
                            const index = activeElements[0].index;
                            const clientName = topParticularsChartInst.data.labels[index];
                            const client = records.find(r => r.Particulars === clientName);
                            if (client) {{
                                openModal(client);
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{ position: 'top', labels: {{ color: '#9ca3af' }} }},
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    return context.dataset.label + ': ' + formatCurrency(context.raw);
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            stacked: true,
                            ticks: {{ color: '#9ca3af', callback: function(value) {{ return '₹' + (value/100000).toFixed(0) + 'L'; }} }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}
                        }},
                        x: {{
                            stacked: true,
                            ticks: {{ color: '#9ca3af', font: {{ size: 9 }} }},
                            grid: {{ display: false }}
                        }}
                    }}
                }}
            }});
        }}

        function switchTab(tabId, el) {{
            // Deactivate tabs
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.dashboard-section').forEach(sect => sect.classList.remove('active'));
            
            // Activate current
            el.classList.add('active');
            document.getElementById('section-' + tabId).classList.add('active');
        }}

        // Search and filter logic
        function handleSearch() {{
            currentSearchQuery = document.getElementById('search-bar').value.toUpperCase().trim();
            currentPage = 1;
            applyFilters();
        }}

        function handleFilter() {{
            currentStatusFilter = document.getElementById('status-filter').value;
            currentPage = 1;
            applyFilters();
        }}

        function applyFilters() {{
            filteredRecords = records.filter(r => {{
                const matchesSearch = r.Particulars.includes(currentSearchQuery);
                const matchesStatus = currentStatusFilter === "ALL" || r.Status === currentStatusFilter;
                return matchesSearch && matchesStatus;
            }});
            
            // Interactivity Feature: Update Filtered Sum
            const filteredSum = filteredRecords.reduce((sum, r) => sum + r.Total_Sales, 0);
            const statusLabelText = currentStatusFilter === "ALL" ? "All Accounts" : `${{currentStatusFilter}} Accounts`;
            const searchLabelText = currentSearchQuery ? ` matching "${{currentSearchQuery}}"` : "";
            document.getElementById('filtered-stats-label').innerText = `Sales Volume for ${{statusLabelText}}${{searchLabelText}} (${{filteredRecords.length}} active):`;
            document.getElementById('filtered-sales-sum').innerText = formatCurrency(filteredSum);
            
            sortRecords();
            renderTable();
        }}

        function handleSort(column) {{
            if (currentSortColumn === column) {{
                currentSortDirection = currentSortDirection === "asc" ? "desc" : "asc";
            }} else {{
                currentSortColumn = column;
                currentSortDirection = "desc"; // Default high to low
            }}
            sortRecords();
            renderTable();
        }}

        function sortRecords() {{
            filteredRecords.sort((a, b) => {{
                let valA = a[currentSortColumn];
                let valB = b[currentSortColumn];
                
                if (typeof valA === "string") {{
                    valA = valA.toLowerCase();
                    valB = valB.toLowerCase();
                }}
                
                if (valA < valB) return currentSortDirection === "asc" ? -1 : 1;
                if (valA > valB) return currentSortDirection === "asc" ? 1 : -1;
                return 0;
            }});
        }}

        function renderTable() {{
            const tbody = document.getElementById('ledger-table-body');
            tbody.innerHTML = "";

            const totalRecords = filteredRecords.length;
            const startIdx = (currentPage - 1) * rowsPerPage;
            const endIdx = Math.min(startIdx + rowsPerPage, totalRecords);

            if (totalRecords === 0) {{
                tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding: 2rem; color: var(--text-secondary);">No client records found.</td></tr>`;
                document.getElementById('pagination-info').innerText = "Showing 0 of 0 accounts";
                document.getElementById('pagination-buttons').innerHTML = "";
                return;
            }}

            const pageData = filteredRecords.slice(startIdx, endIdx);
            pageData.forEach(r => {{
                const tr = document.createElement('tr');
                tr.onclick = () => openModal(r);
                tr.innerHTML = `
                    <td style="font-weight: 500; color: #fff;">${{r.Particulars}}</td>
                    <td style="text-align: center;"><span class="badge badge-${{r.Status.toLowerCase()}}">${{r.Status}}</span></td>
                    <td style="text-align: right;">${{formatCurrency(r.FY_23_24)}}</td>
                    <td style="text-align: right;">${{formatCurrency(r.FY_24_25)}}</td>
                    <td style="text-align: right;">${{formatCurrency(r.FY_25_26)}}</td>
                    <td style="text-align: right; font-weight: 600; color: #fff;">${{formatCurrency(r.Total_Sales)}}</td>
                `;
                tbody.appendChild(tr);
            }});

            // Update Pagination Info
            document.getElementById('pagination-info').innerText = `Showing ${{startIdx + 1}} - ${{endIdx}} of ${{totalRecords}} accounts`;
            renderPaginationButtons(totalRecords);
        }}

        function renderPaginationButtons(totalRecords) {{
            const totalPages = Math.ceil(totalRecords / rowsPerPage);
            const container = document.getElementById('pagination-buttons');
            container.innerHTML = "";

            const prevBtn = document.createElement('button');
            prevBtn.className = "page-btn";
            prevBtn.disabled = currentPage === 1;
            prevBtn.onclick = () => {{ currentPage--; renderTable(); }};
            prevBtn.innerHTML = "&larr;";
            container.appendChild(prevBtn);

            // Determine visible page numbers (max 5)
            let startPage = Math.max(1, currentPage - 2);
            let endPage = Math.min(totalPages, startPage + 4);
            if (endPage - startPage < 4) {{
                startPage = Math.max(1, endPage - 4);
            }}

            for (let i = startPage; i <= endPage; i++) {{
                const pageBtn = document.createElement('button');
                pageBtn.className = `page-btn ${{i === currentPage ? 'active' : ''}}`;
                pageBtn.innerText = i;
                pageBtn.onclick = () => {{ currentPage = i; renderTable(); }};
                container.appendChild(pageBtn);
            }}

            const nextBtn = document.createElement('button');
            nextBtn.className = "page-btn";
            nextBtn.disabled = currentPage === totalPages;
            nextBtn.onclick = () => {{ currentPage++; renderTable(); }};
            nextBtn.innerHTML = "&rarr;";
            container.appendChild(nextBtn);
        }}

        function renderMissedOpportunities() {{
            const lostList = records.filter(r => r.Status === "Lost").slice(0, 30);
            const inactiveList = records.filter(r => r.Status === "Inactive").slice(0, 30);

            const lostContainer = document.getElementById('lost-list-container');
            lostContainer.innerHTML = "";
            lostList.forEach(r => {{
                const item = document.createElement('div');
                item.className = "missed-item";
                item.onclick = () => openModal(r);
                item.style.cursor = "pointer";
                item.innerHTML = `
                    <div>
                        <div class="missed-client-name">${{r.Particulars}}</div>
                        <div class="missed-sub">Active in FY 24-25 (₹${{r.FY_24_25.toLocaleString('en-IN')}} outward volume)</div>
                    </div>
                    <div class="missed-lost-value">- ₹${{r.FY_24_25.toLocaleString('en-IN')}}</div>
                `;
                lostContainer.appendChild(item);
            }});

            const inactiveContainer = document.getElementById('inactive-list-container');
            inactiveContainer.innerHTML = "";
            inactiveList.forEach(r => {{
                const item = document.createElement('div');
                item.className = "missed-item";
                item.onclick = () => openModal(r);
                item.style.cursor = "pointer";
                item.innerHTML = `
                    <div>
                        <div class="missed-client-name">${{r.Particulars}}</div>
                        <div class="missed-sub">Active in FY 23-24 (₹${{r.FY_23_24.toLocaleString('en-IN')}} outward volume)</div>
                    </div>
                    <div class="missed-lost-value" style="color: var(--warning);">- ₹${{r.FY_23_24.toLocaleString('en-IN')}}</div>
                `;
                inactiveContainer.appendChild(item);
            }});
        }}

        // Modal triggers
        function openModal(client) {{
            document.getElementById('modal-client-name').innerText = client.Particulars;
            const statusEl = document.getElementById('modal-client-status');
            statusEl.innerText = client.Status;
            statusEl.className = `modal-subtitle badge badge-${{client.Status.toLowerCase()}}`;
            
            document.getElementById('modal-metric-y1').innerText = formatCurrency(client.FY_23_24);
            document.getElementById('modal-metric-y2').innerText = formatCurrency(client.FY_24_25);
            document.getElementById('modal-metric-y3').innerText = formatCurrency(client.FY_25_26);

            // Compute growth percentages in modal
            const growthY2El = document.getElementById('modal-metric-growth-y2');
            const growthY3El = document.getElementById('modal-metric-growth-y3');

            if (client.FY_23_24 > 0) {{
                const g2 = ((client.FY_24_25 - client.FY_23_24) / client.FY_23_24) * 100;
                growthY2El.className = g2 >= 0 ? "client-metric-growth up" : "client-metric-growth down";
                growthY2El.innerText = (g2 >= 0 ? '▲ +' : '▼ ') + g2.toFixed(1) + '%';
                growthY2El.style.color = g2 >= 0 ? "var(--success)" : "var(--danger)";
            }} else {{
                growthY2El.className = "client-metric-growth neutral";
                growthY2El.innerText = "New Account";
                growthY2El.style.color = "var(--text-secondary)";
            }}

            if (client.FY_24_25 > 0) {{
                const g3 = ((client.FY_25_26 - client.FY_24_25) / client.FY_24_25) * 100;
                growthY3El.className = g3 >= 0 ? "client-metric-growth up" : "client-metric-growth down";
                growthY3El.innerText = (g3 >= 0 ? '▲ +' : '▼ ') + g3.toFixed(1) + '%';
                growthY3El.style.color = g3 >= 0 ? "var(--success)" : "var(--danger)";
            }} else {{
                growthY3El.className = "client-metric-growth neutral";
                growthY3El.innerText = client.FY_25_26 > 0 ? "New Account" : "Inactive";
                growthY3El.style.color = "var(--text-secondary)";
            }}

            document.getElementById('client-modal').style.display = "flex";

            // Render mini chart inside modal
            setTimeout(() => {{
                const ctx = document.getElementById('clientTrendChart').getContext('2d');
                if (clientTrendChartInst) {{
                    clientTrendChartInst.destroy();
                }}
                clientTrendChartInst = new Chart(ctx, {{
                    type: 'line',
                    data: {{
                        labels: ['FY 23-24', 'FY 24-25', 'FY 25-26'],
                        datasets: [{{
                            label: 'Outward Trend',
                            data: [client.FY_23_24, client.FY_24_25, client.FY_25_26],
                            borderColor: '#8b5cf6',
                            backgroundColor: 'rgba(139, 92, 246, 0.1)',
                            fill: true,
                            tension: 0.1,
                            borderWidth: 2.5,
                            pointRadius: 4
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{ legend: {{ display: false }} }},
                        scales: {{
                            y: {{
                                ticks: {{ color: '#9ca3af' }},
                                grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}
                            }},
                            x: {{
                                ticks: {{ color: '#9ca3af' }},
                                grid: {{ display: false }}
                            }}
                        }}
                    }}
                }});
            }}, 50);
        }}

        function closeModal(e) {{
            if (e === null || e.target === document.getElementById('client-modal')) {{
                document.getElementById('client-modal').style.display = "none";
            }}
        }}

        function exportCSV() {{
            let csvContent = "data:text/csv;charset=utf-8,";
            csvContent += "Particulars,Status,FY 23-24,FY 24-25,FY 25-26,Total Sales\\n";
            
            filteredRecords.forEach(r => {{
                let cleanName = r.Particulars.replace(/,/g, " "); // escape commas
                csvContent += `"${{cleanName}}",${{r.Status}},${{r.FY_23_24}},${{r.FY_24_25}},${{r.FY_25_26}},${{r.Total_Sales}}\\n`;
            }});

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", `Sales_Report_${{currentStatusFilter}}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}
    </script>
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Premium HTML dashboard successfully generated at: {html_path}")
