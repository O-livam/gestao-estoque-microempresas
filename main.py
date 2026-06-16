"""
Sistema de Gestão de Estoque para Microempreendedores
Desenvolvido em Python 3.8+ com persistência em JSON e interface CLI.
"""

import json
import os
from datetime import datetime, timedelta

ARQUIVO_ESTOQUE = "estoque.json"

def carregar_estoque():
    """Carrega o estoque do arquivo JSON ou retorna uma lista vazia se não existir."""
    if os.path.exists(ARQUIVO_ESTOQUE):
        try:
            with open(ARQUIVO_ESTOQUE, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except (json.JSONDecodeError, IOError):
            print("Aviso: Arquivo de estoque corrompido ou ilegível. Iniciando com estoque vazio.")
            return []
    return []

def salvar_estoque(estoque):
    """Salva o estado atual do estoque no arquivo JSON com formatação legível."""
    try:
        with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as arquivo:
            json.dump(estoque, arquivo, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Erro ao salvar o estoque: {e}")

def obter_valor_numerico(mensagem, tipo):
    """Auxiliar para validação rigorosa de entradas numéricas."""
    while True:
        try:
            valor = input(mensagem).strip().replace(',', '.')
            return tipo(valor)
        except ValueError:
            print(f"Erro: Entrada inválida. Por favor, insira um número válido ({tipo.__name__}).")

def cadastrar_produto(estoque):
    """Realiza o cadastro estruturado de um novo produto com validação de unicidade."""
    print("\n--- Cadastro de Novo Produto ---")
    codigo = input("Código do produto (único): ").strip()
    
    if any(prod["codigo"] == codigo for prod in estoque):
        print("Erro: Já existe um produto com este código.")
        return

    nome = input("Descrição/Nome do produto: ").strip()
    if not nome:
        print("Erro: A descrição do produto não pode ser vazia.")
        return

    quantidade = obter_valor_numerico("Quantidade inicial: ", int)
    preco_custo = obter_valor_numerico("Preço de custo (R$): ", float)
    preco_venda = obter_valor_numerico("Preço de venda (R$): ", float)
    data_validade = input("Data de validade (AAAA-MM-DD) ou deixe em branco: ").strip()

    if data_validade:
        try:
            datetime.strptime(data_validade, "%Y-%m-%d")
        except ValueError:
            print("Aviso: Formato de data inválido. O campo de validade será deixado em branco.")
            data_validade = ""

    novo_produto = {
        "codigo": codigo,
        "nome": nome,
        "quantidade": quantidade,
        "preco_custo": preco_custo,
        "preco_venda": preco_venda,
        "data_validade": data_validade
    }

    estoque.append(novo_produto)
    salvar_estoque(estoque)
    print("Sucesso: Produto cadastrado com êxito!")

def registrar_movimentacao(estoque, tipo_movimentacao):
    """Registra entrada ou saída de mercadorias com validação de integridade."""
    acao = "Entrada" if tipo_movimentacao == "entrada" else "Saída (Venda)"
    print(f"\n--- Registro de {acao} ---")
    codigo = input("Código do produto: ").strip()
    
    produto = next((prod for prod in estoque if prod["codigo"] == codigo), None)
    if not produto:
        print("Erro: Produto não encontrado no estoque.")
        return

    quantidade = obter_valor_numerico("Quantidade: ", int)
    if quantidade <= 0:
        print("Erro: A quantidade deve ser maior que zero.")
        return

    if tipo_movimentacao == "saida":
        if quantidade > produto["quantidade"]:
            print(f"Erro: Estoque insuficiente. Disponível: {produto['quantidade']} unidades.")
            return
        produto["quantidade"] -= quantidade
    else:
        produto["quantidade"] += quantidade

    salvar_estoque(estoque)
    print(f"Sucesso: {acao} de {quantidade} unidade(s) registrada para o produto '{produto['nome']}'.")
    print(f"Novo saldo em estoque: {produto['quantidade']} unidades.")

def consultar_estoque(estoque):
    """Exibe todos os produtos cadastrados de forma tabular."""
    print("\n--- Consulta Geral de Estoque ---")
    if not estoque:
        print("Nenhum produto cadastrado.")
        return

    print(f"{'Código':<10} | {'Nome':<25} | {'Qtd':<5} | {'Custo (R$)':<10} | {'Venda (R$)':<10} | {'Validade'}")
    print("-" * 85)
    for prod in estoque:
        validade = prod.get("data_validade", "N/A")
        print(f"{prod['codigo']:<10} | {prod['nome']:<25} | {prod['quantidade']:<5} | "
              f"{prod['preco_custo']:<10.2f} | {prod['preco_venda']:<10.2f} | {validade}")

def gerar_alertas(estoque):
    """Gera relatórios proativos de estoque mínimo (<=5) e validade próxima (<=7 dias)."""
    print("\n--- Relatórios de Alerta ---")
    hoje = datetime.now().date()
    alerta_estoque = []
    alerta_validade = []

    for prod in estoque:
        if prod["quantidade"] <= 5:
            alerta_estoque.append(prod)
        
        data_val_str = prod.get("data_validade", "")
        if data_val_str:
            try:
                data_val = datetime.strptime(data_val_str, "%Y-%m-%d").date()
                dias_restantes = (data_val - hoje).days
                if dias_restantes <= 7:
                    alerta_validade.append((prod, dias_restantes))
            except ValueError:
                continue

    print("\n[!] Produtos com Estoque Crítico (<= 5 unidades):")
    if alerta_estoque:
        for prod in alerta_estoque:
            print(f"  - {prod['nome']} (Código: {prod['codigo']}) | Saldo: {prod['quantidade']}")
    else:
        print("  Nenhum produto com estoque crítico.")

    print("\n[!] Produtos com Validade Próxima (<= 7 dias):")
    if alerta_validade:
        for prod, dias in alerta_validade:
            status = "VENCIDO" if dias < 0 else f"Vence em {dias} dia(s)"
            print(f"  - {prod['nome']} (Código: {prod['codigo']}) | {status} ({prod['data_validade']})")
    else:
        print("  Nenhum produto com validade crítica.")

def exibir_menu():
    """Exibe o menu interativo de linha de comando (CLI)."""
    print("\n" + "="*40)
    print(" SISTEMA DE GESTÃO DE ESTOQUE (CLI) ")
    print("="*40)
    print("1. Cadastrar Novo Produto")
    print("2. Registrar Entrada de Mercadoria")
    print("3. Registrar Saída (Venda)")
    print("4. Consultar Estoque Completo")
    print("5. Gerar Relatórios de Alerta")
    print("6. Sair do Sistema")
    print("="*40)

def main():
    """Função principal que orquestra o fluxo do sistema."""
    estoque = carregar_estoque()
    
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção (1-6): ").strip()

        if opcao == "1":
            cadastrar_produto(estoque)
        elif opcao == "2":
            registrar_movimentacao(estoque, "entrada")
        elif opcao == "3":
            registrar_movimentacao(estoque, "saida")
        elif opcao == "4":
            consultar_estoque(estoque)
        elif opcao == "5":
            gerar_alertas(estoque)
        elif opcao == "6":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Erro: Opção inválida. Por favor, selecione um número de 1 a 6.")

if __name__ == "__main__":
    main()
