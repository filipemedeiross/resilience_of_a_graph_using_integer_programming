import streamlit as st
import networkx as nx
from graphy.utils import plot_military_network


# Initial page settings
st.set_page_config(page_title="Military Distribution Network", layout="centered")

# Auxiliary functions
def disabled_attempts():
    st.session_state.disabled = True

def sum_endurance(network, nodes):
    return sum(network.nodes[node]["endurance"] for node in nodes)

# Getting variables that will be used
generator = st.session_state.generator
military_network = st.session_state.military_network
military_solver = st.session_state.military_solver

# Sidebar features
colside1, colside2, colside3 = st.sidebar.columns((4.5, 3, 2.5))

colside1.markdown("### ⚙️ Options")

if colside2.button("Update"):
    st.session_state.disabled = False

    military_network = st.session_state.military_network = generator.military_network()
if colside3.button("Solve"):
    st.session_state.disabled = True

    military_solver.create_model(military_network, st.session_state.fire_power)
    military_solver.optimize()
    
    military_network.remove_nodes_from(military_solver.nodes_to_remove)  # removing nodes obtained by the model 

    st.sidebar.info(f"Solver stopped provisioning {military_solver.objective_value} military units from headquarters", icon="ℹ️")   
    
# User entries and plotting the graph
with st.sidebar:
    form = st.form("user_entries", clear_on_submit=True)

    form.multiselect("Choose the nodes", military_network.nodes, key="nodes", disabled=st.session_state.disabled,
                     format_func=lambda x: f"MU_{x} ({military_network.nodes[x]['endurance']})",
                     help="Military units chosen to be removed from the military distribution network")

    # Checking if the button was pressed
    if form.form_submit_button("Try", on_click=disabled_attempts):
        # Checking if the firepower limit was violated
        if sum_endurance(military_network, st.session_state.nodes) <= st.session_state.fire_power:
            # Saving information about the optimal solution
            military_solver.create_model(military_network, st.session_state.fire_power)
            military_solver.optimize()

            # Perform user attempt
            military_network.remove_nodes_from(st.session_state.nodes)

            # Checking:
            # if the user has completed the objective
            # difference between user solution and integer programming model solution
            win = False
            solution = 0
            for c in map(military_network.subgraph, nx.connected_components(military_network)):
                if "headquarters" not in nx.get_node_attributes(c, "node_prop").values():
                    win = True
                    solution += c.number_of_nodes()

            solution += len(st.session_state.nodes)

            if win:
                st.success(f"You have successfully stopped provisioning {solution} military units from headquarters", icon="✅")
                st.balloons()  # congratulating user who managed to accomplish the goal

                solution_gap = military_solver.objective_value - solution
                
                if solution_gap:
                    st.warning(f"Your solution was worse than the optimum by {solution_gap} units", icon="⚠️")
            else:
                st.error("You failed to stop provisioning any military units", icon="🚨")
        else:
            st.error(f"You have exceeded your firepower limit ({st.session_state.fire_power})", icon="🚨")

# General explanation of the project
st.markdown("""
<h1 style='text-align: center'>Disconnecting a military resource distribution network</h1>
""", unsafe_allow_html=True)

st.markdown("""---""")

st.write("""
    The objective in this context is the destruction of military units (removal of vertices) to interrupt the supply of military resources to the largest number of military units from the **headquarters**, respecting the limit of firepower.
    
    Firepower is limited to 6 units of endurance and each military unit has endurance of 1, 2 or 3 units, with the exception of the headquarters and adjacent units which have 10000 and 100 respectively.
    The vertex of the headquarters is distinguishable in the graph due to its size, to differentiate it one can also observe the respective resistances.

    The sidebar has the mechanisms for interacting with the graph and in it you can try a solution by choosing vertices to be removed.
    Then you will have as feedback the information if objective has been achieved (a viable solution) and if it succeeds, your solution will be compared with the optimal one obtained through the integer programming.
""")

st.pyplot(plot_military_network(military_network))

with st.expander("More information"):
    st.write(r"""
        As the problem is represented as a graph $G=(V, E)$ and has headquarters node $k$, $c_{i}$ **endurance** for each of the military units and firepower limited to $L$,
        let's consider the variables $x_{i}$ $\forall i \in V$ which represents whether the node $i$ is disconnected with respect to the headquarters node and $y_{i}$ $\forall i \in V$ which represents whether the node $i$ has been removed.
        
        Therefore, we have the following integer programming model:

        $$
        Max \sum\limits_{i \in V}x_{i}
        $$

        Subject to:

        $$
        x_{k} = 0
        $$

        $$
        y_{i} + y_{j} \geq x_{i} + x_{j}, \space\space\space \forall (i, j) \in E
        $$

        $$
        y_{i} + y_{j} \geq x_{j} + x_{i}, \space\space\space \forall (i, j) \in E
        $$

        $$
        \sum\limits_{i \in V}c_{i}*x_{i} \leq L, \space\space\space \forall i \in V
        $$

        $$
        x_{i} \in \{0, 1\}, \space\space\space \forall i \in V
        $$

        $$
        y_{i} \in \{0, 1\}, \space\space\space \forall i \in V
        $$
    """)
