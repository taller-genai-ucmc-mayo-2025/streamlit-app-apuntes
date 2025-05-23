import chromadb
import streamlit as st
from chromadb.utils import embedding_functions
import torch

#Esta linea previene que salga una advertencia en consola
#Por un error que tiene temporalmente Streamlit con Torch.
#No es obligatoria y no tiene relacion con la aplicacion
torch.classes.__path__ = [] 

st.write("## Realizar una consulta sobre los documentos almacenados en la base de datos vectorial")

#Iniciar cliente para conectarse a la base de datos vectorial persistente
chroma_client = chromadb.PersistentClient(path="./chroma") 

#Paso 5: Consultar los documentos mas relevantes guardados en la base de datos vectorial
#Se verifica que exista la collecion con nombre 'apuntes' en la base de datos
lista_nombres_colecciones = [collection.name for collection in chroma_client.list_collections()]
if "apuntes" in lista_nombres_colecciones:
    st.write("En el siguiente espacio puedes escribir una frase o pregunta y posteriormente consultar cuales son los 10 documentos más cercanos en la base de datos a esa frase")
    texto_consulta = st.text_input("Escribe tu consultar para la base de datos",placeholder="Escribe tu consulta")

    boton_consulta = st.button("Realizar consulta a la base de datos")
    if boton_consulta:
        #Definir la funcion de embedding que se va a utilizar en la coleccion de la base de datos vectorial
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="ibm-granite/granite-embedding-278m-multilingual"
        )
        #Acceder a la coleccion
        collection_apuntes = chroma_client.get_collection(
            name="apuntes", 
            embedding_function=embedding_function
        )
        documentos = collection_apuntes.query(
            query_texts = [texto_consulta],
            n_results=10
        )

        #Se realiza un bucle para recorrer los documentos y mostrarlos
        for index in range(len(documentos['ids'][0])):
            with st.expander(f"_{documentos['ids'][0][index]}_. ↔️ Distancia respecto a la consulta: {documentos['distances'][0][index]}", expanded=False): 
                st.write(f"{documentos['documents'][0][index]}")

else:
    st.warning("No has agregado apuntes a la base de datos, por favor agregalos para poder realizar consultas en esta pestaña")