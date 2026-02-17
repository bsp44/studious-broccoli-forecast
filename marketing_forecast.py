"""
Marketing Channel Performance Forecasting Tool
Forecasts lead volume changes based on spend adjustments, accounting for efficiency decay
"""

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def forecast_leads(current_spend, current_leads, spend_change_percent, elasticity=0.82):
    """
    Forecast lead volume using a power-law (elasticity) model.
    
    Lead volume scales with spend^elasticity, so:
      new_leads / current_leads = (new_spend / current_spend) ** elasticity
    
    This gives smooth diminishing returns: a 10% spend increase might yield
    ~8% more leads (elasticity 0.82), while a 50% increase yields proportionally
    less (e.g. ~38% more leads). Same formula works for spend decreases.
    
    Elasticity in the 0.75–0.88 range is typical for paid search/social; lower
    = more diminishing returns, higher = closer to linear.
    
    Args:
        current_spend: Current daily spend (e.g., 12500)
        current_leads: Current daily leads (e.g., 1928)
        spend_change_percent: Percentage change in spend (e.g., 10 for 10% increase)
        elasticity: Lead elasticity vs spend (default 0.82). 1.0 = linear; 0.8 = strong diminishing returns.
    
    Returns:
        Dictionary with forecasted metrics
    """
    # Clamp elasticity to a sensible range
    elasticity = max(0.5, min(1.0, float(elasticity)))
    
    # New spend
    spend_multiplier = 1 + (spend_change_percent / 100)
    new_spend = current_spend * spend_multiplier
    
    # Power-law: leads scale as spend^elasticity
    lead_multiplier = spend_multiplier ** elasticity
    new_leads = current_leads * lead_multiplier
    
    # Derived: effective "efficiency" (lead % change / spend % change) for display
    if spend_change_percent == 0:
        efficiency = 1.0
        lead_change_percent = 0.0
    else:
        lead_change_percent = (lead_multiplier - 1) * 100
        efficiency = lead_change_percent / spend_change_percent
        efficiency = max(0.0, min(2.0, efficiency))  # clamp for display
    
    # Calculate metrics
    current_cpl = current_spend / current_leads if current_leads > 0 else 0
    new_cpl = new_spend / new_leads if new_leads > 0 else 0
    cpl_change = ((new_cpl - current_cpl) / current_cpl * 100) if current_cpl > 0 else 0
    
    spend_change_absolute = new_spend - current_spend
    leads_change_absolute = new_leads - current_leads
    
    return {
        "current_spend": round(current_spend, 2),
        "current_leads": round(current_leads, 2),
        "current_cpl": round(current_cpl, 2),
        "spend_change_percent": round(spend_change_percent, 2),
        "new_spend": round(new_spend, 2),
        "spend_change_absolute": round(spend_change_absolute, 2),
        "efficiency_factor": round(efficiency * 100, 1),  # As percentage (can exceed 100 when cutting spend)
        "lead_change_percent": round(lead_change_percent, 2),
        "new_leads": round(new_leads, 2),
        "leads_change_absolute": round(leads_change_absolute, 2),
        "new_cpl": round(new_cpl, 2),
        "cpl_change_percent": round(cpl_change, 2),
        "elasticity": round(elasticity, 2),
    }


@app.route('/')
def index():
    """Render the main forecasting tool page"""
    return render_template('forecast.html')


@app.route('/api/forecast', methods=['POST'])
def api_forecast():
    """API endpoint for calculating forecasts"""
    try:
        data = request.get_json()
        
        current_spend = float(data.get('current_spend', 0))
        current_leads = float(data.get('current_leads', 0))
        spend_change_percent = float(data.get('spend_change_percent', 0))
        elasticity = data.get('elasticity')
        if elasticity is not None:
            elasticity = float(elasticity)
        else:
            elasticity = 0.82
        
        # Validation
        if current_spend <= 0:
            return jsonify({"error": "Current spend must be greater than 0"}), 400
        if current_leads <= 0:
            return jsonify({"error": "Current leads must be greater than 0"}), 400
        
        result = forecast_leads(current_spend, current_leads, spend_change_percent, elasticity=elasticity)
        return jsonify(result)
    
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug, host='0.0.0.0', port=port)

