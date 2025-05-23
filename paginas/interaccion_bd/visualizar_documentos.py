import chromadb
from chromadb.utils import embedding_functions
import streamlit as st
import torch

#Esta linea previene que salga una advertencia en consola
#Por un error que tiene temporalmente Streamlit con Torch.
#No es obligatoria y no tiene relacion con la aplicacion
torch.classes.__path__ = [] 

st.write("## Visualizar los documentos almacenados en la base de datos vectorial")

#Iniciar cliente para conectarse a la base de datos vectorial persistente
chroma_client = chromadb.PersistentClient(path="./chroma") 

#Se verifica que exista la collecion con nombre 'apuntes' en la base de datos
lista_nombres_colecciones = [collection.name for collection in chroma_client.list_collections()]
if "apuntes" in lista_nombres_colecciones:
    st.write("Pulsando en el siguiente boton se pueden visualizar los documentos guardados en la base de datos")

    boton_ver_coleccion = st.button("Ver documentos en la coleccion")
    if boton_ver_coleccion:
        #Definir la funcion de embedding que se va a utilizar en la coleccion de la base de datos vectorial
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="ibm-granite/granite-embedding-278m-multilingual"
        )
        #Acceder a la coleccion
        collection_apuntes = chroma_client.get_collection(
            name="apuntes", 
            embedding_function=embedding_function
        )
        documentos = collection_apuntes.get()
        
        #Se realiza un bucle para recorrer los documentos y mostrarlos
        for index in range(len(documentos['ids'])):
            with st.expander(f"_{documentos['ids'][index]}_", expanded=False): 
                st.write(documentos['documents'][index])

else:
    st.warning("No has agregado apuntes a la base de datos, por favor agregalos para poder visualizarlos en esta pestaña")