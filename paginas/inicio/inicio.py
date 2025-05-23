import streamlit as st

st.write("## ¡Hola! Esto es Apuntes App. 🔎📄✏️")

st.write("Apuntes App es una aplicación que te permite extraer tus apuntes a partir de imágenes y posteriormente consultarlos por medio de un LLM. ")

st.write("Apuntes App se compone de tres secciones:")

st.write("- **Agregar Apuntes**: En esta sección podrás _extraer_ tus apuntes a partir de imágenes y _almacenar_ el texto extraído en una base de datos vectorial. Podrás extraer apuntes de una sola imagen o de varias imágenes al mismo tiempo.")

st.write("- **Interacción con la base de datos vectorial**: En esta sección podrás _visualizar_ todos los apuntes que has guardado. También, en la pestaña _Realizar consulta a la bd_ podrás escribir una _consulta_ y ver cuales apuntes guardados son relevantes para ella.")

st.write("- **RAG**: En esta sección podrás realizar una pregunta sobre tus apuntes a un LLM, el cual intentará responderla basándose en los apuntes más relevantes que tengas guardados.")