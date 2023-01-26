import streamlit as st
from graphy import GraphGenerator, SolverWaterDistribution, SolverMilitaryDistribution


# Initial page settings
st.set_page_config(page_title="Main Page", layout="centered", initial_sidebar_state="expanded")

# Instantiating relevant variables throughout the app
st.session_state.generator = GraphGenerator()
st.session_state.water_solver = SolverWaterDistribution()
st.session_state.military_solver = SolverMilitaryDistribution()

st.session_state.water_network = st.session_state.generator.water_network()
st.session_state.military_network = st.session_state.generator.military_network()
st.session_state.disabled = False

# Buy me a coffee button
button = """
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="filipemedeiross" data-color="#FF5F5F" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#ffffff" data-coffee-color="#FFDD00" ></script>
"""

st.components.v1.html(button, height=70, width=220)

st.markdown("""
<style>
    iframe[width="220"] {
        position: fixed;
        bottom: 60px;
        right: 40px;
    }
</style>
""", unsafe_allow_html=True)

# General explanation of the project
st.markdown("""
<h1 style='text-align: center'>Network Resilience Analysis</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h2 style='text-align: center'>Application of integer programming in analyzing the resilience of a network</h2>
""", unsafe_allow_html=True)

st.markdown("""---""")

st.write("""
    The objective of this project is to demonstrate, without much scientific rigor, the importance of connectivity analysis in investigating the resilience and robustness of a network represented as a graph.

    For this purpose, the integer programming was used to optimize specific objectives while disconnecting connected graphs created by an automatic graph generator implemented to simulate two different practical contexts:
    - A water distribution network with specified origin and destination
    - A military resource distribution network with headquarters specification and different destruction difficulties (:red[endurance]) of the military units (vertices)
""")

tab1, tab2 = st.tabs(["Water network", "Military network"])

tab1.image("media/example_water_network.png")
tab1.write("""
    In the context of the water distribution network, the integer programming model aims to obtain the minimum number of edges to be removed to interrupt the supply from the origin node to the destination.
    Therefore, we are analyzing the connectivity in relation to the edges because, in this case, the fragility of the graph is concentrated in the pipes.
""")

tab2.image("media/example_military_network.png")
tab2.write("""
    In the context of the distribution network of military resources, the objective is to disconnect the largest number of military units from the headquarters, thus interrupting their supply.
    
    Therefore, the analysis is carried out from the perspective of vertex connectivity, considering that the edges only represent the relationships between military units that are not amenable to treatment for the problem because they are not physical links between the vertices.
""")
