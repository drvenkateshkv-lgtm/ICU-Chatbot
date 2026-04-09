import streamlit as st

st.title("🩺 ICU Family Communication Assistant (Offline Mode)")

st.header("Patient Details")

name = st.text_input("Patient Name")
age = st.number_input("Age", 0, 120)
diagnosis = st.text_input("Diagnosis")

st.header("Clinical Data")

sofa = st.slider("SOFA Score", 0, 20)
pf = st.number_input("P/F Ratio", value=150)
trend = st.selectbox("Trend", ["improving", "stable", "worsening"])
icu_day = st.number_input("ICU Day", value=1)

st.header("Organ Support")

ventilator = st.checkbox("Ventilator")
pressors = st.checkbox("Vasopressors")
dialysis = st.checkbox("Dialysis (CRRT)")
sedation = st.checkbox("Sedation")

def get_mortality(sofa):
    if sofa <= 6:
        return "Low risk (<10%)"
    elif 7 <= sofa <= 9:
        return "Moderate risk (15–20%)"
    elif 10 <= sofa <= 12:
        return "High risk (40–50%)"
    else:
        return "Very high risk (>80%)"

def get_ards(pf):
    if pf >= 200:
        return "Mild lung involvement"
    elif 100 <= pf < 200:
        return "Moderate lung involvement"
    else:
        return "Severe lung involvement"

def explain_supports():
    explanations = []
    
    if ventilator:
        explanations.append("a breathing machine helping the lungs rest")
    if pressors:
        explanations.append("medications supporting blood pressure")
    if dialysis:
        explanations.append("a machine cleaning the blood")
    if sedation:
        explanations.append("a medically controlled sleep for comfort")
    
    return explanations

def trend_text(trend):
    if trend == "improving":
        return "There are encouraging signs of improvement."
    elif trend == "worsening":
        return "We are concerned as the condition is worsening."
    else:
        return "The condition is currently stable."

if st.button("Generate Family Update"):

    mortality = get_mortality(sofa)
    ards = get_ards(pf)
    supports = explain_supports()
    trend_msg = trend_text(trend)

    support_text = ", ".join(supports) if supports else "no major organ support required at present"

    response = f"""
Hello, I understand this is a very difficult and stressful time for you.

Your loved one, {name}, is currently in the ICU being treated for {diagnosis}.

At present:
- {trend_msg}
- Lung condition: {ards}
- Severity: {mortality}

We are supporting the body using {support_text}.

In the next 24 hours, we will focus on stabilizing the condition and monitoring closely.

What questions do you have for us today?
"""

    st.subheader("📢 ICU Family Update")
    st.write(response)