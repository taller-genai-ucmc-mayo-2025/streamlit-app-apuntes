import chromadb
import streamlit as st
from chromadb.utils import embedding_functions
from watsonx_connection import call_watsonx_vision_model
import torch

#Esta linea previene que salga una advertencia en consola
#Por un error que tiene temporalmente Streamlit con Torch.
#No es obligatoria y no tiene relacion con la aplicacion
torch.classes.__path__ = [] 


#Iniciar cliente para conectarse a la base de datos vectorial persistente
chroma_client = chromadb.PersistentClient(path="./chroma")

#Se inicializan variables de la sesion que son necesarias para la aplicación
if "imagenes_apuntes" not in st.session_state:
    st.session_state["imagenes_apuntes"] = None

if "lista_textos_extraidos" not in st.session_state:
    st.session_state["lista_textos_extraidos"] = None

if "lista_identificadores" not in st.session_state:
    st.session_state["lista_identificadores"] = None

#Se define una funcion que ayuda a restablecer el valor de las variables de sesion cuando sea necesario
def restablecer_session_state_variables():
    if "imagenes_apuntes" in st.session_state:
        st.session_state["imagenes_apuntes"] = None

    if "lista_textos_extraidos" in st.session_state:
        st.session_state["lista_textos_extraidos"] = None

    if "lista_identificadores" in st.session_state:
        st.session_state["lista_identificadores"] = None

#Mensaje al inicio de la pagina
st.markdown("## Paso a paso para agregar varios apuntes")

#Titulo del paso 1
st.markdown("### Paso 1: Sube las imagenes de los apuntes")
uploaded_files = st.file_uploader("Elige un archivo", ["jpg","jpeg","png"], accept_multiple_files=True)
if uploaded_files is not None:
    #Asignar la variable de estado para mantener la imagen durante la sesion del usuario
    st.session_state["imagenes_apuntes"] = uploaded_files

    #Leer los bytes de cada archivo subido y mostrarla
    #TODO Mejorar visualizacion
    for imagen in st.session_state["imagenes_apuntes"]:
        with st.expander(f"Visualizar imagen _{imagen.name}_", expanded=False): 
            st.image(imagen)

else:
    #Si no hay imagenes subidas, entonces se restablece el valor las variables de estado
    #Esto para prevenir que queden guardados resultados de otras imagenes
    restablecer_session_state_variables()

#Paso 2: Extraer el texto de las imagenes subidas
#Antes de habilitar este paso primero se verifica que hayan imagenes subidas
if st.session_state["imagenes_apuntes"]:
    #Titulo del paso 2
    st.markdown("### Paso 2: Extraer el texto de las imagenes subidas")
    #Boton para extraer el texto de todas las imagenes subidas
    boton_extraer_texto_imagenes = st.button("Extraer texto de las imagenes")
    if boton_extraer_texto_imagenes:
        lista_temporal_textos_extraidos = []
        for imagen in st.session_state["imagenes_apuntes"]:
            #Llamar a watson para extraer el texto y mostrar el texto extraido
            texto_extraido = call_watsonx_vision_model(imagen)
            lista_temporal_textos_extraidos.append(texto_extraido)
        
        st.session_state["lista_textos_extraidos"] = lista_temporal_textos_extraidos
    
    if st.session_state["lista_textos_extraidos"]:
        for index in range(len(st.session_state["lista_textos_extraidos"])):
            with st.expander(f"Texto extraido de la imagen _{st.session_state['imagenes_apuntes'][index].name}_", expanded=False): 
                st.write(st.session_state["lista_textos_extraidos"][index])


#Paso 3: Ingresar el identificador con el que se quiere guardar cada texto extraido anteriormente
if st.session_state["lista_textos_extraidos"]:
    #Titulo del paso 3
    st.markdown("### Paso 3: Ingresar un indentificador para cada apunte que se va a almacenar")
    lista_temporal_identificadores = []
    for imagen in st.session_state["imagenes_apuntes"]:
        st.write("Escribe un identificador para cada uno de los apuntes extraidos de las imagenes:")
        identificador = st.text_input(f"Identificador para los apuntes extraidos de la imagen {imagen.name}",placeholder="MisApuntes")
        lista_temporal_identificadores.append(identificador)

    st.session_state["lista_identificadores"] = lista_temporal_identificadores

#Paso 4: Almacenar todos los textos extraidos en la base de datos vectorial
if st.session_state["lista_identificadores"]:
    boton_almacenar_embedding = st.button("Almacenar texto en la base de datos vectorial")
    if boton_almacenar_embedding:
        #Definir la funcion de embedding que se va a utilizar en la coleccion de la base de datos vectorial
        embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="ibm-granite/granite-embedding-278m-multilingual"
        )

        #Crear o acceder a la coleccion de la base de datos vectorial donde se van a tener los apuntes
        #Se define la funcion de embedding que se va a usar en los documentos de la coleccion
        collection_apuntes = chroma_client.get_or_create_collection(
            name="apuntes", 
            embedding_function=embedding_function
        )

        #Se agregan los textos y los identificadores creados
        collection_apuntes.add(
            ids=st.session_state["lista_identificadores"],
            documents=st.session_state["lista_textos_extraidos"]
        )

        #Si todo el proceso fue exitoso se pone un texto informativo en la pantalla
        st.success("Los textos fueron almacenados correctamente. \n\n- Para visualizar los apuntes guardados puedes ir a la pestaña 'Visualizar documentos guardados'. \n\n- Para subir otro apunte puedes: \n\n  - Subir otras imagenes en esta pestaña. \n\n  - Ir a la sección 'Agregar un apunte' para subir un solo apunte.")
