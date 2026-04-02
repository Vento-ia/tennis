import time  # <--- AÑADE ESTO AL PRINCIPIO DE TODO
import streamlit as st
import pandas as pd
import requests
import urllib.parse
from datetime import datetime, timedelta
from streamlit_gsheets import GSheetsConnection
import random

def generar_titular_tenis(ganador, score):
    try:
        s = str(score).replace(" ", "").split('-')
        g1, g2 = int(s[0]), int(s[1])
        dif = abs(g1 - g2)
        nombre = str(ganador).split()[0]
        
        if dif >= 4:
            frases = [
                f"🎾 Juego impecable de {nombre}, dominando el fondo de la cancha con gran precisión.",
                f"📈 {nombre} impone su ritmo desde el servicio y cierra una victoria contundente.",
                f"✨ Exhibición de tenis por parte de {nombre}, quien desplegó su mejor repertorio."
            ]
        elif dif <= 1:
            frases = [
                f"🤝 ¡Duelo de titanes! {nombre} prevalece en un encuentro que se decidió por detalles.",
                f"🛡️ {nombre} mostró una mentalidad de hierro para llevarse este set tan disputado.",
                f"🔥 Un partido de alto nivel donde {nombre} supo aprovechar los quiebres cruciales."
            ]
        else:
            frases = [
                f"🎾 {nombre} ratifica su solidez y suma una victoria clave para su ascenso en el ranking.",
                f"💪 Con mucha jerarquía, {nombre} sella un resultado positivo manteniendo su servicio.",
                f"🎓 Tenis de alto nivel: {nombre} maneja los tiempos del partido y asegura el triunfo."
            ]
        return random.choice(frases)
    except:
        return f"🏆 Resultado oficial: {ganador} se adjudica la victoria en este encuentro."


# ******************************************************************************
# CONFIGURACIÓN GLOBAL (Esto evita el error de variable no definida)
# ******************************************************************************
SHEET_ID_SOLO = "18sNSVjpX0N14Nk2TdMw3O9Hp317R7qSzZarlTJJacSM"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_SOLO}"
URL_DE_TU_APP = "https://tennis-hub-pro.streamlit.app"
URL_DE_TU_APP = "https://tu-app-de-tennis.streamlit.app"
# ******************************************************************************
# 1. CONFIGURACIÓN DE PÁGINA E IDENTIDAD VISUAL (ESTILO UNIFICADO)
# ******************************************************************************
st.set_page_config(page_title="Tennis Hub Pro", layout="centered", page_icon="🎾")

st.markdown("""
        <style>

    /* 🔥 CONTENEDOR DE LA BARRA SOCIAL */
        .social-row {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* ❤️ BOTONES PEQUEÑOS */
        .social-row button {
        padding: 4px 8px !important;
        font-size: 12px !important;
        width: auto !important;
    }

    /* ✍️ INPUT PEQUEÑO */
        .social-row input {
        height: 32px !important;
        font-size: 12px !important;
    }

    /* 📱 EVITA QUE SE ROMPA EN MÓVIL */
        @media (max-width: 600px) {
        .social-row {
            flex-wrap: nowrap !important;
        }
    }        
            
    <style>
    /* 1. FONDO Y TEXTO GENERAL */
    .stApp { background-color: #0e1117; color: white; }
    h1, h2, h3, p, span, label, div { color: white !important; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }

    /* 2. MÉTRICAS (WIN RATE, PUNTOS) */
    [data-testid="stMetricValue"] { font-size: 24px; color: #00ffcc !important; }

    /* 3. TABS (PESTAÑAS) */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #1e1e1e; 
        border-radius: 10px; 
        padding: 10px; 
        color: white; 
        font-size: 14px;
    }
    /*  INPUT NO SE DESBORDA */
        div[data-testid="stTextInput"] input {
        width: 50% !important;
        font-size: 12px !important;
        padding: 6px !important;
}

    /* BOTONES PEQUEÑOS */
       .stButton > button {
        padding: 4px 6px !important;
        font-size: 12px !important;
}
}        

    /* 4. FOTOS DE JUGADORES (REDONDAS) */
    [data-testid="stImage"] img { 
        border-radius: 50% !important; 
        border: 2px solid #00ffcc; 
        object-fit: cover; 
        width: 35px !important; 
        height: 70px !important; 
    }

    /* 5. TARJETAS DE PARTIDOS Y FEED */
    .feed-card { 
        background: #161b22; 
        padding: 15px; 
        border-radius: 15px; 
        border-left: 5px solid #00ffcc; 
        margin-bottom: 10px; 
        border: 1px solid #30363d; 
    }
    .win-tag { background-color: #28a745; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; }
    .loss-tag { background-color: #dc3545; color: white; padding: 2px 8px; border-radius: 4px; font-weight: bold; }

    /* 6. FIX PARA SELECTBOX */
    div[data-baseweb="select"] > div {
        background-color: #1e2630 !important;
        color: white !important;
        border: 1px solid #30363d !important;
    }
    ul[role="listbox"] {
        background-color: #1e2630 !important;
    }
    li[role="option"] {
        color: white !important;
        background-color: #1e2630 !important;
    }
    li[role="option"]:hover {
        background-color: #3e404b !important;
        color: #00ffcc !important;
    }

    /* 7. ESTILO PARA EL TAB DE MENSAJES (CORAZÓN Y BOTONES) */
    .chat-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 20px;
        margin-top: 10px;
    }

    .heart-icon {
        font-size: 50px;
        margin-bottom: 10px;
        display: block;
    }

        /* BOTONES MÁS FLEXIBLES (NO ROMPEN COLUMNAS) */
    .stButton > button {
        border-radius: 10px !important;
        padding: 6px 8px !important;
        font-size: 12px !important;
    }

    /* INPUT MÁS COMPACTO */
    div[data-testid="stTextInput"] input {
        font-size: 12px !important;
        padding: 6px !important;
    }

     
    </style>
    """, unsafe_allow_html=True)


