import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pdfkit
import tempfile
import os

# ---- Full, clean STROBE Checklist ----
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

st.set_page_config(page_title="STROBE Compact Self-Assessment", layout="wide")
st.title("📝 STROBE Self-Assessment Tool for TriNetX Projects (Compact Table)")

st.markdown("""
This tool helps you assess your TriNetX project using the full STROBE checklist in a single compact table.  
- **Score**: 1 (Not addressed), 2 (Partially), 3 (Fully addressed)  
- **Add comments** in-line  
- **Click a row** to see detailed guidance  
- **Export results** as CSV or PDF  
""")

# Prepare DataFrame for grid
df = pd.DataFrame([
    {
        "Section": item["section"],
        "Checklist Item": item["item"],
        "Score": 2,
        "Comments": "",
        "Guidance": item["guidance"],
        "Link": item["link"],
    }
    for item in STROBE_ITEMS
])

# Build grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column("Score", editable=True, cellEditor='agSelectCellEditor',
                    cellEditorParams={'values': [1, 2, 3]})
gb.configure_column("Comments", editable=True)
gb.configure_column("Checklist Item", width=420, wrapText=True, autoHeight=True)
gb.configure_column("Guidance", hide=True)
gb.configure_column("Link", hide=True)
gb.configure_selection(selection_mode="single", use_checkbox=True)
gridOptions = gb.build()

# Display grid
response = AgGrid(
    df,
    gridOptions=gridOptions,
    update_mode=GridUpdateMode.VALUE_CHANGED | GridUpdateMode.SELECTION_CHANGED,
    fit_columns_on_grid_load=True,
    allow_unsafe_jscode=True,
    height=600,
    theme="streamlit"
)

# Guidance for selected row
selected = response["selected_rows"]
if selected:
    st.info(f"**Guidance for selected item:**\n\n{selected[0]['Guidance']}\n\n[More Info]({selected[0]['Link']})")

# Compile new DataFrame
df_updated = pd.DataFrame(response['data'])

# Summarize scores
percent_fully = round(100 * (df_updated["Score"] == 3).sum() / len(df_updated), 1)
st.write(f"**Percent fully addressed:** {percent_fully}%")
st.write(f"**Average score:** {round(df_updated['Score'].mean(), 2)} / 3")

low_score_df = df_updated[df_updated["Score"] < 3]
if not low_score_df.empty:
    st.warning("### Areas for Improvement")
    for idx, row in low_score_df.iterrows():
        st.markdown(
            f"- **{row['Section']}**: {row['Checklist Item']}\n"
            f"  - Guidance: {row['Guidance']}\n"
            f"  - Your score: {row['Score']}\n"
            f"  - Your comment: {row['Comments']}"
        )
else:
    st.success("All items fully addressed! ✅")

# Download as CSV
csv = df_updated.to_csv(index=False).encode()
st.download_button(
    label="📥 Download as CSV",
    data=csv,
    file_name="strobe_self_assessment.csv",
    mime="text/csv",
)

# PDF Export
def df_to_html(df, low_score_df):
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
    if not low_score_df.empty:
        html += "<ul>"
        for idx, row in low_score_df.iterrows():
            html += f"<li><b>{row['Section']}</b>: {row['Checklist Item']}<br>"
            html += f"Guidance: {row['Guidance']}<br>"
            html += f"Your score: {row['Score']}<br>"
            html += f"Your comment: {row['Comments']}</li><br>"
        html += "</ul>"
    else:
        html += "<p>All items fully addressed! ✅</p>"
    html += "</body></html>"
    return html

if st.button("📄 Download as PDF"):
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tf:
        html = df_to_html(df_updated, low_score_df)
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
