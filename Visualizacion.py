import streamlit as st
from Optimizador import optimizar

class CLS_Estructura_Visualizacion:
    '''
    clase que permite cargar elementos visualizar la transformación del pronostico de reses,
    se apoya en la clase transformación para generar el pronostico y transformar los datos
    '''
    def __init__(self) -> None:
      self.mostrar_navegabilidad()
      
    def mostrar_navegabilidad(self):
        st.sidebar.header("Navegación")
        page = st.sidebar.radio("Ir a:", ["Inicio", "Archivos de muestra","¿Cómo funciona?"])

        if page == "Inicio":
            self.Mostrar_Pantalla_principal('Titulo')
        elif page == "Archivos de muestra":
            self.Mostrar_Pantalla_archivos_muestra('Archivos de muestra')
        elif page=="¿Cómo funciona?":
            self.Mostrar_Pantalla_como_funciona('¿Cómo funciona?')
      
    def Mostrar_Pantalla_principal(self, titulo) -> None:
        '''
        Genera la pantalla principal, habilita la impresión del df de muestra, carga y trasnformación de datos
        '''
        st.title(titulo)
        st.header("Evaluar Precio Óptimo de una linea")

        linea ={}
        Costo_variable_KG ={'ej':1}
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
            material = st.text_input("Material a evaluar")
            frm_Costo_variable_KG = st.number_input("Costo Variable por KG", min_value=0)
            frm_Costo_fijo_total = st.number_input("Costo Fijo de la linea", min_value=0)
            frm_Capacidad_produccion = st.number_input("Capacidad de Producción en KG al mes", min_value=0)
            frm_produccion_inicial = st.number_input("Producción Actual en KG al mes", min_value=0)
            frm_precio_inicial = st.number_input("Precio Actual de Venta", min_value=0)
            frm_elasticidad_pesos = st.slider("Elasticidad del precio, al aumentar los pesos indicados generará una reducción de consumo equivalente a KG al mes", 0, 100)
            frm_elasticidad_kg = st.slider("Elasticidad en KG, al aumentar los pesos indicados anteriormente cuantos reduce en KG el coonsumo al mes", 0, 1000)
            frm_capacidad_maxima = st.slider("Cuanto de la capacidad máxima de la linea se usará %", 0, 100)/100
            frm_submitted = st.form_submit_button("Evaluar")

        if frm_submitted:
            # Agregar los valores del formulario a los diccionarios
            linea[material] = frm_linea
            Costo_variable_KG[material] = frm_Costo_variable_KG
            Costo_fijo_total[material] = frm_Costo_fijo_total
            Capacidad_produccion[material] = frm_Capacidad_produccion
            produccion_inicial[material] = frm_produccion_inicial
            precio_inicial[material] = frm_precio_inicial
            elasticidad_pesos[material] = frm_elasticidad_pesos
            elasticidad_kg[material] = frm_elasticidad_kg
            capacidad_maxima[material] = frm_capacidad_maxima

            optimizar()
      
    def Mostrar_Pantalla_archivos_muestra(self, titulo) -> None:
        '''
        Genera la pantalla principal, habilita la impresión del df de muestra, carga y trasnformación de datos
        '''
        st.title(titulo)
      
    def Mostrar_Pantalla_como_funciona(self, titulo) -> None:
            st.title(titulo)    
            st.subheader('Carga de datos')
            st.write('''Para generar un pronóstico es necesario suministrar información 
                     que sirva de soporte para los nuevos datos a generar, en este caso es necesario 
                     cargar la historia semana a semana de las reses negociadas y su precio, el formato 
                     establecido está indicado en el segmento "Archivos de muestra", allí se muestran
                      algunas tablas que se pueden descargar como formato csv, los titulos deben ser respetados
                      y la información que se cargue debe estar revisada para generar un pronóstico aceptable, 
                      una vez se descarguen los archivos de muestra, se llenan con la información correspondiente,
                      se guardan como archvos "xlsx" y se cargan en los botones habilitados en el segmento "Inicio". 
                     Es posible cargar una serie de tiempo con distintas categorias, al hacer esto se generará un modelo
                     y un pronóstico para cada una de ellas.
                     
                      ''')
            
            st.subheader('¿Qué hay detrás?')
            st.write('''Cuando se cargan los datos, la herramienta genera el mejor modelo de serie de tiempo 
                     que se puede ajustar a los datos cargados, genera el prónostico y lo grafica con un intervalo de
                     confianza del 95% y al 65%, se puede mover algunos parametros como la cantidad de datos a ver de la serie real
                     y la cantidad de datos a pronosticar; el modelo generado tambien puede ser modificado, agregandole un componente
                     estacional, un atributo de tendencia y además seleccionar el tamaño de la muestra usado para generar el mejor modelo, es decir puedes generar
                     tu modelo usando todos los datos cargados o solo los últimos que escojas, es importante mencionar que puedes usar una 
                     muestra pequeña de datos para generar el modelo y aún así ver tu serie de datos completa.  ''')                   
            st.write('''Siendo un poco mas técnicos, Cuando se habla del "mejor modelo" en el contexto de esta función, 
                     se refiere al modelo que mejor se ajusta a los datos de la serie temporal proporcionada. 
                     Esto significa que el modelo seleccionado tiene la capacidad de hacer predicciones precisas 
                     para valores futuros basados en el patrón histórico de los datos. El proceso de encontrar el 
                     "mejor modelo" generalmente implica probar y comparar diferentes combinaciones de parámetros 
                     del modelo (como el orden AR, el orden de diferenciación, el orden MA, etc.) y seleccionar 
                     aquel que minimiza una métrica de evaluación, como el error cuadrático medio (MSE) o el 
                     criterio de información bayesiana (BIC) - Usado actualmente -.  ''')                   
            st.write(''' Al ser una función de ajuste automático, puede generar varios tipos de modelos, algunos de los cuales son:
                     *ARIMA* (Autoregressive Integrated Moving Average): Un modelo que combina componentes autoregresivas, de media móvil y de diferenciación para capturar la estructura de la serie temporal.
                     *SARIMA* (Seasonal ARIMA): Similar a ARIMA, pero con la capacidad de modelar patrones estacionales en los datos.
                     *SARIMAX* (Seasonal ARIMA with exogenous variables): Una extensión de SARIMA que permite incluir variables exógenas que pueden influir en la serie temporal.
                     *ARIMAX* (ARIMA with exogenous variables): Similar a SARIMAX pero sin componente estacional.''')                   
            st.write('''
                     Cada uno de estos modelos tiene sus propias características y puede ser útil en diferentes 
                     situaciones dependiendo de la naturaleza de los datos y los patrones que se intenten capturar. La función usada 
                     ayuda a identificar el modelo óptimo entre estas opciones, teniendo en cuenta la complejidad de los datos y la 
                     precisión de las predicciones.  
                     ''')
            
            st.subheader('Soporte')
            st.write('''Este desarrollo fue generado por el equipo de modelación del negocio cárnico, si hay algún
                     requerimiento, duda o comentario sobre el mismo puede ser a través del líder del equipo
                     Lucas Ramirez, así mismo si se tiene alguna necesidad de desarrollo similar al presente puede
                     comunicarlo con la misma persona o a través del siguente enlace  ''')
            st.markdown('Formulario de soporte equipo modelación negocio cárnico https://docs.google.com/forms/d/e/1FAIpQLSfNVT7yFcuaWHvZ_V-wNlu02tPVvbCNA6nA0I1Bhcj5D4MRkQ/viewform')

    
    