# ******************************************************************************
@st.cache_data(show_spinner=False)
def descargar_foto_drive(file_id):
    if not file_id or str(file_id).lower() in ["nan", "none", ""]:
        return None
    try:
        # Añadimos un "User-Agent" para engañar a Google y que crea que soy un navegador
        headers = {"User-Agent": "Mozilla/5.0"}
        url = f"https://drive.google.com/uc?export=view&id={file_id}"
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.content
        return None
    except:
        return None

# ******************************************************************************
# 3. VARIABLES DE CONEXIÓN Y CONFIGURACIÓN DE GOOGLE SHEETS
# ******************************************************************************
SHEET_ID_SOLO = "18sNSVjpX0N14Nk2TdMw3O9Hp317R7qSzZarlTJJacSM"
GID_JUGADORES = "0"
GID_REPORTES = "1569954908"
GID_CRUCES = "2027781620"

# ******************************************************************************
# 4. CARGA Y LIMPIEZA DE DATOS MAESTROS (JUGADORES Y PARTIDOS)
# ******************************************************************************
@st.cache_data(ttl=120)
def cargar_datos_maestros():
    try:
        # 1. Cargar Jugadores
        url_jug = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_SOLO}/export?format=csv&gid={GID_JUGADORES}"
        df_j = pd.read_csv(url_jug)
        df_j.columns = df_j.columns.str.strip().str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        df_j.columns = [c.replace('cedula', 'Cedula').replace('CEDULA', 'Cedula') for c in df_j.columns]
        
        if 'Cedula' in df_j.columns:
            df_j['Cedula'] = df_j['Cedula'].astype(str).str.strip().str.zfill(10)
        
        # 2. Cargar Reportes (Partidos)
        url_part = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_SOLO}/export?format=csv&gid={GID_REPORTES}"
        df_p = pd.read_csv(url_part)
        df_p.columns = df_p.columns.str.strip()

        # 3. Cargar Configuración (La nueva hoja)
        # Usamos el GID que me pasaste: 2025785966
        url_conf = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_SOLO}/export?format=csv&gid=2025785966"
        df_c = pd.read_csv(url_conf)
        df_c.columns = df_c.columns.str.strip() # Limpiamos espacios en nombres de columnas
        
        # 3. NUEVO: Cargar Hoja de Cruces
        url_cruces = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_SOLO}/export?format=csv&gid={GID_CRUCES}"
        df_cr = pd.read_csv(url_cruces)
        df_cr.columns = df_cr.columns.str.strip() # Limpiamos espacios


        # IMPORTANTE: Devolvemos los 3 DataFrames
        return df_j, df_p, df_c, df_cr

    except Exception as e:
        st.error(f"Error de conexión: {e}")
        # Devolvemos 3 DataFrames vacíos en caso de error para evitar que la app se rompa
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# ******************************************************************************
# 5. LÓGICA DE CÁLCULO PARA EL RANKING (SOLO CONFIRMADOS + FILTRO GRUPO)
# ******************************************************************************
@st.cache_data(ttl=60)
def calcular_ranking_grupo(df_jugadores, df_partidos, categoria_sel, grupo_sel):
    # 1. Filtramos jugadores: solo los que pertenecen a la misma categoría y grupo
    ranking = df_jugadores[
        (df_jugadores['Categoria'] == categoria_sel) & 
        (df_jugadores['Grupo'].astype(str) == str(grupo_sel))
    ].copy()
    
    # Inicializamos contadores en el DataFrame de ranking
    for col in ['PJ', 'PG', 'PP', 'JG', 'JP', 'Puntos']: 
        ranking[col] = 0
    
    # Si hay partidos registrados, procesamos los puntos
    if not df_partidos.empty:
        # 2. FILTRO ESTRICTO: Solo partidos con estado "Confirmado"
        partidos_v = df_partidos[df_partidos['Estado'] == 'Confirmado']
        
        for _, p in partidos_v.iterrows():
            # 3. FILTRO DE SEGURIDAD: Solo procesar partidos de este grupo y categoría específicos
            if str(p.get('Grupo', '')) == str(grupo_sel) and str(p.get('Categoria', '')) == str(categoria_sel):
                ganador = str(p['Ganador']).strip()
                perdedor = str(p['Perdedor']).strip()
                
                # Intentamos extraer el score (ej: 6-4)
                try:
                    score_partes = str(p['Score']).split('-')
                    s_ganador = int(score_partes[0])
                    s_perdedor = int(score_partes[1])
                except: 
                    continue 

                # --- Sumar estadísticas al Ganador ---
                idx_g = ranking[ranking['Nombre'] == ganador].index
                if not idx_g.empty:
                    ranking.loc[idx_g, 'PJ'] += 1
                    ranking.loc[idx_g, 'PG'] += 1
                    ranking.loc[idx_g, 'JG'] += s_ganador
                    ranking.loc[idx_g, 'JP'] += s_perdedor
                    ranking.loc[idx_g, 'Puntos'] += 2

                # --- Sumar estadísticas al Perdedor ---
                idx_p = ranking[ranking['Nombre'] == perdedor].index
                if not idx_p.empty:
                    ranking.loc[idx_p, 'PJ'] += 1
                    ranking.loc[idx_p, 'PP'] += 1
                    ranking.loc[idx_p, 'JG'] += s_perdedor
                    ranking.loc[idx_p, 'JP'] += s_ganador

    # 4. Cálculo final de Diferencia de Juegos (DJ)
    ranking['DJ'] = ranking['JG'] - ranking['JP']
    
    # 5. Ordenar el Ranking: 1. Puntos, 2. Diferencia Juegos, 3. Juegos Ganados
    return ranking.sort_values(by=['Puntos', 'DJ', 'JG'], ascending=False)
    
