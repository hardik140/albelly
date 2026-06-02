import json
import os

json_path = r"e:\albelly\sales_data_consolidated.json"
html_path = r"e:\albelly\index.html"

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
    <!-- SheetJS Excel & CSV Parser -->
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    
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

        .badge-slipping {{
            background: rgba(249, 115, 22, 0.1);
            color: #f97316;
            border: 1px solid rgba(249, 115, 22, 0.2);
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
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
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

        /* Upload Data Tab Styles */
        .upload-container {{
            display: grid;
            grid-template-columns: 1fr 1.2fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        @media (max-width: 900px) {{
            .upload-container {{
                grid-template-columns: 1fr;
            }}
        }}
        .drop-zone {{
            border: 2px dashed rgba(99, 102, 241, 0.3);
            border-radius: 16px;
            padding: 2.5rem 1.5rem;
            text-align: center;
            background: rgba(17, 24, 39, 0.3);
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 1rem;
        }}
        .drop-zone:hover, .drop-zone.dragover {{
            border-color: var(--primary);
            background: rgba(99, 102, 241, 0.05);
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.1);
        }}
        .drop-zone-icon {{
            font-size: 2.5rem;
            color: var(--primary);
            animation: float 3s ease-in-out infinite;
        }}
        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-8px); }}
        }}
        .drop-zone-text {{
            font-size: 0.95rem;
            color: var(--text-primary);
            font-weight: 500;
        }}
        .drop-zone-subtext {{
            font-size: 0.75rem;
            color: var(--text-secondary);
        }}
        .mapping-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }}
        .mapping-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.1rem;
            font-weight: 600;
            color: #fff;
            margin-bottom: 0.25rem;
        }}
        .form-group {{
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }}
        .form-group label {{
            font-size: 0.8125rem;
            color: var(--text-secondary);
            font-weight: 500;
        }}
        .form-control {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.65rem 1rem;
            color: #fff;
            font-size: 0.875rem;
            outline: none;
            transition: all 0.3s ease;
        }}
        .form-control:focus {{
            border-color: var(--primary);
            background: rgba(99, 102, 241, 0.02);
        }}
        .btn-primary {{
            background: var(--primary);
            border: 1px solid var(--primary);
            color: #fff;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
            text-align: center;
        }}
        .btn-primary:hover:not(:disabled) {{
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
            background: #4f46e5;
        }}
        .btn-primary:disabled {{
            opacity: 0.5;
            cursor: not-allowed;
        }}
        .btn-secondary {{
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .btn-secondary:hover {{
            background: rgba(255, 255, 255, 0.08);
        }}
        .profile-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            display: none;
            animation: fadeIn 0.4s ease forwards;
        }}
        .profile-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.25rem;
            margin-top: 1.25rem;
            margin-bottom: 1.25rem;
        }}
        .profile-item {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1rem;
            text-align: center;
        }}
        .profile-lbl {{
            font-size: 0.75rem;
            color: var(--text-secondary);
            margin-bottom: 0.25rem;
        }}
        .profile-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: #fff;
        }}

        /* Comparison Tab Styles */
        .comparison-layout {{
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        @media (max-width: 900px) {{
            .comparison-layout {{
                grid-template-columns: 1fr;
            }}
        }}
        .selector-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.5rem;
            max-height: 680px;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        .search-select-box {{
            position: relative;
        }}
        .client-list-scroll {{
            overflow-y: auto;
            max-height: 480px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding-right: 4px;
        }}
        .client-checkbox-item {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.6rem 0.8rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            border: 1px solid transparent;
        }}
        .client-checkbox-item:hover {{
            background: rgba(255, 255, 255, 0.03);
        }}
        .client-checkbox-item.checked {{
            background: rgba(99, 102, 241, 0.08);
            border-color: rgba(99, 102, 241, 0.2);
        }}
        .client-checkbox-item input {{
            cursor: pointer;
            accent-color: var(--primary);
            width: 16px;
            height: 16px;
        }}
        .client-checkbox-name {{
            font-size: 0.875rem;
            color: var(--text-primary);
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .client-checkbox-item.checked .client-checkbox-name {{
            color: #fff;
        }}
        .comparison-content {{
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }}
        .comparison-placeholder {{
            background: var(--bg-card);
            border: 1px dashed var(--border-color);
            border-radius: 16px;
            padding: 4rem 2rem;
            text-align: center;
            color: var(--text-secondary);
            font-size: 0.95rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            height: 100%;
            min-height: 450px;
        }}
        .insights-panel {{
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
            border: 1px solid rgba(99, 102, 241, 0.15);
            border-radius: 12px;
            padding: 1.25rem;
            margin-top: 1rem;
        }}
        .insights-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 0.95rem;
            font-weight: 600;
            color: #fff;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .insights-list {{
            font-size: 0.875rem;
            color: var(--text-secondary);
            padding-left: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            line-height: 1.5;
        }}
        .insights-list li strong {{
            color: #fff;
        }}
    </style>
</head>
<body>

    <header>
        <div class="logo-section">
            <h1>Sales Performance Hub</h1>
            <p>Unified Ledger Analysis (3 Years)</p>
        </div>
        <div style="margin-left: auto; margin-right: 1.5rem;">
            <a href="plotly_dashboard.html" style="text-decoration: none; color: var(--text-secondary); border: 1px solid var(--border-color); padding: 0.5rem 1rem; border-radius: 8px; font-size: 0.8rem; font-weight: 500; transition: all 0.3s ease; display: inline-flex; align-items: center; gap: 4px;" onmouseover="this.style.color='#fff'; this.style.borderColor='var(--text-secondary)'" onmouseout="this.style.color='var(--text-secondary)'; this.style.borderColor='var(--border-color)'">
                📊 View Plotly Analytics
            </a>
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
            <button class="tab-btn" onclick="switchTab('compare', this)">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 002 2h2a2 2 0 002-2z"></path></svg>
                Compare Accounts
            </button>
            <button class="tab-btn" onclick="switchTab('missed', this)">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
                Leakage & Missed
            </button>
            <button class="tab-btn" onclick="switchTab('upload', this)">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path></svg>
                Upload Data
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
            <!-- Executive Alert Banner for Revenue Leakage -->
            <div style="background: rgba(249, 115, 22, 0.06); border: 1px solid rgba(249, 115, 22, 0.18); border-radius: 12px; padding: 1rem 1.5rem; margin-bottom: 1.5rem; display: flex; align-items: center; justify-content: space-between; gap: 1rem; animation: fadeIn 0.4s ease forwards; cursor: pointer;" onclick="handleKpiClick('Declining', 'Total_Sales')">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 1.4rem; line-height: 1;">⚠️</span>
                    <div>
                        <h4 style="font-family: 'Outfit', sans-serif; font-size: 0.95rem; font-weight: 600; color: #fff; margin-bottom: 2px;">Active Revenue Leakage Warning</h4>
                        <p style="font-size: 0.8125rem; color: var(--text-secondary);"><strong>75 active repeat clients</strong> are ordering less than last year, leaking <strong style="color: #f97316;">₹27,04,495.00</strong> in sales. This is larger than your complete dropout churn!</p>
                    </div>
                </div>
                <div style="font-size: 0.8125rem; color: #f97316; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; display: flex; align-items: center; gap: 4px; white-space: nowrap;">
                    View Slipping Accounts
                    <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7M3 12h13"></path></svg>
                </div>
            </div>
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
                            <option value="Declining">Slipping Accounts (Buying Less)</option>
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

        <!-- TAB 3: REVENUE LEAKAGE & MISSED OPPORTUNITIES -->
        <div id="section-missed" class="dashboard-section">
            <div style="background: rgba(249, 115, 22, 0.05); border: 1px solid rgba(249, 115, 22, 0.15); border-radius: 12px; padding: 1.25rem; margin-bottom: 2rem; display: flex; align-items: flex-start; gap: 1rem;">
                <span style="color: #f97316; font-size: 1.5rem; margin-top: 2px;">⚠️</span>
                <div>
                    <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 600; color: #fff; margin-bottom: 0.25rem;">Revenue Leakage & Missed Opportunities Analysis</h3>
                    <p style="font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5;">Identify where your repeat customer revenue is slipping and target them for proactive win-back outreach. Active repeat clients who are buying less represent your biggest leak (<strong>₹27,04,495.00</strong>), followed by complete dropouts.</p>
                </div>
            </div>

            <div class="missed-opportunities-grid">
                <div class="missed-list-card">
                    <h3 class="chart-title" style="margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem; color: var(--danger); font-size: 0.95rem;">
                        🔴 Recent High-Value Dropouts (Lost in 25-26)
                    </h3>
                    <div id="lost-list-container" style="max-height: 480px; overflow-y: auto; padding-right: 0.5rem;">
                        <!-- Injected dynamically -->
                    </div>
                </div>

                <div class="missed-list-card">
                    <h3 class="chart-title" style="margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem; color: #f97316; font-size: 0.95rem;">
                        ⚠️ Active Slipping Revenue (Buying Less YoY)
                    </h3>
                    <div id="slipping-list-container" style="max-height: 480px; overflow-y: auto; padding-right: 0.5rem;">
                        <!-- Injected dynamically -->
                    </div>
                </div>

                <div class="missed-list-card">
                    <h3 class="chart-title" style="margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.5rem; color: var(--warning); font-size: 0.95rem;">
                        🟠 Older Historical Dropouts (Inactive since 23-24)
                    </h3>
                    <div id="inactive-list-container" style="max-height: 480px; overflow-y: auto; padding-right: 0.5rem;">
                        <!-- Injected dynamically -->
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 4: COMPARE ACCOUNTS -->
        <div id="section-compare" class="dashboard-section">
            <div class="comparison-layout">
                <!-- Left Sidebar: Selection -->
                <div class="selector-card">
                    <h3 class="chart-title">Select Accounts</h3>
                    <p style="font-size: 0.8125rem; color: var(--text-secondary);">Choose 2 or more accounts to compare their sales metrics.</p>
                    
                    <div class="search-select-box">
                        <span class="search-icon" style="left: 0.75rem;">
                            <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                        </span>
                        <input type="text" class="search-input" id="compare-search" placeholder="Search accounts..." oninput="filterCompareList()" style="padding-left: 2.2rem; margin-bottom: 0.5rem; background: rgba(255,255,255,0.02);">
                    </div>
                    
                    <div class="client-list-scroll" id="compare-client-list">
                        <!-- Injected dynamically -->
                    </div>
                </div>
                
                <!-- Right Side: Charts & Table -->
                <div class="comparison-content">
                    <div id="compare-placeholder" class="comparison-placeholder">
                        <div style="font-size: 3rem;">📊</div>
                        <div style="font-weight: 600; color: #fff; font-size: 1.1rem;">No Accounts Selected</div>
                        <div style="max-width: 380px; line-height: 1.5;">Select multiple client accounts from the left panel to compare their financial history, YoY growth trajectory, and performance breakdown.</div>
                    </div>
                    
                    <div id="compare-results" style="display: none; animation: fadeIn 0.4s ease forwards;">
                        <!-- Comparison Charts -->
                        <div class="chart-grid" style="grid-template-columns: 1fr 1fr;">
                            <div class="chart-card">
                                <div class="chart-header">
                                    <div class="chart-title">Sales Trajectory Comparison</div>
                                </div>
                                <div class="chart-subtitle">YoY sales trends of selected accounts</div>
                                <div style="height: 280px; position: relative;">
                                    <canvas id="comparisonChart"></canvas>
                                </div>
                            </div>
                            <div class="chart-card">
                                <div class="chart-header">
                                    <div class="chart-title">YoY Growth Comparison</div>
                                </div>
                                <div class="chart-subtitle">Latest Year YoY growth rate (%)</div>
                                <div style="height: 280px; position: relative;">
                                    <canvas id="comparisonGrowthChart"></canvas>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Side-by-side Table -->
                        <div class="table-card" style="margin-bottom: 0;">
                            <div class="chart-header" style="margin-bottom: 1.25rem;">
                                <div class="chart-title">Side-by-Side Account Metrics</div>
                            </div>
                            <div class="table-responsive">
                                <table>
                                    <thead>
                                        <tr id="compare-table-headers">
                                            <!-- Injected dynamically -->
                                        </tr>
                                    </thead>
                                    <tbody id="compare-table-body">
                                        <!-- Injected dynamically -->
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <!-- Text Insights -->
                        <div class="insights-panel">
                            <div class="insights-title">
                                <span>💡</span> Account Performance Comparison Insights
                            </div>
                            <ul class="insights-list" id="comparison-insights-list">
                                <!-- Injected dynamically -->
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: UPLOAD & AUDIT NEW DATA -->
        <div id="section-upload" class="dashboard-section">
            <div style="background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.15); border-radius: 12px; padding: 1.25rem; margin-bottom: 2rem; display: flex; align-items: flex-start; gap: 1rem;">
                <span style="color: var(--primary); font-size: 1.5rem; margin-top: 2px;">📂</span>
                <div>
                    <h3 style="font-family: 'Outfit', sans-serif; font-size: 1.05rem; font-weight: 600; color: #fff; margin-bottom: 0.25rem;">Upload Future Data Records</h3>
                    <p style="font-size: 0.875rem; color: var(--text-secondary); line-height: 1.5;">
                        Drag and drop a new outward sales CSV or Excel file to analyze future data, profile transaction volume, audit compatibility with your current repeat customers, and dynamically integrate it into all active charts.
                    </p>
                </div>
            </div>

            <div class="upload-container">
                <!-- Drop zone -->
                <div class="drop-zone" id="upload-dropzone" onclick="document.getElementById('file-input').click()">
                    <div class="drop-zone-icon">📤</div>
                    <div class="drop-zone-text">Drag & Drop CSV or Excel File here</div>
                    <div class="drop-zone-subtext">Supports .csv, .xlsx, .xls files (up to 10MB)</div>
                    <input type="file" id="file-input" style="display: none;" accept=".csv, .xlsx, .xls" onchange="handleFileSelect(event)">
                </div>

                <!-- Column Mapping & Actions -->
                <div class="mapping-card">
                    <div class="mapping-title">Column Mapping Configuration</div>
                    <p style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.5rem;">Map your spreadsheet columns to dashboard ledger properties.</p>
                    
                    <div class="form-group">
                        <label for="map-particulars">Account Name Column (Particulars)</label>
                        <select class="select-filter form-control" id="map-particulars" disabled style="width: 100%;">
                            <option value="">Select column...</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="map-value">Sales Value Column (INR / Amount)</label>
                        <select class="select-filter form-control" id="map-value" disabled style="width: 100%;">
                            <option value="">Select column...</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="map-year-label">Target Period / Fiscal Year Label</label>
                        <input type="text" class="form-control" id="map-year-label" placeholder="e.g. FY 26-27" value="FY 26-27">
                    </div>

                    <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                        <button class="btn-primary" id="btn-apply-data" disabled onclick="integrateUploadedData('dashboard')">
                            Showcase on Dashboard
                        </button>
                        <button class="btn-secondary" id="btn-compare-data" disabled onclick="integrateUploadedData('compare')" style="border-color: rgba(99, 102, 241, 0.4); color: #a5b4fc; background: rgba(99, 102, 241, 0.05); font-weight: 600;">
                            Integrate & Compare Accounts
                        </button>
                    </div>
                </div>
            </div>

            <!-- Profile and Audit card -->
            <div class="profile-card" id="upload-profile-card">
                <div class="mapping-title" style="border-bottom: 1px solid var(--border-color); padding-bottom: 0.75rem; display: flex; justify-content: space-between; align-items: center;">
                    <span>📊 Uploaded File Data Profile & Integrity Audit</span>
                    <span class="badge badge-new" id="profile-filename" style="font-weight: 500;">Filename.xlsx</span>
                </div>
                
                <div class="profile-grid">
                    <div class="profile-item">
                        <div class="profile-lbl">Total Raw Revenue</div>
                        <div class="profile-val" id="profile-total-revenue">₹0.00</div>
                    </div>
                    <div class="profile-item">
                        <div class="profile-lbl">Total Records</div>
                        <div class="profile-val" id="profile-total-records">0</div>
                    </div>
                    <div class="profile-item">
                        <div class="profile-lbl">Client Match Rate</div>
                        <div class="profile-val" id="profile-match-rate">0.0%</div>
                    </div>
                    <div class="profile-item">
                        <div class="profile-lbl">New Clients Identified</div>
                        <div class="profile-val" id="profile-new-clients-count">0</div>
                    </div>
                </div>

                <div class="chart-grid" style="grid-template-columns: 1.2fr 0.8fr; margin-top: 1.5rem; margin-bottom: 0;">
                    <!-- New clients listing -->
                    <div class="missed-list-card">
                        <h3 class="chart-title" style="margin-bottom: 1rem; color: var(--primary); font-size: 0.95rem;">
                            ✨ Newly Identified Customer Accounts (<span id="profile-new-label">0</span>)
                        </h3>
                        <div id="profile-new-list" style="max-height: 220px; overflow-y: auto; padding-right: 0.5rem; font-size: 0.8125rem;">
                            <!-- Injected dynamically -->
                        </div>
                    </div>
                    <!-- Audit Status -->
                    <div class="missed-list-card" style="display: flex; flex-direction: column; justify-content: center; gap: 1rem; padding: 1.5rem;">
                        <h3 class="chart-title" style="color: var(--success); font-size: 0.95rem; margin-bottom: 0.25rem;">
                            ✅ Audit Results
                        </h3>
                        <p style="font-size: 0.8125rem; color: var(--text-secondary); line-height: 1.5;" id="profile-audit-summary">
                            File parsed successfully with SheetJS. All numerical values mapped. Direct integration will append a new fiscal year column and recalculate growth vectors.
                        </p>
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
        let comparisonChartInst = null;
        let comparisonGrowthChartInst = null;

        let yearsList = ['FY_23_24', 'FY_24_25', 'FY_25_26'];
        let activeYearLabels = ['FY 23-24', 'FY 24-25', 'FY 25-26'];
        let rawUploadedRows = null;
        let uploadedHeaders = [];
        let selectedCompareClients = [];

        // Initialize App
        window.addEventListener('DOMContentLoaded', () => {{
            updateKPIs();
            renderDashboardCharts();
            applyFilters(); // Trigger filters rendering table & subsets
            renderMissedOpportunities();
            setupUploadListeners();
            renderCompareClientList();
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
            
            // Trigger layout calculations for Chart.js if switching tabs
            if (tabId === 'compare' && selectedCompareClients.length >= 2) {{
                setTimeout(() => {{
                    if (comparisonChartInst) comparisonChartInst.resize();
                    if (comparisonGrowthChartInst) comparisonGrowthChartInst.resize();
                }}, 50);
            }}
        }}

        /* Data Upload Feature implementation */
        function setupUploadListeners() {{
            const dropzone = document.getElementById('upload-dropzone');
            if (!dropzone) return;
            
            ['dragenter', 'dragover'].forEach(eventName => {{
                dropzone.addEventListener(eventName, (e) => {{
                    e.preventDefault();
                    dropzone.classList.add('dragover');
                }}, false);
            }});
            
            ['dragleave', 'drop'].forEach(eventName => {{
                dropzone.addEventListener(eventName, (e) => {{
                    e.preventDefault();
                    dropzone.classList.remove('dragover');
                }}, false);
            }});
            
            dropzone.addEventListener('drop', (e) => {{
                const dt = e.dataTransfer;
                const files = dt.files;
                if (files.length > 0) {{
                    document.getElementById('file-input').files = files;
                    handleFileSelect({{ target: {{ files: files }} }});
                }}
            }}, false);
        }}

        function handleFileSelect(e) {{
            const files = e.target.files;
            if (!files || files.length === 0) return;
            const file = files[0];
            
            // Update UI filename indicator
            document.getElementById('profile-filename').innerText = file.name;
            
            const reader = new FileReader();
            reader.onload = function(evt) {{
                try {{
                    const data = evt.target.result;
                    let workbook;
                    
                    if (file.name.endsWith('.csv')) {{
                        workbook = XLSX.read(data, {{ type: 'string' }});
                    }} else {{
                        const arr = new Uint8Array(data);
                        workbook = XLSX.read(arr, {{ type: 'array' }});
                    }}
                    
                    const firstSheetName = workbook.SheetNames[0];
                    const worksheet = workbook.Sheets[firstSheetName];
                    
                    rawUploadedRows = XLSX.utils.sheet_to_json(worksheet, {{ header: 1 }});
                    
                    if (!rawUploadedRows || rawUploadedRows.length < 2) {{
                        alert("The file seems empty or lacks a header row.");
                        return;
                    }}
                    
                    rawUploadedRows = rawUploadedRows.filter(row => row && row.length > 0);
                    uploadedHeaders = rawUploadedRows[0].map(h => h ? h.toString().trim() : '');
                    
                    populateMappingOptions();
                    autoDetectColumns();
                    analyzeUploadedData();
                    
                }} catch (err) {{
                    console.error("Error parsing workbook:", err);
                    alert("Error parsing file. Please verify it is a valid CSV or Excel document.");
                }}
            }};
            
            if (file.name.endsWith('.csv')) {{
                reader.readAsText(file);
            }} else {{
                reader.readAsArrayBuffer(file);
            }}
        }}

        function populateMappingOptions() {{
            const partSelect = document.getElementById('map-particulars');
            const valSelect = document.getElementById('map-value');
            
            partSelect.innerHTML = '<option value="">Select column...</option>';
            valSelect.innerHTML = '<option value="">Select column...</option>';
            
            uploadedHeaders.forEach((header, idx) => {{
                if (!header) return;
                const opt1 = document.createElement('option');
                opt1.value = idx;
                opt1.innerText = header;
                partSelect.appendChild(opt1);
                
                const opt2 = document.createElement('option');
                opt2.value = idx;
                opt2.innerText = header;
                valSelect.appendChild(opt2);
            }});
            
            partSelect.disabled = false;
            valSelect.disabled = false;
            
            partSelect.onchange = analyzeUploadedData;
            valSelect.onchange = analyzeUploadedData;
        }}

        function autoDetectColumns() {{
            const partSelect = document.getElementById('map-particulars');
            const valSelect = document.getElementById('map-value');
            
            const partKeywords = ['particulars', 'particular', 'name', 'client', 'customer', 'account', 'party', 'store', 'shop'];
            const valKeywords = ['sales', 'value', 'amount', 'total', 'revenue', 'fy', 'outward', 'net', 'turnover'];
            
            let detectedPart = -1;
            let detectedVal = -1;
            
            uploadedHeaders.forEach((header, idx) => {{
                const hLower = header.toLowerCase();
                if (detectedPart === -1 && partKeywords.some(kw => hLower.includes(kw))) {{
                    detectedPart = idx;
                }}
                if (detectedVal === -1 && valKeywords.some(kw => hLower.includes(kw))) {{
                    detectedVal = idx;
                }}
            }});
            
            if (detectedPart === -1 && uploadedHeaders.length > 0) detectedPart = 0;
            if (detectedVal === -1 && uploadedHeaders.length > 1) {{
                detectedVal = 1;
            }} else if (detectedVal === -1 && uploadedHeaders.length > 0) {{
                detectedVal = 0;
            }}
            
            if (detectedPart !== -1) partSelect.value = detectedPart;
            if (detectedVal !== -1) valSelect.value = detectedVal;
        }}

        function analyzeUploadedData() {{
            const partIdx = parseInt(document.getElementById('map-particulars').value);
            const valIdx = parseInt(document.getElementById('map-value').value);
            const btnApply = document.getElementById('btn-apply-data');
            const btnCompare = document.getElementById('btn-compare-data');
            const profileCard = document.getElementById('upload-profile-card');
            
            if (isNaN(partIdx) || isNaN(valIdx)) {{
                btnApply.disabled = true;
                if (btnCompare) btnCompare.disabled = true;
                profileCard.style.display = 'none';
                return;
            }}
            
            btnApply.disabled = false;
            if (btnCompare) btnCompare.disabled = false;
            profileCard.style.display = 'block';
            
            let totalRevenue = 0;
            let recordCount = 0;
            let matchedCount = 0;
            let newClients = [];
            
            const existingParticularsSet = new Set(records.map(r => r.Particulars.toUpperCase().trim()));
            
            for (let i = 1; i < rawUploadedRows.length; i++) {{
                const row = rawUploadedRows[i];
                if (!row || row.length <= Math.max(partIdx, valIdx)) continue;
                
                const clientName = row[partIdx] ? row[partIdx].toString().trim() : '';
                if (!clientName) continue;
                
                let valStr = row[valIdx] !== undefined ? row[valIdx].toString().replace(/[^0-9.-]/g, '') : '0';
                const val = parseFloat(valStr) || 0;
                
                totalRevenue += val;
                recordCount++;
                
                if (existingParticularsSet.has(clientName.toUpperCase())) {{
                    matchedCount++;
                }} else {{
                    newClients.push({{ name: clientName, value: val }});
                }}
            }}
            
            const matchRate = recordCount > 0 ? (matchedCount / recordCount) * 100 : 0;
            
            document.getElementById('profile-total-revenue').innerText = formatCurrency(totalRevenue);
            document.getElementById('profile-total-records').innerText = recordCount.toLocaleString();
            document.getElementById('profile-match-rate').innerText = matchRate.toFixed(1) + '%';
            document.getElementById('profile-new-clients-count').innerText = newClients.length.toLocaleString();
            document.getElementById('profile-new-label').innerText = newClients.length.toLocaleString();
            
            const newListContainer = document.getElementById('profile-new-list');
            newListContainer.innerHTML = '';
            
            if (newClients.length === 0) {{
                newListContainer.innerHTML = '<div style="color: var(--text-secondary); padding: 1rem 0;">No new customer accounts identified. All match existing ledger.</div>';
            }} else {{
                newClients.sort((a, b) => b.value - a.value);
                newClients.forEach(nc => {{
                    const div = document.createElement('div');
                    div.style.display = 'flex';
                    div.style.justify = 'space-between';
                    div.style.padding = '0.4rem 0';
                    div.style.borderBottom = '1px solid rgba(255,255,255,0.02)';
                    div.innerHTML = `
                        <span style="color: #fff; font-weight: 500;">${{nc.name}}</span>
                        <span style="color: var(--primary); font-weight: 600;">${{formatCurrency(nc.value)}}</span>
                    `;
                    newListContainer.appendChild(div);
                }});
            }}
            
            const auditSummary = document.getElementById('profile-audit-summary');
            if (matchRate > 80) {{
                auditSummary.innerHTML = `✅ <strong>Excellent Data Integrity!</strong> Matched <strong>${{matchedCount}} out of ${{recordCount}}</strong> clients against historical records. Match rate of <strong>${{matchRate.toFixed(1)}}%</strong> represents high repeat customer consistency. Applying this data will extend the timeline.`;
                auditSummary.style.color = 'var(--success)';
            }} else if (matchRate > 40) {{
                auditSummary.innerHTML = `⚠️ <strong>Moderate Compatibility:</strong> Matched <strong>${{matchedCount}} out of ${{recordCount}}</strong> client names (${{matchRate.toFixed(1)}}%). Detected <strong>${{newClients.length}}</strong> new client accounts. Verify that client name spelling matches exactly.`;
                auditSummary.style.color = 'var(--warning)';
            }} else {{
                auditSummary.innerHTML = `🔴 <strong>Low Matching Audit:</strong> Only <strong>${{matchRate.toFixed(1)}}%</strong> match rate. Identified <strong>${{newClients.length}}</strong> completely new accounts. This suggests a different customer base or spelling formats. You can still apply the file to import them.`;
                auditSummary.style.color = '#f97316';
            }}
        }}

        function integrateUploadedData(destination) {{
            const partIdx = parseInt(document.getElementById('map-particulars').value);
            const valIdx = parseInt(document.getElementById('map-value').value);
            let yearLabelInput = document.getElementById('map-year-label').value.trim();
            
            if (!yearLabelInput) {{
                alert("Please enter a period/year label (e.g. FY 26-27).");
                return;
            }}
            
            const yearProp = yearLabelInput.replace(/[-\\s]/g, '_');
            
            if (yearsList.includes(yearProp)) {{
                if (!confirm(`Warning: Data for ${{yearLabelInput}} has already been integrated or exists. Overwrite?`)) {{
                    return;
                }}
            }} else {{
                yearsList.push(yearProp);
                activeYearLabels.push(yearLabelInput);
            }}
            
            const uploadedMap = new Map();
            const rawMatchedNames = [];
            const existingParticularsSet = new Set(records.map(r => r.Particulars.toUpperCase().trim()));
            
            for (let i = 1; i < rawUploadedRows.length; i++) {{
                const row = rawUploadedRows[i];
                if (!row || row.length <= Math.max(partIdx, valIdx)) continue;
                
                const name = row[partIdx] ? row[partIdx].toString().trim() : '';
                if (!name) continue;
                
                let valStr = row[valIdx] !== undefined ? row[valIdx].toString().replace(/[^0-9.-]/g, '') : '0';
                const val = parseFloat(valStr) || 0;
                
                uploadedMap.set(name.toUpperCase(), (uploadedMap.get(name.toUpperCase()) || 0) + val);
                
                if (existingParticularsSet.has(name.toUpperCase())) {{
                    rawMatchedNames.push({{ name: name, value: val }});
                }}
            }}
            
            records.forEach(r => {{
                const uKey = r.Particulars.toUpperCase().trim();
                const newVal = uploadedMap.get(uKey) || 0;
                r[yearProp] = newVal;
                
                r.Total_Sales = yearsList.reduce((sum, yKey) => sum + (r[yKey] || 0), 0);
                
                const prevYearProp = yearsList[yearsList.length - 2];
                if (r[prevYearProp] > 0) {{
                    r[`Growth_${{prevYearProp}}_to_${{yearProp}}`] = ((newVal - r[prevYearProp]) / r[prevYearProp]) * 100;
                }} else {{
                    r[`Growth_${{prevYearProp}}_to_${{yearProp}}`] = 0;
                }}
                
                let activePrevious = yearsList.slice(0, -1).some(yKey => (r[yKey] || 0) > 0);
                if (newVal > 0) {{
                    r.Status = activePrevious ? "Retained" : "New";
                }} else {{
                    r.Status = activePrevious ? "Lost" : "Inactive";
                }}
            }});
            
            uploadedMap.forEach((val, nameKey) => {{
                const nameInLedger = records.find(r => r.Particulars.toUpperCase().trim() === nameKey);
                if (nameInLedger) return;
                
                const newRecord = {{
                    Particulars: nameKey,
                    Status: "New",
                    Total_Sales: val
                }};
                
                yearsList.forEach(yKey => {{
                    newRecord[yKey] = 0;
                }});
                newRecord[yearProp] = val;
                
                yearsList.forEach((yKey, idx) => {{
                    if (idx === 0) return;
                    const prevKey = yearsList[idx - 1];
                    newRecord[`Growth_${{prevKey}}_to_${{yKey}}`] = 0;
                }});
                
                records.push(newRecord);
            }});
            
            const newTotals = {{}};
            yearsList.forEach(yKey => {{
                newTotals[yKey] = records.reduce((sum, r) => sum + (r[yKey] || 0), 0);
            }});
            newTotals.Cumulative = yearsList.reduce((sum, yKey) => sum + newTotals[yKey], 0);
            salesData.totals = newTotals;
            
            const newCounts = {{
                total_clients: records.length,
                retained_active: records.filter(r => r.Status === "Retained").length,
                new_active: records.filter(r => r.Status === "New").length,
                lost_active: records.filter(r => r.Status === "Lost").length,
                inactive_active: records.filter(r => r.Status === "Inactive").length
            }};
            salesData.counts = newCounts;
            
            updateKPIs();
            
            trajectoryChartInst.data.labels = activeYearLabels;
            trajectoryChartInst.data.datasets[0].data = activeYearLabels.map((lbl, idx) => newTotals[yearsList[idx]]);
            trajectoryChartInst.update();
            
            distributionChartInst.data.datasets[0].data = [
                newCounts.retained_active,
                newCounts.new_active,
                newCounts.lost_active,
                newCounts.inactive_active
            ];
            distributionChartInst.update();
            
            const topRecords = [...records].sort((a,b) => b.Total_Sales - a.Total_Sales).slice(0, 15);
            topParticularsChartInst.data.labels = topRecords.map(r => r.Particulars);
            
            topParticularsChartInst.data.datasets = [];
            const yearColors = ['#8b5cf6', '#ec4899', '#10b981', '#f59e0b', '#3b82f6', '#14b8a6'];
            
            yearsList.forEach((yKey, yIdx) => {{
                topParticularsChartInst.data.datasets.push({{
                    label: activeYearLabels[yIdx],
                    data: topRecords.map(r => r[yKey] || 0),
                    backgroundColor: yearColors[yIdx % yearColors.length]
                }});
            }});
            topParticularsChartInst.update();
            
            currentPage = 1;
            applyFilters();
            renderMissedOpportunities();
            
            if (destination === 'compare') {{
                // Auto select top matched clients from this file
                rawMatchedNames.sort((a, b) => b.value - a.value);
                const selectCount = Math.min(4, rawMatchedNames.length);
                selectedCompareClients = [];
                for (let i = 0; i < selectCount; i++) {{
                    const matchLedger = records.find(r => r.Particulars.toUpperCase().trim() === rawMatchedNames[i].name.toUpperCase());
                    if (matchLedger) {{
                        selectedCompareClients.push(matchLedger.Particulars);
                    }}
                }}
                
                renderCompareClientList();
                updateComparisonView();
                
                alert(`Success! Data for ${{yearLabelInput}} integrated.\nAutomatically selected ${{selectedCompareClients.length}} matched accounts for comparison.`);
                
                const compBtn = document.querySelector('button[onclick*="compare"]');
                switchTab('compare', compBtn);
            }} else {{
                renderCompareClientList();
                alert(`Success! Data for ${{yearLabelInput}} successfully integrated.\nTotal Cumulative Sales updated to ${{formatCurrency(newTotals.Cumulative)}}.`);
                
                const dashBtn = document.querySelector('button[onclick*="dashboard"]');
                switchTab('dashboard', dashBtn);
            }}
        }}

        /* Comparison Feature implementation */
        function renderCompareClientList() {{
            const listContainer = document.getElementById('compare-client-list');
            if (!listContainer) return;
            
            listContainer.innerHTML = '';
            const sortedForSelect = [...records].sort((a, b) => a.Particulars.localeCompare(b.Particulars));
            
            sortedForSelect.forEach(r => {{
                const isChecked = selectedCompareClients.includes(r.Particulars);
                const div = document.createElement('div');
                div.className = `client-checkbox-item ${{isChecked ? 'checked' : ''}}`;
                div.onclick = () => handleCompareCheckboxChange(r.Particulars);
                
                div.innerHTML = `
                    <input type="checkbox" id="comp-chk-${{r.Particulars.replace(/\\s+/g, '-')}}" ${{isChecked ? 'checked' : ''}} onclick="event.stopPropagation(); handleCompareCheckboxChange('${{r.Particulars}}')">
                    <span class="client-checkbox-name" title="${{r.Particulars}}">${{r.Particulars}}</span>
                `;
                listContainer.appendChild(div);
            }});
        }}

        function filterCompareList() {{
            const query = document.getElementById('compare-search').value.toUpperCase().trim();
            const items = document.querySelectorAll('#compare-client-list .client-checkbox-item');
            
            items.forEach(item => {{
                const name = item.querySelector('.client-checkbox-name').innerText.toUpperCase();
                if (name.includes(query)) {{
                    item.style.display = 'flex';
                }} else {{
                    item.style.display = 'none';
                }}
            }});
        }}

        function handleCompareCheckboxChange(clientName) {{
            const idx = selectedCompareClients.indexOf(clientName);
            if (idx === -1) {{
                selectedCompareClients.push(clientName);
            }} else {{
                selectedCompareClients.splice(idx, 1);
            }}
            
            renderCompareClientList();
            updateComparisonView();
        }}

        function updateComparisonView() {{
            const placeholder = document.getElementById('compare-placeholder');
            const results = document.getElementById('compare-results');
            
            if (selectedCompareClients.length < 2) {{
                placeholder.style.display = 'flex';
                results.style.display = 'none';
                return;
            }}
            
            placeholder.style.display = 'none';
            results.style.display = 'block';
            
            const selectedRecords = records.filter(r => selectedCompareClients.includes(r.Particulars));
            
            const thRow = document.getElementById('compare-table-headers');
            thRow.innerHTML = `<th>Particulars</th><th>Status</th>`;
            yearsList.forEach((yProp, idx) => {{
                thRow.innerHTML += `<th style="text-align: right;">${{activeYearLabels[idx]}}</th>`;
            }});
            thRow.innerHTML += `<th style="text-align: right;">Total Sales</th>`;
            
            const tbody = document.getElementById('compare-table-body');
            tbody.innerHTML = '';
            
            selectedRecords.forEach(r => {{
                const tr = document.createElement('tr');
                let displayStatusClass = r.Status.toLowerCase();
                
                let rowHtml = `
                    <td style="font-weight: 500; color: #fff;">${{r.Particulars}}</td>
                    <td style="text-align: center;"><span class="badge badge-${{displayStatusClass}}">${{r.Status}}</span></td>
                `;
                
                yearsList.forEach(yProp => {{
                    rowHtml += `<td style="text-align: right;">${{formatCurrency(r[yProp] || 0)}}</td>`;
                }});
                
                rowHtml += `<td style="text-align: right; font-weight: 600; color: #fff;">${{formatCurrency(r.Total_Sales)}}</td>`;
                tr.innerHTML = rowHtml;
                tbody.appendChild(tr);
            }});
            
            const ctxLine = document.getElementById('comparisonChart').getContext('2d');
            if (comparisonChartInst) {{
                comparisonChartInst.destroy();
            }}
            
            const lineDatasets = selectedRecords.map((r, rIdx) => {{
                const borderColors = ['#6366f1', '#10b981', '#ec4899', '#f59e0b', '#8b5cf6', '#14b8a6'];
                return {{
                    label: r.Particulars,
                    data: yearsList.map(yProp => r[yProp] || 0),
                    borderColor: borderColors[rIdx % borderColors.length],
                    backgroundColor: borderColors[rIdx % borderColors.length] + '15',
                    fill: false,
                    borderWidth: 2.5,
                    tension: 0.1,
                    pointRadius: 4
                }};
            }});
            
            comparisonChartInst = new Chart(ctxLine, {{
                type: 'line',
                data: {{
                    labels: activeYearLabels,
                    datasets: lineDatasets
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{ position: 'top', labels: {{ color: '#9ca3af', boxWidth: 10 }} }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{ color: '#9ca3af', callback: function(value) {{ return '₹' + (value/100000).toFixed(1) + 'L'; }} }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}
                        }},
                        x: {{
                            ticks: {{ color: '#9ca3af' }},
                            grid: {{ display: false }}
                        }}
                    }}
                }}
            }});
            
            const ctxGrowth = document.getElementById('comparisonGrowthChart').getContext('2d');
            if (comparisonGrowthChartInst) {{
                comparisonGrowthChartInst.destroy();
            }}
            
            const targetYearProp = yearsList[yearsList.length - 1];
            const prevYearProp = yearsList[yearsList.length - 2];
            
            const growthData = selectedRecords.map(r => {{
                const prevVal = r[prevYearProp] || 0;
                const nextVal = r[targetYearProp] || 0;
                if (prevVal > 0) {{
                    return ((nextVal - prevVal) / prevVal) * 100;
                }}
                return 0;
            }});
            
            const backgroundColors = selectedRecords.map((r, rIdx) => {{
                const colors = ['#6366f1', '#10b981', '#ec4899', '#f59e0b', '#8b5cf6', '#14b8a6'];
                return colors[rIdx % colors.length];
            }});
            
            comparisonGrowthChartInst = new Chart(ctxGrowth, {{
                type: 'bar',
                data: {{
                    labels: selectedRecords.map(r => r.Particulars),
                    datasets: [{{
                        label: 'Growth Rate (%)',
                        data: growthData,
                        backgroundColor: backgroundColors,
                        borderWidth: 0,
                        borderRadius: 4
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
                                    return 'Growth: ' + context.raw.toFixed(1) + '%';
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            ticks: {{ color: '#9ca3af', callback: function(value) {{ return value.toFixed(1) + '%'; }} }},
                            grid: {{ color: 'rgba(255, 255, 255, 0.05)' }}
                        }},
                        x: {{
                            ticks: {{ color: '#9ca3af', font: {{ size: 9 }} }},
                            grid: {{ display: false }}
                        }}
                    }}
                }}
            }});
            
            const insightsContainer = document.getElementById('comparison-insights-list');
            insightsContainer.innerHTML = '';
            
            const sortedBySales = [...selectedRecords].sort((a,b) => b.Total_Sales - a.Total_Sales);
            const largestClient = sortedBySales[0];
            const secondLargest = sortedBySales[1];
            
            const largestLI = document.createElement('li');
            largestLI.innerHTML = `<strong>Top Performer:</strong> <strong>${{largestClient.Particulars}}</strong> contributes the highest volume in this group, with a lifetime outward volume of <strong>${{formatCurrency(largestClient.Total_Sales)}}</strong>, which is <strong>${{((largestClient.Total_Sales / secondLargest.Total_Sales) * 100).toFixed(0)}}%</strong> of the next highest account (<strong>${{secondLargest.Particulars}}</strong>: ${{formatCurrency(secondLargest.Total_Sales)}}).`;
            insightsContainer.appendChild(largestLI);
            
            const growthRatesList = selectedRecords.map((r, idx) => ({{ name: r.Particulars, rate: growthData[idx] }}));
            growthRatesList.sort((a,b) => b.rate - a.rate);
            
            const topGrower = growthRatesList[0];
            const bottomGrower = growthRatesList[growthRatesList.length - 1];
            
            if (topGrower.rate > 0) {{
                const growerLI = document.createElement('li');
                growerLI.innerHTML = `<strong>High Growth Leader:</strong> <strong>${{topGrower.name}}</strong> demonstrates the best trajectory, growing at a rapid pace of <strong>+${{topGrower.rate.toFixed(1)}}%</strong> YoY in the last reported period.`;
                insightsContainer.appendChild(growerLI);
            }}
            
            if (bottomGrower.rate < 0) {{
                const declineLI = document.createElement('li');
                declineLI.innerHTML = `<strong>Attention Required:</strong> <strong>${{bottomGrower.name}}</strong> is exhibiting declining volume at <strong>${{bottomGrower.rate.toFixed(1)}}%</strong> YoY. Re-engagement is recommended to avoid further revenue leakage.`;
                insightsContainer.appendChild(declineLI);
            }}
            
            const lostClients = selectedRecords.filter(r => r.Status === "Lost");
            if (lostClients.length > 0) {{
                const lostLI = document.createElement('li');
                lostLI.innerHTML = `⚠️ <strong>Churn Warning:</strong> <strong>${{lostClients.map(c => c.Particulars).join(', ')}}</strong> is categorized as <strong>Lost</strong> in the latest period. Proactive outreach should be prioritized.`;
                insightsContainer.appendChild(lostLI);
            }}
        }}

        function switchTab(tabId, el) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.dashboard-section').forEach(sect => sect.classList.remove('active'));
            
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
                let matchesStatus = false;
                if (currentStatusFilter === "ALL") {{
                    matchesStatus = true;
                }} else if (currentStatusFilter === "Declining") {{
                    matchesStatus = r.Status === "Retained" && r.FY_25_26 < r.FY_24_25 && r.FY_24_25 > 0;
                }} else {{
                    matchesStatus = r.Status === currentStatusFilter;
                }}
                return matchesSearch && matchesStatus;
            }});
            
            // Interactivity Feature: Update Filtered Sum
            const filteredSum = filteredRecords.reduce((sum, r) => sum + r.Total_Sales, 0);
            const statusLabelText = currentStatusFilter === "ALL" ? "All Accounts" : (currentStatusFilter === "Declining" ? "Slipping Accounts" : `${{currentStatusFilter}} Accounts`);
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

                let displayStatus = r.Status;
                let displayStatusClass = r.Status.toLowerCase();
                if (r.Status === "Retained" && r.FY_25_26 < r.FY_24_25 && r.FY_24_25 > 0) {{
                    displayStatus = "Slipping";
                    displayStatusClass = "slipping";
                }}

                let fy24_25_val = formatCurrency(r.FY_24_25);
                if (r.FY_23_24 > 0 && r.FY_24_25 < r.FY_23_24) {{
                    fy24_25_val = `<span style="color: #f97316;" title="Declined from previous year">▼ ${{fy24_25_val}}</span>`;
                }} else if (r.FY_23_24 > 0 && r.FY_24_25 > r.FY_23_24) {{
                    fy24_25_val = `<span style="color: var(--success);" title="Grew from previous year">▲ ${{fy24_25_val}}</span>`;
                }}

                let fy25_26_val = formatCurrency(r.FY_25_26);
                if (r.FY_24_25 > 0 && r.FY_25_26 < r.FY_24_25) {{
                    fy25_26_val = `<span style="color: #f97316;" title="Declined from previous year">▼ ${{fy25_26_val}}</span>`;
                }} else if (r.FY_24_25 > 0 && r.FY_25_26 > r.FY_24_25) {{
                    fy25_26_val = `<span style="color: var(--success);" title="Grew from previous year">▲ ${{fy25_26_val}}</span>`;
                }}

                tr.innerHTML = `
                    <td style="font-weight: 500; color: #fff;">${{r.Particulars}}</td>
                    <td style="text-align: center;"><span class="badge badge-${{displayStatusClass}}">${{displayStatus}}</span></td>
                    <td style="text-align: right;">${{formatCurrency(r.FY_23_24)}}</td>
                    <td style="text-align: right;">${{fy24_25_val}}</td>
                    <td style="text-align: right;">${{fy25_26_val}}</td>
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
            
            const slippingList = records
                .filter(r => r.Status === "Retained" && r.FY_25_26 < r.FY_24_25 && r.FY_24_25 > 0)
                .map(r => ({{ ...r, drop: r.FY_24_25 - r.FY_25_26 }}))
                .sort((a, b) => b.drop - a.drop)
                .slice(0, 30);

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

            const slippingContainer = document.getElementById('slipping-list-container');
            if (slippingContainer) {{
                slippingContainer.innerHTML = "";
                slippingList.forEach(r => {{
                    const item = document.createElement('div');
                    item.className = "missed-item";
                    item.onclick = () => openModal(r);
                    item.style.cursor = "pointer";
                    item.innerHTML = `
                        <div>
                            <div class="missed-client-name">${{r.Particulars}}</div>
                            <div class="missed-sub">Buying Less: FY25-26 ₹${{r.FY_25_26.toLocaleString('en-IN')}} vs FY24-25 ₹${{r.FY_24_25.toLocaleString('en-IN')}}</div>
                        </div>
                        <div class="missed-lost-value" style="color: #f97316;">- ₹${{r.drop.toLocaleString('en-IN')}}</div>
                    `;
                    slippingContainer.appendChild(item);
                }});
            }}

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
