
import streamlit as st
import pandas as pd
import unicodedata
import os

st.set_page_config(page_title="Revision de Bioslis", layout="wide")

st.title("Revision de Bioslis")

# Rutas esperadas de los archivos (deben estar en la raíz del repo)
path_bioslis = "bioslis.xlsx"
path_siel = "EXAMENES_SIEL.xlsx"

# Función para normalizar texto
def normalizar(col):
    return col.str.upper().apply(lambda x: unicodedata.normalize("NFKD", x).encode("ASCII", "ignore").decode("utf-8"))

# Función para normalizar nombres de columnas
def normalizar_columnas(df):
    df.columns = [unicodedata.normalize("NFKD", col).encode("ASCII", "ignore").decode("utf-8").strip().upper() for col in df.columns]
    return df

# Verifica que los archivos existan antes de continuar
if not os.path.exists(path_bioslis) or not os.path.exists(path_siel):
    st.error("❌ No se encontraron los archivos Excel requeridos en el repositorio.")
    st.markdown("Asegúrate de que `bioslis.xlsx` y `EXAMENES_SIEL.xlsx` estén en el mismo directorio que este archivo .py")
else:
    df_bioslis = pd.read_excel(path_bioslis)
    df_siel = pd.read_excel(path_siel)

    # Normalizar columnas
    df_bioslis = normalizar_columnas(df_bioslis)
    df_siel = normalizar_columnas(df_siel)

    # Asegurar tipos y contenido limpio
    df_bioslis["CODIGO EXAMEN"] = df_bioslis["CODIGO EXAMEN"].astype(str)
    df_siel["NUMERO"] = df_siel["NUMERO"].astype(str)

    if "EXAMEN" in df_bioslis.columns:
        df_bioslis["EXAMEN"] = normalizar(df_bioslis["EXAMEN"])
    if "NOMBRE EXAMEN" in df_siel.columns:
        df_siel["NOMBRE EXAMEN"] = normalizar(df_siel["NOMBRE EXAMEN"])

    # Vista previa de ambos archivos
    st.subheader("📄 Vista previa de BIOSLIS")
    st.dataframe(df_bioslis.head())

    st.subheader("📄 Vista previa de SIEL")
    st.dataframe(df_siel.head())

    # Comparación por códigos de examen
    if "CODIGO EXAMEN" in df_bioslis.columns and "NUMERO" in df_siel.columns:
    if "CODIGO EXAMEN" in df_bioslis.columns and "NUMERO" in df_siel.columns:
        st.header("📌 Comparación: BIOSLIS vs SIEL (por CÓDIGO EXAMEN)")
        codigos_bioslis = set(df_bioslis["CODIGO EXAMEN"])
        codigos_siel = set(df_siel["NUMERO"])

        en_bioslis_no_en_siel = df_bioslis[~df_bioslis["CODIGO EXAMEN"].isin(codigos_siel)]
        en_siel_no_en_bioslis = df_siel[~df_siel["NUMERO"].isin(codigos_bioslis)]

        conteo = {
            "Solo en BIOSLIS": len(en_bioslis_no_en_siel),
        "Solo en SIEL": len(en_siel_no_en_bioslis),
    }
        st.bar_chart(pd.Series(conteo))

        col1, col2 = st.columns(2)
    with col1:
        if st.checkbox("🔍 Ver BIOSLIS no presentes en SIEL"):
    st.subheader("BIOSLIS no presentes en SIEL")
        st.subheader("BIOSLIS no presentes en SIEL")
        st.dataframe(en_bioslis_no_en_siel, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", en_bioslis_no_en_siel.to_csv(index=False), file_name="en_bioslis_no_en_siel.csv")
        st.dataframe(en_bioslis_no_en_siel, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", en_bioslis_no_en_siel.to_csv(index=False), file_name="no_en_siel.csv")

    with col2:
        if st.checkbox("🔍 Ver SIEL no presentes en BIOSLIS"):
    st.subheader("SIEL no presentes en BIOSLIS")
        st.subheader("SIEL no presentes en BIOSLIS")
        st.dataframe(en_siel_no_en_bioslis, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", en_siel_no_en_bioslis.to_csv(index=False), file_name="en_siel_no_en_bioslis.csv")
        st.dataframe(en_siel_no_en_bioslis, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", en_siel_no_en_bioslis.to_csv(index=False), file_name="no_en_bioslis.csv")

    # Comparación LABORATORIO vs SECCION
    st.header("⚙️ Comparación: LABORATORIO BIOSLIS vs SECCION SIEL")
    if "LABORATORIO" in df_bioslis.columns and "SECCION" in df_siel.columns:
        labs_bioslis = set(df_bioslis["LABORATORIO"])
        secciones_siel = set(df_siel["SECCION"])

        no_en_siel = df_bioslis[~df_bioslis["LABORATORIO"].isin(secciones_siel)]
        no_en_bioslis = df_siel[~df_siel["SECCION"].isin(labs_bioslis)]

        st.metric("LABORATORIOS no presentes en SIEL", len(no_en_siel))
        st.metric("SECCIONES de SIEL no presentes en BIOSLIS", len(no_en_bioslis))

        if st.checkbox("🔍 Ver LABORATORIOS no presentes en SIEL"):
    st.subheader("LABORATORIOS no presentes en SIEL")
        st.subheader("LABORATORIOS no presentes en SIEL")
        st.dataframe(no_en_siel, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", no_en_siel.to_csv(index=False), file_name="no_en_siel.csv")
        st.dataframe(no_en_siel, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", no_en_siel.to_csv(index=False), file_name="lab_no_en_siel.csv")

        if st.checkbox("🔍 Ver SECCIONES de SIEL no presentes en BIOSLIS"):
    st.subheader("SECCIONES no presentes en BIOSLIS")
        st.subheader("SECCIONES no presentes en BIOSLIS")
        st.dataframe(no_en_bioslis, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", no_en_bioslis.to_csv(index=False), file_name="no_en_bioslis.csv")
        st.dataframe(no_en_bioslis, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", no_en_bioslis.to_csv(index=False), file_name="seccion_no_en_bioslis.csv")
    else:
        st.warning("⚠️ Las columnas 'LABORATORIO' o 'SECCION' no están presentes en los archivos.")

    # Comparación SECCION vs AREA DE TRABAJO
    st.header("📁 Comparación: SECCION BIOSLIS vs AREA DE TRABAJO SIEL")
    if "SECCION" in df_bioslis.columns and "AREA DE TRABAJO" in df_siel.columns:
        secciones_bioslis = set(df_bioslis["SECCION"])
        areas_siel = set(df_siel["AREA DE TRABAJO"])

        no_en_siel = df_bioslis[~df_bioslis["SECCION"].isin(areas_siel)]
        no_en_bioslis = df_siel[~df_siel["AREA DE TRABAJO"].isin(secciones_bioslis)]

        st.metric("SECCIONES no presentes en SIEL", len(no_en_siel))
        st.metric("ÁREAS de SIEL no presentes en BIOSLIS", len(no_en_bioslis))

        if st.checkbox("🔍 Ver SECCIONES de BIOSLIS no presentes en SIEL"):
    st.subheader("SECCIONES no presentes en SIEL")
        st.subheader("SECCIONES no presentes en SIEL")
        st.dataframe(no_en_siel, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", no_en_siel.to_csv(index=False), file_name="no_en_siel.csv")
        st.dataframe(no_en_siel, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", no_en_siel.to_csv(index=False), file_name="seccion_no_en_siel.csv")

        if st.checkbox("🔍 Ver ÁREAS DE TRABAJO no presentes en BIOSLIS"):
    st.subheader("ÁREAS DE TRABAJO no presentes en BIOSLIS")
        st.subheader("ÁREAS DE TRABAJO no presentes en BIOSLIS")
        st.dataframe(no_en_bioslis, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", no_en_bioslis.to_csv(index=False), file_name="no_en_bioslis.csv")
        st.dataframe(no_en_bioslis, use_container_width=True, height=600)
        st.download_button("⬇️ Descargar", no_en_bioslis.to_csv(index=False), file_name="area_no_en_bioslis.csv")
    else:
        st.warning("⚠️ Las columnas 'SECCION' o 'AREA DE TRABAJO' no están presentes en los archivos.")