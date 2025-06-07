import streamlit as st
import pandas as pd

# ... (same STROBE_ITEMS as previous answer) ...

score_labels = {1: "1 = Not addressed", 2: "2 = Partially", 3: "3 = Fully addressed"}

if "scores" not in st.session_state:
    st.session_state.scores = [2] * len(STROBE_ITEMS)
if "comments" not in st.session_state:
    st.session_state.comments = [""] * len(STROBE_ITEMS)
if "last_sample_idx" not in st.session_state:
    st.session_state.last_sample_idx = [0] * len(STROBE_ITEMS)

st.set_page_config(page_title="STROBE Self-Assessment (Redesigned)", layout="wide")
st.title("📝 STROBE Self-Assessment Tool for TriNetX Projects (Three-Column Design)")

st.markdown("""
**Instructions:**  
- Review each STROBE item and guidance.
- Select your score (1 = Not addressed, 2 = Partially, 3 = Fully).
- Optionally add feedback: Select a general comment or type your own in the box.
- Download your completed checklist as CSV.
""")

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
            # Detect selection and update comment only when sample comment changes
            chosen_sample = st.selectbox(
                "General comment",
                item['sample_comments'],
                index=st.session_state.last_sample_idx[idx],
                key=f"sample_comment_{idx}",
            )
            # Only update comment if user picked a new sample (not just re-render)
            if chosen_sample != "Other…":
                if (chosen_sample != st.session_state.comments[idx]
                    and chosen_sample != item['sample_comments'][st.session_state.last_sample_idx[idx]]):
                    st.session_state.comments[idx] = chosen_sample
            st.session_state.last_sample_idx[idx] = item['sample_comments'].index(chosen_sample)
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
