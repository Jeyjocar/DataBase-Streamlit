import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Dashboard Ventas 2024", page_icon=":bar_chart:", layout="wide")


# LEER ARCHIVO EXCEL o base de datos

@st.cache_data
def get_data_from_excel():
    df= pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine= "openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000,

    )

    df["hour"] = pd.to_datetime(df["Time"], format= "%H:%M:%S").dt.hour
    return df

df= get_data_from_excel()

st.sidebar.header("Por favor Ingresa tu filtro")
city = st.sidebar.multiselect(
    "Selecciona una Ciudad",
    options= df["City"].unique(),
    default= df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Seleccione el tipo cliente: ",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()

)

gender = st.sidebar.multiselect(
    "Seleccione el tipo De Genero: ",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()

)

df_selection = df.query (
    "City == @city & Customer_type == @customer_type & Gender  == @gender"
)

#Validar si la tabla esta vacia
if df_selection.empty:
    st.warning("No hay datos para mostrar......! que mal")
    st.stop()

st.title(":bar_chart: Ventas Asiaticas 2024")
st.markdown("##")

total_sales = int(df_selection ["Total"].sum())
average_rating= round(df_selection["Rating"].mean(), 1)
start_rating= ":star:" * int(round(average_rating, 0))
average_sale_by_transaction= round(df_selection["Total"].mean(), 2)


left_column, middle_column, right_column= st.columns(3)

with left_column:
    st.subheader("Total Ventas 2024")
    st.subheader(f" USD $ {total_sales:,}")


with middle_column:
    st.subheader("Promedio Rangos ")
    st.subheader(f"{average_rating} {start_rating}")

with right_column:
    st.subheader("promedio ventas por transaccion 2024")
    st.subheader(f" USD $ {average_sale_by_transaction}")


st.markdown("------")

#Gráfico dispersión ventas Male Female
scatter_plot = px.scatter(df_selection, x='Rating', y='Total', color='Gender', title='Ventas Hombre vs Mujeres', template='plotly_white')
st.plotly_chart(scatter_plot, use_container_width=True)

#Estadísticas descriptivas de ventas
st.subheader("Descripción Ventas 2024")
st.write(df_selection["Total"].describe())

sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Ventas Por Producto: </b>",
    color_discrete_sequence=["#ade"]*len(sales_by_product_line),
    template= "plotly_white",

)

fig_product_sales.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis=(dict(showgrid= False))
)

# ventas por hora

sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales= px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title= "<b>Ventas Por hora</b>",
    color_discrete_sequence=["#33FF36"] * len(sales_by_hour),
    template= "plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis=(dict(tickmode= "linear")),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis=(dict(showgrid= False))

    
)

left_column,right_column= st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width= True)

#Gráfico distribución ventas por ciudad
st.subheader("Ventas por ciudad")
sales_by_city = df_selection.groupby(by=["City"])[["Total"]].sum()
fig_city_sales = px.pie(
    sales_by_city, 
    values='Total',  
    names = sales_by_city.index,
    title= "<b>Distribución de Ventas por Ciudad </b>" ,
    labels={'Total':'Ventas'},
    #color_continuous_scale=px.colors.sequential.Plasma,
    template = "plotly_white"
)

st.plotly_chart(fig_city_sales,use_container_width=True)

#Resumen ventas
resume_sales = df_selection.groupby(["Customer_type", "Gender"]).agg({"Total": ["sum","mean"]})
st.subheader("Resumen de Ventas por tipo de Cliente")
st.write(resume_sales)


hide_st_style = """
          <style>
          #MainMenu {visibility: hidden;}
          footer {visibility: hidden;}
          header {visibility: hidden;}
          </style>


        """

st.markdown(hide_st_style, unsafe_allow_html=True)

# añadir la columna hora al dataframe

