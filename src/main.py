import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.storage import (
    init_db,
    salvar_medicamento,
    listar_medicamentos,
    listar_medicamentos_pendentes,
    marcar_medicamento_tomado,
    salvar_agua,
    buscar_total_agua_hoje,
    buscar_historico_agua_semanal,
    buscar_historico_medicamentos_semanal
)

META_AGUA = 2000

def exibir_progresso_agua(consumido):
    percentual = min(int((consumido / META_AGUA) * 100), 100)
    
    blocos_cheios = percentual // 5
    blocos_vazios = 20 - blocos_cheios
    barra = "█" * blocos_cheios + "░" * blocos_vazios
    
    print("\n" + "=" * 45)
    print(f"💧 HIDRATAÇÃO DIÁRIA: {consumido}ml / {META_AGUA}ml")
    print(f"   Progresso: [{barra}] {percentual}%")
    
    if consumido >= META_AGUA:
        print("   🎉 🎉 META DIÁRIA DE ÁGUA CONCLUÍDA! 🎉 🎉")
        print("   Excelente trabalho! Você se manteve muito bem hidratado hoje!")
    print("=" * 45)

def registrar_novo_medicamento():
    print("\n--- 💊 Registrar Medicamento ---")
    nome = input("Nome do medicamento: ").strip()
    if not nome:
        print("❌ O nome do medicamento não pode ser vazio!")
        return
        
    horario = input("Horário de toma (ex: 08:00, 14:30): ").strip()
    if not horario:
        print("❌ O horário não pode ser vazio!")
        return
        
    try:
        salvar_medicamento(nome, horario)
        print(f"✅ Medicamento '{nome}' agendado com sucesso para as {horario}!")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco de dados: {e}")

def registrar_nova_agua():
    print("\n--- 💧 Registrar Hidratação ---")
    try:
        quantidade = int(input("Quantidade de água consumida (em ml): "))
        if quantidade <= 0:
            print("❌ Digite uma quantidade válida maior que zero!")
            return
            
        salvar_agua(quantidade)
        print(f"✅ Sucesso! {quantidade}ml de água registrados.")
        
        total_atual = buscar_total_agua_hoje()
        if total_atual >= META_AGUA and (total_atual - quantidade) < META_AGUA:
            print("\n🌟 PARABÉNS! Com esse copo você acabou de bater a sua meta de hidratação do dia! 🌟")
            
    except ValueError:
        print("❌ Digite apenas números inteiros para os mililitros.")
    except Exception as e:
        print(f"❌ Erro ao salvar no banco de dados: {e}")

def confirmar_medicamento_tomado():
    print("\n--- 📋 Confirmar Toma de Remédio ---")
    try:
        pendentes = listar_medicamentos_pendentes()
        
        if not pendentes:
            print("😊 Todos os seus medicamentos de hoje já foram tomados! Nenhuma pendência.")
            return
            
        print("Medicamentos pendentes hoje:")
        for med in pendentes:
            med_id, nome, horario = med
            print(f"  [{med_id}] {nome} - agendado para as {horario}")
            
        opcao = input("\nDigite o número [ID] do remédio que você tomou (ou 'S' para voltar): ").strip()
        if opcao.upper() == 'S':
            return
            
        med_id_escolhido = int(opcao)
        
        sucesso = marcar_medicamento_tomado(med_id_escolhido)
        if sucesso:
            print("🎉 Parabéns por cuidar da sua saúde! Registro updated com sucesso.")
        else:
            print("❌ ID de medicamento inválido ou já concluído.")
            
    except ValueError:
        print("❌ Por favor, informe um número de ID válido.")
    except Exception as e:
        print(f"❌ Erro ao atualizar no banco de dados: {e}")

def exibir_resumo():
    print("\n" + "=" * 15 + " RESUMO DO DIA " + "=" * 15)
    
    print("\n📋 MEDICAMENTOS AGENDADOS:")
    try:
        medicamentos = listar_medicamentos()
        if not medicamentos:
            print("  Nenhum medicamento agendado para hoje.")
        else:
            for med in medicamentos:
                _, nome, horario, concluido = med
                status = "✅ Tomado" if concluido else "❌ Pendente"
                print(f"  [{horario}] - {nome} ({status})")
    except Exception as e:
        print(f"  Erro ao ler medicamentos: {e}")
        
    try:
        total_agua = buscar_total_agua_hoje()
        print(f"\n💧 HIDRATAÇÃO TOTAL: {total_agua} ml / {META_AGUA} ml")
        if total_agua >= META_AGUA:
            print("  🎉 Meta de água batida com sucesso hoje!")
    except Exception as e:
        print(f"  Erro ao calcular água: {e}")
        
    print("\n" + "=" * 45)

