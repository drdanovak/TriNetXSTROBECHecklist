import streamlit as st
import pandas as pd

# STROBE Checklist Items with customized sample comments for each
STROBE_ITEMS = [
    {
        "section": "Title and Abstract",
        "item": "Indicate the study’s design with a commonly used term in the title or the abstract.",
        "guidance": "Clearly state the study design (e.g., cohort, case-control, cross-sectional) in the title or abstract.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "No mention of study design in the title or abstract.",
            "Study design is referenced but not clearly or consistently.",
            "Study design is clearly and appropriately stated.",
            "Other…"
        ]
    },
    {
        "section": "Title and Abstract",
        "item": "Provide in the abstract an informative and balanced summary of what was done and what was found.",
        "guidance": "Summarize study purpose, methods, key results, and conclusions in the abstract.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "The abstract is missing key information about methods or results.",
            "The abstract provides some summary but is incomplete or unbalanced.",
            "The abstract gives a clear, informative, and balanced summary.",
            "Other…"
        ]
    },
    {
        "section": "Introduction",
        "item": "Explain the scientific background and rationale for the investigation being reported.",
        "guidance": "Describe why the study was done, with context and relevant literature.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Scientific background and rationale are missing.",
            "Some background is given but lacks context or sufficient detail.",
            "Rationale is well described and contextualized with relevant literature.",
            "Other…"
        ]
    },
    {
        "section": "Introduction",
        "item": "State specific objectives, including any prespecified hypotheses.",
        "guidance": "Clearly state what you set out to do, including hypotheses.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Objectives or hypotheses are not stated.",
            "Objectives are stated but are vague or hypotheses are missing.",
            "Objectives and hypotheses are clearly stated and specific.",
            "Other…"
        ]
    },
    {
        "section": "Methods",
        "item": "Present key elements of study design early in the paper.",
        "guidance": "Identify the type of study and its key design features.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Key elements of the study design are not presented.",
            "Some study design elements are given but not early or not all are present.",
            "Study design and its key features are introduced clearly at the start.",
            "Other…"
        ]
    },
    {
        "section": "Methods",
        "item": "Describe the setting, locations, and relevant dates, including periods of recruitment, exposure, follow-up, and data collection.",
        "guidance": "State where and when the study was done.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Setting, locations, or study dates are missing.",
            "Setting or dates are partially reported.",
            "All relevant settings, locations, and dates are well described.",
            "Other…"
        ]
    },
    {
        "section": "Methods",
        "item": "Give the eligibility criteria, and the sources and methods of selection of participants. Describe methods of follow-up. For matched studies, give matching criteria and number of exposed/unexposed.",
        "guidance": "Explain how participants were identified, included, excluded, and how they were followed up.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Eligibility criteria or selection methods are not described.",
            "Some eligibility or selection details are given but are incomplete.",
            "Eligibility criteria and participant selection are fully explained.",
            "Other…"
        ]
    },
    {
        "section": "Methods",
        "item": "For each variable of interest, give sources of data and details of methods of assessment (measurement).",
        "guidance": "Describe how each variable was measured or obtained.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Variables or their measurement are not described.",
            "Some variables or measurement methods are described.",
            "All variables and measurement methods are described in detail.",
            "Other…"
        ]
    },
    {
        "section": "Methods",
        "item": "Describe any efforts to address potential sources of bias.",
        "guidance": "Discuss what you did to minimize bias (e.g., blinding, statistical adjustments).",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "No mention of efforts to address bias.",
            "Some efforts to reduce bias are described but lack detail.",
            "Potential sources of bias and mitigation efforts are thoroughly discussed.",
            "Other…"
        ]
    },
    {
        "section": "Methods",
        "item": "Explain how the study size was arrived at.",
        "guidance": "Provide rationale for sample size, power calculations if possible.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "No explanation for how the sample size was determined.",
            "Sample size is mentioned, but rationale or calculations are lacking.",
            "Sample size rationale and calculations are clearly explained.",
            "Other…"
        ]
    },
    {
        "section": "Methods",
        "item": "Explain how quantitative variables were handled in the analyses. If applicable, describe which groupings were chosen and why.",
        "guidance": "Describe handling of quantitative data (e.g., categorized, continuous).",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Handling of quantitative variables is not described.",
            "Some information on quantitative variables is given but not complete.",
            "Quantitative variable handling and groupings are well described.",
            "Other…"
        ]
    },
    {
        "section": "Methods",
        "item": "Describe all statistical methods, including those used to control for confounding.",
        "guidance": "Outline your statistical approach, including confounder adjustment, missing data handling, etc.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Statistical methods are not described.",
            "Some statistical methods are given but confounders or missing data not addressed.",
            "All statistical methods, confounding, and missing data approaches are detailed.",
            "Other…"
        ]
    },
    {
        "section": "Results",
        "item": "Report numbers of individuals at each stage of study (e.g., eligible, included, follow-up, analyzed). Give reasons for non-participation at each stage. Consider use of a flow diagram.",
        "guidance": "Show a flow of participant numbers, with reasons for exclusions.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Numbers at each stage are not reported.",
            "Some numbers or reasons for non-participation are given, but incomplete.",
            "All numbers and reasons for non-participation are reported, with a flow diagram if applicable.",
            "Other…"
        ]
    },
    {
        "section": "Results",
        "item": "Give characteristics of study participants (e.g., demographic, clinical, social) and information on exposures and potential confounders. Indicate number of participants with missing data for each variable. Summarize follow-up time.",
        "guidance": "Provide descriptive stats for the sample, and report missing data.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Participant characteristics and missing data are not reported.",
            "Some characteristics or missing data are reported, but not all.",
            "All participant characteristics, confounders, and missing data are fully reported.",
            "Other…"
        ]
    },
    {
        "section": "Results",
        "item": "Report numbers of outcome events or summary measures over time.",
        "guidance": "Present main outcome data (events, summary measures).",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Outcome events or summary measures are not reported.",
            "Some outcome events are reported, but data is incomplete.",
            "Outcome events and summary measures are fully and clearly reported.",
            "Other…"
        ]
    },
    {
        "section": "Results",
        "item": "Give unadjusted estimates and, if applicable, confounder-adjusted estimates and their precision (e.g., 95% confidence interval). Report category boundaries when continuous variables were categorized. If relevant, consider translating estimates of relative risk into absolute risk.",
        "guidance": "Show both crude and adjusted results with precision (CIs), and define any group boundaries.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Estimates and precision are not reported.",
            "Estimates are given, but adjusted results or CIs are missing or incomplete.",
            "Both unadjusted and adjusted estimates, precision, and category boundaries are fully reported.",
            "Other…"
        ]
    },
    {
        "section": "Results",
        "item": "Report other analyses done (e.g., subgroup analyses and sensitivity analyses).",
        "guidance": "Describe any secondary, subgroup, or sensitivity analyses.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "No additional analyses are reported.",
            "Some secondary analyses are described, but not all relevant analyses.",
            "All secondary, subgroup, and sensitivity analyses are clearly reported.",
            "Other…"
        ]
    },
    {
        "section": "Discussion",
        "item": "Summarize key results with reference to study objectives.",
        "guidance": "Recap the main findings in light of the objectives.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Key results are not summarized.",
            "Results are summarized but not linked to study objectives.",
            "Key results are well summarized with clear reference to objectives.",
            "Other…"
        ]
    },
    {
        "section": "Discussion",
        "item": "Discuss limitations of the study, taking into account sources of potential bias or imprecision. Discuss both direction and magnitude of any potential bias.",
        "guidance": "Acknowledge weaknesses and possible biases; discuss direction and size.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Study limitations are not discussed.",
            "Some limitations are discussed, but bias or imprecision are not fully considered.",
            "Limitations, potential bias, and their direction and magnitude are thoroughly discussed.",
            "Other…"
        ]
    },
    {
        "section": "Discussion",
        "item": "Give a cautious overall interpretation of results considering objectives, limitations, multiplicity of analyses, results from similar studies, and other relevant evidence.",
        "guidance": "Discuss meaning and context, but avoid overstating conclusions.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Overall interpretation is missing or overstates conclusions.",
            "Interpretation is present but does not fully consider limitations or other evidence.",
            "Interpretation is cautious and well-contextualized with study limitations and existing literature.",
            "Other…"
        ]
    },
    {
        "section": "Discussion",
        "item": "Discuss the generalizability (external validity) of the study results.",
        "guidance": "Comment on how well results may apply elsewhere.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "No discussion of generalizability or external validity.",
            "Generalizability is mentioned but not fully discussed.",
            "Generalizability and external validity are clearly discussed.",
            "Other…"
        ]
    },
    {
        "section": "Other Information",
        "item": "Give the source of funding and the role of the funders for the present study and, if applicable, for the original study on which the present article is based.",
        "guidance": "State how the study was funded and any role of the sponsor.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "Funding information is not provided.",
            "Funding is stated, but the role of funders is not described.",
            "Funding sources and funders' roles are fully described.",
            "Other…"
        ]
    }
]

st.set_page_config(page_title="STROBE Self-Assessment (Redesigned)", layout="wide")
st.title("📝 STROBE Self-Assessment Tool for TriNetX Projects (Three-Column Design)")

st.markdown("""
**Instructions:**  
- Review each STROBE item and guidance.
- Select your score (1 = Not addressed, 2 = Partially, 3 = Fully).
- Optionally add feedback: Select a general comment (or type your own) in the expandable box.
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
            chosen_sample = st.selectbox(
                "General comment",
                item['sample_comments'],
                index=0,
                key=f"sample_comment_{idx}",
            )
            # Button to use the selected sample comment in the comment box
            if st.button(f"Use selected comment for item {idx+1}", key=f"use_sample_{idx}"):
                st.session_state.comments[idx] = "" if chosen_sample == "Other…" else chosen_sample
            with st.expander("Comments / Feedback", expanded=False):
                comment = st.text_area(
                    "",
                    value=st.session_state.comments[idx],
                    key=f"comment_{idx}"
                )
                st.session_state.comments[idx] = comment
        st.session_state.scores[idx] = score
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
