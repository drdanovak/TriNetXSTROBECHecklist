import streamlit as st
import pandas as pd
import pdfkit
import tempfile
import os

# ---- Paste the STROBE_ITEMS list here from above ----

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
