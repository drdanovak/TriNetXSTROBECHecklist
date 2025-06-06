import streamlit as st
import pandas as pd
import pdfkit
import tempfile
import os

# ---- Full STROBE Checklist with Guidance and Links ----
STROBE_ITEMS = [
    {"section": "Title and Abstract", "item": "1. Indicate the study’s design with a commonly used term in the title or the abstract.", "guidance": "Clearly state the study design (e.g., cohort, case-control, cross-sectional) in the title or abstract.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Title and Abstract", "item": "2. Provide in the abstract an informative and balanced summary of what was done and what was found.", "guidance": "Summarize study purpose, methods, key results, and conclusions in the abstract.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Introduction", "item": "3. Explain the scientific background and rationale for the investigation being reported.", "guidance": "Describe why the study was done, with context and relevant literature.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Introduction", "item": "4. State specific objectives, including any prespecified hypotheses.", "guidance": "Clearly state what you set out to do, including hypotheses.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "5. Present key elements of study design early in the paper.", "guidance": "Identify the type of study and its key design features.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "6. Describe the setting, locations, and relevant dates, including periods of recruitment, exposure, follow-up, and data collection.", "guidance": "State where and when the study was done.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "7. (a) Give the eligibility criteria, and the sources and methods of selection of participants. (b) Describe methods of follow-up. (c) For matched studies, give matching criteria and number of exposed/unexposed.", "guidance": "Explain how participants were identified, included, excluded, and how they were followed up.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "8. For each variable of interest, give sources of data and details of methods of assessment (measurement).", "guidance": "Describe how each variable was measured or obtained.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "9. Describe any efforts to address potential sources of bias.", "guidance": "Discuss what you did to minimize bias (e.g., blinding, statistical adjustments).", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "10. Explain how the study size was arrived at.", "guidance": "Provide rationale for sample size, power calculations if possible.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "11. Explain how quantitative variables were handled in the analyses. If applicable, describe which groupings were chosen and why.", "guidance": "Describe handling of quantitative data (e.g., categorized, continuous).", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "12. Describe all statistical methods, including those used to control for confounding.", "guidance": "Outline your statistical approach, including confounder adjustment, missing data handling, etc.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Results", "item": "13. (a) Report numbers of individuals at each stage of study (e.g., eligible, included, follow-up, analyzed). (b) Give reasons for non-participation at each stage. (c) Consider use of a flow diagram.", "guidance": "Show a flow of participant numbers, with reasons for exclusions.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Results", "item": "14. (a) Give characteristics of study participants (e.g., demographic, clinical, social) and information on exposures and potential confounders. (b) Indicate number of participants with missing data for each variable. (c) Summarize follow-up time.", "guidance": "Provide descriptive stats for the sample, and report missing data.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Results", "item": "15. Report numbers of outcome events or summary measures over time.", "guidance": "Present main outcome data (events, summary measures).", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Results", "item": "16. (a) Give unadjusted estimates and, if applicable, confounder-adjusted estimates and their precision (e.g., 95% confidence interval). (b) Report category boundaries when continuous variables were categorized. (c) If relevant, consider translating estimates of relative risk into absolute risk.", "guidance": "Show both crude and adjusted results with precision (CIs), and define any group boundaries.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Results", "item": "17. Report other analyses done (e.g., subgroup analyses and sensitivity analyses).", "guidance": "Describe any secondary, subgroup, or sensitivity analyses.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Discussion", "item": "18. Summarize key results with reference to study objectives.", "guidance": "Recap the main findings in light of the objectives.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Discussion", "item": "19. Discuss limitations of the study, taking into account sources of potential bias or imprecision. Discuss both direction and magnitude of any potential bias.", "guidance": "Acknowledge weaknesses and possible biases; discuss direction and size.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Discussion", "item": "20. Give a cautious overall interpretation of results considering objectives, limitations, multiplicity of analyses, results from similar studies, and other relevant evidence.", "guidance": "Discuss meaning and context, but avoid overstating conclusions.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Discussion", "item": "21. Discuss the generalizability (external validity) of the study results.", "guidance": "Comment on how well results may apply elsewhere.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Other Information", "item": "22. Give the source of funding and the role of the funders for the present study and, if applicable, for the original study on which the present article is based.", "guidance": "State how the study was funded and any role of the sponsor.", "link": "https://www.strobe-statement.org/checklists/"},
]

st.set_page_config(page_title="STROBE Self-Assessment for TriNetX", layout="wide")
st.title("📝 STROBE Self-Assessment Tool for TriNetX Projects")

st.markdown("""
Evaluate your observational study using the full **STROBE Statement** checklist.
- Score each item 1 (not addressed), 2 (partially addressed), or 3 (fully addressed).
- Add comments if you wish.
- Download your completed checklist as a PDF or CSV.
- At the end, you’ll get a summary of strengths and areas for improvement.
[Full STROBE guidance](https://www.strobe-statement.org/index.php?id=available-checklists)
""")

# Set up persistent session state
if 'scores' not in st.session_state:
    st.session_state.scores = [2]*len(STROBE_ITEMS)
if 'comments' not in st.session_state:
    st.session_state.comments = [""]*len(STROBE_ITEMS)

score_labels = {
    1: "1 = Not addressed",
    2: "2 = Partially addressed",
    3: "3 = Fully addressed"
}

with st.form("strobe_form"):
    st.write("### Checklist")
    for idx, item in enumerate(STROBE_ITEMS):
        st.markdown(f"**{item['section']}** — [{item['item']}]({item['link']})")
        with st.expander(f"Guidance for item {idx+1}", expanded=False):
            st.write(item["guidance"])
        col1, col2 = st.columns([1, 3])
        with col1:
            score = st.radio(
                f"Score (1–3) for item {idx+1}",
                [1, 2, 3],
                format_func=lambda x: score_labels[x],
                key=f"score_{idx}",
                index=st.session_state.scores[idx]-1
            )
        with col2:
            comment = st.text_area(
                f"Comments for item {idx+1}",
                value=st.session_state.comments[idx],
                key=f"comment_{idx}"
            )
        # Save to session
        st.session_state.scores[idx] = score
        st.session_state.comments[idx] = comment
        st.markdown("---")
    submitted = st.form_submit_button("Submit Self-Assessment")

# --- Compile results ---
if submitted:
    df = pd.DataFrame([
        {
            "Section": item["section"],
            "Checklist Item": item["item"],
            "Score": st.session_state.scores[idx],
            "Comments": st.session_state.comments[idx],
            "Guidance Link": item["link"]
        }
        for idx, item in enumerate(STROBE_ITEMS)
    ])
    st.success("Assessment Complete!")
    st.dataframe(df)

    percent_fully = round(100 * sum(s == 3 for s in st.session_state.scores) / len(STROBE_ITEMS), 1)
    st.write(f"**Percent fully addressed:** {percent_fully}%")
    st.write(f"**Average score:** {round(sum(st.session_state.scores)/len(STROBE_ITEMS), 2)} / 3")

    # --- Areas for improvement summary ---
    low_score_idxs = [i for i, s in enumerate(st.session_state.scores) if s < 3]
    if low_score_idxs:
        st.warning("### Areas for Improvement")
        for i in low_score_idxs:
            st.markdown(
                f"- **{STROBE_ITEMS[i]['section']}**: [{STROBE_ITEMS[i]['item']}]({STROBE_ITEMS[i]['link']})\n"
                f"  - Guidance: {STROBE_ITEMS[i]['guidance']}\n"
                f"  - Your score: {st.session_state.scores[i]}\n"
                f"  - Your comment: {st.session_state.comments[i]}"
            )
    else:
        st.success("All items fully addressed! ✅")

    # --- Download options ---
    csv = df.to_csv(index=False).encode()
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="strobe_self_assessment.csv",
        mime="text/csv",
    )

    # --- PDF Export (using pdfkit, must have wkhtmltopdf installed on server) ---
    def df_to_html(df):
        # Simple HTML template
        html = f"""
        <html>
        <head>
            <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ccc; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
        <h1>STROBE Self-Assessment Results</h1>
        {df.to_html(index=False, escape=False)}
        <h2>Areas for Improvement</h2>
        """
        if low_score_idxs:
            html += "<ul>"
            for i in low_score_idxs:
                html += f"<li><b>{STROBE_ITEMS[i]['section']}</b>: {STROBE_ITEMS[i]['item']}<br>"
                html += f"Guidance: {STROBE_ITEMS[i]['guidance']}<br>"
                html += f"Your score: {st.session_state.scores[i]}<br>"
                html += f"Your comment: {st.session_state.comments[i]}</li><br>"
            html += "</ul>"
        else:
            html += "<p>All items fully addressed! ✅</p>"
        html += "</body></html>"
        return html

    if st.button("📄 Download as PDF"):
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tf:
            html = df_to_html(df)
            tf.write(html.encode())
            tf.flush()
            pdf_path = tf.name.replace(".html", ".pdf")
            try:
                pdfkit.from_file(tf.name, pdf_path)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_file.read(),
                        file_name="strobe_self_assessment.pdf",
                        mime="application/pdf"
                    )
                os.remove(pdf_path)
            except Exception as e:
                st.error(f"PDF generation failed: {e}. "
                         "Is `wkhtmltopdf` installed on the server? (Try CSV instead.)")
            finally:
                os.remove(tf.name)
