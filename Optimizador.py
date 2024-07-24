import numpy as np
from scipy.optimize import minimize
import streamlit as st
import pandas as pd

def optimizar(  materiales,
                Costo_variable_KG,
                Costo_fijo_total,
                Capacidad_produccion,
                precio_inicial,
                produccion_inicial,
                elasticidad_pesos,
                elasticidad_kg,
                capacidad_maxima):
    

    """
        Optimiza los precios y cantidades producidas de varios materiales para maximizar el beneficio.

        Parámetros:
        - materiales (list): Lista de materiales.
        - Costo_variable_KG (dict): Diccionario con el costo variable por kilogramo para cada material.
        - Costo_fijo_total (dict): Diccionario con el costo fijo total asociado a la producción de cada material.
        - Capacidad_produccion (dict): Diccionario con la capacidad de producción inicial de cada material.
        - precio_inicial (dict): Diccionario con el precio inicial de cada material.
        - produccion_inicial (dict): Diccionario con la producción inicial en kg de cada material.
        - elasticidad_pesos (dict): Diccionario con la elasticidad del precio en relación a la cantidad producida.
        - elasticidad_kg (dict): Diccionario con la elasticidad de la cantidad producida en relación al precio.
        - capacidad_maxima (dict): Diccionario con la capacidad máxima de producción permitida para cada material.

        Retorna:
        - precio_final (dict): Diccionario con los precios finales óptimos para cada material.
        - KG_Propuestos (dict): Diccionario con las cantidades producidas óptimas para cada material.
        - beneficio_esperado (dict): Diccionario con los beneficios esperados para cada material.
    """    
    # Definir datos (estos valores deben ser proporcionados para cada material)


    # Variables iniciales (precios y cantidades iniciales para optimización)
    x0 = np.array([precio_inicial[i] for i in materiales] + [produccion_inicial[i] for i in materiales])

    # Función objetivo
    def objetivo(x):
        precio_final = x[:len(materiales)]
        kg = x[len(materiales):]
        return -sum(
            precio_final[i] - Costo_variable_KG[materiales[i]] - (Costo_fijo_total[materiales[i]] / kg[i])
            for i in range(len(materiales))
        )

    # Restricciones
    restricciones = []

    for i in range(len(materiales)):
        # Relacion kg y precio
        restricciones.append({
            'type': 'eq',
            'fun': lambda x, i=i: produccion_inicial[materiales[i]] - (x[i]-precio_inicial[materiales[i]]) * elasticidad_kg[materiales[i]] / elasticidad_pesos[materiales[i]] - x[len(materiales) + i]
        })
        # Capacidad produccion
        restricciones.append({
            'type': 'ineq',
            'fun': lambda x, i=i: Capacidad_produccion[materiales[i]]*capacidad_maxima[materiales[i]] - x[len(materiales) + i]
        })
        # Precio final <= Precio inicial
        restricciones.append({
            'type': 'ineq',
            'fun': lambda x, i=i: precio_inicial[materiales[i]] - x[i]
        })
        # Produccion mínima
        restricciones.append({
            'type': 'ineq',
            'fun': lambda x, i=i: x[len(materiales) + i] - 0.1
        })

    # Resolver el problema
    solucion = minimize(objetivo, x0, constraints=restricciones, bounds=[(0, None)] * len(x0))

    # Mostrar resultados
    precio_final={}
    KG_Propuestos={}
    beneficio_esperado={}
    if solucion.success:
        print("Estado: Óptimo encontrado")
        precio_final_sol = solucion.x[:len(materiales)]
        kg_sol = solucion.x[len(materiales):]
        for i in range(len(materiales)):
            material = materiales[i]
            # st.write(f"Linea: {material}")
            # st.write(f"Precio final: {precio_final_sol[i]}")
            # st.write(f"Producción final (kg): {kg_sol[i]}")
            beneficio = precio_final_sol[i] - Costo_variable_KG[material] - (Costo_fijo_total[material] / kg_sol[i])
            # st.write(f"Beneficio: {beneficio}")
            # st.write()            
            
            precio_final[material] = precio_final_sol[i]
            KG_Propuestos[material] = kg_sol[i]
            beneficio_esperado[material] = beneficio

    else:
        st.write("No se encontró una solución óptima")
        return None,None,None
    
    return precio_final,    KG_Propuestos,    beneficio_esperado


def generar_dataframe_calculo_Kg(kg_producidos,kg_propuestos, Precio_venta, Costos_fijos, costo_variable,elasticidad_pesos,elasticidad_kg,precio_inicial,produccion_inicial,precio_analisis):
    """
        Genera un DataFrame con cálculos relacionados con la producción, precios de venta, costos y beneficios por kilogramo producido.

        Parámetros:
        - kg_producidos (int): Cantidad inicial de kilogramos producidos.
        - kg_propuestos (int): Cantidad propuesta de kilogramos a producir.
        - Precio_venta (float): Precio de venta del kilogramo.
        - Costos_fijos (float): Costos fijos totales.
        - costo_variable (float): Costo variable por kilogramo.
        - elasticidad_pesos (float): Elasticidad del precio en relación a la cantidad producida.
        - elasticidad_kg (float): Elasticidad de la cantidad producida en relación al precio.
        - precio_inicial (float): Precio inicial del kilogramo.
        - produccion_inicial (float): Producción inicial en kilogramos.
        - precio_analisis (float): Precio de análisis del kilogramo.

        Retorna:
        - df (pd.DataFrame): DataFrame con los siguientes cálculos por kilogramo:
            - 'KG producidos': Rango de kilogramos desde kg_producidos hasta kg_propuestos.
            - 'Precio de venta KG': Precio de venta calculado por kilogramo.
            - 'Costos fijos por KG': Costos fijos por kilogramo.
            - 'Costos variable por KG': Costos variables por kilogramo.
            - 'Costos totales por KG': Costos totales (fijos + variables) por kilogramo.
            - 'Beneficio por KG': Beneficio por kilogramo.
            - 'KG producidos_real': Precio de análisis repetido para cada kilogramo.
            - 'Beneficio analisis': Beneficio basado en el precio de análisis por kilogramo.
    """ 
    
    data = {
        'KG producidos':[x for x in range(kg_producidos, kg_propuestos)],
        'Precio de venta KG':[precio_inicial+elasticidad_pesos*((produccion_inicial-x)/elasticidad_kg) for x in range(kg_producidos, kg_propuestos) ],
        'Costos fijos por KG': [Costos_fijos / x for x in range(kg_producidos, kg_propuestos)],
        'Costos variable por KG': [costo_variable]*(-kg_producidos + kg_propuestos),
        'Costos totales por KG': [(Costos_fijos / kg) + costo_variable for kg in range(kg_producidos, kg_propuestos )],
        'Beneficio por KG': [Precio_venta - ((Costos_fijos / kg) + costo_variable) for kg in range(kg_producidos, kg_propuestos )],       
        'KG producidos_real':[precio_analisis]*(-kg_producidos + kg_propuestos),
        'Beneficio analisis': [precio_analisis - ((Costos_fijos / kg) + costo_variable) for kg in range(kg_producidos, kg_propuestos )],   
        }
    df = pd.DataFrame(data)

    return df