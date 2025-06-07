import streamlit as st
import pandas as pd

# ---- Full STROBE Checklist ----
STROBE_ITEMS = [
    {"section": "Title and Abstract", "item": "Indicate the study’s design with a commonly used term in the title or the abstract.", "guidance": "Clearly state the study design (e.g., cohort, case-control, cross-sectional) in the title or abstract.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Title and Abstract", "item": "Provide in the abstract an informative and balanced summary of what was done and what was found.", "guidance": "Summarize study purpose, methods, key results, and conclusions in the abstract.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Introduction", "item": "Explain the scientific background and rationale for the investigation being reported.", "guidance": "Describe why the study was done, with context and relevant literature.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Introduction", "item": "State specific objectives, including any prespecified hypotheses.", "guidance": "Clearly state what you set out to do, including hypotheses.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "Present key elements of study design early in the paper.", "guidance": "Identify the type of study and its key design features.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "Describe the setting, locations, and relevant dates, including periods of recruitment, exposure, follow-up, and data collection.", "guidance": "State where and when the study was done.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "Give the eligibility criteria, and the sources and methods of selection of participants. Describe methods of follow-up. For matched studies, give matching criteria and number of exposed/unexposed.", "guidance": "Explain how participants were identified, included, excluded, and how they were followed up.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "For each variable of interest, give sources of data and details of methods of assessment (measurement).", "guidance": "Describe how each variable was measured or obtained.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "Describe any efforts to address potential sources of bias.", "guidance": "Discuss what you did to minimize bias (e.g., blinding, statistical adjustments).", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "Explain how the study size was arrived at.", "guidance": "Provide rationale for sample size, power calculations if possible.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "Explain how quantitative variables were handled in the analyses. If applicable, describe which groupings were chosen and why.", "guidance": "Describe handling of quantitative data (e.g., categorized, continuous).", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Methods", "item": "Describe all statistical methods, including those used to control for confounding.", "guidance": "Outline your statistical approach, including confounder adjustment, missing data handling, etc.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Results", "item": "Report numbers of individuals at each stage of study (e.g., eligible, included, follow-up, analyzed). Give reasons for non-participation at each stage. Consider use of a flow diagram.", "guidance": "Show a flow of participant numbers, with reasons for exclusions.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Results", "item": "Give characteristics of study participants (e.g., demographic, clinical, social) and information on exposures and potential confounders. Indicate number of participants with missing data for each variable. Summarize follow-up time.", "guidance": "Provide descriptive stats for the sample, and report missing data.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Results", "item": "Report numbers of outcome events or summary measures over time.", "guidance": "Present main outcome data (events, summary measures).", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Results", "item": "Give unadjusted estimates and, if applicable, confounder-adjusted estimates and their precision (e.g., 95% confidence interval). Report category boundaries when continuous variables were categorized. If relevant, consider translating estimates of relative risk into absolute risk.", "guidance": "Show both crude and adjusted results with precision (CIs), and define any group boundaries.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Results", "item": "Report other analyses done (e.g., subgroup analyses and sensitivity analyses).", "guidance": "Describe any secondary, subgroup, or sensitivity analyses.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Discussion", "item": "Summarize key results with reference to study objectives.", "guidance": "Recap the main findings in light of the objectives.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Discussion", "item": "Discuss limitations of the study, taking into account sources of potential bias or imprecision. Discuss both direction and magnitude of any potential bias.", "guidance": "Acknowledge weaknesses and possible biases; discuss direction and size.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Discussion", "item": "Give a cautious overall interpretation of results considering objectives, limitations, multiplicity of analyses, results from similar studies, and other relevant evidence.", "guidance": "Discuss meaning and context, but avoid overstating conclusions.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Discussion", "item": "Discuss the generalizability (external validity) of the study results.", "guidance": "Comment on how well results may apply elsewhere.", "link": "https://www.strobe-statement.org/checklists/"},
    {"section": "Other Information", "item": "Give the source of funding and the role of the funders for the present study and, if applicable, for the original study on which the present article is based.", "guidance": "State how the study was funded and any role of the sponsor.", "link": "https://www.strobe-statement.org/checklists/"},
]

st.set_page_config(page_title="STROBE Self-Assessment (Redesigned)", layout="wide")
st.title("📝 STROBE Self-Assessment Tool for TriNetX Projects (Three-Column Design)")

st.markdown("""
**Instructions:**  
- Review each STROBE item and guidance.
- Select your score (1 = Not addressed, 2 = Partially, 3 = Fully).
- Optionally add feedback in the expandable comment box.
- Download your completed checklist as CSV.
""")

score_labels = {1: "1 = Not addressed", 2: "2 = Partially", 3: "3 = Fully addressed"}

if "scores" not in st.session_state:
    st.session_state.scores = [2] * len(STROBE_ITEMS)
if "comments" not in st.session_state:
    st.session_state.comments = [""] * len(STROBE_ITEMS)

with st.form("strobe_form"):
    st.markdown("### Self-Assessment Checklist")
    for idx, item in enumerate(STROBE_ITEMS):
        # Three columns: description, score, comment
        c1, c2, c3 = st.columns([3, 1, 2])
        with c1:
            st.markdown(
                f"**{item['section']}**<br>"
                f"<span style='font-weight:bold;'>{item['item']}</span>"
                f"<br><span style='font-size:0.85em; color: #555;'>{item['guidance']}</span>",
                unsafe_allow_html=True
            )
            st.markdown(f"<a href='{item['link']}' style='font-size:0.85em;' target='_blank'>[STROBE Guidance]</a>", unsafe_allow_html=True)
        with c2:
            score = st.selectbox(
                "",
                [1, 2, 3],
                index=st.session_state.scores[idx] - 1,
                format_func=lambda x: score_labels[x],
                key=f"score_{idx}"
            )
        with c3:
            with st.expander("Comments / Feedback", expanded=False):
                comment = st.text_area(
                    "",
                    value=st.session_state.comments[idx],
                    key=f"comment_{idx}"
                )
        st.session_state.scores[idx] = score
        st.session_state.comments[idx] = comment
        st.markdown("---")
    submitted = st.form_submit_button("Submit Self-Assessment")

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
    st.dataframe(df, use_container_width=True)

    percent_fully = round(100 * (df['Score'] == 3).sum() / len(df), 1)
    st.write(f"**Percent fully addressed:** {percent_fully}%")
    st.write(f"**Average score:** {round(df['Score'].mean(), 2)} / 3")

    low_scores = df[df["Score"] < 3]
    if not low_scores.empty:
        st.warning("### Areas for Improvement")
        for i, row in low_scores.iterrows():
            st.markdown(
                f"- **{row['Section']}**: [{row['Checklist Item']}]({row['Guidance Link']})  \n"
                f"  - Your score: {row['Score']}\n"
                f"  - Your comment: {row['Comments']}"
            )
    else:
        st.success("All items fully addressed! ✅")

    csv = df.to_csv(index=False).encode()
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="strobe_self_assessment.csv",
        mime="text/csv",
    )
