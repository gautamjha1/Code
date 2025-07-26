
import streamlit as st
import pandas as pd

# ---------- AI Helper Function (Mock) ----------
def get_industry_research(deal_type):
    return f"""
### 🧠 Industry Research Summary: {deal_type}

- 📊 **Market Trends**: Consolidation activity is growing in the {deal_type.lower()} sector.
- ⚠️ **Risks**: Regulatory changes, competitive pressure, valuation volatility.
- 💡 **Opportunities**: Technological adoption, recurring revenue models, regional expansion.

*This is a simplified output. AI-powered insights can be integrated later.*
"""

# ---------- Streamlit App ----------
st.set_page_config(page_title="Deal-Genie.com", layout="wide")

st.title("💼 Deal-Genie.com")
st.subheader("Accessible M&A software for smaller buy-side deal teams")

st.markdown("""
- ✅ **72% higher likelihood of deal conversion**
- ✅ **Save ~6 hours/week via better time management**
- ✅ **AI to build institutional knowledge & avoid bad acquisitions**
""")

st.markdown("---")

# ---- Upload Section ----
st.header("📁 Upload Your Deal Pipeline")
uploaded_file = st.file_uploader("Upload a CSV of your deals", type=["csv"])

if uploaded_file:
    deals_df = pd.read_csv(uploaded_file)
    st.success("✅ Deals uploaded successfully!")
    st.dataframe(deals_df.head())

    if 'edited_df' not in st.session_state:
        st.session_state.edited_df = deals_df.copy()

    # ---- Individual Deal View + Editable Form ----
    st.markdown("---")
    st.header("🗂️ Individual Deal Dashboard")
    selected = st.selectbox("Choose a deal", deals_df["Project Name"])
    editable_df = st.session_state.edited_df
    deal_idx = editable_df[editable_df["Project Name"] == selected].index[0]
    deal = editable_df.loc[deal_idx]

    st.markdown("### ✏️ Edit Deal Details")
    with st.form("edit_form"):
        project_name = st.text_input("Project Name", value=deal["Project Name"])
        size = st.text_input("Deal Size", value=deal["Size"])
        seller = st.text_input("Seller", value=deal["Seller"])
        source = st.text_input("Source", value=deal["Source"])
        stage = st.selectbox("Stage", options=["Early Contact", "Lead", "Review", "LOI", "Diligence", "Term Sheet"], index=["Early Contact", "Lead", "Review", "LOI", "Diligence", "Term Sheet"].index(deal["Stage"]))
        deal_type = st.selectbox("Type", options=list(deals_df["Type"].unique()), index=list(deals_df["Type"].unique()).index(deal["Type"]))
        deadline = st.date_input("Deadline", pd.to_datetime(deal["Deadline"]))
        lead = st.text_input("Deal Lead", value=deal["Deal Lead"])
        follow_up = st.text_input("Follow-up", value=deal["Follow-up"])
        comments = st.text_area("Comments", value=deal.get("Comments", ""))

        submitted = st.form_submit_button("💾 Save Changes")

        if submitted:
            editable_df.at[deal_idx, "Project Name"] = project_name
            editable_df.at[deal_idx, "Size"] = size
            editable_df.at[deal_idx, "Seller"] = seller
            editable_df.at[deal_idx, "Source"] = source
            editable_df.at[deal_idx, "Stage"] = stage
            editable_df.at[deal_idx, "Type"] = deal_type
            editable_df.at[deal_idx, "Deadline"] = deadline.strftime('%Y-%m-%d')
            editable_df.at[deal_idx, "Deal Lead"] = lead
            editable_df.at[deal_idx, "Follow-up"] = follow_up
            editable_df.at[deal_idx, "Comments"] = comments
            st.success("Changes saved successfully!")

    st.markdown("---")

    # ---- Kanban-like Overview ----
    st.header("📌 Consolidated Deal View by Stage")
    stages = editable_df["Stage"].unique()
    cols = st.columns(len(stages))

    for idx, stage in enumerate(stages):
        stage_deals = editable_df[editable_df["Stage"] == stage]["Project Name"].tolist()
        with cols[idx]:
            st.subheader(stage)
            for deal in stage_deals:
                st.markdown(f"- {deal}")

    st.markdown("---")

    # ---- Document Categories (Mocked) ----
    st.header("📄 Document Categories")
    doc_cols = st.columns(4)
    with doc_cols[0]: st.markdown("- Seller Docs")
    with doc_cols[1]: st.markdown("- Internal Notes")
    with doc_cols[2]: st.markdown("- Generated TEAs")
    with doc_cols[3]: st.markdown("- Data Room Links")

    st.markdown("### 📥 Download Updated Pipeline")
    st.download_button("Download CSV", data=editable_df.to_csv(index=False), file_name="updated_pipeline.csv")

else:
    st.info("👈 Upload your deal pipeline to get started or try a demo file.")

# ---- Optional: Sample CSV Download ----
sample = pd.DataFrame({
    "Project Name": ["Project Q", "AlphaTech", "GreenFields"],
    "Size": ["$5M", "$12M", "$8M"],
    "Seller": ["John Smith", "CEO Email", "Broker"],
    "Source": ["Inbound", "Cold Outreach", "Warm Intro"],
    "Stage": ["Lead", "Review", "LOI"],
    "Type": ["SaaS", "AgriTech", "Healthcare"],
    "Deadline": ["2025-09-01", "2025-08-15", "2025-10-10"],
    "Deal Lead": ["Alex", "Jamie", "Taylor"],
    "Follow-up": ["Next week", "Pending NDA", "Setup meeting"]
})
st.download_button("📥 Download Sample CSV", data=sample.to_csv(index=False), file_name="sample_pipeline.csv")
