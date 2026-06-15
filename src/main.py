import sys
import os
# Adiciona o diretório atual ao path para garantir que a importação do storage funcione
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.storage import (
    init_db,
    salvar_medicamento,
    listar_medicamentos,
    listar_medicamentos_pendentes,
    marcar_medicamento_tomado,
    salvar_agua,
    buscar_total_agua_hoje
)

META_AGUA = 2000

def exibir_progresso_agua(consumido):
    percentual = min(int((consumido / META_AGUA) * 100), 100)
    
    blocos_cheios = percentual // 5
    blocos_vazios = 20 - blocos_cheios
    barra = "█" * blocos_cheios + "░" * blocks_vazios if 'blocks_vazios' in locals() else "█" * blocos_cheios + "░" * blocos_vazios
    
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
        
        # Executa a atualização
        sucesso = marcar_medicamento_tomado(med_id_escolhido)
        if sucesso:
            print("🎉 Parabéns por cuidar da sua saúde! Registro atualizado com sucesso.")
        else:
            print("❌ ID de medicamento inválido ou já concluído.")
            
    except ValueError:
        print("❌ Por favor, informe um número de ID válido.")
    except Exception as e:
        print(f"❌ Erro ao atualizar no banco de dados: {e}")

def exibir_resumo():
    print("\n" + "=" * 15 + " RESUMO DO DIA " + "=" * 15)
    
    # Mostra medicamentos de hoje
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
        
    # Mostra água de hoje
    try:
        total_agua = buscar_total_agua_hoje()
        print(f"\n💧 HIDRATAÇÃO TOTAL: {total_agua} ml / {META_AGUA} ml")
        if total_agua >= META_AGUA:
            print("  🎉 Meta de água batida com sucesso hoje!")
    except Exception as e:
        print(f"  Erro ao calcular água: {e}")
        
    print("\n" + "=" * 45)

def main():
    try:
        init_db()
    except Exception as e:
        print(f"⚠️ Alerta de conexão: Não foi possível conectar ao Supabase.")
        print(f"Verifique sua conexão e o arquivo .env. Detalhes: {e}")
        sys.exit(1)

    while True:
        total_agua = buscar_total_agua_hoje()
        exibir_progresso_agua(total_agua)
        
        print("\n=== Menu CareTrack CLI ===")
        print("1. Registrar Novo Medicamento")
        print("2. Registrar Consumo de Água (ml)")
        print("3. Ver Resumo Completo do Dia")
        print("4. Confirmar que Tomou um Remédio")
        print("5. Sair")
        
        opcao = input("\nEscolha uma opção (1-5): ").strip()
        
        if opcao == "1":
            registrar_novo_medicamento()
        elif opcao == "2":
            registrar_nova_agua()
        elif opcao == "3":
            exibir_resumo()
        elif opcao == "4":
            confirmar_medicamento_tomado()
        elif opcao == "5":
            print("\nObrigado por usar o CareTrack. Cuide bem da sua saúde! Até logo! 👋")
            break
        else:
            print("❌ Opção inválida! Escolha um número entre 1 e 5.")

if __name__ == "__main__":
    main()