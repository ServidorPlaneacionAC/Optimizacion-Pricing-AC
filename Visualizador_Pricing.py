import streamlit as st
from Optimizador import optimizar, generar_dataframe

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

            precio,kg,ben=optimizar(
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
            st.write(precio)
            st.write(kg)
            st.write(ben)

            # generar_dataframe(KG)

      