def exibir_resumo_semanal_manual():
    print("\n" + "=" * 12 + " 📈 RELATÓRIO SEMANAL DE SAÚDE " + "=" * 12)
    print("Compilado dos dados de consumo e adesão dos últimos 7 dias\n")

    relatorio_diario = {}

    try:
        dados_agua = buscar_historico_agua_semanal()
        if dados_agua:
            for data, quantidade in dados_agua:
                data_formatada = data.strftime('%d/%m') if isinstance(data, datetime.date) else str(data)
                if data_formatada not in relatorio_diario:
                    relatorio_diario[data_formatada] = {"agua": 0, "tomados": 0, "esquecidos": 0, "possui_meds": False}
                relatorio_diario[data_formatada]["agua"] = quantidade
    except Exception as e:
        print(f"❌ Erro ao ler histórico de água: {e}")

    try:
        dados_meds = buscar_historico_medicamentos_semanal()
        if dados_meds:
            for data, concluido, contagem in dados_meds:
                data_formatada = data.strftime('%d/%m') if isinstance(data, datetime.date) else str(data)
                if data_formatada not in relatorio_diario:
                    relatorio_diario[data_formatada] = {"agua": 0, "tomados": 0, "esquecidos": 0, "possui_meds": False}
                
                relatorio_diario[data_formatada]["possui_meds"] = True
                if concluido:
                    relatorio_diario[data_formatada]["tomados"] += contagem
                else:
                    relatorio_diario[data_formatada]["esquecidos"] += contagem
    except Exception as e:
        print(f"❌ Erro ao ler histórico de medicamentos: {e}")

    if not relatorio_diario:
        print("  Nenhum registro de saúde encontrado nos últimos 7 dias.")
    else:
        print("📅 DETALHAMENTO DIÁRIO DE METAS:")
        print("-" * 65)
        
        dias_perfeitos = 0
        total_dias_avaliados = len(relatorio_diario)
        
        for data_dia, dados in sorted(relatorio_diario.items()):
            agua = dados["agua"]
            tomados = dados["tomados"]
            esquecidos = dados["esquecidos"]
            possui_meds = dados["possui_meds"]
            
            meta_agua_ok = agua >= META_AGUA
            meta_meds_ok = True if not possui_meds else (esquecidos == 0 and (tomados > 0 or esquecidos == 0))
            
            status_agua = "✅" if meta_agua_ok else "❌"
            status_meds = "✅" if meta_meds_ok else "❌"
            
            if meta_agua_ok and meta_meds_ok:
                dias_perfeitos += 1
                status_geral = "⭐ DIA PERFEITO!"
            else:
                status_geral = ""
                
            print(f"  [{data_dia}] Água: {agua:4}ml {status_agua} | Remédios: (Tomados: {tomados}/Esquecidos: {esquecidos}) {status_meds}  {status_geral}")

        print("\n" + "=" * 20 + " GRÁFICO VISUAL " + "=" * 20)
        for data_dia, dados in sorted(relatorio_diario.items()):
            agua = dados["agua"]
            esquecidos = dados["esquecidos"]
            possui_meds = dados["possui_meds"]
            
            meta_agua_ok = agua >= META_AGUA
            meta_meds_ok = True if not possui_meds else (esquecidos == 0)
            
            caractere_grafico = "■" if (meta_agua_ok and meta_meds_ok) else "□"
            print(f"  [{data_dia}] {caractere_grafico} Concluído")
            
        print("=" * 56)
        print(f"\n📊 DESEMPENHO ACUMULADO DA SEMANA:")
        print(f"  Dias em que cumpriu TODAS as metas: {dias_perfeitos} de {total_dias_avaliados}")
        
        taxa_sucesso = (dias_perfeitos / total_dias_avaliados * 100) if total_dias_avaliados > 0 else 0
        print(f"  Taxa de consistência geral: {taxa_sucesso:.1f}%")
        
        if taxa_sucesso == 100:
            print("  🌟 Incrível! Desempenho impecável em todos os dias avaliados!")
        elif taxa_sucesso >= 70:
            print("  👍 Excelente nível de consistência! Continue mantendo a rotina firme.")
        elif taxa_sucesso >= 40:
            print("  ⚠️ Consistência moderada. Tente reduzir os esquecimentos e focar na hidratação.")
        else:
            print("  🚨 Atenção! Nível de cumprimento crítico. Recomenda-se revisar a rotina.")

    print("\n" + "=" * 55 + "\n")
    input("Pressione [ENTER] para voltar ao menu principal...")

def main():
    try:
        init_db()
    except Exception as e:
        print(f"⚠️ Alerta de conexão: Não foi possível conectar ao Supabase.")
        print(f"Verifique sua conexão e o arquivo .env. Detalhes: {e}")
        sys.exit(1)

    while True:
        try:
            total_agua = buscar_total_agua_hoje()
        except:
            total_agua = 0
            
        exibir_progresso_agua(total_agua)
        
        print("\n=== Menu CareTrack CLI ===")
        print("1. Registrar Novo Medicamento")
        print("2. Registrar Consumo de Água (ml)")
        print("3. Ver Resumo Completo do Dia")
        print("4. Confirmar que Tomou um Remédio")
        print("5. Ver Resumo Semanal de Saúde [Novo]")
        print("6. Sair")
        
        opcao = input("\nEscolha uma opção (1-6): ").strip()
        
        if opcao == "1":
            registrar_novo_medicamento()
        elif opcao == "2":
            registrar_nova_agua()
        elif opcao == "3":
            exibir_resumo()
        elif opcao == "4":
            confirmar_medicamento_tomado()
        elif opcao == "5":
            exibir_resumo_semanal_manual()
        elif opcao == "6":
            print("\nObrigado por usar o CareTrack. Cuide bem da sua saúde! Até logo! 👋")
            break
        else:
            print("❌ Opção inválida! Escolha um número entre 1 e 6.")

if __name__ == "__main__":
    main()