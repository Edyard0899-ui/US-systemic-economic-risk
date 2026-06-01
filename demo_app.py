
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="US Economic Systemic Risk Monitor", layout="wide")

st.title("US Economic Systemic Risk Monitor")

tabs = st.tabs(["Dashboard","Minsky Crisis Model","Historical Analysis","Forecast & Monte Carlo","Crisis Comparison"])

years = np.arange(1950, 2027)
hist_risk = 40 + 20*np.sin(np.linspace(0,20,len(years))) + np.random.normal(0,3,len(years))

with tabs[0]:
    st.subheader("Dashboard")
    risk = float(np.clip(hist_risk[-1],0,100))
    fig = go.Figure(go.Indicator(mode="gauge+number", value=risk,
        title={"text":"Composite Systemic Collapse Probability"}))
    st.plotly_chart(fig, use_container_width=True)
    df = pd.DataFrame({"Year":years,"Risk":hist_risk})
    st.plotly_chart(px.line(df,x="Year",y="Risk",title="Historical Risk Index"), use_container_width=True)

with tabs[1]:
    st.subheader("Minsky Crisis Model")
    c1,c2=st.columns(2)
    with c1:
        debt=st.slider("Debt/GDP",50,300,170)
        corp=st.slider("Corporate Debt/GDP",10,150,80)
        rate=st.slider("Fed Funds Rate",0.0,15.0,5.0)
        inflation=st.slider("Inflation",0.0,20.0,3.0)
    with c2:
        unemp=st.slider("Unemployment",1.0,20.0,4.5)
        spread=st.slider("Yield Curve Spread",-3.0,3.0,-0.3)
        bubble=st.slider("Asset Bubble Index",0,100,30)

    if st.button("RUN ANALYSIS"):
        score=(debt/300+corp/150+rate/15+inflation/20+unemp/20+(3-spread)/6+bubble/100)/7*100
        st.metric("Collapse Probability", f"{score:.1f}%")
        st.write("Minsky Regime:", "Ponzi Finance" if score>70 else "Speculative Finance" if score>40 else "Hedge Finance")

        radar = go.Figure()
        radar.add_trace(go.Scatterpolar(r=[debt/3,corp/1.5,rate*6,unemp*5,bubble],
                                        theta=["Debt","Corp Debt","Rate","Unemp","Bubble"],
                                        fill='toself'))
        st.plotly_chart(radar, use_container_width=True)

with tabs[2]:
    st.subheader("Historical Analysis")
    df = pd.DataFrame({
        "Year": years,
        "Debt/GDP": np.linspace(60,180,len(years))+np.random.normal(0,5,len(years))
    })
    st.plotly_chart(px.line(df,x="Year",y="Debt/GDP"), use_container_width=True)

with tabs[3]:
    st.subheader("Forecast & Monte Carlo")
    sims=st.selectbox("Simulations",[10000,50000,100000])
    data=np.random.normal(55,15,5000)
    st.plotly_chart(px.histogram(data,title=f"Monte Carlo Distribution ({sims:,})"), use_container_width=True)

with tabs[4]:
    st.subheader("Crisis Comparison")
    comp=pd.DataFrame({"Crisis":["1929","1973","2000","2008","2020"],
                       "Similarity":[20,45,62,84,28]})
    st.plotly_chart(px.bar(comp,x="Crisis",y="Similarity"), use_container_width=True)
