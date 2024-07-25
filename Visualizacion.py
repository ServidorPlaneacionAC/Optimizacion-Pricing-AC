import streamlit as st
from Optimizador import optimizar, generar_dataframe_calculo_Kg
from Visualizador_Pricing import CLS_Visualizacion_pricing

class CLS_Estructura_Visualizacion:
    '''
    clase que permite ser la estrutura inicial de la visualización en streamlit, primer paso en la estandarización de desarrollos 
    '''
    def __init__(self) -> None:
      self.mostrar_navegabilidad(["Inicio", "¿Cómo funciona?"])
      
    def mostrar_navegabilidad(self,paginas=["Inicio", "Archivos de muestra","¿Cómo funciona?"]):
        '''
        Genera el slider que permite navegar entre interfaces del desarrollo

        Parametros:
        paginas [list]: definir las paginas que iran en el slider
        '''
        st.sidebar.header("Navegación")
        page = st.sidebar.radio("Ir a:", paginas)

        if page == "Inicio":
            self.Mostrar_Pantalla_principal('Encontrar Precio óptimo')
        elif page == "Archivos de muestra":
            self.Mostrar_Pantalla_archivos_muestra('Archivos de muestra')
        elif page=="¿Cómo funciona?":
            self.Mostrar_Pantalla_como_funciona('¿Cómo funciona?')
      
    def Mostrar_Pantalla_principal(self, titulo) -> None:
        '''
        Genera la pantalla principal, habilita la impresión del df de muestra, carga y trasnformación de datos
        
        Parametros:
        titulo (str): Indica el titulo de la página actual
        '''
        st.title(titulo)
        st.header("Evaluar Precio Óptimo de una linea")

        pricing=CLS_Visualizacion_pricing()
      
    def Mostrar_Pantalla_archivos_muestra(self, titulo) -> None:
        '''
        Genera la pantalla principal, habilita la impresión del df de muestra, carga y trasnformación de datos
        '''
        st.title(titulo)
      
    def Mostrar_Pantalla_como_funciona(self, titulo) -> None:
            st.title(titulo)    
            st.subheader("Modelo Matemático del Problema de Optimización")
            st.write('''Para desarrollar esta solución se uso programación lineal para encontrar el valor óptimo donde
                     el modelo matemático busca maximizar el beneficio total, ajustando los precios y las cantidades 
                     producidas de varios materiales. Para lograr esto, se consideran varios factores como los costos fijos y variables,
                      las capacidades de producción, y la elasticidad del precio y la producción ''')

            st.markdown("### Variables de Decisión:")
            st.latex(r"p_i \text{: Precio final del material } i")
            st.latex(r"q_i \text{: Cantidad producida del material } i")

            st.markdown("### Parámetros:")
            st.latex(r"\text{CV}_i \text{: Costo variable por kilogramo del material } i")
            st.latex(r"\text{CF}_i \text{: Costo fijo total del material } i")
            st.latex(r"\text{CP}_i \text{: Capacidad de producción inicial del material } i")
            st.latex(r"\text{PI}_i \text{: Precio inicial del material } i")
            st.latex(r"\text{QI}_i \text{: Producción inicial del material } i")
            st.latex(r"\epsilon_{p,i} \text{: Elasticidad del precio con respecto a la cantidad producida del material } i")
            st.latex(r"\epsilon_{q,i} \text{: Elasticidad de la cantidad producida con respecto al precio del material } i")
            st.latex(r"\text{CM}_i \text{: Capacidad máxima de producción permitida para el material } i")

            st.markdown("### Función Objetivo:")
            st.latex(r"\max \sum_{i=1}^{n} \left( p_i - \text{CV}_i - \frac{\text{CF}_i}{q_i} \right) q_i")
            st.write('''El objetivo principal es maximizar el beneficio total. El beneficio por cada material 
                     se calcula como la diferencia entre el precio de venta y los costos (tanto fijos como variables),
                       multiplicado por la cantidad producida:''')

            st.markdown("### Restricciones:") 
            st.write('''La cantidad producida qi está relacionada con el precio final pi
                       mediante la elasticidad del precio y de la producción. La ecuación es:
                    ''')
            st.latex(r"1. \ q_i = \text{QI}_i - \left( \frac{p_i - \text{PI}_i}{\epsilon_{p,i}} \right) \epsilon_{q,i}")
           
            st.write('''La cantidad producida qi no puede exceder la capacidad máxima de producción permitida:''')
            st.latex(r"2. \ q_i \leq \text{CP}_i \times \text{CM}_i")

            st.write('''El precio final pi no puede ser mayor que el precio inicial:''')
            st.latex(r"3. \ p_i \leq \text{PI}_i")

            st.write('''La cantidad producida qi debe ser al menos 0.1 para evitar valores triviales:''')
            st.latex(r"4. \ q_i \geq 0.1")

            st.markdown("### Consideraciones:")
            st.write('''Importante considerar factores tenidos en cuenta y obviados al momento de calcular los beneficios en cada escenario
                    ,los costos asociados al inventario y costo capital del mismo no está siendo considerados en el ejercicio; así mismo,
                    los únicos costos en el modelo son los diligenciados por el usuario en la captura de información, se sugiere al usuario
                    calcular todos los costos y relacionarlos como fijos o variables en función de los Kg producidos.''')
            st.write('''
                    Se asume como parte del ejercicio que todos los Kg producidos serán vendidos exitosamente en el mercado, de igual manera,
                    en la optimización de Kg a producir se restringe la venta disminción del precio, según la elasticidad del producto indicada,
                    en los escenarios que se generan a partir de modificar el precio del material no se considera la elasticidad del producto.
            ''')

            st.title('Soporte')
            st.write('''Este desarrollo fue generado por el equipo de modelación del negocio cárnico, si hay algún
                     requerimiento, duda o comentario sobre el mismo puede ser a través del líder del equipo
                     Lucas Ramirez, así mismo si se tiene alguna necesidad de desarrollo similar al presente puede
                     comunicarlo con la misma persona o a través del siguente enlace  ''')
            st.markdown('Formulario de soporte equipo modelación negocio cárnico https://docs.google.com/forms/d/e/1FAIpQLSfNVT7yFcuaWHvZ_V-wNlu02tPVvbCNA6nA0I1Bhcj5D4MRkQ/viewform')

    
    
