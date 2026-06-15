import streamlit as st
import sys
import os
import pandas as pd
import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.storage import (
    init_db,
    salvar_medicamento,
    listar_medicamentos,
    marcar_medicamento_tomado,
    salvar_agua,
    buscar_total_agua_hoje,
    buscar_historico_agua_semanal,
    buscar_historico_medicamentos_semanal
)

st.set_page_config(
    page_title="CareTrack - Dashboard de Saúde",
    page_icon="💊",
    layout="wide"
)

try:
    init_db()
except Exception as e:
    st.error(f"⚠️ Erro ao conectar à base de dados Supabase: {e}")

META_AGUA = 2000

DICAS_SAUDE = [
    "💧 **Hidratação constante:** Idosos sentem menos sede. Ofereça água em pequenos intervalos, mesmo que não a peçam!",
    "💊 **Organização é tudo:** Mantenha os medicamentos nas caixas originais ou use organizadores semanais identificados por cores.",
    "🚶‍♂️ **Atividade física leve:** Caminhadas curtas e alongamentos diários ajudam a manter a mobilidade e a saúde cardiovascular.",
    "🩺 **Anotações médicas:** Registe qualquer sintoma diferente ou efeito colateral para relatar ao médico na próxima consulta.",
    "🍉 **Alimentos ricos em água:** Frutas como melancia, melão, morango e laranja são excelentes aliadas para complementar a hidratação diária.",
    "🛡️ **Segurança doméstica:** Garanta caminhos livres de tapetes soltos e melhore a iluminação nos corridors para evitar quedas à noite.",
    "🧠 **Estímulo cognitivo:** Atividades como leitura, palavras cruzadas ou jogos de tabuleiro ajudam a exercitar a mente diariamente."
]

st.title("CareTrack 💊💧")
st.subheader("Gestor de Rotina Integrado para Idosos e Cuidadores")

dia_do_ano = datetime.date.today().timetuple().tm_yday
dica_do_dia = DICAS_SAUDE[dia_do_ano % len(DICAS_SAUDE)]
st.info(f"💡 **Dica de Saúde do Dia:** {dica_do_dia}")

aba_diaria, aba_semanal = st.tabs(["📋 Controlo Diário", "📈 Relatório Semanal (Etapa 3)"])

