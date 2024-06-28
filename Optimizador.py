import numpy as np
from scipy.optimize import minimize
import streamlit as st

def optimizar():
    # Definir datos (estos valores deben ser proporcionados para cada material)
    materiales = ['Chorizos', 'material_2']

    # Parámetros (deben ser diccionarios indexados por materiales)
    Costo_variable_KG = {'Chorizos': 10341, 'material_2': 3}
    Costo_fijo_total = {'Chorizos': 4981461166, 'material_2': 150}
    Capacidad_produccion = {'Chorizos': 770879, 'material_2': 600}
    precio_inicial = {'Chorizos': 35096, 'material_2': 15}
    produccion_inicial = {'Chorizos': 691245, 'material_2': 450}
    elasticidad_pesos = {'Chorizos': 1, 'material_2': 0.3}
    elasticidad_kg = {'Chorizos': 400, 'material_2': 0.8}
    capacidad_maxima=1

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
            'fun': lambda x, i=i: Capacidad_produccion[materiales[i]]*capacidad_maxima - x[len(materiales) + i]
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
    if solucion.success:
        print("Estado: Óptimo encontrado")
        precio_final_sol = solucion.x[:len(materiales)]
        kg_sol = solucion.x[len(materiales):]
        for i in range(len(materiales)):
            material = materiales[i]
            st.write(f"Linea: {material}")
            st.write(f"Precio final: {precio_final_sol[i]}")
            st.write(f"Producción final (kg): {kg_sol[i]}")
            beneficio = precio_final_sol[i] - Costo_variable_KG[material] - (Costo_fijo_total[material] / kg_sol[i])
            st.write(f"Beneficio: {beneficio}")
            st.write()
    else:
        st.write("No se encontró una solución óptima.")
