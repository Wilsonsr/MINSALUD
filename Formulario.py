import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -------- Configuración inicial --------
st.set_page_config(page_title="Formulario Gestión THS", layout="centered")

# -------- Estilos CSS --------
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab"] {
        background-color: #e6f7ff;
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
        margin-right: 5px;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #004d99;
        color: #ffffff;
    }

    .stButton button {
        background-color: #004d99;
        color: #ffffff;
        font-weight: bold;
        padding: 8px 16px;
        border-radius: 10px;
    }

    .stButton button:hover {
        background-color: #0073e6;
    }

    .required-field::after {
        content: " *";
        color: red;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
### **Formulario de Captura de Gestión Territorial del THS**
> Esta aplicación es una demostración técnica.  
> Los campos marcados con **(*)** son obligatorios.
""")

# -------- Cargar municipios y departamentos --------
try:
    municipios_df = pd.read_excel("DIVIPOLA_Municipios.xlsx")
    if "Nombre Departamento" not in municipios_df.columns or "Nombre Municipio" not in municipios_df.columns:
        st.error("El archivo no tiene las columnas esperadas ('Nombre Departamento' y 'Nombre Municipio').")
        st.stop()
    
    departamentos = municipios_df["Nombre Departamento"].drop_duplicates().sort_values()

except FileNotFoundError:
    st.error("Error: No se encontró el archivo 'DIVIPOLA_Municipios.xlsx'. Verifica que esté en la misma carpeta que este script.")
    st.stop()

# -------- Selección de Departamento y Municipio --------
departamento = st.selectbox("Seleccione el departamento *", departamentos)
municipios_filtrados = municipios_df[municipios_df["Nombre Departamento"] == departamento]["Nombre Municipio"].sort_values().tolist()
municipio = st.selectbox("Municipio *", municipios_filtrados)

nombre_responsable = st.text_input("Nombre de quien diligencia *")
fecha = datetime.today().strftime('%Y-%m-%d')

st.markdown("---")

# -------- Inicialización de errores --------
errores = []

# -------- Pestañas --------
tabs = st.tabs([
    "Despacho", 
    "Planeación", 
    "Seguridad Social", 
    "Sistemas de Información",
    "CRUE", 
    "Salud Pública", 
    "Laboratorio", 
    "Fondo Rotatorio", 
    "Otra Dependencia"
])

# -------- Pestaña: Despacho --------
with tabs[0]:
    st.subheader("Despacho del Secretario/a de Salud")
    ths_despacho = st.number_input("Número de THS en Despacho *", min_value=0, step=1)
    if ths_despacho == 0:
        errores.append("El campo 'Número de THS en Despacho' es obligatorio.")

# ---- Pestaña: Oficina de Planeación ----
with tabs[1]:
    st.subheader("Oficina de Planeación")
    ths_planeacion = st.number_input("Número de THS en Planeación *", min_value=0, step=1)
    if ths_planeacion == 0:
        errores.append("El campo 'Número de THS en Planeación' es obligatorio.")

# ---- Pestaña: Seguridad Social ----
with tabs[2]:
    st.subheader("Dirección de Seguridad Social y Aseguramiento")
    ths_seguridad = st.number_input("Número de THS en Seguridad Social *", min_value=0, step=1)
    if ths_seguridad == 0:
        errores.append("El campo 'Número de THS en Seguridad Social' es obligatorio.")

# ---- Pestaña: Sistemas de Información ----
with tabs[3]:
    st.subheader("Grupo de Sistemas de Información")
    ths_sistemas = st.number_input("Número de THS en Sistemas *", min_value=0, step=1)
    if ths_sistemas == 0:
        errores.append("El campo 'Número de THS en Sistemas' es obligatorio.")

# -------- Pestaña: CRUE --------
with tabs[4]:
    st.subheader("Centro Regulador de Urgencias y Emergencias (CRUE)")
    ths_crue = st.number_input("Número de THS en CRUE *", min_value=0, step=1)
    otros_crue = st.number_input("Número de otros trabajadores en CRUE", min_value=0, step=1)
    if ths_crue == 0:
        errores.append("El campo 'Número de THS en CRUE' es obligatorio.")

# -------- Pestaña: Salud Pública --------
with tabs[5]:
    st.subheader("Salud Pública")

    st.markdown("**Vigilancia en Salud Pública**")
    ths_vigilancia = st.number_input("Número de THS en Vigilancia *", min_value=0, step=1)
    if ths_vigilancia == 0:
        errores.append("El campo 'Número de THS en Vigilancia' es obligatorio.")

    st.markdown("**Acciones Programáticas**")
    ths_acciones = st.number_input("Número de THS en Acciones *", min_value=0, step=1)
    if ths_acciones == 0:
        errores.append("El campo 'Número de THS en Acciones' es obligatorio.")

    st.markdown("**Plan de Intervenciones Colectivas**")
    ths_plan = st.number_input("Número de THS en Intervenciones *", min_value=0, step=1)
    if ths_plan == 0:
        errores.append("El campo 'Número de THS en Intervenciones' es obligatorio.")

# -------- Pestaña: Laboratorio --------
with tabs[6]:
    st.subheader("Laboratorio Departamental de Salud Pública")
    ths_lab = st.number_input("THS en Laboratorio *", min_value=0, step=1)
    if ths_lab == 0:
        errores.append("El campo 'THS en Laboratorio' es obligatorio.")

# -------- Pestaña: Fondo Rotatorio --------
with tabs[7]:
    st.subheader("Fondo Rotatorio de Estupefacientes")
    fondo_rotatorio = st.number_input("Número de trabajadores en Fondo Rotatorio *", min_value=0, step=1)
    if fondo_rotatorio == 0:
        errores.append("El campo 'Número de trabajadores en Fondo Rotatorio' es obligatorio.")

# -------- Pestaña: Otra Dependencia --------
with tabs[8]:
    st.subheader("Otra Dependencia")
    otra_dependencia = st.text_input("Otra área o dependencia (opcional)")

st.markdown("---")

# -------- Botón de Envío con Validación --------
if st.button("Guardar Información"):
    if errores:
        for error in errores:
            st.error(error)
    else:
        st.success("Información registrada correctamente.")
        # Crear un DataFrame con los datos ingresados
        data = {
            "Fecha": [fecha],
            "Departamento": [departamento],
            "Municipio": [municipio],
            "Nombre Responsable": [nombre_responsable],
            "Despacho": [ths_despacho],
            "Planeación": [ths_planeacion],
            "Seguridad Social": [ths_seguridad],
            "Sistemas de Información": [ths_sistemas],
            "CRUE": [ths_crue],
            "Otros CRUE": [otros_crue],
            "Vigilancia en Salud Pública": [ths_vigilancia],
            "Acciones Programáticas": [ths_acciones],
            "Plan de Intervenciones Colectivas": [ths_plan],
            "Laboratorio Departamental": [ths_lab],
            "Fondo Rotatorio": [fondo_rotatorio],
            "Otra Dependencia": [otra_dependencia]
        } 
        df = pd.DataFrame(data)

        # Definir ruta del archivo
        archivo_csv = "captura_ths.csv"

        # Verificar si el archivo ya existe
        if os.path.exists(archivo_csv):
            # Si existe, agregar sin sobrescribir (modo 'a')
            df.to_csv(archivo_csv, mode='a', header=False, index=False)
        else:
            # Si no existe, crear el archivo con los encabezados
            df.to_csv(archivo_csv, mode='w', header=True, index=False)

        st.success(f"Los datos han sido guardados en {archivo_csv}")