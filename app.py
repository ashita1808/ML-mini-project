from flask import Flask, render_template, request, jsonify, make_response
import pandas as pd
import numpy as np
import os
import io

app = Flask(__name__)

FEATURES = ["Month","DayOfWeek","CRSDepTime","CRSArrTime","Distance"]

current_predictions_df = None

# ------------------ ML (Dummy Model) ------------------
def predict_delay(df):
    df["DelayProbability"] = np.random.rand(len(df))
    df["PredictedDelay"] = (df["DelayProbability"] > 0.5).astype(int)
    return df

# ------------------ Gate Status Simulation ------------------
def assign_gate_status(df):
    gate_list = [f"{letter}{num}" for letter in ["A", "B", "C", "D"] for num in range(1, 11)]
    status_options = ["On Time", "Boarding", "Cleaning", "Departed", "Delayed"]

    gates = []
    statuses = []
    for _, row in df.iterrows():
        gate = np.random.choice(gate_list)
        if row["DelayProbability"] >= 0.75:
            status = "Delayed"
        elif row["PredictedDelay"] == 1:
            status = np.random.choice(["Delayed", "Boarding"])
        else:
            status = np.random.choice(status_options, p=[0.55, 0.2, 0.1, 0.1, 0.05])

        gates.append(gate)
        statuses.append(status)

    df["Gate"] = gates
    df["GateStatus"] = statuses
    return df

# ------------------ Weather (Simple Demo) ------------------
def get_weather(location="Demo City"):
    weather_types = ["Clear", "Cloudy", "Windy", "Rain", "Fog", "Storm"]
    condition = np.random.choice(weather_types)

    impact_map = {
        "Clear": 0,
        "Cloudy": 0.1,
        "Windy": 0.12,
        "Rain": 0.25,
        "Fog": 0.3,
        "Storm": 0.5
    }

    description_map = {
        "Clear": "Clear sky",
        "Cloudy": "Cloudy conditions",
        "Windy": "Windy conditions",
        "Rain": "Rain showers",
        "Fog": "Foggy visibility",
        "Storm": "Stormy weather"
    }

    temperature = int(np.random.uniform(10, 28))
    humidity = int(np.random.uniform(45, 90))

    return {
        "location": location,
        "condition": condition,
        "description": description_map.get(condition, condition),
        "temperature": temperature,
        "humidity": humidity,
        "impact": impact_map.get(condition, 0.15),
        "source": "demo"
    }

# ------------------ Staff Scheduling ------------------
def staff_calc(df):
    df["Hour"] = df["CRSDepTime"] // 100
    hourly = df.groupby("Hour").size()

    staff = []
    for h, flights in hourly.items():
        required = max(1, int(flights * 0.6))   # FIX: no zero staff
        available = int(required * np.random.uniform(0.7, 1.2))

        status = "OK" if available >= required else "Shortage"

        staff.append({
            "hour": int(h),
            "flights": int(flights),
            "required": int(required),
            "available": int(available),
            "status": status
        })

    return staff

# ------------------ ROUTE ------------------
@app.route("/", methods=["GET","POST"])
def index():
    kpis = None
    charts = {"labels": [], "values": []}
    table = None
    gate_data = None
    staff_data = None
    weather = None
    error = None

    if request.method == "POST":
        file = request.files.get("file")
        location = request.form.get("weather_location", "Demo City") or "Demo City"

        if not file:
            error = "Upload CSV file"
        else:
            try:
                df = pd.read_csv(file, encoding="latin1")

                # Keep required columns
                df = df[FEATURES].copy()
                df = df.fillna(0)

                # Prediction
                df = predict_delay(df)

                # Weather
                weather = get_weather(location)
                df["DelayProbability"] += weather["impact"]
                df["DelayProbability"] = df["DelayProbability"].clip(0,1)

                # Gate status
                df = assign_gate_status(df)

                # KPIs
                kpis = {
                    "total_flights": int(len(df)),
                    "delay_rate": round(df["PredictedDelay"].mean() * 100, 1),
                    "high_risk_flights": int((df["DelayProbability"] > 0.7).sum())
                }

                # Charts (SAFE JSON)
                delay_counts = df["PredictedDelay"].value_counts()

                charts = {
                    "labels": ["On Time", "Delayed"],
                    "values": [
                        int(delay_counts.get(0, 0)),
                        int(delay_counts.get(1, 0))
                    ]
                }

                # Staff
                staff_data = staff_calc(df)

                # Table
                table = df.drop(columns=["Gate", "GateStatus"], errors="ignore").head(20).to_html(classes="table table-striped", index=False)
                gate_data = df[["Gate", "GateStatus"]].head(20).to_dict(orient="records")

                global current_predictions_df
                current_predictions_df = df.copy()

            except Exception as e:
                error = str(e)

    return render_template(
        "index.html",
        kpis=kpis,
        charts=charts,
        table=table,
        gate_data=gate_data,
        staff_data=staff_data,
        weather=weather,
        error=error
    )

@app.route("/export")
def export_predictions():
    if current_predictions_df is None:
        return jsonify({"error": "No prediction data available. Upload CSV and run analysis."}), 400

    output = io.StringIO()
    current_predictions_df.to_csv(output, index=False)
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=flight_predictions.csv"
    response.headers["Content-Type"] = "text/csv"
    return response

# ------------------ API ------------------
@app.route("/api/staff")
def api_staff():
    return jsonify({"message": "Use UI to generate data"})

# ------------------ RUN ------------------
if __name__ == "__main__":
    app.run(debug=True)