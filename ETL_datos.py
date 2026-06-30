import pandas as pd
import numpy as np
import streamlit as st

GSHEET_URL = "https://docs.google.com/spreadsheets/d/1R4IelEYRFWRhuJWX2eYxpQT3zdbIFVX3/export?format=csv&gid=818503085"

@st.cache_data(ttl=3600)
def load_and_clean_data(url=GSHEET_URL):
    df = pd.read_csv(url)
    
    def clean_group(val):
        if pd.isna(val):
            return "No Registrado"
        val_str = str(val).strip()
        val_upper = val_str.upper()
        if "LING" in val_upper:
            return "Lingüística Aplicada - ILA"
        elif "CURR" in val_upper:
            return "Educación y Currículo"
        elif "GICMOS" in val_upper:
            return "GICMOS"
        return val_str
        
    df['Grupo de Investigación Clean'] = df['Grupo de Investigación'].apply(clean_group)
    
    def clean_typology(val):
        if pd.isna(val):
            return "No Registrado"
        val_str = str(val).strip().upper()
        if "RECURSO" in val_str or "HUMANO" in val_str or "CTEL" in val_str:
            return "Formación de Recurso Humano CTeI"
        elif "NUEVO" in val_str or "NUEVOS" in val_str or "GENERACION" in val_str or "GENERACI" in val_str:
            return "Generación de Nuevo Conocimiento"
        elif "APROPIACION" in val_str or "APROPIACI" in val_str or "SOCIAL" in val_str or "DIVULGACI" in val_str:
            return "Apropiación Social del Conocimiento"
        elif "TECNOLO" in val_str or "DESARROLLO" in val_str or "INNOVACI" in val_str:
            return "Desarrollo Tecnológico e Innovación"
        elif "ARTICULO" in val_str:
            return "Artículo Científico"
        elif "POSTER" in val_str:
            return "Póster / Evento"
        elif "PONENTE" in val_str:
            return "Ponente / Evento"
        if len(val_str) > 50:
            return val_str[:50] + "..."
        return val_str.title()
        
    df['Tipología Clean'] = df['Tipología'].apply(clean_typology)
    
    def clean_subcategory(val):
        if pd.isna(val):
            return "No Registrado"
        val_str = str(val).replace('_', ' ').strip().title()
        if "Inicial" in val_str:
            return "Formación Inicial"
        if "Avanzada" in val_str:
            return "Formación Avanzada"
        if "Cientifica" in val_str or "Científica" in val_str:
            if "Editorial" in val_str:
                return "Producción Editorial Científica"
            return "Producción Científica"
        if "Circulacion" in val_str or "Circulación" in val_str:
            return "Circulación de Conocimiento Especializado"
        if "Transferencia" in val_str:
            return "Transferencia y Asesoría Técnica"
        return val_str
        
    df['Subcategoría Clean'] = df['Subcategoría'].apply(clean_subcategory)
    
    def clean_state(val):
        if pd.isna(val):
            return "No Registrado"
        val_str = str(val).strip().upper()
        if "APROBADO" in val_str or "APROBADA" in val_str:
            if "MENCI" in val_str:
                return "Aprobado con Mención"
            return "Aprobado"
        if "REPROBADA" in val_str or "REPROBADO" in val_str:
            return "Reprobado"
        if "COTERMINAL" in val_str:
            return "Coterminal"
        if "SIN SUSTENTAR" in val_str:
            return "Sin Sustentar"
        return val_str.title()
        
    df['Estado Clean'] = df['Estado'].apply(clean_state)
    
    def clean_link(val):
        if pd.isna(val):
            return ""
        val_str = str(val).strip()
        if val_str.startswith("10."):
            return f"https://doi.org/{val_str}"
        if val_str.startswith("http"):
            return val_str
        return ""
        
    df['Enlace Clean'] = df['DOI / Link'].apply(clean_link)
    
    df['Año Clean'] = pd.to_numeric(df['Año'], errors='coerce').fillna(0).astype(int)
    
    def extract_authors(row):
        authors = []
        if pd.notna(row['Director / Investigador Principal']):
            d = str(row['Director / Investigador Principal']).strip().title()
            if d and d not in ['N/A', 'Nan', 'None', '-']:
                authors.append((d, "Director/Investigador"))
        if pd.notna(row['Codirector']):
            c = str(row['Codirector']).strip().title()
            if c and c not in ['N/A', 'Nan', 'None', '-']:
                authors.append((c, "Codirector"))
        for i in range(1, 11):
            col_name = f'Autor/Estudiante {i}'
            if col_name in row and pd.notna(row[col_name]):
                a = str(row[col_name]).strip().title()
                if a and a not in ['N/A', 'Nan', 'None', '-']:
                    authors.append((a, "Estudiante/Autor"))
        return authors

    df['Autores Detalle'] = df.apply(extract_authors, axis=1)
    df['Autores Lista'] = df['Autores Detalle'].apply(lambda x: list(dict.fromkeys([item[0] for item in x])))
    df['Autores Texto'] = df['Autores Lista'].apply(lambda x: ", ".join(x))
    
    df['Título'] = df['Título'].fillna("Sin Título Especificado").str.strip()
    df['Fuente de información'] = df['Fuente de información'].fillna("No Registrada").str.strip()
    df['Nivel de formación'] = df['Nivel de formación'].fillna("No Registrado").str.strip()
    df['Programa'] = df['Programa'].fillna("No Registrado").str.strip()
    
    return df
