"""Optional Streamlit dashboard for the synthetic CRM/lifecycle demo."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"

st.set_page_config(page_title="Grocery Lifecycle CRM Demo", page_icon="🛒", layout="wide")
st.title("AI-Powered Grocery CRM & Lifecycle Automation")
st.caption("Portfolio demo • synthetic customer data • simulated historical campaign outcomes • no messages sent")
st.warning("All campaign performance metrics are simulated for demonstration. They are not FirstClub results or a claim of real campaign lift.")

kpi_path = OUTPUTS / "kpi_report.json"
queue_path = OUTPUTS / "campaign_queue.csv"
summary_path = OUTPUTS / "segment_summary.csv"

if not kpi_path.exists() or not queue_path.exists():
    st.info("Run `py -3 scripts/generate_synthetic_data.py` and `py -3 scripts/run_demo.py --as-of-date 2026-10-27` from the project folder, then refresh this page.")
    st.stop()

report = json.loads(kpi_path.read_text(encoding="utf-8"))
queue = pd.read_csv(queue_path) if queue_path.stat().st_size else pd.DataFrame()
segment_summary = pd.read_csv(summary_path) if summary_path.exists() and summary_path.stat().st_size else pd.DataFrame()
overall = report["overall"]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Eligible drafts", f"{len(queue):,}")
c2.metric("Simulated delivery", f"{overall['delivered']:,}")
c3.metric("Simulated conversion rate", f"{overall['conversion_rate']:.1%}")
c4.metric("Simulated attributed revenue", f"₹{overall['attributed_revenue_inr']:,.0f}")

left, right = st.columns(2)
with left:
    st.subheader("Drafts by lifecycle segment")
    if not segment_summary.empty:
        chart_df = segment_summary.groupby("segment", as_index=True)["queued_customers"].sum().sort_values(ascending=False)
        st.bar_chart(chart_df)
    else:
        st.write("No eligible drafts for the selected evaluation date.")
with right:
    st.subheader("Simulated performance by segment")
    segment_kpis = report.get("by_segment", {})
    if segment_kpis:
        chart_df = pd.DataFrame([
            {"Segment": segment, "Conversion rate": values["conversion_rate"]}
            for segment, values in segment_kpis.items()
        ]).set_index("Segment").sort_values("Conversion rate", ascending=False)
        st.bar_chart(chart_df)
    else:
        st.write("No campaign history available.")

st.subheader("Campaign queue preview")
if not queue.empty:
    display_cols = [col for col in ["customer_id", "segment", "campaign_type", "recommended_offer", "subject", "status", "send_approved"] if col in queue.columns]
    st.dataframe(queue[display_cols].head(50), use_container_width=True, hide_index=True)
    st.download_button("Download campaign drafts CSV", queue.to_csv(index=False).encode("utf-8-sig"), file_name="campaign_queue.csv", mime="text/csv")
else:
    st.write("No campaign drafts have been queued.")

with st.expander("Metric definitions and assumptions"):
    st.json(report["metric_definitions"])
    st.write(f"Assumed gross margin: {overall['assumed_gross_margin']:.0%}. ROI is estimated gross profit minus campaign cost, divided by campaign cost. Attribution does not prove incrementality; a randomized holdout is required to estimate lift.")
