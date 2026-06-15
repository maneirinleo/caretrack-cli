import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.storage import (
    init_db,
    salvar_medicamento,
    listar_medicamentos,
    marcar_medicamento_tomado,
    salvar_agua,
    buscar_total_agua_hoje
)

st.set_page_config(
    page_title="CareTrack - Controle de Saúde",
    page_icon="💊",
    layout="centered"
)

# inicializa as tabelas do db
try:
    init_db()
except Exception as e:
    st.error(f"⚠️ Erro ao conectar ao banco de dados Supabase: {e}")

META_AGUA = 2000

st.title("CareTrack 💊💧")
st.subheader("Gerenciador de Rotina para Idosos e Cuidadores")

# criando duas colunas principais no painel
col_esquerda, col_direita = st.columns(2)

with col_esquerda:
    st.header("💧 Hidratação")
    
    # busca dados atualizados do banco
    try:
        total_agua = buscar_total_agua_hoje()
    except Exception as e:
        st.error(f"Erro ao buscar consumo de água: {e}")
        total_agua = 0

    # calcula percentual para a barra de progresso
    percentual_agua = min(total_agua / META_AGUA, 1.0)
    percentual_exibido = int(percentual_agua * 100)
    
    # exibe informações de consumo
    st.metric(
        label="Água Consumida Hoje", 
        value=f"{total_agua} ml", 
        delta=f"{max(0, META_AGUA - total_agua)} ml restantes para a meta" if total_agua < META_AGUA else "🎉 Meta Batida!"
    )
    
    # Barra de Progresso visual
    st.progress(percentual_agua)
    st.write(f"**Progresso:** {percentual_exibido}% da meta de {META_AGUA} ml")
    
    # comemoração interativa se atingir a meta
    if total_agua >= META_AGUA:
        st.success("🎉 Sensacional! Meta diária de água concluída!")
        st.balloons()

    # registro rápido de água
    st.markdown("---")
    st.write("➕ **Registrar Água:**")
    
    # botões de clique rápido
    col_copo, col_garrafa = st.columns(2)
    with col_copo:
        if st.button("🥤 Copo (250 ml)", use_container_width=True):
            try:
                salvar_agua(250)
                st.toast("Copo de 250ml registrado com sucesso!", icon="💧")
                st.rerun() # recarrega a página para atualizar o progresso instantaneamente
            except Exception as e:
                st.error(f"Erro ao registrar: {e}")
                
    with col_garrafa:
        if st.button("🍼 Garrafa (500 ml)", use_container_width=True):
            try:
                salvar_agua(500)
                st.toast("Garrafa de 500ml registrada com sucesso!", icon="💧")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao registrar: {e}")

    quantidade_manual = st.number_input("Ou digite uma quantidade personalizada (ml):", min_value=0, step=50)
    if st.button("Registrar ml Personalizado", use_container_width=True):
        if quantidade_manual > 0:
            try:
                salvar_agua(int(quantidade_manual))
                st.toast(f"{quantidade_manual}ml registrados com sucesso!", icon="💧")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao registrar: {e}")
        else:
            st.warning("Insira um valor válido maior que zero.")

with col_direita:
    st.header("💊 Medicamentos")
    
    # lista medicamentos agendados p hj
    try:
        lista_meds = listar_medicamentos()
    except Exception as e:
        st.error(f"Erro ao buscar medicamentos: {e}")
        lista_meds = []

    if not lista_meds:
        st.info("Nenhum medicamento agendado para o dia de hoje.")
    else:
        st.write("Marque as caixas abaixo para confirmar a tomada:")
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
                    st.toast(f"Parabéns! Você tomou o medicamento: {nome}", icon="✅")
                    st.rerun() # atualiza a tela para marcar como "Concluído"
                except Exception as e:
                    st.error(f"Erro ao registrar tomada do remédio: {e}")

    # adicionar novo medicamento
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