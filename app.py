from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="E-Commerce Customer Insights", page_icon="🛍️", layout="wide")
DATA_FILE = Path(__file__).parent / "ecommerce_customers.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

st.title("🛍️ E-Commerce Customer Behavior Dashboard")
st.write("Explore customer engagement, membership length, and yearly spending patterns.")

if not DATA_FILE.exists():
    st.error("Dataset not found. Keep ecommerce_customers.csv in the same folder as app.py.")
    st.stop()

df = load_data(DATA_FILE)
numeric_cols = ["Avg. Session Length", "Time on App", "Time on Website",
                "Length of Membership", "Yearly Amount Spent"]
if not set(numeric_cols).issubset(df.columns):
    st.error("The dataset does not contain all expected numeric columns.")
    st.stop()

st.sidebar.header("Customer filters")
m_min, m_max = float(df["Length of Membership"].min()), float(df["Length of Membership"].max())
s_min, s_max = float(df["Yearly Amount Spent"].min()), float(df["Yearly Amount Spent"].max())
membership = st.sidebar.slider("Membership length (years)", m_min, m_max, (m_min, m_max))
spending = st.sidebar.slider("Yearly amount spent", s_min, s_max, (s_min, s_max))
filtered = df[df["Length of Membership"].between(*membership) &
              df["Yearly Amount Spent"].between(*spending)].copy()

st.caption(f"Showing {len(filtered):,} of {len(df):,} customers.")
if filtered.empty:
    st.warning("No customers match these filters. Adjust the sliders.")
    st.stop()

a, b, c, d = st.columns(4)
a.metric("Customers", f"{len(filtered):,}")
b.metric("Average yearly spend", f"${filtered['Yearly Amount Spent'].mean():,.2f}")
c.metric("Average membership", f"{filtered['Length of Membership'].mean():.2f} years")
d.metric("Highest yearly spend", f"${filtered['Yearly Amount Spent'].max():,.2f}")

left, right = st.columns(2)
with left:
    fig = px.histogram(filtered, x="Yearly Amount Spent", nbins=30,
                       title="Distribution of Yearly Spending")
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.histogram(filtered, x="Length of Membership", nbins=30,
                       title="Distribution of Membership Length")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    fig = px.scatter(filtered, x="Time on App", y="Yearly Amount Spent",
                     trendline="ols", title="App Time vs Yearly Spending")
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.scatter(filtered, x="Time on Website", y="Yearly Amount Spent",
                     trendline="ols", title="Website Time vs Yearly Spending")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    fig = px.scatter(filtered, x="Length of Membership", y="Yearly Amount Spent",
                     trendline="ols", title="Membership Length vs Yearly Spending")
    st.plotly_chart(fig, use_container_width=True)
with right:
    fig = px.imshow(filtered[numeric_cols].corr(), text_auto=".2f", zmin=-1, zmax=1,
                    color_continuous_scale="RdBu_r", title="Correlation Heatmap")
    st.plotly_chart(fig, use_container_width=True)

app_r = filtered["Time on App"].corr(filtered["Yearly Amount Spent"])
web_r = filtered["Time on Website"].corr(filtered["Yearly Amount Spent"])
st.subheader("App vs Website engagement")
comparison = pd.DataFrame({"Channel": ["App", "Website"],
                            "Correlation with yearly spending": [app_r, web_r]})
fig = px.bar(comparison, x="Channel", y="Correlation with yearly spending",
             title="Channel engagement correlation with spending", text_auto=".3f")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Main findings")
member_r = filtered["Length of Membership"].corr(filtered["Yearly Amount Spent"])
strongest_name, strongest_val = max(
    [("App time", abs(app_r)), ("Website time", abs(web_r)),
     ("Membership length", abs(member_r))], key=lambda item: item[1])
st.write(f"- App-time correlation with yearly spending: **{app_r:.3f}**.")
st.write(f"- Website-time correlation with yearly spending: **{web_r:.3f}**.")
st.write(f"- Strongest of these relationships: **{strongest_name}** (absolute r = **{strongest_val:.3f}**).")
st.write("- Correlation indicates association, not causation.")
if st.checkbox("Show raw customer data"):
    st.dataframe(filtered, use_container_width=True)
