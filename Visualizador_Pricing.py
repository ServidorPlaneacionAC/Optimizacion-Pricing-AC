import streamlit as st
from Optimizador import optimizar, generar_dataframe_calculo_Kg
import mplcursors
from plotly.subplots import make_subplots
import plotly.graph_objs as go

class CLS_Visualizacion_pricing:
    '''
    clase que permite tener todas las particularidades necesarias
      para la visualización del modelo de pricing
    '''
    def __init__(self) -> None:
      
      self.materiales=[]
      self.linea ={}
      self.Costo_variable_KG ={}
      self.Costo_fijo_total ={}
      self.Capacidad_produccion ={}
      self.produccion_inicial ={}
      self.precio_inicial ={}
      self.elasticidad_pesos ={}
      self.elasticidad_kg ={}
      self.capacidad_maxima ={}
      self.beneficio=None
      self.generar_formulario()

    def generar_formulario(self):

        # with st.form("add_ticket_form"):
            # issue = st.text_area("Describe the issue")
        frm_linea = st.selectbox("Linea a evaluar", ["Otro", "Chorizos", "Salchichas","Salchichones",
                                                        "Jamones", "Larga Vida", "Carnes Frescas", "Mortadelas"])
        frm_material = st.text_input("Material a evaluar",value="Material de ejemplo")
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
        self.materiales.append(frm_material)
        self.linea[frm_material] = frm_linea
        self.Costo_variable_KG[frm_material] = frm_Costo_variable_KG
        self.Costo_fijo_total[frm_material] = frm_Costo_fijo_total
        self.Capacidad_produccion[frm_material] = frm_Capacidad_produccion
        self.produccion_inicial[frm_material] = frm_produccion_inicial
        self.precio_inicial[frm_material] = frm_precio_inicial
        self.elasticidad_pesos[frm_material] = frm_elasticidad_pesos
        self.elasticidad_kg[frm_material] = frm_elasticidad_kg
        self.capacidad_maxima[frm_material] = frm_capacidad_maxima

        precio,kg,beneficio=optimizar(
            self.materiales,
            self.Costo_variable_KG,
            self.Costo_fijo_total,
            self.Capacidad_produccion,
            self.precio_inicial,
            self.produccion_inicial,
            self.elasticidad_pesos,
            self.elasticidad_kg,
            self.capacidad_maxima
        )
        if beneficio is not None:            
            st.header("Resultados iniciales:")
            self.imprimir_conclusiones(
                frm_material,
                kg[frm_material],
                precio[frm_material],
                beneficio[frm_material])

            inicio_grafica = st.slider("Valores del eje x de la grafica (KG producidos)", 1, int(kg[frm_material]), value=int(kg[frm_material]/2))
            precio_analizar = st.slider("Precio para analizar diferentes escenarios", int(precio[frm_material]*0.85), int(self.precio_inicial[frm_material]*1.25), value=int(precio[frm_material]))
            df=generar_dataframe_calculo_Kg(
                    Costos_fijos=self.Costo_fijo_total[frm_material]
                    ,Precio_venta=precio[frm_material]
                    ,kg_producidos=int(inicio_grafica)
                    ,kg_propuestos=int(kg[frm_material])
                    ,costo_variable= frm_Costo_variable_KG
                    ,elasticidad_pesos=self.elasticidad_pesos[frm_material]  
                    ,elasticidad_kg=self.elasticidad_kg[frm_material]   
                    ,precio_inicial=self.precio_inicial[frm_material]   
                    ,produccion_inicial=self.produccion_inicial[frm_material]  
                    ,precio_analisis= precio_analizar          
                    ) 
            self.grafica_lineas(df)
            if precio_analizar!=int(precio[frm_material]):
                beneficio_inicial=self.precio_inicial[frm_material]-self.Costo_variable_KG[frm_material]-self.Costo_fijo_total[frm_material]/self.produccion_inicial[frm_material]
                diferencia_en_kg=kg[frm_material]-self.produccion_inicial[frm_material]
                nuevo_beneficio_imprimir=self.formatear_dinero((df.iloc[-1, -1]-beneficio_inicial)*diferencia_en_kg, simbolo='COP ')
                st.success(f'Con el nuevo precio ingresado, se obtendría un beneficio adicional total de {nuevo_beneficio_imprimir} sobre el beneficio actual')
        else:
            st.error('No se encuentra un posible mejor escenario')


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
        precio_nuevo=df[df.columns[6]]
        beneficio_nuevo=df[df.columns[7]]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=kg, y=Precio_venta, 
                                name='Precio venta', mode='lines', line=dict(color='green'), legendrank=True))
    
        fig.add_trace(go.Scatter(x=kg, y=Costos_fijos, 
                                name='Costos fijos', mode='lines', line=dict(color='Orange'), legendrank=True))
    
        fig.add_trace(go.Scatter(x=kg, y=costo_variable, 
                                name='Costo variable', mode='lines', line=dict(color='Red'), legendrank=True))
        
        fig.add_trace(go.Scatter(x=kg, y=costo_totales, 
                                name='Costo totales', mode='lines', line=dict(color='yellow'), legendrank=True))
        
        fig.add_trace(go.Scatter(x=kg, y=beneficio, 
                                name='Beneficio', mode='lines', line=dict(color='blue'), legendrank=True))
            
        fig.add_trace(go.Scatter(x=kg, y=precio_nuevo, 
                                name='Precio nuevo', mode='lines', line=dict(color='green',dash='dash'), legendrank=True))
          
        fig.add_trace(go.Scatter(x=kg, y=beneficio_nuevo, 
                                name='Beneficio nuevo fijo', mode='lines', line=dict(color='blue',dash='dash'), legendrank=True))
      
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

    def imprimir_conclusiones(self,
                              material,
                              kg_producir,
                              precio_propuesto,
                              beneficio):
        
            produccion_inicial_imprimir=self.formatear_dinero(self.produccion_inicial[material])  
            kg_producir_imprimir=self.formatear_dinero(kg_producir)   
            precio_imprimir=self.formatear_dinero(precio_propuesto,simbolo='COP ')
            beneficio_inicial=self.precio_inicial[material]-self.Costo_variable_KG[material]-self.Costo_fijo_total[material]/self.produccion_inicial[material]
            diferencia_beneficio=beneficio-beneficio_inicial
            diferencia_beneficio_total_imprimir=diferencia_beneficio
            beneficio_inicial=self.formatear_dinero(beneficio_inicial,simbolo='COP ')
            beneficio_imprimir=self.formatear_dinero(beneficio,simbolo='COP ')
            diferencia_beneficio=self.formatear_dinero(diferencia_beneficio,simbolo='COP ')
            diferencia_en_precio_imprimir=self.formatear_dinero(self.precio_inicial[material]-precio_propuesto,simbolo='COP ')

            diferencia_en_kg=kg_producir-self.produccion_inicial[material]
            diferencia_beneficio_total_imprimir=self.formatear_dinero(diferencia_beneficio_total_imprimir*diferencia_en_kg,simbolo='COP ')
            diferencia_en_kg_imprimir=self.formatear_dinero(diferencia_en_kg)
            
            st.success(f'Se ha encontrado una solución óptima, con el precio {precio_imprimir} el nuevo beneficio sera {beneficio_imprimir} por KG, pasando de fabricar {produccion_inicial_imprimir} KG a fabricar {kg_producir_imprimir} KG')        
            st.success(f'El beneficio anterior era {beneficio_inicial} por Kg lo que nos indica una variación en el beneficio de {diferencia_beneficio} por KG')
            st.success(f'Con una reducción en el precio de {diferencia_en_precio_imprimir} y produciendo {diferencia_en_kg_imprimir} kg mas se obtiene en total un beneficio adicional de {diferencia_beneficio_total_imprimir}')
            