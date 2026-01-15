from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "rainsafe_secret_key"

@app.route("/")
def home():
    return render_template("rainwater.html")

@app.route("/input")
def input_page():
    return render_template("rainwater2.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    # Store page 2 data in session
    session["rainfall"] = request.form["rainfall"]
    session["roof"] = request.form["roof"]
    session["soil"] = request.form["soil"]
    session["space"] = request.form["space"]
    session["source"] = request.form["source"]

    # Redirect to page 3
    return redirect(url_for("usage_page"))

@app.route("/usage")
def usage_page():
    return render_template("rainwater3.html")


@app.route("/recommend", methods=["POST"])
def recommend():
    # ---- Page 2 data from session ----
    rainfall = session.get("rainfall")
    roof = session.get("roof")
    soil = session.get("soil")
    space = session.get("space")
    source = session.get("source")

    # ---- Page 3 data from form ----
    climate = request.form["climate"]
    usage = request.form["usage"]
    served = request.form["served"]
    land = request.form["land"]
    storage = request.form["storage"]

    # ---- Extract numbers ----
    rainfall_mm = int(rainfall.split("—")[1].replace("mm", "").strip())
    roof_area_sqft = int(roof.split("—")[1].replace("sq.ft", "").strip())
    roof_area_m2 = roof_area_sqft * 0.092903

    runoff_coeff = 0.8
    if "metal" in roof.lower():
        runoff_coeff = 0.9
    elif "tile" in roof.lower():
        runoff_coeff = 0.75
    elif "thatch" in roof.lower():
        runoff_coeff = 0.6

    annual_liters = roof_area_m2 * rainfall_mm * runoff_coeff
    tank_size = annual_liters * 0.15
    savings = (annual_liters / 1000) * 15

    # ---- Recommendations ----
    recommendations = []

    recommendations = []

    # --- Climate-based recommendations ---
    if climate in ["Hot and dry", "Semi-arid"]:
        recommendations.append({
            "title": "Covered Storage Tank Recommended",
            "reason": "Your climate experiences high temperatures and evaporation losses. Covered tanks help reduce water loss and preserve stored rainwater."
        })

    elif climate in ["Humid coastal", "Tropical monsoon"]:
        recommendations.append({
            "title": "Overflow Recharge System Recommended",
            "reason": "High and intense rainfall in your region can cause overflow. Recharge pits help divert excess water safely into the ground."
        })

    # --- Usage-based recommendations ---
    if usage in ["Irrigation", "Kitchen garden"]:
        recommendations.append({
            "title": "Hybrid Storage + Recharge System",
            "reason": "Irrigation requires steady water availability. A hybrid system ensures immediate use through storage and long-term groundwater recharge."
        })

    elif usage == "Drinking (filtered)":
        recommendations.append({
            "title": "Filtration & First-Flush System Required",
            "reason": "Drinking purposes require higher water quality. Filtration and first-flush systems remove initial roof contaminants."
        })

    # --- Land-based recommendations ---
    if land in ["Slightly sloped", "Steep"]:
        recommendations.append({
            "title": "Controlled Runoff Channels Advised",
            "reason": "Sloped land increases runoff speed. Channels help guide water safely into storage or recharge structures."
        })

    # --- Storage preference ---
    if storage == "Both":
        recommendations.append({
            "title": "Hybrid Design Offers Maximum Flexibility",
            "reason": "Combining storage and recharge allows you to store usable water while also improving groundwater levels."
        })

    return render_template(
        "result.html",
        rainfall=rainfall,
        roof=roof,
        soil=soil,
        space=space,
        source=source,
        annual_liters=round(annual_liters, 2),
        tank_size=round(tank_size, 2),
        savings=round(savings, 2),
        recommendations=recommendations
    )

@app.route("/feedback")
def feedback():
    return render_template("rainwater4.html")


@app.route("/ping")
def ping():
    return "PONG - Flask backend is alive"

if __name__ == "__main__":
    app.run(debug=True)
