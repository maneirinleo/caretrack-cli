import storage
import api_client

def mostrar_menu():
    print("\n====== CareTrack CLI ======")
    print("1. Registrar medicamento")
    print("2. Registrar hidratação (ml)")
    print("3. Ver resumo do Dia")
    print("4. Sair")
    return input("Escolha uma opção: ")

def main():
    print("\n---- Dica de Bem-Estar do Dia ----")
    dica = api_client.get_daily_tip()
    print(f"💡 {dica}")
    print("--------------------------------")

def main():
    while True:
        opcao = mostrar_menu()

        if opcao == "1":
            nome = input("Nome do medicamento: ")
            horario = input("Horário (ex: 08:00): ")
            storage.add_medicamento(nome, horario)
            print(f"Sucesso! {nome} agendado para {horario}.")

        elif opcao == "2":
            try:
                ml = int(input("Quantidade de água consumida (ml): "))
                storage.add_agua(ml)
                print(f"Sucesso! {ml}ml registrados.")
            except ValueError as e:
                print(f"Erro: {e}")

        elif opcao == "3":
            dados = storage.load_data()
            print("\n--- Resumo do Dia ---")
            print(f"Água consumida: {dados.get('agua_ml', 0)} ml")
            print("Medicamentos:")
            if not dados.get("medicamentos"):
                print(" Nenhum medicamento registrado.")
            else:
                for med in dados.get("medicamentos", []):
                    print(f" - {med['horario']}: {med['nome']}")

        elif opcao == "4":
            print("Saindo do CareTrack. Cuide-se bem!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
        main()
