import streamlit as st
import pandas as pd
from collections import defaultdict

# 22 STROBE checklist items grouped by section, with tag options for feedback
STROBE_ITEMS = [
    # ... (same checklist items as before; omitted here for brevity) ...
    # Copy your full STROBE_ITEMS list here from the previous code block
]

score_labels = {1: "1 = Not addressed", 2: "2 = Partially", 3: "3 = Fully addressed"}

if "scores" not in st.session_state:
    st.session_state.scores = [2] * len(STROBE_ITEMS)
if "comments" not in st.session_state:
    st.session_state.comments = [""] * len(STROBE_ITEMS)
if "selected_tags" not in st.session_state:
    st.session_state.selected_tags = [[] for _ in STROBE_ITEMS]
if "manual_comment_edit" not in st.session_state:
    st.session_state.manual_comment_edit = [False] * len(STROBE_ITEMS)

st.set_page_config(page_title="STROBE Self-Assessment (Tag/Comment System)", layout="wide")
st.title("📝 STROBE Self-Assessment Tool for TriNetX Projects (Multi-Tag + Comments)")

st.markdown("""
**Instructions:**  
- Expand each section below and work through each checklist item.
- Select your score (1 = Not addressed, 2 = Partially, 3 = Fully).
- For feedback, check one or more relevant tags, or type your own comments below the tags.
- Download your completed checklist as CSV.
""")

# Group items by section
section_items = defaultdict(list)
for i, item in enumerate(STROBE_ITEMS):
    section_items[item["section"]].append((i, item))

with st.form("strobe_form"):
    st.markdown("### Self-Assessment Checklist")
    for section, items in section_items.items():
        with st.expander(section, expanded=False):  # Now collapsed by default!
            for idx, item in items:
                c1, c2, c3 = st.columns([3, 1, 2])
                with c1:
                    st.markdown(
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
                    st.markdown("**Select feedback tags:**")
                    tags = []
                    for tag_idx, tag in enumerate(item["tag_options"]):
                        checked = tag in st.session_state.selected_tags[idx]
                        new_checked = st.checkbox(tag, value=checked, key=f"tag_{idx}_{tag_idx}")
                        if new_checked:
                            tags.append(tag)
                    if not st.session_state.manual_comment_edit[idx]:
                        comment_val = "; ".join(tags)
                        st.session_state.comments[idx] = comment_val
                    st.session_state.selected_tags[idx] = tags
                    comment_input = st.text_area(
                        "Comments / Feedback",
                        value=st.session_state.comments[idx],
                        key=f"comment_{idx}"
                    )
                    if comment_input != "; ".join(st.session_state.selected_tags[idx]):
                        st.session_state.manual_comment_edit[idx] = True
                    else:
                        st.session_state.manual_comment_edit[idx] = False
                    st.session_state.comments[idx] = comment_input
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
