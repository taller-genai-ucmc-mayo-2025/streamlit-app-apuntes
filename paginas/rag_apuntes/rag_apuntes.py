import chromadb
import streamlit as st
from chromadb.utils import embedding_functions
from watsonx_connection import call_watsonx
import torch

#Esta linea previene que salga una advertencia en consola
#Por un error que tiene temporalmente Streamlit con Torch.
#No es obligatoria y no tiene relacion con la aplicacion
torch.classes.__path__ = [] 

st.write("## Realizar una consulta a un LLM que se soporta en los apuntes mas relevantes")

#Iniciar cliente para conectarse a la base de datos vectorial persistente
chroma_client = chromadb.PersistentClient(path="./chroma") 

# Realizar una consulta a un LLM que se soporta en los documentos mas relevantes
#Para esto, primero se verifica que Se verifica que exista la collecion con nombre 'apuntes' en la base de datos
lista_nombres_colecciones = [collection.name for collection in chroma_client.list_collections()]
if "apuntes" in lista_nombres_colecciones:
    st.write("En el siguiente espacio puedes escribir una pregunta para realizar a un LLM, el cual va a intentar resolverla teniendo en cuenta los 3 documentos (apuntes) más relevantes que esten almacenados en la base de datos vectorial.")
    texto_consulta_llm = st.text_input("Escribe tu consulta para el LLM",placeholder="Escribe tu consulta")

    boton_consulta_llm = st.button("Consultar al LLM")
    if boton_consulta_llm:
        #Primero se intentan extraer los 5 documentos mas relevantes para la pregunta de la base de datos vectorial
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
            query_texts = [texto_consulta_llm],
            n_results=3
        )

        #Se construye un string con cada uno de los apuntes
        #Se realiza un bucle para recorrer los documentos y mostrarlos
        string_apuntes = ""
        for index in range(len(documentos['ids'][0])):
            string_apuntes += f"Apunte {index+1}: {documentos['documents'][0][index]}\n\n"

        #Una vez se tiene un string con todos los apuntes relevantes se arma el prompt final para el modelo
        prompt_final = f'''Eres un asistente encargado de resolver preguntas del usuario basandote principalmente en los apuntes que se tienen guardados sobre el tema de la pregunta del usuario.

Tu objetivo es responder la pregunta del usuario basandote principalmente en la siguiente lista de apuntes, 
en caso de que en los apuntes no haya informacion que consideres relevante para resolver la pregunta del usuario 
entonces unicamente responde "No se encontraron apuntes relevantes para la pregunta"
 y mencionas cual fue la pregunta del usuario.

La lista de apuntes es la siguiente:\n
{string_apuntes}

La pregunta del usuario es la siguiente: {texto_consulta_llm}

Tu respuesta es:\n
'''

        #Se llama al modelo del lenguaje con el prompt creado:
        respuesta_llm = call_watsonx(prompt_final)
        
        #Una vez armado el prompt se muestra el prompt en la aplicacion para mostrar exactamente la consulta realizada
        with st.expander("📄 Prompt utilizado en la consulta", expanded=False):
            st.write(prompt_final)
        
        with st.expander("✨ Respuesta generada", expanded=True):
            st.write(respuesta_llm)


else:
    st.warning("No has agregado apuntes a la base de datos, por favor agregalos para poder realizar consultas en esta pestaña")