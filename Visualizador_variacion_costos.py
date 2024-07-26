from plotly.subplots import make_subplots
import plotly.graph_objs as go
import streamlit as st
import pandas as pd
from openpyxl.styles import PatternFill

class CLS_Visualizacion_variacion_costos:
    '''
    clase que permite tener todas las particularidades necesarias
      para la visualización del los costos y sus variaciones
    '''
    def __init__(self) -> None:
        self.pagina_principal('Variacion de costos')

    def pagina_principal(self, titulo):
        st.title(titulo)

        df=self.habilitar_carga_datos('Carga aca el dfaa')
        # self.create_waterfall(df)

    def habilitar_carga_datos(self,mensaje):
        '''
        Habilita el boton de carga de archivos y retorna un df con la información del archivo cargado
        '''
        data_file = st.file_uploader(mensaje, type=["XLSX"]) 
        if data_file is not None:
            df=pd.read_excel(data_file) 
            self.cascada3(df[df['Mes'] != 'Enero'])
            return        df
        
    def create_waterfall(self,df):
        # Agrupar por mes y sumar los costos por elemento
        df_grouped = df.groupby(['Mes', 'Costo por Elemento'])['Costo total'].sum().reset_index()
        
        # Crear una lista para las categorías del eje x (mes y elemento)
        categories = []
        for mes in df['Mes'].unique():
            categories.extend(df_grouped[df_grouped['Mes'] == mes]['Costo por Elemento'].tolist())
            categories.append(f"Total {mes}")
        
        # Crear listas para los valores del diagrama de cascada
        y_values = []
        y_text = []
        total_previous_month = 0
        
        for mes in df['Mes'].unique():
            df_mes = df_grouped[df_grouped['Mes'] == mes]
            total_mes = df_mes['Costo total'].sum()
            
            for _, row in df_mes.iterrows():
                y_values.append(row['Costo por Elemento'])
                y_text.append(f"{row['Costo por Elemento']} ({mes})")
            
            y_values.append(total_mes - total_previous_month)
            y_text.append(f"Total {mes}")
            
            total_previous_month = total_mes
        
        # Crear el gráfico de cascada con Plotly
        fig = go.Figure(go.Waterfall(
            x=categories,
            y=y_values,
            text=y_text,
            measure=["relative" if "Total" not in x else "total" for x in categories]
        ))
        
        fig.update_layout(title="Diagrama de Cascada de Costos por Elemento y Mes",
                        xaxis_title="Mes y Elemento",
                        yaxis_title="Costo",
                        showlegend=False)
        
        st.plotly_chart(fig)

    def cascada2(self,df):
        import numpy as np
        import plotly.express as px
        import waterfall_chart
        concepto = ['Ingresos publicidad', 'Ingresos cuotas', 'Gastos fijos', 'Gastos variables', 'Impuestos']
        cantidad = [12023, 3012, -8443, -1324, -1239]

        waterfall_chart.plot(concepto, cantidad)

        data = pd.DataFrame({'Concepto': concepto, 'Cantidad': cantidad})

        # Título de la aplicación
        st.title("Gráfico de Barras de Conceptos y Cantidades")

        # Crear el gráfico de barras con Plotly
        fig = px.bar(data, x='Concepto', y='Cantidad', title="Gráfico de Barras", labels={'Cantidad':'Cantidad', 'Concepto':'Concepto'}, text='Cantidad')

        # Mostrar el gráfico de barras en Streamlit
        st.plotly_chart(fig)

    def cascada3(self,df):
        ''' debe recibir el df filtrado, es decir el mes inicial y sus gastos y el resto de meses con sus gastos'''

        df_grouped = df.groupby(['Mes', 'Costo por Elemento'])['Costo total'].sum().reset_index()
        
        df_totales_por_mes=df_grouped.groupby(['Mes'])['Costo total'].sum().reset_index()
        df_grouped=df_grouped[df_grouped['Mes'] != 'Febrero']
        #eliminaria de mi df_group los meses que no necesito
        df_costos_por_elemento=df_grouped.groupby(['Costo por Elemento'])['Costo total'].sum().reset_index()
        categorias = df_costos_por_elemento['Costo por Elemento'].tolist()
        valores = df_costos_por_elemento['Costo total'].tolist()

        mes_anterior=df_totales_por_mes[df_totales_por_mes['Mes'] == 'Febrero']['Costo total'][0]
        valores.insert(0, mes_anterior)
        categorias.insert(0, 'Febrerot')
        valores.append(sum(valores))
        categorias.append('Marzot')

        # Agregar el total manualmente

        # Crear el diagrama de cascada
        fig = go.Figure(go.Waterfall(
            x=categorias,
            y=valores,
            measure=["relative"] * len(valores[:-1]) + ["total"],  # Los últimos datos son 'total'
            text=[str(i) for i in valores],
            textposition="outside",
            connector={"line": {"color": "rgb(63, 63, 63)"}}
        ))
        fig.update_layout(
            title="Diagrama de Cascada",
            showlegend=False,
            # yaxis=dict(
            #     title='Valor',
            #     rangemode='fixed',  # Mantener el rango fijo
            #     range=[300000000, 400000000000]  # Ajusta el rango del eje Y para controlar la altura
            # )
        )

        # # # Mostrar el gráfico
        st.plotly_chart(fig)