with aba_diaria:
    col_esquerda, col_direita = st.columns(2)

    with col_esquerda:
        st.header("💧 Hidratação")
        
        try:
            total_agua = buscar_total_agua_hoje()
        except Exception as e:
            st.error(f"Erro ao buscar consumo de água: {e}")
            total_agua = 0

        percentual_agua = min(total_agua / META_AGUA, 1.0)
        percentual_exibido = int(percentual_agua * 100)
        
        st.metric(
            label="Água Consumida Hoje", 
            value=f"{total_agua} ml", 
            delta=f"{max(0, META_AGUA - total_agua)} ml restantes para a meta" if total_agua < META_AGUA else "🎉 Meta Atingida!"
        )
        
        st.progress(percentual_agua)
        st.write(f"**Progresso:** {percentual_exibido}% da meta de {META_AGUA} ml")
        
        if total_agua >= META_AGUA:
            st.success("🎉 Sensacional! Meta diária de água concluída!")
            st.balloons()

        st.markdown("---")
        st.write("➕ **Registar Água:**")
        
        col_copo, col_garrafa = st.columns(2)
        with col_copo:
            if st.button("🥤 Copo (250 ml)", use_container_width=True, key="btn_copo"):
                try:
                    salvar_agua(250)
                    st.toast("Copo de 250ml registado com sucesso!", icon="💧")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao registar: {e}")
                    
        with col_garrafa:
            if st.button("🍼 Garrafa (500 ml)", use_container_width=True, key="btn_garrafa"):
                try:
                    salvar_agua(500)
                    st.toast("Garrafa de 500ml registada com sucesso!", icon="💧")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao registar: {e}")

        quantidade_manual = st.number_input("Ou digite uma quantidade personalizada (ml):", min_value=0, step=50, key="manual_agua")
        if st.button("Registar ml Personalizado", use_container_width=True, key="btn_manual"):
            if quantidade_manual > 0:
                try:
                    salvar_agua(int(quantidade_manual))
                    st.toast(f"{quantidade_manual}ml registados com sucesso!", icon="💧")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao registar: {e}")
            else:
                st.warning("Insira um valor válido maior que zero.")

    with col_direita:
        st.header("💊 Medicamentos")
        
        try:
            lista_meds = listar_medicamentos()
        except Exception as e:
            st.error(f"Erro ao buscar medicamentos: {e}")
            lista_meds = []

        if not lista_meds:
            st.info("Nenhum medicamento agendado para o dia de hoje.")
        else:
            st.write("Marque as caixas abaixo para confirmar a toma:")
            for med in lista_meds:
                med_id, nome, horario, concluido = med
                texto_checkbox = f"⏱️ **{horario}** - {nome}"
                
                checkbox_selecionado = st.checkbox(
                    texto_checkbox, 
                    value=concluido, 
                    key=f"med_{med_id}",
                    disabled=concluido
                )
                
                if checkbox_selecionado and not concluido:
                    try:
                        marcar_medicamento_tomado(med_id)
                        st.toast(f"Parabéns! Tomou o medicamento: {nome}", icon="✅")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao registar toma do medicamento: {e}")

        st.markdown("---")
        st.write("➕ **Agendar Novo Medicamento:**")
        
        with st.form("form_medicamento", clear_on_submit=True):
            novo_nome = st.text_input("Nome do Medicamento:")
            novo_horario = st.text_input("Horário (ex: 08:00):")
            
            enviar_form = st.form_submit_button("Agendar Medicamento", use_container_width=True)
            if enviar_form:
                if novo_nome.strip() and novo_horario.strip():
                    try:
                        salvar_medicamento(novo_nome.strip(), novo_horario.strip())
                        st.success(f"Medicamento '{novo_nome}' agendado para as {novo_horario}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar: {e}")
                else:
                    st.warning("Preencha todos os campos do formulário!")


