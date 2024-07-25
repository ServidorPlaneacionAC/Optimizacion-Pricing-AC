import streamlit as st
from Optimizador import optimizar, generar_dataframe_calculo_Kg, generar_dataframe_calculo_total
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
            beneficio_inicial_numerico=self.imprimir_conclusiones(
                frm_material,
                kg[frm_material],
                precio[frm_material],
                beneficio[frm_material])

            inicio_grafica = st.slider("Valores del eje x de la grafica (KG producidos)", 1, int(kg[frm_material]), value=int(kg[frm_material]/2))
            precio_analizar = st.slider("Precio para analizar diferentes escenarios", int(precio[frm_material]*0.85), int(self.precio_inicial[frm_material]*1.25), value=int(precio[frm_material]))
            
            opciones  = ['Análisis por KG', 'Análisis completo']
            opcion_seleccionada = st.selectbox('Selecciona una opción para analizar:', opciones)
            if opcion_seleccionada == 'Análisis por KG':
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
                self.grafica_lineas(df,titulo_grafico='Análisis de costos y rendimientos por Kg',lineas_punteadas=['Beneficio nuevo','Precio nuevo'],linea_horizontal=beneficio_inicial_numerico,titulo_linea_horizontal='Beneficio Actual')
                if precio_analizar!=int(precio[frm_material]): #Genera conclusión final del escenario what if
                    beneficio_inicial=self.precio_inicial[frm_material]-self.Costo_variable_KG[frm_material]-self.Costo_fijo_total[frm_material]/self.produccion_inicial[frm_material]
                    nuevo_beneficio_imprimir=self.formatear_dinero((df.iloc[-1, -1]*kg[frm_material]-beneficio_inicial*self.produccion_inicial[frm_material]), simbolo='COP ')
                    st.success(f'Con el nuevo precio ingresado, se obtendría un beneficio adicional total de {nuevo_beneficio_imprimir} sobre el beneficio actual')
            else:
                
                df=generar_dataframe_calculo_total(
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
                
                self.grafica_lineas(df,titulo_grafico='Análisis de costos y rendimientos totales',lineas_punteadas=['Beneficio nuevo','Nueva venta total'],linea_horizontal=beneficio_inicial_numerico*self.produccion_inicial[frm_material]titulo_linea_horizontal='Beneficio Actual')
                # if precio_analizar!=int(precio[frm_material]): #Genera conclusión final del escenario what if
                beneficio_inicial=self.precio_inicial[frm_material]*self.produccion_inicial[frm_material]-self.Costo_variable_KG[frm_material]*self.produccion_inicial[frm_material]-self.Costo_fijo_total[frm_material]
                nuevo_beneficio_imprimir=self.formatear_dinero((df.iloc[-1, -1]-beneficio_inicial), simbolo='COP ')
                st.success(f'Con el nuevo precio ingresado, se obtendría un beneficio adicional total de {nuevo_beneficio_imprimir} sobre el beneficio actual')
       

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

    def grafica_lineas(self,df,titulo_grafico='',titulo_ejex='',titulo_eje_y='',titulos=None, colores=None, lineas_punteadas=[],linea_horizontal=None,titulo_linea_horizontal=''):  
        """
            Método que recibe un DataFrame y grafica líneas para cada columna (excepto la primera) en función del eje y.

            Parámetros:
            - df (pd.DataFrame): DataFrame que contiene los datos a graficar. La primera columna se usa como eje x.
            - titulo_grafico (str, opcional): Título del gráfico. Por defecto es una cadena vacía.
            - titulo_ejex (str, opcional): Título del eje x. Si no se proporciona, se utiliza el nombre de la primera columna del DataFrame.
            - titulo_eje_y (str, opcional): Título del eje y. Por defecto es una cadena vacía.
            - titulos (list, opcional): Lista de títulos para las líneas. Si no se proporciona, se utilizan los nombres de las columnas del DataFrame (excepto la primera).
            - colores (list, opcional): Lista de colores para las líneas. Si no se proporciona, se generan colores automáticamente.
            - lineas_punteadas (list, opcional): Lista de títulos que deben ser representados con líneas punteadas. Por defecto es una lista vacía.

            Retorna:
            - None: Este método no retorna ningún valor, pero muestra el gráfico generado en Streamlit.
        """ 
        lineas = [df[df.columns[i]] for i in range(8)]
        titulos= df.columns[1:] if titulos is None else titulos
        colores= self.generar_colores(df.shape[1]-1) if colores is None else colores
        titulo_ejex = df.columns[0] if titulo_ejex=='' else titulo_ejex
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for i,titulo,color in zip(lineas[1:],titulos,colores):
            if titulo in lineas_punteadas:
                linea=dict(color=color,dash='dash')
            else:
                linea=dict(color=color)
            fig.add_trace(go.Scatter(x=lineas[0], y=i, 
                                    name=titulo, mode='lines', line=linea, legendrank=True))
  
        if linea_horizontal is not None:
            fig.add_trace(go.Scatter(
                x=[df[df.columns[0]].min(), df[df.columns[0]].max()],
                y=[linea_horizontal, linea_horizontal],
                mode='lines',
                name=titulo_linea_horizontal,
                line=dict(color='black', width=2, dash='dash')
            ))

        fig.update_layout(title=titulo_grafico,
                        xaxis=dict(title=titulo_ejex),
                        yaxis=dict(title=titulo_eje_y),
                        legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ))

        st.write(fig)

    def generar_colores(self,cantidad):
        """
        Genera una lista de colores diferentes.

        Parámetros:
        - cantidad (int): Número de colores diferentes a generar.

        Retorna:
        - lista_colores (list): Lista de colores en formato hexadecimal.
        """
        import matplotlib.colors as mcolors
        # Obtener una lista de colores únicos predefinidos en matplotlib
        colores_predefinidos = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())
        
        # Si la cantidad de colores solicitados es menor o igual al número de colores predefinidos, devolvemos los primeros 'cantidad' colores
        if cantidad <= len(colores_predefinidos):
            return colores_predefinidos[:cantidad]
        
        # Si se requieren más colores, generar colores adicionales
        else:
            import numpy as np
            import matplotlib.pyplot as plt
            from matplotlib.colors import rgb2hex
            
            # Generar colores adicionales
            colores_adicionales = []
            for i in np.linspace(0, 1, cantidad - len(colores_predefinidos)):
                colores_adicionales.append(plt.cm.tab20(i))  # Cambiar 'tab20' por cualquier otro mapa de colores si es necesario
            
            # Convertir los colores adicionales a formato hexadecimal
            colores_adicionales_hex = [rgb2hex(color) for color in colores_adicionales]
            
            # Combinar los colores predefinidos con los colores adicionales
            return colores_predefinidos + colores_adicionales_hex



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
            diferencia_beneficio_total=beneficio*kg_producir -beneficio_inicial*self.produccion_inicial[material]
            beneficio_inicial_numerico=beneficio_inicial
            beneficio_inicial=self.formatear_dinero(beneficio_inicial,simbolo='COP ')
            beneficio_imprimir=self.formatear_dinero(beneficio,simbolo='COP ')
            diferencia_beneficio=self.formatear_dinero(diferencia_beneficio,simbolo='COP ')
            diferencia_en_precio_imprimir=self.formatear_dinero(self.precio_inicial[material]-precio_propuesto,simbolo='COP ')

            diferencia_en_kg=kg_producir-self.produccion_inicial[material]
            diferencia_beneficio_total_imprimir=self.formatear_dinero(diferencia_beneficio_total,simbolo='COP ')
            diferencia_en_kg_imprimir=self.formatear_dinero(diferencia_en_kg)
            
            st.success(f'Se ha encontrado una solución óptima, con el precio {precio_imprimir} el nuevo beneficio sera {beneficio_imprimir} por KG, pasando de fabricar {produccion_inicial_imprimir} KG a fabricar {kg_producir_imprimir} KG')        
            st.success(f'El beneficio anterior era {beneficio_inicial} por Kg lo que nos indica una variación en el beneficio de {diferencia_beneficio} por KG')
            st.success(f'Con una reducción en el precio de {diferencia_en_precio_imprimir} y produciendo {diferencia_en_kg_imprimir} kg mas se obtiene en total un beneficio adicional de {diferencia_beneficio_total_imprimir}')
            
            return beneficio_inicial_numerico