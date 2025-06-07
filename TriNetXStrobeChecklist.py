import streamlit as st
import pandas as pd

# Full STROBE Checklist and general sample comments
STROBE_ITEMS = [
    {
        "section": "Title and Abstract",
        "item": "Indicate the study’s design with a commonly used term in the title or the abstract.",
        "guidance": "Clearly state the study design (e.g., cohort, case-control, cross-sectional) in the title or abstract.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "The study design is not clearly stated in the title or abstract.",
            "The design is mentioned but could be clearer or more consistent.",
            "The study design is clearly and accurately indicated.",
            "Other…"
        ]
    },
    {
        "section": "Title and Abstract",
        "item": "Provide in the abstract an informative and balanced summary of what was done and what was found.",
        "guidance": "Summarize study purpose, methods, key results, and conclusions in the abstract.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "The abstract lacks a summary of the key results or methods.",
            "The abstract summarizes some but not all necessary elements.",
            "The abstract is informative and balanced.",
            "Other…"
        ]
    },
    {
        "section": "Introduction",
        "item": "Explain the scientific background and rationale for the investigation being reported.",
        "guidance": "Describe why the study was done, with context and relevant literature.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "The scientific background or rationale is not adequately explained.",
            "Background is present but lacks detail or context.",
            "The rationale is clearly and thoroughly described.",
            "Other…"
        ]
    },
    # ... Repeat for all 22 items, changing sample_comments as appropriate ...
    {
        "section": "Other Information",
        "item": "Give the source of funding and the role of the funders for the present study and, if applicable, for the original study on which the present article is based.",
        "guidance": "State how the study was funded and any role of the sponsor.",
        "link": "https://www.strobe-statement.org/checklists/",
        "sample_comments": [
            "No information about funding is provided.",
            "Funding is mentioned, but the funders' roles are unclear.",
            "Funding sources and the role of funders are fully described.",
            "Other…"
        ]
    },
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
            # Add a selectbox for sample comments
            chosen_sample = st.selectbox(
                "General comment",
                item['sample_comments'],
                index=0,
                key=f"sample_comment_{idx}",
            )
            # Button to use the selected sample comment in the comment box
            if st.button(f"Use selected comment for item {idx+1}", key=f"use_sample_{idx}"):
                st.session_state.comments[idx] = "" if chosen_sample == "Other…" else chosen_sample
            # Text area for comment (editable)
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