with aba_semanal:
    st.header("📈 Acompanhamento Semanal de Saúde")
    st.write("Esta secção compila os registos dos últimos 7 dias para análise de consistência e adesão ao tratamento.")

    df_agua_analise = pd.DataFrame()
    try:
        dados_agua = buscar_historico_agua_semanal()
        if dados_agua:
            df_agua_analise = pd.DataFrame(dados_agua, columns=["Data", "Consumido (ml)"])
            df_agua_analise["Data"] = pd.to_datetime(df_agua_analise["Data"]).dt.strftime('%d/%m')
            df_agua_analise = df_agua_analise.set_index("Data")
    except Exception as e:
        st.error(f"Erro ao processar dados de água: {e}")

    df_meds_analise = pd.DataFrame()
    try:
        dados_meds = buscar_historico_medicamentos_semanal()
        if dados_meds:
            df_bruto = pd.DataFrame(dados_meds, columns=["Data", "Concluido", "Quantidade"])
            df_bruto["Data"] = pd.to_datetime(df_bruto["Data"]).dt.strftime('%d/%m')
            
            df_pivot = df_bruto.pivot(index="Data", columns="Concluido", values="Quantidade").fillna(0)
            df_pivot = df_pivot.rename(columns={True: "Tomados", False: "Esquecidos"})
            
            if "Tomados" not in df_pivot.columns:
                df_pivot["Tomados"] = 0
            if "Esquecidos" not in df_pivot.columns:
                df_pivot["Esquecidos"] = 0
                
            df_meds_analise = df_pivot[["Tomados", "Esquecidos"]].astype(int)
    except Exception as e:
        st.error(f"Erro ao processar dados de medicamentos: {e}")

    if not df_agua_analise.empty and not df_meds_analise.empty:
        st.markdown("---")
        st.subheader("🎯 Visão Geral de Metas Combinadas")
        
        df_combinado = df_agua_analise.join(df_meds_analise, how="inner")
        
        if not df_combinado.empty:
            df_combinado["Meta Água Concluída"] = df_combinado["Consumido (ml)"] >= META_AGUA
            df_combinado["Remédios Concluídos"] = df_combinado["Esquecidos"] == 0
            df_combinado["Dia Perfeito"] = df_combinado["Meta Água Concluída"] & df_combinado["Remédios Concluídos"]
            
            dias_perfeitos = df_combinado["Dia Perfeito"].sum()
            total_dias_comb = len(df_combinado)
            
            col_perf1, col_perf2 = st.columns([1, 2])
            with col_perf1:
                st.metric(
                    label="🥇 Dias Perfeitos na Semana", 
                    value=f"{dias_perfeitos} / {total_dias_comb}"
                )
            with col_perf2:
                if dias_perfeitos == total_dias_comb:
                    st.success("🌟 Incrível! Todos os dias avaliados foram perfeitos! Excelente cuidado!")
                elif dias_perfeitos >= (total_dias_comb / 2):
                    st.info("👍 Bom desempenho! A rotina está no caminho certo, continue firme.")
                else:
                    st.warning("⚠️ Atenção: Menos da metade dos dias cumpriram ambas as metas. Vale a pena rever os alarmes.")

            df_grafico_metas = df_combinado[["Meta Água Concluída", "Remédios Concluídos"]].astype(int)
            df_grafico_metas.columns = ["Meta de Água (≥2000ml)", "Todos os Remédios Tomados"]
            
            st.write("**Gráfico de Cumprimento Diário de Metas:** (1 = Sucesso, 0 = Incompleto)")
            st.line_chart(df_grafico_metas)
        st.markdown("---")

    col_graf_agua, col_graf_meds = st.columns(2)

    with col_graf_agua:
        st.subheader("💧 Consumo Diário de Água vs Meta")
        if df_agua_analise.empty:
            st.info("Ainda não existem registos de água nos últimos 7 dias.")
        else:
            df_agua_exibir = df_agua_analise.copy()
            df_agua_exibir["Meta (2000 ml)"] = META_AGUA
            st.bar_chart(df_agua_exibir)
            
            dias_meta_batida = sum(1 for consumo in df_agua_analise["Consumido (ml)"] if consumo >= META_AGUA)
            st.write(f"💡 **Análise:** O idoso atingiu a meta de água em **{dias_meta_batida} de {len(df_agua_analise)} dias** registados.")

    with col_graf_meds:
        st.subheader("💊 Adesão aos Medicamentos")
        if df_meds_analise.empty:
            st.info("Ainda não existem registos de medicamentos nos últimos 7 dias.")
        else:
            st.bar_chart(df_meds_analise)
            
            total_tomados = df_meds_analise["Tomados"].sum()
            total_esquecidos = df_meds_analise["Esquecidos"].sum()
            total_geral = total_tomados + total_esquecidos
            taxa_adesao = (total_tomados / total_geral * 100) if total_geral > 0 else 0
            
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Total de Tomas Concluídas", f"{total_tomados} doses")
            with col_m2:
                st.metric("Adesão Geral do Período", f"{taxa_adesao:.1f}%")
                
            if taxa_adesao >= 90:
                st.success("🌟 Excelente nível de adesão! O tratamento está a ser cumprido rigorosamente.")
            elif taxa_adesao >= 70:
                st.warning("⚠️ Adesão moderada. Fique atento para evitar esquecimentos frequentes.")
            else:
                st.error("🚨 Atenção! Nível de adesão crítico. Recomenda-se rever os alertas e horários.")