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
      '''
      Se inicializan los diccionarios para generar calculos, este diseño inicial esta pensado para evaluar un único material pero 
      se generan diccionarios y listas estimando un posible crecimiento del desarrollo
      
      Atributos
        materiales([list]) Lista de materiales a evaluar
        linea({dicc}) Clave: Material, Valor: Linea del material 
        Costo_variable_KG({dicc}) Clave: Material, Valor: costo variable por kilogramo 
        Costo_fijo_total({dicc}) Clave: Material, Valor: Costo fijo total asociado a fabricar este material
        Capacidad_produccion({dicc}) Clave: Material, Valor: Capacidad total de la linea de producción 
        produccion_inicial({dicc}) Clave: Material, Valor: Producción actual  
        precio_inicial({dicc}) Clave: Material, Valor: Precio de comersalización actual 

        Elasticidad de un producto, si el precio de un articulo aunmenta p pesos la demanda de dicho articulo disminuirá q unidades

        elasticidad_pesos ({dicc}) #Clave: Material, Valor: según la definición anterior los pesos p que aumentará el valor del articulo
        elasticidad_kg ({dicc}) #Clave: Material, Valor: según la definición anterior la demanda q (expresada en KG) que disminuye mi articulo 
                                                          Importante: asumo que el precio aumenta y mi demanda disminuye
                                                                      tambien asumo que el precio baja mi demanda aumenta

        capacidad_maxima ({dicc}) Clave: Material, Valor: Capacidad maxima de producción 
        beneficio ({dicc}) Clave: Material, Valor: Beneficio calculado 
      '''
      self.materiales=[] #Lista de materiales a evaluar
      self.linea ={} #Clave: Material, Valor: Linea del material 
      self.Costo_variable_KG ={} #Clave: Material, Valor: costo variable por kilogramo 
      self.Costo_fijo_total ={} #Clave: Material, Valor: Costo fijo total asociado a fabricar este material
      self.Capacidad_produccion ={} #Clave: Material, Valor: Capacidad total de la linea de producción 
      self.produccion_inicial ={} #Clave: Material, Valor: Producción actual  
      self.precio_inicial ={} #Clave: Material, Valor: Precio de comersalización actual 

      # Elasticidad de un producto, si el precio de un articulo aunmenta p pesos la demanda de dicho articulo disminuirá q unidades

      self.elasticidad_pesos ={} #Clave: Material, Valor: según la definición anterior los pesos p que aumentará el valor del articulo
      self.elasticidad_kg ={} #Clave: Material, Valor: según la definición anterior la demanda q (expresada en KG) que disminuye mi articulo 
                                 #                      Importante: asumo que el precio aumenta y mi demanda disminuye
                                 #                                  tambien asumo que el precio baja mi demanda aumenta

      self.capacidad_maxima ={} #Clave: Material, Valor: Capacidad maxima de producción 
      self.beneficio=None #Clave: Material, Valor: Beneficio calculado 
      self.generar_formulario()

    def generar_formulario(self):
        '''
        Genera los campos de captura de información y los inicializa con un valor de ejemplo
        inicializa los diccionarios e invoca el metodo de generar calculos
        '''
        frm_linea = st.selectbox("Linea a evaluar", ["Otro", "Chorizos", "Salchichas","Salchichones",
                                                        "Jamones", "Larga Vida", "Carnes Frescas", "Mortadelas"])
        frm_material = st.text_input("Material a evaluar",value="Material de ejemplo")
        frm_Costo_variable_KG = st.number_input("Costo Variable por KG", min_value=0, value=10341)
        frm_Costo_fijo_total = st.number_input("Costo Fijo de la linea", min_value=0, value=4981461166)
        frm_Capacidad_produccion = st.number_input("Capacidad de Producción en KG al mes", min_value=0, value=770879)
        frm_produccion_inicial = st.number_input("Producción Actual en KG al mes", min_value=0, value=691245)
        frm_precio_inicial = st.number_input("Precio Actual de Venta", min_value=0, value=35096)

        st.info('Elasticidad de un producto, si el precio de un articulo aumenta p pesos la demanda de dicho articulo disminuirá q unidades')
        st.info('Se asume que el precio aumenta y la demanda disminuye, así mismo se asume que el precio baja y la demanda aumenta')
        frm_elasticidad_pesos = st.slider("Elasticidad del precio, según la definición anterior la cantidad de pesos p que el precio aumenta ", 0, 100, value=1)
        frm_elasticidad_kg = st.slider("Elasticidad en KG, según la definición anterior la cantidad de kg q que la demanda disminuye ", 0, 1000, value=400)
        frm_capacidad_maxima = st.slider("Cuanto de la capacidad máxima de la linea se usará %", 0, 100, value=100)/100

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
        self.generar_calculos(frm_material)

    def generar_calculos(self,frm_material):
        '''
        Genera calculos y muestra resultados, si desde la optimiazacion en cuentra un resultado optimo 
        imprime los resultados de la optimizacion
        genera las opciones para el escenario what if
        genera el df requerido para el grafico resultante

        Paramteros:
        frm_material (str): Material que es la clave de los diccionarios para el que se generará el análisis
        '''
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
        if beneficio is not None: #Si el resultado de la optimizacion es un valor factible           
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
                    ,costo_variable= self.Costo_variable_KG[frm_material]
                    ,elasticidad_pesos=self.elasticidad_pesos[frm_material]  
                    ,elasticidad_kg=self.elasticidad_kg[frm_material]   
                    ,precio_inicial=self.precio_inicial[frm_material]   
                    ,produccion_inicial=self.produccion_inicial[frm_material]  
                    ,precio_analisis= precio_analizar          
                    ) 
            self.grafica_lineas(df)
            if precio_analizar!=int(precio[frm_material]): #Genera conclusión final del escenario what if
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
            