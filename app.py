import streamlit as st
from CoolProp.CoolProp import PropsSI

st.set_page_config(page_title="Controle de Qualidade - Linha Contínua", layout="wide")

st.title("🏭 Sistema de Conferência e Qualidade de Fabricação")
st.markdown("Controle Avançado para Máquinas Contínuas, Racks e Tanques Industriais.")

st.divider()

# --- BLOCO 1: DADOS COMPLETOS, MODELO DA MÁQUINA E TENSÃO ---
st.subheader("📋 Identificação da Máquina e Fluidos")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    cliente = st.text_input("Nome do Cliente:")
with col2:
    num_serie = st.text_input("Número de Série / OS:")
with col3:
    modelo_maquina = st.selectbox(
        "Modelo da Máquina:", 
        [
            "Contínua 200", 
            "Contínua 300", 
            "Contínua 400", 
            "Contínua 600", 
            "Contínua 1000", 
            "Contínua Tripla", 
            "Picoleteira 2000", 
            "Picoleteira 4000", 
            "Picoleteira 10000", 
            "Outro Modelo"
        ]
    )
with col4:
    gas_tipo = st.selectbox("Tipo de Gás:", ["R507A", "R404A", "R22", "R134a", "R717"])
with col5:
    carga_gas = st.number_input("Carga de Gás (kg):", value=0.0, step=0.5)

# Linha extra para a Tensão
st.write("")
col_tensao = st.columns(3)
with col_tensao[0]:
    tensao = st.selectbox("Tensão de Alimentação da Máquina:", ["220V Trifásico", "380V Trifásico", "220V Monofásico"])

st.divider()

# --- BLOCO 2: PARTE ELÉTRICA E CORRENTES DOS MOTORES ---
st.subheader("⚡ Monitoramento Elétrico e Correntes em Regime de Trabalho")
st.markdown("Registre a corrente (A) de cada motor. Em máquinas contínuas, a corrente do batedor define a firmeza e o ponto exato do sorvete.")

col_elec1, col_elec2, col_elec3 = st.columns(3)

with col_elec1:
    corrente_comp = st.number_input("Corrente do Compressor (A):", value=0.0, step=0.1, key="curr_comp")
    st.caption("Monitore o consumo das fases do compressor de refrigeração.")

with col_elec2:
    corrente_batedor = st.number_input("Corrente do Batedor / Raspador (A):", value=0.0, step=0.1, key="curr_bat")
    st.caption("Indica a força do motor de rotação das facas raspadoras dentro do cilindro.")

with col_elec3:
    corrente_bombas = st.number_input("Corrente das Bombas / Coletora (A):", value=0.0, step=0.1, key="curr_bomb")
    st.caption("Para bomba de calda (Contínuas), bomba de engrenagem ou bomba de circulação.")

st.divider()

# --- BLOCO 3: PROCESSO DE VÁCUO (COM ALERTAS COLORIDOS) ---
st.subheader("🌪️ Processo de Vácuo (Desidratação do Circuito)")
col_vac1, col_vac2, col_vac3 = st.columns(3)

with col_vac1:
    data_vac = st.date_input("Data do Vácuo:")
with col_vac2:
    vacuo_atingido = st.number_input("Vácuo Atingido (Microns):", value=0, step=50)
with col_vac3:
    if vacuo_atingido > 0:
        if vacuo_atingido < 500:
            st.success("🟢 Vácuo Excelente! (Abaixo de 500 microns)")
        elif 500 <= vacuo_atingido <= 700:
            st.warning("🟡 Vácuo Aceitável. (Entre 500 e 700 microns - Monitorar)")
        else:
            st.error("🔴 ALERTA: Vácuo Ruim! (Acima de 700 microns - Requer atenção)")

st.divider()

# --- BLOCO 4: TESTE DE ESTANQUEIDADE COM COMPARATIVO TÉRMICO ---
st.subheader("🛡️ Teste de Estanqueidade (Pressurização com Nitrogênio)")
st.markdown("Insira os dados do início e do final do teste para o cálculo automático de compensação de temperatura.")

col_dia1, col_dia2 = st.columns(2)

with col_dia1:
    st.markdown("### 🔴 INÍCIO (Dia 1)")
    data_ini = st.date_input("Data Inicial:", key="dat_ini")
    # Alterado o step para 1.0 para subir de 1 em 1 PSI
    p_ini = st.number_input("Pressão Inicial de Teste (PSI):", value=0.0, step=1.0, key="p1")
    t_ini = st.number_input("Temperatura Ambiente Inicial (°C):", value=25.0, step=0.5, key="t1")

with col_dia2:
    st.markdown("### 🔵 FINAL (Dia 2)")
    data_fim = st.date_input("Data Final:", key="dat_fim")
    # Alterado o step para 1.0 para subir de 1 em 1 PSI
    p_fim = st.number_input("Pressão Final Medida (PSI):", value=0.0, step=1.0, key="p2")
    t_fim = st.number_input("Temperatura Ambiente Final (°C):", value=25.0, step=0.5, key="t2")

# Cálculo de Variação Térmica Inteligente
if p_ini > 0:
    t1_k = t_ini + 273.15
    t2_k = t_fim + 273.15
    p1_abs = p_ini + 14.7
    p2_abs_medida = p_fim + 14.7
    
    p2_abs_esperada = p1_abs * (t2_k / t1_k)
    p2_manometrica_esperada = p2_abs_esperada - 14.7
    diferenca = p_fim - p2_manometrica_esperada
    
    st.divider()
    st.subheader("📊 Diagnóstico do Teste de Estanqueidade")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric(
            label="Pressão Esperada por Física (Corrigida pela Temp.)", 
            value=f"{p2_manometrica_esperada:.1f} PSI",
            delta=f"Variação térmica ideal: {(p2_manometrica_esperada - p_ini):.1f} PSI"
        )
    
    with col_res2:
        if diferenca >= -1.5:
            st.success(f"✅ ESTANQUEIDADE APROVADA! A variação foi normal devido ao clima (Diferença de apenas {diferenca:.1f} PSI).")
        else:
            st.error(f"❌ ALERTA DE VAZAMENTO! A pressão caiu {abs(diferenca):.1f} PSI a mais do que a temperatura justifica.")

st.divider()

# Bloco Final de Observações e Geração do Relatório
obs = st.text_area("Observações Gerais / Anotações da Inspeção:")

# Botão para salvar em PDF / Imprimir
st.markdown(
    """
    <button onclick="window.print()" style="
        width: 100%; 
        background-color: #00CC66; 
        color: white; 
        padding: 15px; 
        border: none; 
        border-radius: 4px; 
        cursor: pointer;
        font-weight: bold;
        font-size: 16px;
    ">
        🖨️ Finalizar e Gerar PDF do Checklist
    </button>
    """, 
    unsafe_allow_html=True
)
