from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

# --------------------------------------------------
# Create Flask application
# --------------------------------------------------

app = Flask(__name__)


# --------------------------------------------------
# Load all three trained ML models
# --------------------------------------------------

readmission_model = joblib.load(
    "hospital_readmission_model.pkl"
)

cost_model = joblib.load(
    "hospital_cost_model.pkl"
)

condition_model = joblib.load(
    "hospital_condition_model.pkl"
)


# --------------------------------------------------
# Home Page
# --------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------------------------
# Readmission Prediction
# --------------------------------------------------

@app.route("/predict-readmission", methods=["POST"])
def predict_readmission():

    try:

        data = request.get_json()

        patient_data = pd.DataFrame([{

            "Age": float(data["Age"]),

            "Gender": data["Gender"],

            "Condition": data["Condition"],

            "Procedure": data["Procedure"],

            "Cost": float(data["Cost"]),

            "Length_of_Stay": float(data["Length_of_Stay"]),

            "Satisfaction": float(data["Satisfaction"])

        }])

        # Make prediction
        prediction = readmission_model.predict(
            patient_data
        )[0]

        # Get probability
        probability = readmission_model.predict_proba(
            patient_data
        )[0][1]

        # Convert prediction to readable result
        if prediction == 1:

            result = "High Risk of Readmission"

        else:

            result = "Low Risk of Readmission"

        return jsonify({

            "result": result,

            "probability": round(
                float(probability) * 100,
                2
            )

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


# --------------------------------------------------
# Treatment Cost Prediction
# --------------------------------------------------

@app.route("/predict-cost", methods=["POST"])
def predict_cost():

    try:

        data = request.get_json()

        patient_data = pd.DataFrame([{

            "Age": float(data["Age"]),

            "Gender": data["Gender"],

            "Condition": data["Condition"],

            "Procedure": data["Procedure"],

            "Length_of_Stay": float(
                data["Length_of_Stay"]
            ),

            "Satisfaction": float(
                data["Satisfaction"]
            )

        }])

        # Predict treatment cost
        predicted_cost = cost_model.predict(
            patient_data
        )[0]

        return jsonify({

            "predicted_cost": round(
                float(predicted_cost),
                2
            )

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


# --------------------------------------------------
# Condition Prediction
# --------------------------------------------------

@app.route("/predict-condition", methods=["POST"])
def predict_condition():

    try:

        data = request.get_json()

        patient_data = pd.DataFrame([{

            "Age": float(data["Age"]),

            "Gender": data["Gender"],

            "Procedure": data["Procedure"],

            "Cost": float(data["Cost"]),

            "Length_of_Stay": float(
                data["Length_of_Stay"]
            ),

            "Satisfaction": float(
                data["Satisfaction"]
            )

        }])

        # Predict condition
        predicted_condition = condition_model.predict(
            patient_data
        )[0]

        # Get probability
        probabilities = condition_model.predict_proba(
            patient_data
        )[0]

        # Find highest probability
        confidence = max(probabilities) * 100

        return jsonify({

            "condition": predicted_condition,

            "confidence": round(
                float(confidence),
                2
            )

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


# --------------------------------------------------
# Run Flask application
# --------------------------------------------------

if __name__ == "__main__":

    app.run(debug=True)