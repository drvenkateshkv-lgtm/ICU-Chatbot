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

# ---------------- VIEW ----------------
view_mode = st.radio("Select View", ["Doctor View", "Family View"], horizontal=True)

st.divider()

# ---------------- FUNCTIONS ----------------

def interpret_risk(prob):
    if prob < 0.3:
        return "Mild", \
        "Low predicted mortality risk", \
        "At present, the condition appears relatively stable, and we are hopeful with ongoing treatment."

    elif prob <= 0.7:
        return "Moderate", \
        "Moderate predicted mortality risk", \
        "The illness is serious, and there is a significant risk. Recovery is possible, but uncertain, and requires close monitoring."

    else:
        return "High", \
        "High predicted mortality risk", \
        "The condition is very critical, and there is a high risk to life at this stage. Recovery is uncertain, and we are providing maximum possible support."

def trend_text(tr):
    if tr == "improving":
        return "There are encouraging signs of improvement."
    elif tr == "worsening":
        return "The condition is worsening."
    return "The condition is currently stable."

def family_supports(v, p, d, s):
    supports = []
    if v:
        supports.append("a breathing machine")
    if p:
        supports.append("medications for blood pressure")
    if d:
        supports.append("a machine to clean the blood")
    if s:
        supports.append("medications for comfort")
    return ", ".join(supports) if supports else "close monitoring"

def doctor_supports(v, p, d, s):
    supports = []
    if v:
        supports.append("Mechanical Ventilation")
    if p:
        supports.append("Vasopressors")
    if d:
        supports.append("CRRT")
    if s:
        supports.append("Sedation")
    return ", ".join(supports)

def key_concerns(v, p, d):
    concerns = []
    if v:
        concerns.append("Breathing support requirement")
    if p:
        concerns.append("Low blood pressure requiring support")
    if d:
        concerns.append("Kidney function support")
    return concerns

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

        concerns_list = key_concerns(ventilator, pressors, dialysis)
        concerns_text = ", ".join(concerns_list) if concerns_list else "No major organ concerns at present"

        # Doctor summary
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

Key Concerns: {concerns_text}
"""

        # Family communication
        family_output = f"""
ICU FAMILY UPDATE

Patient: {name}
Diagnosis: {diagnosis}

Current condition:
{trend_text(trend)}

Risk level:
{risk}

What this means:
{family_risk_text}

Key concerns right now:
{concerns_text}

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
