import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64
import os

st.set_page_config(
    page_title="Repositorio Educación",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
}

.stAppDeployButton {visibility: hidden !important; display: none !important;}
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}

div[role="radiogroup"] {
    gap: 8px !important;
}
div[role="radiogroup"] label {
    background-color: rgba(120, 120, 120, 0.08) !important;
    border: 1px solid rgba(120, 120, 120, 0.15) !important;
    border-radius: 12px !important;
    padding: 12px 16px !important;
    margin: 0 !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02) !important;
    width: 100% !important;
}
div[role="radiogroup"] label:hover {
    background-color: rgba(11, 124, 140, 0.12) !important;
    border-color: #0b7c8c !important;
    transform: translateX(4px);
}
div[role="radiogroup"] label[data-checked="true"] {
    background: linear-gradient(135deg, #0b7c8c 0%, #26d4a5 100%) !important;
    border-color: #26d4a5 !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(11, 124, 140, 0.3) !important;
}
div[role="radiogroup"] label div[role="presentation"] {
    display: none !important;
}
div[role="radiogroup"] label p {
    color: inherit !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
}

.metric-card {
    background: linear-gradient(135deg, #0b7c8c 0%, #034b54 100%);
    border: 1px solid rgba(38, 212, 165, 0.25);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 15px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    color: white;
}

.metric-card:hover {
    transform: translateY(-4px);
    border-color: #26d4a5;
    box-shadow: 0 20px 25px -5px rgba(38, 212, 165, 0.25);
}

.metric-title {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    opacity: 0.8;
    margin-bottom: 6px;
    font-weight: 600;
}

.metric-value {
    font-size: 2.2rem;
    font-weight: 800;
    color: #f8fafc;
    line-height: 1.1;
    background: linear-gradient(to right, #26d4a5, #a7f3d0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.metric-sub {
    font-size: 0.75rem;
    opacity: 0.55;
    margin-top: 8px;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

from ETL_datos import load_and_clean_data, GSHEET_URL

try:
    df_raw = load_and_clean_data()
except Exception as e:
    st.error(f"Error al conectar con el repositorio de datos UCEVA: {e}")
    st.stop()

def render_header_banner():
    st.markdown(f"""
    <div style="background-color: #F0F2F6; padding: 22px 30px; border-radius: 16px; margin-bottom: 25px; border-left: 6px solid #0b7c8c; box-shadow: 0px 4px 6px rgba(0,0,0,0.03);">
        <div style="display: flex; align-items: center; gap: 24px;">
            <div style="background-color: #ffffff; padding: 10px 14px; border-radius: 12px; box-shadow: 0px 2px 6px rgba(0,0,0,0.06); display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 32px;">🎓</span>
            </div>
            <div>
                <h1 style="margin: 0; color: #1E2B6D; font-size: 1.8rem; font-weight: 800; font-family: \'Outfit\', sans-serif; letter-spacing: -0.01em; text-transform: uppercase;">
                    Repositorio Educación
                </h1>
                <h3 style="margin: 3px 0 0 0; color: #0b7c8c; font-size: 1.15rem; font-weight: 600; font-family: \'Outfit\', sans-serif;">
                    Facultad de Ciencias de la Educación
                </h3>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def apply_plotly_theme(fig, title, height=350):
    fig.update_layout(
        title={
            'text': f"<b>{title}</b>",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 14, 'family': 'Outfit, sans-serif'}
        },
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=65, b=40),
        height=height,
        font=dict(family="Inter, sans-serif", size=12),
        hovermode="closest"
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(11, 124, 140, 0.1)', zeroline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(11, 124, 140, 0.1)', zeroline=False)
    return fig

uceva_palette = ['#0b7c8c', '#149cae', '#26d4a5', '#55e3c0', '#8bf0d7']

st.sidebar.markdown("### 🎓 Repositorio Educación")
st.sidebar.markdown("Navegación institucional:")

if st.sidebar.button("🔄 Restablecer Filtros", use_container_width=True):
    st.session_state.clear()
    st.rerun()

groups_list = sorted(df_raw['Grupo de Investigación Clean'].unique())
navigation_options = [
    "📊 Vista General",
    "🔍 Explorador de Productos",
    "👥 Investigadores y Coautores"
] + [f"🏫 Grupo: {g}" for g in groups_list]

selected_page = st.sidebar.radio(
    "Navegación del Repositorio",
    options=navigation_options,
    label_visibility="collapsed"
)

st.sidebar.divider()
st.sidebar.markdown("**Facultad de Ciencias de la Educación**")
st.sidebar.caption("Sincronización: Google Sheets (Línea)")
st.sidebar.link_button(
    "📂 Ver Base de Datos (Google Sheets)",
    GSHEET_URL.replace('/export?format=csv&gid=818503085', '/edit'),
    use_container_width=True
)

def render_page_filters(df, page_key, show_group_filter=True):
    with st.expander("🛠️ Filtros de Análisis", expanded=True):
        num_cols = 4 if show_group_filter else 3
        cols = st.columns(num_cols)
        
        years_available = sorted(df['Año Clean'].unique())
        valid_years = [y for y in years_available if 2018 <= y <= 2027]
        if not valid_years:
            valid_years = [2020, 2026]
        min_year_val = min(valid_years)
        max_year_val = max(valid_years)
        with cols[0]:
            selected_years = st.slider(
                "Rango de Años de Publicación",
                min_value=int(df['Año Clean'].min()),
                max_value=int(df['Año Clean'].max()),
                value=(int(min_year_val), int(max_year_val)),
                key=f"{page_key}_filter_years"
            )
            
        with cols[1]:
            typo_options = sorted(df['Tipología Clean'].unique())
            selected_typos = st.multiselect(
                "Tipología de Producto (MinCiencias)",
                options=typo_options,
                default=typo_options,
                key=f"{page_key}_filter_typos"
            )
            
        with cols[2]:
            prog_options = sorted(df['Programa'].unique())
            selected_progs = st.multiselect(
                "Programa Académico Vinculado",
                options=prog_options,
                default=prog_options,
                key=f"{page_key}_filter_progs"
            )
            
        if show_group_filter:
            with cols[3]:
                group_options = sorted(df['Grupo de Investigación Clean'].unique())
                selected_groups = st.multiselect(
                    "Grupo de Investigación",
                    options=group_options,
                    default=group_options,
                    key=f"{page_key}_filter_groups"
                )
        else:
            selected_groups = None
            
    df_filtered = df[
        (df['Año Clean'] >= selected_years[0]) & 
        (df['Año Clean'] <= selected_years[1]) &
        (df['Tipología Clean'].isin(selected_typos)) &
        (df['Programa'].isin(selected_progs))
    ]
    if show_group_filter and selected_groups is not None:
        df_filtered = df_filtered[df_filtered['Grupo de Investigación Clean'].isin(selected_groups)]
        
    return df_filtered

if selected_page == "📊 Vista General":
    render_header_banner()
    df_filtered = render_page_filters(df_raw, "vista_general", show_group_filter=True)
    
    if df_filtered.empty:
        st.warning("⚠️ No hay datos registrados con los filtros seleccionados.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        total_products = len(df_filtered)
        total_groups = df_filtered['Grupo de Investigación Clean'].nunique()
        all_authors_filtered = list(set([author for lst in df_filtered['Autores Lista'] for author in lst]))
        total_researchers = len(all_authors_filtered)
        total_journals = df_filtered['Fuente de información'].nunique()
        
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Productos Registrados</div><div class="metric-value">{total_products:,}</div><div class="metric-sub">Histórico acumulado</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Grupos Investigativos</div><div class="metric-value">{total_groups}</div><div class="metric-sub">Grupos categorizados</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Investigadores Activos</div><div class="metric-value">{total_researchers}</div><div class="metric-sub">Docentes y coinvestigadores</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Canales de Difusión</div><div class="metric-value">{total_journals}</div><div class="metric-sub">Revistas e indexaciones</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        row1_col1, row1_col2 = st.columns([3, 2])
        with row1_col1:
            trend_df = df_filtered.groupby(['Año Clean', 'Grupo de Investigación Clean']).size().reset_index(name='Cantidad')
            trend_df = trend_df[trend_df['Año Clean'] > 0]
            fig_trend = px.line(
                trend_df, x='Año Clean', y='Cantidad', color='Grupo de Investigación Clean', markers=True,
                color_discrete_sequence=uceva_palette,
                labels={'Año Clean': 'Año', 'Cantidad': 'Número de Productos', 'Grupo de Investigación Clean': 'Grupo'}
            )
            apply_plotly_theme(fig_trend, "Evolución Histórica de Publicaciones por Grupo", height=380)
            fig_trend.update_xaxes(dtick=1)
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with row1_col2:
            typo_df = df_filtered['Tipología Clean'].value_counts().reset_index()
            typo_df.columns = ['Tipología', 'Cantidad']
            fig_typo = px.pie(
                typo_df, names='Tipología', values='Cantidad', hole=0.45,
                color_discrete_sequence=uceva_palette
            )
            apply_plotly_theme(fig_typo, "Distribución de Productos por Tipología (MinCiencias)", height=380)
            fig_typo.update_traces(textposition='inside', textinfo='percent+label')
            fig_typo.update_layout(showlegend=False)
            st.plotly_chart(fig_typo, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        row2_col1, row2_col2 = st.columns([1, 1])
        with row2_col1:
            group_counts = df_filtered['Grupo de Investigación Clean'].value_counts().reset_index()
            group_counts.columns = ['Grupo', 'Cantidad']
            fig_group = px.bar(
                group_counts, x='Cantidad', y='Grupo', orientation='h', color='Cantidad',
                color_continuous_scale=uceva_palette,
                labels={'Grupo': 'Grupo de Investigación', 'Cantidad': 'Productos'}
            )
            apply_plotly_theme(fig_group, "Producción Total por Grupo de Investigación", height=350)
            fig_group.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False)
            st.plotly_chart(fig_group, use_container_width=True)
            
        with row2_col2:
            sub_counts = df_filtered['Subcategoría Clean'].value_counts().reset_index()
            sub_counts.columns = ['Subcategoría', 'Cantidad']
            fig_sub = px.bar(
                sub_counts.head(8), x='Cantidad', y='Subcategoría', orientation='h', color='Cantidad',
                color_continuous_scale=uceva_palette,
                labels={'Subcategoría': 'Subcategoría', 'Cantidad': 'Productos'}
            )
            apply_plotly_theme(fig_sub, "Principales Subcategorías de Productos", height=350)
            fig_sub.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False)
            st.plotly_chart(fig_sub, use_container_width=True)

elif selected_page == "🔍 Explorador de Productos":
    st.markdown("## 🔍 Explorador y Buscador de Productos Científicos")
    
    df_filtered = render_page_filters(df_raw, "explorador", show_group_filter=True)
    
    if df_filtered.empty:
        st.warning("⚠️ No hay datos registrados con los filtros seleccionados.")
    else:
        search_query = st.text_input("🔍 Filtro por texto libre (Título, Grupo o Investigador):", "", placeholder="Escribe aquí para buscar...")
        states_available = sorted(df_filtered['Estado Clean'].unique())
        selected_states = st.multiselect("Filtrar por Estado de Aprobación Institucional:", states_available, default=states_available)
        
        df_explored = df_filtered[df_filtered['Estado Clean'].isin(selected_states)]
        
        if search_query:
            query = search_query.lower()
            title_mask = df_explored['Título'].str.lower().str.contains(query)
            group_mask = df_explored['Grupo de Investigación Clean'].str.lower().str.contains(query)
            authors_mask = df_explored['Autores Texto'].str.lower().str.contains(query)
            df_explored = df_explored[title_mask | group_mask | authors_mask]
            
        if df_explored.empty:
            st.warning("⚠️ No se encontraron registros con los criterios ingresados.")
        else:
            st.write(f"Mostrando **{len(df_explored)}** registros coincidentes:")
            df_display = df_explored[[
                'No.', 'Título', 'Año Clean', 'Grupo de Investigación Clean', 'Tipología Clean', 
                'Autores Texto', 'Fuente de información', 'Estado Clean', 'Enlace Clean'
            ]].rename(columns={
                'Año Clean': 'Año',
                'Grupo de Investigación Clean': 'Grupo',
                'Tipología Clean': 'Tipología',
                'Autores Texto': 'Investigadores / Autores',
                'Fuente de información': 'Canal de Publicación',
                'Estado Clean': 'Estado',
                'Enlace Clean': 'Enlace'
            })
            
            st.dataframe(
                df_display,
                column_config={
                    "Enlace": st.column_config.LinkColumn(
                        "Enlace / DOI 🔗", help="Enlace oficial externo", validate="^http", display_text="Acceder ↗"
                    ),
                    "Año": st.column_config.NumberColumn("Año", format="%d"),
                    "No.": st.column_config.NumberColumn("ID", format="%d")
                },
                use_container_width=True, hide_index=True, height=400
            )
            
            csv_data = df_explored[[
                'No.', 'Título', 'Año Clean', 'Grupo de Investigación Clean', 'Tipología Clean', 
                'Subcategoría Clean', 'Autores Texto', 'Fuente de información', 'Estado Clean', 'Enlace Clean'
            ]].to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Exportar Resultados (CSV)", data=csv_data,
                file_name=f"repositorio_investigacion_uceva_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv'
            )
            
            st.markdown("---")
            st.markdown("### 📋 Ficha Técnica y Detalle del Producto")
            selected_title = st.selectbox("Selecciona un producto de la lista para ver el desglose completo:", options=df_explored['Título'].unique())
            
            if selected_title:
                row_det = df_explored[df_explored['Título'] == selected_title].iloc[0]
                d_col1, d_col2 = st.columns(2)
                with d_col1:
                    st.markdown(f"#### **{row_det['Título']}**")
                    st.markdown(f"**Grupo de Investigación Vinculado:** {row_det['Grupo de Investigación Clean']}")
                    st.markdown(f"**Año Lectivo:** {row_det['Año Clean']} | **Periodo Académico:** {row_det['Periodo'] if pd.notna(row_det['Periodo']) else 'N/A'}")
                    st.markdown(f"**Tipología (MinCiencias):** {row_det['Tipología Clean']}")
                    st.markdown(f"**Clasificación Subcategoría:** {row_det['Subcategoría Clean']}")
                    st.markdown(f"**Revista / Editorial / Medio:** {row_det['Fuente de información']}")
                with d_col2:
                    st.markdown("#### **Participantes & Evaluación de Pares**")
                    st.markdown("**Investigadores Asociados:**")
                    for auth, role in row_det['Autores Detalle']:
                        role_badge = "👔" if "Director" in role else ("🤝" if "Codirector" in role else "🎓")
                        st.markdown(f"- {role_badge} **{auth}** ({role})")
                    st.markdown(f"**Estado de aprobación:** `{row_det['Estado Clean']}`")
                    jurados = [str(row_det[j]).strip().title() for j in ['Jurado 1', 'Jurado 2', 'Jurado 3'] if pd.notna(row_det[j]) and str(row_det[j]).strip() not in ['', 'nan', '-']]
                    if jurados:
                        st.markdown(f"**Jurados Evaluadores Internos/Externos:** {', '.join(jurados)}")
                    if row_det['Enlace Clean']:
                        st.markdown(f"**Enlace Oficial:** [Ver publicación original ↗️]({row_det['Enlace Clean']})")

elif selected_page == "👥 Investigadores y Coautores":
    st.markdown("## 👥 Liderazgo y Participación de Investigadores")
    
    df_filtered = render_page_filters(df_raw, "investigadores", show_group_filter=True)
    
    if df_filtered.empty:
        st.warning("⚠️ No hay datos registrados con los filtros seleccionados.")
    else:
        flat_authors = [author for lst in df_filtered['Autores Lista'] for author in lst]
        authors_series = pd.Series(flat_authors)
        
        if not authors_series.empty:
            top_authors_df = authors_series.value_counts().reset_index()
            top_authors_df.columns = ['Investigador', 'Productos']
            top_15_authors = top_authors_df.head(15)
            
            col_lead_1, col_lead_2 = st.columns([3, 2])
            with col_lead_1:
                fig_lead = px.bar(
                    top_15_authors, x='Productos', y='Investigador', orientation='h', color='Productos',
                    color_continuous_scale=uceva_palette,
                    labels={'Investigador': 'Investigador', 'Productos': 'Número de Productos'}
                )
                apply_plotly_theme(fig_lead, "Top 15 Investigadores con Mayor Producción Registrada", height=450)
                fig_lead.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False)
                st.plotly_chart(fig_lead, use_container_width=True)
                
            with col_lead_2:
                level_df = df_filtered[df_filtered['Nivel de formación'] != 'No Registrado']['Nivel de formación'].value_counts().reset_index()
                level_df.columns = ['Nivel de formación', 'Cantidad']
                if not level_df.empty:
                    fig_level = px.pie(
                        level_df, names='Nivel de formación', values='Cantidad',
                        color_discrete_sequence=uceva_palette
                    )
                    apply_plotly_theme(fig_level, "Productos de Formación Académica Asociada", height=220)
                    st.plotly_chart(fig_level, use_container_width=True)
                else:
                    st.info("ℹ️ No hay productos vinculados a formación académica (tesis/proyectos de grado) en esta selección.")
                
                prog_df = df_filtered[df_filtered['Programa'] != 'No Registrado']['Programa'].value_counts().reset_index()
                prog_df.columns = ['Programa Académico', 'Cantidad']
                if not prog_df.empty:
                    st.markdown("#### Producción Registrada por Programa Académico")
                    st.dataframe(prog_df, use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No hay registros de coautores vinculados a los filtros seleccionados.")

elif selected_page.startswith("🏫 Grupo: "):
    group_name = selected_page.replace("🏫 Grupo: ", "")
    st.markdown(f"## 🏫 Dashboard Especializado del Grupo")
    st.markdown(f"### **{group_name}**")
    
    df_group_raw = df_raw[df_raw['Grupo de Investigación Clean'] == group_name]
    df_filtered = render_page_filters(df_group_raw, f"grupo_{group_name.replace(' ', '_')}", show_group_filter=False)
    
    if df_filtered.empty:
        st.warning("⚠️ No hay datos registrados con los filtros seleccionados para este grupo.")
    else:
        col1, col2, col3 = st.columns(3)
        total_products = len(df_filtered)
        all_authors_filtered = list(set([author for lst in df_filtered['Autores Lista'] for author in lst]))
        total_researchers = len(all_authors_filtered)
        years_active = df_filtered[df_filtered['Año Clean'] > 0]['Año Clean'].nunique()
        
        with col1:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Productos del Grupo</div><div class="metric-value">{total_products:,}</div><div class="metric-sub">Publicaciones y proyectos</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Integrantes Registrados</div><div class="metric-value">{total_researchers}</div><div class="metric-sub">Autores y directores de línea</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="metric-card"><div class="metric-title">Años de Actividad</div><div class="metric-value">{years_active}</div><div class="metric-sub">Años con publicaciones registradas</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_g1, col_g2 = st.columns([3, 2])
        with col_g1:
            trend_df = df_filtered.groupby('Año Clean').size().reset_index(name='Cantidad')
            trend_df = trend_df[trend_df['Año Clean'] > 0]
            fig_trend = px.bar(
                trend_df, x='Año Clean', y='Cantidad',
                color='Cantidad', color_continuous_scale=uceva_palette,
                labels={'Año Clean': 'Año', 'Cantidad': 'Número de Productos'}
            )
            apply_plotly_theme(fig_trend, "Historial de Producción Anual del Grupo", height=350)
            fig_trend.update_layout(coloraxis_showscale=False)
            fig_trend.update_xaxes(dtick=1)
            st.plotly_chart(fig_trend, use_container_width=True)
            
        with col_g2:
            typo_df = df_filtered['Tipología Clean'].value_counts().reset_index()
            typo_df.columns = ['Tipología', 'Cantidad']
            fig_typo = px.pie(
                typo_df, names='Tipología', values='Cantidad', hole=0.4,
                color_discrete_sequence=uceva_palette
            )
            apply_plotly_theme(fig_typo, "Tipología de Productos en el Grupo (MinCiencias)", height=350)
            fig_typo.update_traces(textposition='inside', textinfo='percent+label')
            fig_typo.update_layout(showlegend=False)
            st.plotly_chart(fig_typo, use_container_width=True)
            
        st.markdown("---")
        st.markdown("#### Integrantes Más Activos del Grupo")
        flat_authors = [author for lst in df_filtered['Autores Lista'] for author in lst]
        if flat_authors:
            g_authors_df = pd.Series(flat_authors).value_counts().reset_index()
            g_authors_df.columns = ['Investigador', 'Productos Registrados']
            st.dataframe(g_authors_df.head(10), use_container_width=True, hide_index=True)
        else:
            st.info("ℹ️ No hay registros de coautores vinculados a este grupo.")
            
        st.markdown("#### Publicaciones y Productos del Grupo")
        df_display = df_filtered[[
            'Título', 'Año Clean', 'Tipología Clean', 'Autores Texto', 'Fuente de información', 'Estado Clean', 'Enlace Clean'
        ]].rename(columns={
            'Año Clean': 'Año',
            'Tipología Clean': 'Tipología',
            'Autores Texto': 'Investigadores / Autores',
            'Fuente de información': 'Canal / Editorial',
            'Estado Clean': 'Estado',
            'Enlace Clean': 'Enlace'
        }).head(15)
        
        st.dataframe(
            df_display,
            column_config={
                "Enlace": st.column_config.LinkColumn(
                    "Enlace / DOI 🔗", help="Enlace externo", validate="^http", display_text="Acceder ↗"
                ),
                "Año": st.column_config.NumberColumn("Año", format="%d")
            },
            use_container_width=True, hide_index=True
        )
