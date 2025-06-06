# app.py

import streamlit as st
import pandas as pd

@st.cache_data
def load_cosmos_data():
    """
    Load Company1 (Cosmos - M-series) data from CSV.
    """
    m_df = pd.read_csv('Cosmos-data.csv')
    m_df = m_df.set_index('SPECIFICATION')
    return m_df

@st.cache_data
def load_ace_data():
    """
    Load Company2 (Ace - DC-series) data from CSV.
    """
    dc_df = pd.read_csv('Ace-data.csv')
    dc_df = dc_df.set_index('Specification')
    return dc_df

def main():
    # Set page layout
    st.set_page_config(page_title='Machine Comparison', layout='wide')

    # Load both datasets
    company1_df = load_cosmos_data()
    company2_df = load_ace_data()

    # Extract machine lists (exclude the “UNIT”/“Units” column)
    cosmos_machines = [col for col in company1_df.columns if col != "UNIT"]
    ace_machines   = [col for col in company2_df.columns if col != "Units"]

    # Define company‐to‐data mapping
    companies = {
        "Cosmos (M-series)": {
            "df": company1_df,
            "machines": cosmos_machines,
            "color": "#008080"
        },
        "Ace (DC-series)": {
            "df": company2_df,
            "machines": ace_machines,
            "color": "#ff000d"
        }
    }

    # Sidebar: choose comparison type
    st.sidebar.title("Comparison Options")
    comparison_type = st.sidebar.radio(
        "Compare:",
        ("Within Same Company", "Across Companies")
    )

    st.sidebar.markdown("---")

    # If comparing within a single company:
    if comparison_type == "Within Same Company":
        st.sidebar.markdown("### Select Company")
        company = st.sidebar.selectbox("Company", list(companies.keys()), key="company_only")
        color = companies[company]["color"]
        st.sidebar.markdown(
            f"<span style='color:{color}; font-weight:bold;'>Selected: {company}</span>",
            unsafe_allow_html=True,
        )

        machines = companies[company]["machines"]
        st.sidebar.markdown("#### Machine A")
        machine_a = st.sidebar.selectbox("Machine A", machines, key="machine_a_within")
        st.sidebar.markdown("#### Machine B")
        machine_b = st.sidebar.selectbox("Machine B", machines, key="machine_b_within")

        # Main Title & Instruction
        st.title("Machine Comparison Tool")
        st.markdown(
            f"Comparing two machines **within** the same company: **{company}**."
        )

        if machine_a and machine_b:
            if machine_a == machine_b:
                st.warning("Please select two different machines to compare.")
            else:
                df = companies[company]["df"]
                specs_a = df[machine_a].rename(machine_a)
                specs_b = df[machine_b].rename(machine_b)
                comparison_df = pd.concat([specs_a, specs_b], axis=1)
                st.subheader(f"{machine_a}  vs.  {machine_b}")
                st.dataframe(comparison_df.fillna("-"))

                csv = comparison_df.to_csv().encode("utf-8")
                st.download_button(
                    label="Download comparison as CSV",
                    data=csv,
                    file_name=f"{company}_{machine_a}_vs_{machine_b}.csv",
                    mime="text/csv",
                )

    # If comparing machines across two different companies:
    else:
        # Machine A selection
        st.sidebar.markdown("### Machine A")
        company_a = st.sidebar.selectbox("Company A", list(companies.keys()), key="company_a")
        color_a = companies[company_a]["color"]
        st.sidebar.markdown(
            f"<span style='color:{color_a}; font-weight:bold;'>Selected: {company_a}</span>",
            unsafe_allow_html=True
        )
        machine_a = st.sidebar.selectbox("Machine A", companies[company_a]["machines"], key="machine_a_across")

        st.sidebar.markdown("---")

        # Machine B selection
        st.sidebar.markdown("### Machine B")
        company_b = st.sidebar.selectbox("Company B", list(companies.keys()), index=1, key="company_b")
        color_b = companies[company_b]["color"]
        st.sidebar.markdown(
            f"<span style='color:{color_b}; font-weight:bold;'>Selected: {company_b}</span>",
            unsafe_allow_html=True
        )
        machine_b = st.sidebar.selectbox("Machine B", companies[company_b]["machines"], key="machine_b_across")

        # Main Title & Instruction
        st.title("Machine Comparison Tool")
        st.markdown(
            "Comparing one machine from **Cosmos** against one machine from **Ace**."
        )

        if machine_a and machine_b:
            df_a = companies[company_a]["df"]
            df_b = companies[company_b]["df"]

            specs_a = df_a[machine_a].rename(f"{company_a} – {machine_a}")
            specs_b = df_b[machine_b].rename(f"{company_b} – {machine_b}")

            comparison_df = pd.concat([specs_a, specs_b], axis=1)
            st.subheader(f"{company_a} – {machine_a}  vs.  {company_b} – {machine_b}")
            st.dataframe(comparison_df.fillna("-"))

            csv = comparison_df.to_csv().encode("utf-8")
            st.download_button(
                label="Download comparison as CSV",
                data=csv,
                file_name=f"{company_a}_{machine_a}_vs_{company_b}_{machine_b}.csv",
                mime="text/csv",
            )

if __name__ == "__main__":
    main()