# ******************************************************************************
# 7. MOTOR DE INTELIGENCIA ARTIFICIAL (PREDICCIÓN DE PROBABILIDADES)
# ******************************************************************************
def calcular_probabilidad_ia(j1, j2, df_p):
    def get_wins(nombre):
        m = df_p[((df_p['Ganador'] == nombre) | (df_p['Perdedor'] == nombre)) & (df_p['Score'].notnull())]
        w = len(m[m['Ganador'] == nombre])
        return w, len(m)

    try:
        (w1, t1), (w2, t2) = get_wins(j1), get_wins(j2)
        r1 = (w1 / t1) if t1 > 0 else 0.5
        r2 = (w2 / t2) if t2 > 0 else 0.5
        prob1 = round((r1 / (r1 + r2)) * 100) if (r1 + r2) > 0 else 50
        return prob1, 100 - prob1
    except: return 50, 50

# ******************************************************************************
# 8. FUNCIÓN PRINCIPAL: INTERFAZ DE USUARIO (MAIN)
# ******************************************************************************
def main():
    # **************************************************************************
    # ESTILOS ADICIONALES PARA MODO OSCURO
    # **************************************************************************
    st.markdown("""
        <style>
            .stApp { background-color: #0e1117; color: white; }
            h1, h2, h3, p, span, label, div { color: white !important; }
            [data-testid="stMetricValue"] { color: #28a745 !important; }
            [data-testid="stHeader"] { background: rgba(0,0,0,0); }
            .stTabs [data-baseweb="tab-list"] { gap: 8px; }
            .stTabs [data-baseweb="tab"] { background-color: #1e2130; border-radius: 5px; padding: 8px; font-size: 14px; }
        </style>
    """, unsafe_allow_html=True)

    df_jugadores, df_partidos, df_config, df_cruces_maestros = cargar_datos_maestros()
    
    # **************************************************************************
    # LÓGICA DE LOGIN (CONTROL DE ACCESO POR CÉDULA)
    # **************************************************************************
    if 'auth' not in st.session_state:
        st.title("🎾 Tennis Hub Pro")
        cedula_input = st.text_input("Ingresa tu Cédula:")
        if st.button("Entrar"):
            user_data = df_jugadores[df_jugadores['Cedula'] == cedula_input.strip().zfill(10)]
            if not user_data.empty:
                st.session_state['auth'] = True
                st.session_state['user'] = user_data.iloc[0].to_dict()
                st.rerun()
            else:
                st.error("Cédula no encontrada.")
        return

    # **************************************************************************
    # CONFIGURACIÓN DE SESIÓN Y CONEXIÓN A GOOGLE SHEETS
    # **************************************************************************
    user = st.session_state['user']
    nombre_u = user['Nombre']
    cat_u = user['Categoria']
    grupo_u = user['Grupo']
    SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID_SOLO}"
    conn = st.connection("gsheets", type=GSheetsConnection)

    # --- CONFIGURACIÓN DE SESIÓN OPTIMIZADA PARA MUCHOS USUARIOS ---
    # Solo buscamos en df_config si no lo hemos guardado ya en esta sesión
    if 'fase_actual' not in st.session_state:
        torneo_u = user.get('Torneo')
        conf_t = df_config[df_config['Torneo'] == torneo_u]

        if not conf_t.empty:
            ultima_fila = conf_t.iloc[-1]
            st.session_state['torneo_u'] = torneo_u
            st.session_state['fase_actual'] = ultima_fila['Fase']
            st.session_state['fecha_limite'] = pd.to_datetime(ultima_fila['Fecha_Limite'], dayfirst=True)
        else:
            # Caso de seguridad si el torneo no existe en la hoja Config
            st.session_state['torneo_u'] = torneo_u if torneo_u else "Sin Torneo"
            st.session_state['fase_actual'] = "Bloqueado"
            st.session_state['fecha_limite'] = datetime.now()

    # Extraemos las variables del session_state para que estén disponibles en todos los Tabs
    torneo_u = st.session_state['torneo_u']
    fase_actual = st.session_state['fase_actual']
    fecha_limite = st.session_state['fecha_limite']

    # **************************************************************************
    # 8. HEADER VISUAL (FOTO DE DRIVE + SALUDO PERSONALIZADO) - FIX FINAL
    # **************************************************************************
    
    # 1. Obtención del ID (Usando el nombre exacto de tu columna)
    id_foto = str(user.get('ID FOTO', '')) 
    foto_bytes = descargar_foto_drive(id_foto)

    # 2. Conversión a Base64 para el HTML
    import base64
    def get_base64(bin_file):
        if bin_file:
            return base64.b64encode(bin_file).decode()
        return None

    img_base64 = get_base64(foto_bytes)

    # 3. HTML Único para mantener todo en una sola fila (Desktop y Móvil)
    if img_base64:
        # Si la foto se descargó correctamente
        header_html = f'''
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                <img src="data:image/png;base64,{img_base64}" 
                     style="width: 75px; height: 75px; border-radius: 50%; border: 2px solid #00ffcc; object-fit: cover;">
                <div>
                    <h3 style="margin: 0; color: white; font-size: 20px;">¡Hola, {nombre_u.split()[0]}!</h3>
                    <p style="margin: 0; color: #00ffcc; font-size: 14px;">🏆 {cat_u} | 👥 G{grupo_u}</p>
                </div>
            </div>
        '''
    else:
        # Avatar de respaldo si la celda está vacía o el ID no funciona
        header_html = f'''
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                <div style="background-color:#1e2630; border-radius:50%; width:75px; height:75px; 
                            display:flex; align-items:center; justify-content:center; border:2px solid #00ffcc; font-size:35px;">
                    👤
                </div>
                <div>
                    <h3 style="margin: 0; color: white; font-size: 20px;">¡Hola, {nombre_u.split()[0]}!</h3>
                    <p style="margin: 0; color: #00ffcc; font-size: 14px;">🏆 {cat_u} | 👥 G{grupo_u}</p>
                </div>
            </div>
        '''

    st.markdown(header_html, unsafe_allow_html=True)
    st.write("---")
    # **************************************************************************
    # NAVEGACIÓN POR PESTAÑAS (TABS)
    # **************************************************************************
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔥 Noticias", "🏆 Ranking", "👤 Perfil", "👮 Árbitro", "🎾 Playoffs"])

    # **************************************************************************
        # --- TAB 1: NOTICIAS (FEED SOCIAL ULTRA-COMPACTO PRO) ---
    # --- TAB 1: NOTICIAS & RANKING (CRÓNICA DEPORTIVA) ---
    with tab1:
        st.markdown('### 🎾 Estado del Torneo')
        
        # 1. CÁLCULO DE PUNTOS GLOBALES
        puntos_globales = {}
        if not df_partidos.empty:
            df_confirmados = df_partidos[df_partidos['Estado'] == 'Confirmado']
            for _, row in df_confirmados.iterrows():
                ganador, perdedor = row['Ganador'], row['Perdedor']
                try:
                    s = str(row['Score']).replace(" ", "").split('-')
                    dif = abs(int(s[0]) - int(s[1]))
                except: dif = 0
                puntos_globales[ganador] = puntos_globales.get(ganador, 0) + 10 + dif + 1
                puntos_globales[perdedor] = puntos_globales.get(perdedor, 0) + 1

        # ---------------------------------------------------------
        # 2. EL LÍDER (Versión reducida y elegante)
        # ---------------------------------------------------------
        if puntos_globales:
            mvp_nombre = max(puntos_globales, key=puntos_globales.get)
            total_puntos = puntos_globales[mvp_nombre]
            datos_mvp = df_jugadores[df_jugadores['Nombre'] == mvp_nombre]
            id_foto_mvp = datos_mvp['ID FOTO'].values[0] if not datos_mvp.empty else ""
            url_mvp = f"https://drive.google.com/thumbnail?id={id_foto_mvp}&sz=200" if id_foto_mvp else ""

            st.markdown(f'''
                <div style="background: linear-gradient(145deg, #1e2530, #0d1117); padding: 12px; border-radius: 12px; border: 1px solid #fbcf00; margin-bottom: 20px; display: flex; align-items: center; gap: 12px;">
                    <div style="position: relative;">
                        <img src="{url_mvp}" style="width: 55px; height: 55px; border-radius: 50%; border: 2px solid #fbcf00; object-fit: cover;">
                        <div style="position: absolute; bottom: -3px; right: -3px; background: #fbcf00; color: #000; border-radius: 50%; width: 18px; height: 18px; font-size: 10px; font-weight: bold; text-align: center; line-height: 18px;">#1</div>
                    </div>
                    <div>
                        <p style="color: #fbcf00; font-size: 9px; font-weight: bold; margin: 0; letter-spacing: 1px;">LÍDER DEL RANKING</p>
                        <h3 style="margin: 0; color: white; font-size: 16px;">{mvp_nombre}</h3>
                        <p style="color: #aaa; font-size: 11px; margin: 0;">{total_puntos} pts acumulados</p>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

        # ---------------------------------------------------------
        # 3. ÚLTIMOS 2 RESULTADOS CON CRÓNICA AUTOMÁTICA
        # ---------------------------------------------------------
        if not df_partidos.empty:
            st.markdown('<p style="color: #888; font-size: 12px; font-weight: bold; margin-bottom: 8px;">📢 ÚLTIMAS CRÓNICAS</p>', unsafe_allow_html=True)
            noticias = df_partidos[df_partidos['Estado'] == 'Confirmado'].tail(2).iloc[::-1]
            
            for _, p in noticias.iterrows():
                id_g = df_jugadores[df_jugadores['Nombre'] == p['Ganador']]['ID FOTO'].values
                id_p = df_jugadores[df_jugadores['Nombre'] == p['Perdedor']]['ID FOTO'].values
                url_g = f"https://drive.google.com/thumbnail?id={id_g[0]}&sz=100" if len(id_g) > 0 else ""
                url_p = f"https://drive.google.com/thumbnail?id={id_p[0]}&sz=100" if len(id_p) > 0 else ""
                
                # Aquí llamamos a tu función de prensa deportiva
                titular = generar_titular_tenis(p['Ganador'], p['Score'])

                st.markdown(f'''
                <div style="background:#161b22; padding:12px; border-radius:12px; border:1px solid #30363d; margin-bottom:12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; text-align: center;">
                        <div style="width: 25%;">
                            <img src="{url_g}" style="width: 40px; height: 40px; border-radius: 50%; border: 2px solid #00ffcc; object-fit: cover;">
                            <p style="font-size: 9px; margin-top:4px; color: white; font-weight: bold;">{str(p['Ganador']).split()[0]}</p>
                        </div>
                        <div style="width: 50%;">
                            <h2 style="margin: 0; color: #00ffcc !important; font-size: 20px;">{p['Score']}</h2>
                            <p style="color: #666; font-size: 8px; margin:0;">{p['Fecha']}</p>
                        </div>
                        <div style="width: 25%;">
                            <img src="{url_p}" style="width: 40px; height: 40px; border-radius: 50%; border: 2px solid #444; object-fit: cover;">
                            <p style="font-size: 9px; margin-top:4px; color: white;">{str(p['Perdedor']).split()[0]}</p>
                        </div>
                    </div>
                    <div style="margin-top: 10px; padding-top: 8px; border-top: 1px solid #222;">
                        <p style="color: #eee; font-size: 11.5px; font-style: italic; margin: 0; line-height: 1.4; color: #cbd5e0;">
                            📰 {titular}
                        </p>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

        # ---------------------------------------------------------
        # ---------------------------------------------------------
        # 4. RANKING GENERAL COMPLETO (Todos los jugadores)
        # ---------------------------------------------------------
        if puntos_globales:
            st.markdown('<p style="color: #fbcf00; font-size: 13px; font-weight: bold; margin: 20px 0 8px 0;">📊 RANKING GENERAL DE TENISTAS</p>', unsafe_allow_html=True)
            
            # Convertimos todo el diccionario a DataFrame
            df_ranking = pd.DataFrame(list(puntos_globales.items()), columns=['Tenista', 'Puntos'])
            
            # Ordenamos de mayor a menor puntuación
            df_ranking = df_ranking.sort_values(by='Puntos', ascending=False).reset_index(drop=True)
            
            # Ajustamos el índice para que sea la posición real (1, 2, 3...)
            df_ranking.index += 1
            
            # Mostramos la tabla completa con barra de búsqueda automática de Streamlit
            st.dataframe(
                df_ranking, 
                use_container_width=True,
                height=400, # Altura fija para que no se haga infinita la página si hay muchos
                column_config={
                    "Puntos": st.column_config.NumberColumn(
                        "Pts Totales",
                        help="Suma de victorias, bonus por diferencia de juegos y participación.",
                        format="%d 🏆"
                    ),
                    "Tenista": st.column_config.TextColumn("Jugador")
                }
            )
            
            st.caption("💡 Tip: Puedes hacer clic en las columnas para ordenar o buscar tu nombre.")
# TAB 2: TABLA DE POSICIONES (PARA PEGAR EN TU APP)
# **************************************************************************
    with tab2:
        # 1. BOTÓN DE ACTUALIZACIÓN (Lo nuevo para el caché)
        col_ref, col_vacia = st.columns([1, 3])
        with col_ref:
            if st.button("🔄 Actualizar"):
                st.cache_data.clear()
                st.rerun()
        st.markdown(f"### 🏆 Tabla de Posiciones - {cat_u} (G{grupo_u})")
        
        df_rank = calcular_ranking_grupo(df_jugadores, df_partidos, cat_u, grupo_u)
        
        if not df_rank.empty:
            # Mostramos la tabla limpia
            st.dataframe(
                df_rank[['Nombre', 'PJ', 'PG', 'PP', 'Puntos', 'DJ']], 
                use_container_width=True, 
                hide_index=True,
                column_config={
                    "Nombre": "Jugador",
                    "Puntos": st.column_config.NumberColumn("Pts", format="%d 🔥"),
                    "DJ": "Dif. Juegos"
                }
            )
        else:
            st.info("Aún no hay partidos 'Confirmados' en este grupo.")

    # **************************************************************************
    # TAB 3: MI PERFIL (ESTADÍSTICAS Y SCOUTING)
    # **************************************************************************
    with tab3:
        st.header("📊 Mi estado de Forma")

        # --- 1. FUNCIÓN DE RENDERIZADO (Estética de la imagen) ---
        def render_tarjeta_tenis(oponente, score, resultado):
            # Colores: Verde para Ganar, Rojo para Perder
            bg_color = "#1e2530"
            label_color = "#00c853" if (resultado in ["✅ Ganaste", "🟢 Ganó"]) else "#ff1744"
            letra_res = "GANADO" if (resultado in ["✅ Ganaste", "🟢 Ganó"]) else "PERDIDO"
            
            st.markdown(f'''
                <div style="background:{bg_color}; padding:12px; border-radius:10px; margin-bottom:10px; border: 1px solid #30363d;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div style="color:white; font-size:14px; font-weight:500;">vs {oponente}</div>
                        <div style="display:flex; align-items:center; gap:12px;">
                            <span style="color:#888; font-size:12px; font-family:monospace;">{score}</span>
                            <span style="background:{label_color}; color:white; padding:2px 10px; border-radius:6px; font-weight:bold; font-size:12px;">{letra_res}</span>
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

        # --- 2. MI ESTADO DE FORMA (Métricas + Historial) ---
        st.subheader("🎾 Mi Estado de Forma")
        
        # Filtramos todos tus partidos confirmados
        todos_mis_p = df_partidos[
            ((df_partidos['Ganador'] == nombre_u) | (df_partidos['Perdedor'] == nombre_u)) & 
            (df_partidos['Estado'] == 'Confirmado')
        ]

        if not todos_mis_p.empty:
            # Cálculo de Métricas Globales
            total_juegos = len(todos_mis_p)
            victorias = len(todos_mis_p[todos_mis_p['Ganador'] == nombre_u])
            tasa_win = (victorias / total_juegos) * 100

            # Diseño de Métricas Superiores
            m1, m2 = st.columns(2)
            m1.metric("Partidos Totales", total_juegos)
            m2.metric("Tasa de Victorias", f"{tasa_win:.1f}%")
            
            st.write("") # Espacio estético

            # Mostrar tus últimos 5 partidos con diseño estético
            mis_5 = todos_mis_p.sort_index(ascending=False).head(5)
            for _, fila in mis_5.iterrows():
                res = "✅ Ganaste" if fila['Ganador'] == nombre_u else "❌ Perdiste"
                rival = fila['Perdedor'] if fila['Ganador'] == nombre_u else fila['Ganador']
                render_tarjeta_tenis(rival, fila['Score'], res)
        else:
            st.info("Aún no tienes partidos registrados para calcular estadísticas.")

        st.divider()

        # --- 3. SCOUTING DE RIVALES ---
        st.subheader("🔍 Scouting de Jugadores")
        
        # Lista de jugadores (excluyéndote a ti y filtrando por tu categoría)
        lista_scouting = sorted(df_jugadores[
            (df_jugadores['Categoria'] == cat_u) & (df_jugadores['Nombre'] != nombre_u)
        ]['Nombre'].unique())
        
        rival_analizar = st.selectbox("Selecciona un jugador para analizar:", ["Seleccionar..."] + list(lista_scouting))

        if rival_analizar != "Seleccionar...":
            # Historial del Rival Seleccionado
            st.markdown(f"#### 📈 Forma de {rival_analizar}")
            p_rival = df_partidos[
                ((df_partidos['Ganador'] == rival_analizar) | (df_partidos['Perdedor'] == rival_analizar)) & 
                (df_partidos['Estado'] == 'Confirmado')
            ].sort_index(ascending=False).head(5)

            if not p_rival.empty:
                for _, fila in p_rival.iterrows():
                    res_rival = "🟢 Ganó" if fila['Ganador'] == rival_analizar else "🔴 Perdió"
                    oponente = fila['Perdedor'] if fila['Ganador'] == rival_analizar else fila['Ganador']
                    render_tarjeta_tenis(oponente, fila['Score'], res_rival)
            else:
                st.write("Este jugador no tiene partidos registrados.")

            st.write("") # Espacio

            # --- 4. H2H Y PREDICCIÓN IA ---
            st.markdown(f"#### ⚔️ Cara a Cara: {nombre_u} vs {rival_analizar}")
            
            # Cálculo de enfrentamientos directos
            h2h = df_partidos[
                ((df_partidos['Ganador'] == nombre_u) & (df_partidos['Perdedor'] == rival_analizar)) |
                ((df_partidos['Ganador'] == rival_analizar) & (df_partidos['Perdedor'] == nombre_u))
            ]
            mis_victorias = len(h2h[h2h['Ganador'] == nombre_u])
            sus_victorias = len(h2h[h2h['Ganador'] == rival_analizar])

            # Tarjeta H2H Estética (Fight Card)
            st.markdown(f'''
                <div style="background: linear-gradient(145deg, #161b22, #1e2530); padding:20px; border-radius:15px; border: 1px solid #30363d; margin-bottom:20px;">
                    <div style="display:flex; justify-content:space-around; align-items:center; text-align:center;">
                        <div>
                            <p style="margin:0; color:#888; font-size:12px;">Tus Victorias</p>
                            <h2 style="margin:0; color:#00ffcc; font-size:28px;">{mis_victorias}</h2>
                        </div>
                        <div style="font-weight:bold; color:#444; font-size:20px;">VS</div>
                        <div>
                            <p style="margin:0; color:#888; font-size:12px;">Victorias Rival</p>
                            <h2 style="margin:0; color:#ff1744; font-size:28px;">{sus_victorias}</h2>
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

            # Análisis de Probabilidad IA
            st.markdown("#### Probabilidad De Victoria")
            p1, p2 = calcular_probabilidad_ia(nombre_u, rival_analizar, df_partidos)
            
            # Seguros para evitar errores en celular
            p1 = max(0.1, p1 if p1 is not None else 50.0)
            p2 = max(0.1, p2 if p2 is not None else 50.0)

            st.progress(p1/100)
            
            col_ia1, col_ia2 = st.columns(2)
            col_ia1.metric(nombre_u, f"{p1:.1f}%")
            col_ia2.metric(rival_analizar, f"{p2:.1f}%")

            # Veredicto Final
            if p1 > p2:
                st.success(f"🔥 Favorito: **{nombre_u}**. Tienes mejores métricas frente a este rival.")
            else:
                st.warning(f"⚠️ Favorito: **{rival_analizar}**. El rival llega en mejor posición estadística.")

    # **************************************************************************
    with tab4:
        st.subheader("📣 Juez de Silla")
        ahora = datetime.now()

        # --- 1. VALIDACIÓN DE ENTORNO ---
        if 'fase_actual' not in locals():
            st.error("⚠️ No se pudo cargar la configuración del torneo. Reintenta el ingreso.")
        else:
            # Determinamos si la fase de grupos está cerrada por fecha
            fase_grupos_cerrada = ahora > fecha_limite

            # --- 2. GESTIÓN DE PENDIENTES (Confirmaciones del Perdedor) ---
            st.markdown("### 📥 Mis Validaciones Pendientes")
            df_partidos_tmp = df_partidos.copy()
            
            mis_pendientes = df_partidos_tmp[
                (df_partidos_tmp['Perdedor'] == nombre_u) & 
                (df_partidos_tmp['Estado'] == 'Pendiente') &
                (df_partidos_tmp['Torneo'] == torneo_u)
            ]

            if not mis_pendientes.empty:
                for idx, fila in mis_pendientes.iterrows():
                    with st.container(border=True):
                        st.write(f"🎾 **{fila['Ganador']}** reportó victoria contra ti: `{fila['Score']}`")
                        st.caption(f"Fase: {fila['Fase']} | Fecha: {fila['Fecha']}")
                        
                        col_ok, col_no = st.columns(2)
                        if col_ok.button("✅ Confirmar", key=f"btn_ok_{idx}", use_container_width=True):
                            df_partidos_tmp.at[idx, 'Estado'] = 'Confirmado'
                            conn.update(spreadsheet=SHEET_URL, worksheet="Reportes", data=df_partidos_tmp)
                            st.success("¡Resultado validado!")
                            st.balloons()
                            time.sleep(1)
                            st.rerun()
                        
                        if col_no.button("❌ Rechazar", key=f"btn_no_{idx}", use_container_width=True):
                            df_partidos_tmp.at[idx, 'Estado'] = 'Rechazado'
                            conn.update(spreadsheet=SHEET_URL, worksheet="Reportes", data=df_partidos_tmp)
                            st.error("Has rechazado el reporte.")
                            time.sleep(1)
                            st.rerun()
            else:
                st.success("✅ ¡Estás al día con tus confirmaciones!")

            st.divider()

            # --- 3. SUBIR NUEVO RESULTADO (LÓGICA CORREGIDA PARA PLAYOFFS) ---
            st.markdown(f"### 🚀 Reportar Resultado")
            
            # Buscamos si el usuario tiene un cruce asignado en la hoja de CRUCES
            mi_cruce_playoff = df_cruces_maestros[
                (df_cruces_maestros['Torneo'] == torneo_u) &
                (df_cruces_maestros['Categoria'] == cat_u) & 
                ((df_cruces_maestros['Jugador1'] == nombre_u) | (df_cruces_maestros['Jugador2'] == nombre_u))
            ]

            # ¿Es fase de grupos o ya estamos en playoffs (basado en si hay cruces generados)?
            es_playoff = not mi_cruce_playoff.empty

            # Solo bloqueamos si es Grupos y ya pasó la fecha. Si es Playoff, dejamos reportar.
            if "Grupos" in fase_actual and fase_grupos_cerrada and not es_playoff:
                st.error(f"🚫 **Fase de Grupos Cerrada:** Terminó el {fecha_limite.strftime('%d/%m %H:%M')}.")
                st.info("Espera a que el administrador publique los cruces oficiales para reportar tu siguiente partido.")
            else:
                label_fase = "Playoffs" if es_playoff else fase_actual
                with st.expander(f"➕ Registrar victoria en {label_fase}", expanded=True):
                    
                    lista_rivales = []
                    fase_reporte = fase_actual # Por defecto

                    if es_playoff:
                        # LÓGICA DE PLAYOFFS: Sacamos el rival de la fila de CRUCES
                        fila_c = mi_cruce_playoff.iloc[0]
                        rival_oficial = fila_c['Jugador2'] if fila_c['Jugador1'] == nombre_u else fila_c['Jugador1']
                        fase_reporte = fila_c['Fase'] # Ej: "Octavos", "Cuartos"...
                        st.info(f"🏆 **Rival de Llave:** {rival_oficial} ({fase_reporte})")
                        lista_rivales = [rival_oficial]
                    else:
                        # LÓGICA DE GRUPOS: Filtro normal por grupo
                        df_riv = df_jugadores[
                            (df_jugadores['Torneo'] == torneo_u) & 
                            (df_jugadores['Grupo'].astype(str) == str(grupo_u)) & 
                            (df_jugadores['Nombre'] != nombre_u)
                        ]
                        lista_rivales = df_riv['Nombre'].unique().tolist()

                    # --- FORMULARIO DE ENVÍO ---
                    with st.form("nuevo_reporte", clear_on_submit=True):
                        rival = st.selectbox("¿A quién le ganaste?", lista_rivales) if lista_rivales else None
                        c1, c2 = st.columns(2)
                        m_j = c1.number_input("Mis Juegos", 0, 15, 8)
                        s_j = c2.number_input("Sus Juegos", 0, 15, 0)
                        
                        btn_enviar = st.form_submit_button("Subir Resultado", use_container_width=True)

                        if btn_enviar and rival:
                            if m_j <= s_j:
                                st.error("Solo el ganador puede reportar el partido.")
                            else:
                                # VALIDACIÓN DE DUPLICADOS (Evitar reportar 2 veces el mismo cruce)
                                duplicado = df_partidos[
                                    (df_partidos['Torneo'] == torneo_u) & 
                                    (df_partidos['Fase'] == fase_reporte) & 
                                    (df_partidos['Estado'] != 'Rechazado') & 
                                    (
                                        ((df_partidos['Ganador'] == nombre_u) & (df_partidos['Perdedor'] == rival)) | 
                                        ((df_partidos['Ganador'] == rival) & (df_partidos['Perdedor'] == nombre_u))
                                    )
                                ]

                                if not duplicado.empty:
                                    st.warning(f"⚠️ Este partido ya fue registrado.")
                                else:
                                    nueva_data = pd.DataFrame([{
                                        "Fecha": ahora.strftime("%d/%m/%Y %H:%M"),
                                        "Ganador": nombre_u,
                                        "Perdedor": rival,
                                        "Score": f"{m_j}-{s_j}",
                                        "Estado": "Pendiente",
                                        "Categoria": cat_u,
                                        "Grupo": grupo_u,
                                        "Torneo": torneo_u,
                                        "Fase": fase_reporte
                                    }])
                                    
                                    df_actualizado = pd.concat([df_partidos, nueva_data], ignore_index=True)
                                    conn.update(spreadsheet=SHEET_URL, worksheet="Reportes", data=df_actualizado)
                                    
                                    # Notificación WhatsApp
                                    try:
                                        tel_r = df_jugadores[df_jugadores['Nombre'] == rival]['Telefono'].values[0]
                                        tel_clean = str(tel_r).replace(" ", "").split('.')[0]
                                        msg_wa = urllib.parse.quote(f"🎾 *Tennis Hub*\n{nombre_u} reportó victoria {m_j}-{s_j}.\n¡Confirma en la app!")
                                        st.markdown(f'''<a href="https://wa.me/{tel_clean}?text={msg_wa}" target="_blank" style="text-decoration:none;">
                                            <div style="background-color:#25D366; color:white; padding:10px; border-radius:10px; text-align:center; font-weight:bold;">📲 Notificar Rival por WhatsApp</div></a>''', unsafe_allow_html=True)
                                    except:
                                        pass
                                    
                                    st.success("✅ ¡Reporte enviado con éxito!")
                                    st.cache_data.clear()
                                    time.sleep(2)
                                    st.rerun()
# --- TAB 5: CUADRO FINAL (LÓGICA PROFESIONAL ADAPTATIVA) ---
    # **************************************************************************
    # --- TAB 5: CUADRO FINAL (LÓGICA PROFESIONAL ADAPTATIVA + PANEL ADMIN) ---
    # **************************************************************************
    with tab5:
        st.header("✨Llave Pro (Ranking Profesional)✨")
        
        # 1. Selector de tipo de llave para la VISUALIZACIÓN
        tipo_llave = st.pills(
            "Ver Proyección de:", 
            ["🏆 Principal", "🥈 Llave Intermedia"],
            default="🏆 Principal"
        )

        # 2. GENERAR CUADRO VISUAL (Proyección en vivo)
        # --------------------------------------------------------------------------
        if st.button("✨ Generar Cuadro Visual"):
            todos_jugadores = df_jugadores[df_jugadores['Categoria'] == cat_u]
            clasificados_A = []
            clasificados_B = []
            
            grupos_activos = sorted(todos_jugadores['Grupo'].unique())
            
            for grp in grupos_activos:
                df_res = calcular_ranking_grupo(df_jugadores, df_partidos, cat_u, grp)
                if len(df_res) >= 2:
                    clasificados_A.extend([df_res.iloc[0].to_dict(), df_res.iloc[1].to_dict()])
                if len(df_res) >= 4:
                    clasificados_B.extend([df_res.iloc[2].to_dict(), df_res.iloc[3].to_dict()])

            lista_final = clasificados_A if "Principal" in tipo_llave else clasificados_B
            
            # Ordenamos por mérito (Ranking General de la fase de grupos)
            df_f = pd.DataFrame(lista_final).sort_values(by=['Puntos', 'DJ', 'JG'], ascending=False).reset_index(drop=True)

            if len(df_f) < 2:
                st.warning("Faltan resultados para proyectar la llave.")
            else:
                n = len(df_f)
                # Determinamos fase según cantidad de clasificados
                if n >= 16: limite, titulo_fase, orden_indices = 16, "Octavos de Final", [(0,15), (7,8), (4,11), (3,12), (1,14), (6,9), (5,10), (2,13)]
                elif n >= 8: limite, titulo_fase, orden_indices = 8, "Cuartos de Final", [(0,7), (3,4), (1,6), (2,5)]
                elif n >= 4: limite, titulo_fase, orden_indices = 4, "Semifinales", [(0,3), (1,2)]
                else: limite, titulo_fase, orden_indices = 2, "Gran Final", [(0,1)]
                
                df_llave = df_f.head(limite)
                st.subheader(f"🏆 {titulo_fase} - {tipo_llave}")

                # Mostramos los cruces con el diseño HTML
                for i, (idx_top, idx_bot) in enumerate(orden_indices):
                    j1 = df_llave.iloc[idx_top]
                    j2 = df_llave.iloc[idx_bot]
                    
                    # Etiqueta para saber en qué lado del cuadro están
                    lado = "Lado A (Arriba)" if i < (len(orden_indices)/2) else "Lado B (Abajo)"
                    st.caption(f"🎾 Encuentro {i+1} - {lado}")

                    st.markdown(f"""
                    <div style="border: 1px solid #666; border-radius: 10px; padding: 15px; margin-bottom: 10px; background-color: rgba(255, 255, 255, 0.05);">
                        <div style="display: flex; justify-content: space-between;">
                            <span><b>{j1['Nombre']}</b></span>
                            <span style="color: #4CAF50; font-size: 0.8em; font-weight: bold;">RANKING #{idx_top+1}</span>
                        </div>
                        <hr style="margin: 10px 0; border: 0; border-top: 1px solid #444;">
                        <div style="display: flex; justify-content: space-between;">
                            <span><b>{j2['Nombre']}</b></span>
                            <span style="color: #aaa; font-size: 0.8em;">RANKING #{idx_bot+1}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # 3. PANEL DE ADMINISTRADOR (Escritura en Excel)
        # --------------------------------------------------------------------------
        st.write("")
        st.write("---")
        with st.expander("🔐 PANEL DE CONTROL: Publicar Cruces"):
            clave = st.text_input("Clave Maestra:", type="password", key="admin_key_llave")
            
            if clave == "1234":
                if st.button("🚀 Publicar a Hoja CRUCES", use_container_width=True):
                    # 1. Recalcular TODO (Principal e Intermedia) para subir al Excel
                    todos_j = df_jugadores[df_jugadores['Categoria'] == cat_u]
                    cA, cB = [], []
                    for g in sorted(todos_j['Grupo'].unique()):
                        df_r = calcular_ranking_grupo(df_jugadores, df_partidos, cat_u, g)
                        if len(df_r) >= 2: cA.extend([df_r.iloc[0].to_dict(), df_r.iloc[1].to_dict()])
                        if len(df_r) >= 4: cB.extend([df_r.iloc[2].to_dict(), df_r.iloc[3].to_dict()])

                    def obtener_filas_excel(lista, tipo_label):
                        df_temp = pd.DataFrame(lista).sort_values(by=['Puntos', 'DJ', 'JG'], ascending=False).reset_index(drop=True)
                        n_t = len(df_temp)
                        if n_t < 2: return []
                        
                        if n_t >= 16: lim, f_t, ord_i = 16, "Octavos", [(0,15), (7,8), (4,11), (3,12), (1,14), (6,9), (5,10), (2,13)]
                        elif n_t >= 8: lim, f_t, ord_i = 8, "Cuartos", [(0,7), (3,4), (1,6), (2,5)]
                        elif n_t >= 4: lim, f_t, ord_i = 4, "Semifinales", [(0,3), (1,2)]
                        else: lim, f_t, ord_i = 2, "Final", [(0,1)]
                        
                        df_l = df_temp.head(lim)
                        return [{"Torneo": torneo_u, "Categoria": cat_u, "Tipo_Llave": tipo_label, 
                                "Jugador1": df_l.iloc[it]['Nombre'], "Jugador2": df_l.iloc[ib]['Nombre'], "Fase": f_t} 
                                for it, ib in ord_i]

                    # Consolidar todas las filas
                    data_subir = obtener_filas_excel(cA, "Principal") + obtener_filas_excel(cB, "Intermedia")
                    
                    if data_subir:
                        # Limpiar cruces viejos de esta categoría/torneo y subir nuevos
                        df_cruces_limpio = df_cruces_maestros[~((df_cruces_maestros['Torneo'] == torneo_u) & (df_cruces_maestros['Categoria'] == cat_u))]
                        df_final = pd.concat([df_cruces_limpio, pd.DataFrame(data_subir)], ignore_index=True)
                        
                        conn.update(spreadsheet=SHEET_URL, worksheet="CRUCES", data=df_final)
                        st.success("✅ Cruces publicados. Ahora los jugadores pueden reportar en Juez de Silla.")
                        st.cache_data.clear()
                        time.sleep(1)
                        st.rerun()
# ******************************************************************************
# INICIO DE LA APLICACIÓN
# ******************************************************************************
if __name__ == "__main__":
    main()