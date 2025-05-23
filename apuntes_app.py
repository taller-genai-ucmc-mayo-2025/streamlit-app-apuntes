import streamlit as st
import torch

#Esta linea previene que salga una advertencia en consola
#Por un error que tiene temporalmente Streamlit con Torch.
#No es obligatoria y no tiene relacion con la aplicacion
torch.classes.__path__ = [] 

#Definir las páginas que va a tener la aplicacion
inicio_page = st.Page(page='paginas/inicio/inicio.py', title='Inicio', icon='🏠')
agregar_individual_page = st.Page(page='paginas/agregar_apuntes/agregar_individual.py', title='Agregar un apunte', icon='📗')
agregar_varios_page = st.Page(page='paginas/agregar_apuntes/agregar_varios.py', title='Agregar varios apuntes', icon='📚')
visualizar_documentos_page = st.Page(page='paginas/interaccion_bd/visualizar_documentos.py', title='Visualizar documentos guardados', icon='📖')
realizar_consulta_bd_page = st.Page(page='paginas/interaccion_bd/realizar_consulta_bd.py', title='Realizar consulta a la bd', icon='📑')
rag_apuntes_page = st.Page(page='paginas/rag_apuntes/rag_apuntes.py', title='RAG sobre los apuntes', icon='🔍')

#Indicar cuales paginas existen en la aplicacion para que sean incluidas en la barra de navegacion
pg = st.navigation(
    {
        "Inicio": [inicio_page],
        "Agregar Apuntes": [agregar_individual_page, agregar_varios_page],
        "Interacción con la base de datos vectorial": [visualizar_documentos_page,realizar_consulta_bd_page],
        "RAG": [rag_apuntes_page]
    }
)

pg.run()