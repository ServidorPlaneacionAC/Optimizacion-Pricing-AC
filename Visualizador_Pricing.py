import streamlit as st
from Optimizador import optimizar, generar_dataframe_calculo_Kg
from streamlit_echarts import st_echarts
import mplcursors
from plotly.subplots import make_subplots
import plotly.graph_objs as go

class CLS_Visualizacion_pricing:
    '''
    clase que permite tener todas las particularidades necesarias
      para la visualización del modelo de pricing
    '''
    def __init__(self) -> None:
      self.generar_formulario()

    def generar_formulario(self):
        materiales=[]
        linea ={}
        Costo_variable_KG ={}
        Costo_fijo_total ={}
        Capacidad_produccion ={}
        produccion_inicial ={}
        precio_inicial ={}
        elasticidad_pesos ={}
        elasticidad_kg ={}
        capacidad_maxima ={}

        with st.form("add_ticket_form"):
            # issue = st.text_area("Describe the issue")
            frm_linea = st.selectbox("Linea a evaluar", ["Otro", "Chorizos", "Salchichas","Salchichones",
                                                        "Jamones", "Larga Vida", "Carnes Frescas", "Mortadelas"])
            frm_material = st.text_input("Material a evaluar")
            frm_Costo_variable_KG = st.number_input("Costo Variable por KG", min_value=0, value=10341)
            frm_Costo_fijo_total = st.number_input("Costo Fijo de la linea", min_value=0, value=4981461166)
            frm_Capacidad_produccion = st.number_input("Capacidad de Producción en KG al mes", min_value=0, value=770879)
            frm_produccion_inicial = st.number_input("Producción Actual en KG al mes", min_value=0, value=691245)
            frm_precio_inicial = st.number_input("Precio Actual de Venta", min_value=0, value=35096)
            frm_elasticidad_pesos = st.slider("Elasticidad del precio, al aumentar los pesos indicados generará una reducción de consumo equivalente a KG al mes", 0, 100, value=1)
            frm_elasticidad_kg = st.slider("Elasticidad en KG, al aumentar los pesos indicados anteriormente cuantos reduce en KG el coonsumo al mes", 0, 1000, value=400)
            frm_capacidad_maxima = st.slider("Cuanto de la capacidad máxima de la linea se usará %", 0, 100, value=100)/100
            frm_submitted = st.form_submit_button("Evaluar")

        if frm_submitted:
            # Agregar los valores del formulario a los diccionarios
            materiales.append(frm_material)
            linea[frm_material] = frm_linea
            Costo_variable_KG[frm_material] = frm_Costo_variable_KG
            Costo_fijo_total[frm_material] = frm_Costo_fijo_total
            Capacidad_produccion[frm_material] = frm_Capacidad_produccion
            produccion_inicial[frm_material] = frm_produccion_inicial
            precio_inicial[frm_material] = frm_precio_inicial
            elasticidad_pesos[frm_material] = frm_elasticidad_pesos
            elasticidad_kg[frm_material] = frm_elasticidad_kg
            capacidad_maxima[frm_material] = frm_capacidad_maxima

            precio,kg,beneficio=optimizar(
                materiales,
                Costo_variable_KG,
                Costo_fijo_total,
                Capacidad_produccion,
                precio_inicial,
                produccion_inicial,
                elasticidad_pesos,
                elasticidad_kg,
                capacidad_maxima
            )
            df=generar_dataframe_calculo_Kg(Costos_fijos=frm_Costo_fijo_total
                      ,Precio_venta=precio[frm_material]
                      ,kg_producidos=int(produccion_inicial[frm_material])
                      ,kg_propuestos=int(kg[frm_material])
                      ,costo_variable= frm_Costo_variable_KG
                      ) 
            # st.write(df)
            st.write('df cor59')
            st.write(df[df.columns[0]])
            self.grafica_linea_cursosrs(df)


    def grafico_lineas(self,df,titulo='Gráfico de lineas'):  
        st.write(list(df.columns[1,2]))     
        options = {
            "title": {"text": titulo},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": list(df.columns[0],df.columns[1])},
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "toolbox": {"feature": {"saveAsImage": {}}},
            "xAxis": {
                "type": "value",
                "boundaryGap": False,
                # "data": ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"],
            },
            "yAxis": {"type": "value"},
            "series": [
                {
                    "name": "serie 1",
                    "type": "line",
                    "stack": "Total",
                    "data": list(df.column[0]),
                },
                {
                    "name": "serie 2",
                    "type": "line",
                    "stack": "Total",
                    "data": list(df.column[1]),
                },
                # {
                #     "name": "Anuncios de video",
                #     "type": "line",
                #     "stack": "Total",
                #     "data": [150, 232, 201, 154, 190, 330, 410],
                # },
                # {
                #     "name": "Acceso directo",
                #     "type": "line",
                #     "stack": "Total",
                #     "data": [320, 332, 301, 334, 390, 330, 320],
                # },
                # {
                #     "name": "Motores de búsqueda",
                #     "type": "line",
                #     "stack": "Total",
                #     "data": [820, 932, 901, 934, 1290, 1330, 1320],
                # },
            ],
        }
        st_echarts(options=options, height="400px")


    def grafico_lineas_gpt(self, df, titulo='Gráfico de líneas'):
        eje_x = df.iloc[:, 0].tolist()
        series_data = df.iloc[:, 1:]  # Excluir la primera columna de las series de datos

        # Crear una lista de series de datos a partir de las columnas restantes del DataFrame
        series = [
            {
                "name": col,
                "type": "line",
                "stack": "Total",
                "data": series_data[col].tolist(),  # Convertir los datos de la columna a una lista
            }
            for col in series_data.columns  # Iterar sobre todas las columnas restantes
        ]
        
        opciones = {
            "title": {"text": titulo},
            "tooltip": {"trigger": "axis"},
            "legend": {"data": series_data.columns.tolist()},  # Usar los nombres de las columnas restantes como leyenda
            "grid": {"left": "3%", "right": "4%", "bottom": "3%", "containLabel": True},
            "toolbox": {"feature": {"saveAsImage": {}}},
            "xAxis": {
                "type": "category",
                "boundaryGap": False,
                "data": eje_x,  # Usar la primera columna como etiquetas del eje x
            },
            "yAxis": {"type": "value", "data":[x for x in range(0, 20000)]},
            "series": series,  # Añadir las series de datos generadas
        }
        
        st_echarts(options=opciones, height="400px")

  
    def grafica_linea_cursosrs(self,df,nuevo_precio=0.0):  

        ''' Metodo que recibe una lista de elementos que varian en funcion del eje y '''       
        kg=df[df.columns[0]]
        Precio_venta=df[df.columns[1]]
        Costos_fijos=df[df.columns[2]]
        costo_variable=df[df.columns[3]]
        Precio_venta=df[df.columns[4]]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=kg, y=Precio_venta, 
                                name='Precio_venta', mode='lines', line=dict(color='green'), legendrank=True))
    
        fig.add_trace(go.Scatter(x=kg, y=Costos_fijos, 
                                name='Costos_fijos', mode='lines', line=dict(color='Orange'), legendrank=True))
    
        fig.add_trace(go.Scatter(x=kg, y=costo_variable, 
                                name='costo_variable', mode='lines', line=dict(color='Red'), legendrank=True))
        
        # fig.add_trace(go.Scatter(x=kg, y=linea_base, 
        #                         name='linea base', mode='lines', line=dict(color='Yellow'), legendrank=True))

        if nuevo_precio>0:
            fig.add_shape(
                type="line",
                x0=nuevo_precio, y0=min(Precio_venta), x1=nuevo_precio, y1=max(Precio_venta),
                line=dict(color="blue", width=2, dash="dash"),
            )

        fig.update_layout(title='Variación de indicadores financieros en funcion del precio',
                        xaxis=dict(title='Precios'),
                        yaxis=dict(title='Valor'),
                        legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ))

        st.write(fig)