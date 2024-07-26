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

        df=self.habilitar_carga_datos('Carga aca el df')
        st.write('df')
        st.write(df)

    def habilitar_carga_datos(self,mensaje):
        '''
        Habilita el boton de carga de archivos y retorna un df con la información del archivo cargado
        '''
        data_file = st.file_uploader(mensaje, type=["XLSX"]) 
        if data_file is not None:
            return pd.read_excel(data_file)