// =========================================
// GET PATIENT DATA
// =========================================

function getPatientData() {

    return {

        Age: document.getElementById("Age").value,

        Gender: document.getElementById("Gender").value,

        Condition: document.getElementById("Condition").value,

        Procedure: document.getElementById("Procedure").value,

        Cost: document.getElementById("Cost").value,

        Length_of_Stay:
            document.getElementById("Length_of_Stay").value,

        Satisfaction:
            document.getElementById("Satisfaction").value

    };
}


// =========================================
// CHECK REQUIRED INPUTS
// =========================================

function validatePatientData() {

    const data = getPatientData();

    for (let key in data) {

        if (data[key] === "") {

            alert("Please enter " + key);

            return false;
        }
    }

    return true;
}


// =========================================
// READMISSION PREDICTION
// =========================================

async function predictReadmission() {

    if (!validatePatientData()) {
        return;
    }

    const resultDiv =
        document.getElementById("readmissionResult");

    resultDiv.innerHTML =
        "<p>Processing...</p>";

    const patientData = getPatientData();

    try {

        const response = await fetch(
            "/predict-readmission",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(patientData)
            }
        );


        const data = await response.json();


        if (data.error) {

            resultDiv.innerHTML =
                "<p>Error: " + data.error + "</p>";

            return;
        }


        resultDiv.innerHTML =

            "<div class='result-value'>" +
            data.result +
            "</div>" +

            "<p>Probability: " +
            data.probability +
            "%</p>";

    }

    catch (error) {

        resultDiv.innerHTML =
            "<p>Unable to connect to server.</p>";
    }
}


// =========================================
// COST PREDICTION
// =========================================

async function predictCost() {

    if (!validatePatientData()) {
        return;
    }

    const resultDiv =
        document.getElementById("costResult");

    resultDiv.innerHTML =
        "<p>Calculating...</p>";

    const patientData = getPatientData();


    try {

        const response = await fetch(
            "/predict-cost",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(patientData)
            }
        );


        const data = await response.json();


        if (data.error) {

            resultDiv.innerHTML =
                "<p>Error: " + data.error + "</p>";

            return;
        }


        resultDiv.innerHTML =

            "<div class='result-value'>" +

            "₹ " +

            data.predicted_cost.toFixed(2) +

            "</div>";


    }

    catch (error) {

        resultDiv.innerHTML =
            "<p>Unable to connect to server.</p>";
    }
}


// =========================================
// CONDITION PREDICTION
// =========================================

async function predictCondition() {

    if (!validatePatientData()) {
        return;
    }

    const resultDiv =
        document.getElementById("conditionResult");

    resultDiv.innerHTML =
        "<p>Analyzing...</p>";

    const patientData = getPatientData();


    try {

        const response = await fetch(
            "/predict-condition",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(patientData)
            }
        );


        const data = await response.json();


        if (data.error) {

            resultDiv.innerHTML =
                "<p>Error: " + data.error + "</p>";

            return;
        }


        resultDiv.innerHTML =

            "<div class='result-value'>" +

            data.condition +

            "</div>" +

            "<p>Confidence: " +

            data.confidence +

            "%</p>";

    }

    catch (error) {

        resultDiv.innerHTML =
            "<p>Unable to connect to server.</p>";
    }
}