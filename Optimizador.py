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
    
    return precio_final,    KG_Propuestos,    beneficio_esperado


def generar_dataframe_calculo_Kg(kg_producidos,kg_propuestos, Precio_venta, Costos_fijos, costo_variable):
    if (kg_producidos> kg_propuestos*0.5):
        kg_producidos=int(kg_propuestos*0.5)
        st.write('condicional')
    data = {
        'KG producidos': [x for x in range(kg_producidos, kg_propuestos)],
        'Precio de venta KG': [Precio_venta]*(-kg_producidos + kg_propuestos),
        'Costos fijos por KG': [Costos_fijos / x for x in range(kg_producidos, kg_propuestos)],
        'Costos variable por KG': [costo_variable]*(-kg_producidos + kg_propuestos),
        'Costos totales por KG': [(Costos_fijos / kg) + costo_variable for kg in range(kg_producidos, kg_propuestos )],
        'Beneficio por KG': [Precio_venta - ((Costos_fijos / kg) + costo_variable) for kg in range(kg_producidos, kg_propuestos )]
    }
    df = pd.DataFrame(data)

    return df