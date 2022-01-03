import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Kontorlna ploča prodaje",
                    page_icon=":bar_chart:",
                    layout="wide"
                    )

st.header('Interaktivna kontrolna ploča')

st.write("""
# :bar_chart:Ova aplikacija izdvaja rezultate iz Excel datoteke ovisno o uvjetu iz kontrolne ploče
                      APP by prof.Požega Josip, mag.inf.
***
""")


df = pd.read_excel(io="supermarket.xlsx",engine="openpyxl",sheet_name="Prodajni",skiprows=3,usecols="B:R",nrows=1000,)
# Dodajemo stupac "Sati" u DATAFRAME
df["Sati"] = pd.to_datetime(df["Vrijeme"], format="%H:%M:%S").dt.hour


st.dataframe(df)


st.sidebar.header("Molim filtrirajte po gradovima:")
city = st.sidebar.multiselect(
    "Odaberite grad:",
    options=df["City"].unique(),
    default=df["City"].unique(),
)


st.sidebar.header("Filtrirajte po Vrsti kupca:")
customer_type = st.sidebar.multiselect(
    "Odaberite vrstu kupca:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

st.sidebar.header("Filtrirajte po Spolu:")
gender = st.sidebar.multiselect(
"Odaberite spol kupca:",
options=df["Gender"].unique(),
default=df["Gender"].unique()
)

df_selection = df.query(
    "City == @city & Customer_type ==@customer_type & Gender == @gender"
)

st.dataframe(df_selection)

st.title("Informacije o prodaji proizvoda")
st.markdown("##")

total_sales = int(df_selection["Ukupno"].sum())
average_rating = round(df_selection["Ocjena"].mean(),1)
star_rating = ":star:" * int(round(average_rating,0))
average_sale_by_transaction = round(df_selection["Ukupno"].mean(),2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Ukupna prodaja:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Prosječna ocjena:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Prosječna prodaja po transakciji:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")


sales_by_product_line = (
    df_selection.groupby(by=["Linija proizvoda"]).sum()[["Ukupno"]].sort_values(by="Ukupno")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Ukupno",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Prodaja po jedinici proizvoda</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template = "plotly_white"

)

fig_product_sales.update_layout(
plot_bgcolor="rgba(0,0,0,0)",
xaxis=(dict(showgrid=False))
)

# PRODAJA PO SATIMA 
sales_by_hour = df_selection.groupby(by=["Vrijeme"]).sum()[["Ukupno"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Ukupno",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)
