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
        beneficio=None

        # with st.form("add_ticket_form"):
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
        # frm_submitted = st.form_submit_button("Evaluar")

        # if frm_submitted:
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
        if beneficio is not None:
            produccion_inicial_imprimir=self.formatear_dinero(frm_produccion_inicial)  
            kg_producir=self.formatear_dinero( kg[frm_material])   

            beneficio_inicial=precio_inicial[frm_material]-Costo_variable_KG[frm_material]-Costo_fijo_total[frm_material]/produccion_inicial[frm_material]
            diferencia_beneficio=beneficio[frm_material]-beneficio_inicial
            beneficio_inicial=self.formatear_dinero(beneficio_inicial)
            beneficio_imprimir=self.formatear_dinero(beneficio[frm_material],simbolo='$')
            diferencia_beneficio=self.formatear_dinero(diferencia_beneficio)

            st.success(f'Se ha encontrado una solución óptima, el nuevo beneficio sera {beneficio_imprimir} por KG, pasando de fabricar {produccion_inicial_imprimir} KG a fabricar {kg_producir} KG')        
            st.success(f'El beneficio anterior era {beneficio_inicial} por Kg lo que nos indica una variación en el beneficio de {diferencia_beneficio} ')
            
            inicio_grafica = st.slider("KG iniciales para comparar en la grafica", 0, int(kg[frm_material]), value=int(kg[frm_material]/2))
            df=generar_dataframe_calculo_Kg(Costos_fijos=frm_Costo_fijo_total
                    ,Precio_venta=precio[frm_material]
                    ,kg_producidos=int(inicio_grafica)
                    ,kg_propuestos=int(kg[frm_material])
                    ,costo_variable= frm_Costo_variable_KG
                    ) 
            self.grafica_lineas(df)
        else:
            st.error('No se encuentra un posible mejor escenario ')

    def formatear_dinero(self,valor,decimales=2, simbolo=''):
        """
        Redondea un valor y lo muestra en formato de dinero.

        Parámetros:
        valor (float): El valor numérico a formatear.
        simbolo (str): El símbolo de la moneda a utilizar. Por defecto es '$'.

        Retorna:
        str: El valor formateado como dinero.
        """
        valor_redondeado = round(valor, decimales)
        formato_dinero = f"{simbolo}{valor_redondeado:,.2f}"
        return formato_dinero


    def grafica_lineas(self,df):  

        ''' Metodo que recibe una lista de elementos que varian en funcion del eje y '''       
        kg=df[df.columns[0]]
        Precio_venta=df[df.columns[1]]
        Costos_fijos=df[df.columns[2]]
        costo_variable=df[df.columns[3]]
        costo_totales=df[df.columns[4]]
        beneficio=df[df.columns[5]]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=kg, y=Precio_venta, 
                                name='Precio venta por kg', mode='lines', line=dict(color='green'), legendrank=True))
    
        fig.add_trace(go.Scatter(x=kg, y=Costos_fijos, 
                                name='Costos fijos por kg', mode='lines', line=dict(color='Orange'), legendrank=True))
    
        fig.add_trace(go.Scatter(x=kg, y=costo_variable, 
                                name='costo variable por kg', mode='lines', line=dict(color='Red'), legendrank=True))
        
        fig.add_trace(go.Scatter(x=kg, y=costo_totales, 
                                name='costo totales por kg', mode='lines', line=dict(color='yellow'), legendrank=True))
        
        fig.add_trace(go.Scatter(x=kg, y=beneficio, 
                                name='beneficio por KG', mode='lines', line=dict(color='blue'), legendrank=True))
        
        fig.update_layout(title='Análisis de costos y rendimientos por Kg',
                        xaxis=dict(title='Kg producidos'),
                        yaxis=dict(title='$$'),
                        legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ))

        st.write(fig)