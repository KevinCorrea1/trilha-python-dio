menu = """
[d] Depósito 
[s] Sacar
[e] Extrato
[q] Sair

=> """
saldo = 0
limite = 500
extrato = ""
nunero_saques = 0
LIMTE_SAQUES = 3

while True:
  opcao = input(menu) 
  
  if opcao == "d":
     valor = float(input("Informe o valor do depósito:"))
     if valor > 0:
        saldo += valor
        extrato += f"Depósito : R$ {valor:.2f}\n" 
     else: 
        print("Operação falhou! O valor informado e inválido.")
        
  elif opcao == "s":
     valor = float(input("Informe o valor do saque: "))
     excedeu_saldo = valor > saldo
     excedeu_limite = valor > limite
     excedeu_saques = nunero_saques >= LIMTE_SAQUES 

     if excedeu_saldo:
        print("Operação falhou ! Voçê  não tem saldo o suficiente.")
     elif excedeu_limite:
        print("Operação falhou ! o valor do saque excedeu o limite disponível.")
     elif excedeu_saques:
        print("Operação falhou ! Número máximo de saques excedido.")
     elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        nunero_saques += 1
     else :
        print("Operação falhou ! o valor informado e inválido")

  elif opcao == "e":
     print("\n===============Extrato==============")
     print("Não foram realizadas Movimentações." if not extrato else extrato)
     print(f"\nSaldo: R$ {saldo:.2f}")
     print("========================================") 
  elif opcao == "q":
     break
  else:
     print("Operação inválida, por favor selicione novamente a operação desejada.")