import streamlit as st

st.set_page_config(page_title="ICU Communication Assistant", layout="centered")

st.title("🩺 ICU Family Communication Assistant")

# ---------------- SESSION STATE ----------------
if "generated" not in st.session_state:
    st.session_state.generated = False

if "family_text" not in st.session_state:
    st.session_state.family_text = ""

if "doctor_text" not in st.session_state:
    st.session_state.doctor_text = ""

# ---------------- VIEW SELECT ----------------
view_mode = st.radio("Select View", ["Doctor View", "Family View"], horizontal=True)

st.divider()

# ================= FUNCTIONS =================

def interpret_risk(prob):
    if prob < 0.3:
        return "Low", "Low predicted mortality risk", "The overall situation appears relatively stable."
    elif prob <= 0.7:
        return "Moderate", "Moderate predicted mortality risk", "The condition is serious and requires close monitoring."
    else:
        return "High", "High predicted mortality risk", "The condition is critical and requires intensive care."

def trend_text(tr):
    if tr == "improving":
        return "Showing improvement"
    elif tr == "worsening":
        return "Condition worsening"
    return "Stable"

def family_supports(ventilator, pressors, dialysis, sedation):
    s = []
    if ventilator:
        s.append("a breathing machine")
    if pressors:
        s.append("medications for blood pressure")
    if dialysis:
        s.append("a machine to clean the blood")
    if sedation:
        s.append("medications for comfort")
    return ", ".join(s) if s else "close monitoring"

def doctor_supports(ventilator, pressors, dialysis, sedation):
    s = []
    if ventilator:
        s.append("Mechanical Ventilation")
    if pressors:
        s.append("Vasopressors")
    if dialysis:
        s.append("CRRT")
    if sedation:
        s.append("Sedation")
    return ", ".join(s)

# ================= DOCTOR VIEW =================
if view_mode == "Doctor View":

    st.header("🧑‍⚕️ Doctor Input")

    name = st.text_input("Patient Name")
    age = st.number_input("Age", 0, 120)
    diagnosis = st.text_input("Diagnosis")

    st.header("Clinical Data")
    sofa = st.slider("SOFA Score", 0, 20)
    pf = st.number_input("P/F Ratio", value=150)
    trend = st.selectbox("Trend", ["improving", "stable", "worsening"])
    icu_day = st.number_input("ICU Day", value=1)

    probability = st.number_input("Predicted mortality probability (0–1)", 0.0, 1.0, step=0.01)

    st.subheader("Organ Support")
    ventilator = st.checkbox("Ventilator")
    pressors = st.checkbox("Vasopressors")
    dialysis = st.checkbox("Dialysis")
    sedation = st.checkbox("Sedation")

    if st.button("Generate ICU Update"):

        risk, doctor_risk_text, family_risk_text = interpret_risk(probability)

        doctor_output = f"""
ICU DOCTOR SUMMARY

Patient: {name}, {age}
Diagnosis: {diagnosis}

SOFA: {sofa}
PF Ratio: {pf}
Trend: {trend}
ICU Day: {icu_day}

Support: {doctor_supports(ventilator, pressors, dialysis, sedation)}

Predicted Probability: {probability:.2f}
Risk Category: {risk}
Interpretation: {doctor_risk_text}
"""

        family_output = f"""
ICU FAMILY UPDATE

Patient: {name}
Diagnosis: {diagnosis}

Current condition:
{trend_text(trend)}

What this means:
{family_risk_text}

Support:
{family_supports(ventilator, pressors, dialysis, sedation)}

Next 24 hours:
Close monitoring and ongoing treatment

We understand this is a difficult time. The ICU team is doing everything possible and will keep you updated regularly.
"""

        st.session_state.generated = True
        st.session_state.family_text = family_output
        st.session_state.doctor_text = doctor_output

        st.success("Update generated. Switch to Family View.")

    if st.session_state.generated:
        st.subheader("📄 Doctor Summary")
        st.code(st.session_state.doctor_text)

# ================= FAMILY VIEW =================
else:

    st.header("💙 Family Communication")

    if not st.session_state.generated:
        st.warning("Please generate update in Doctor View first.")
    else:
        st.write(st.session_state.family_text)

        st.subheader("📋 Copy Message")
        st.code(st.session_state.family_text)
