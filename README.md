# Sistema de Gestão de Estoque para Microempreendedores

## 📌 Sobre o Projeto
Este repositório contém um sistema de gestão de estoque desenvolvido em Python, voltado especificamente para pequenos comércios (mercearias, farmácias de bairro e lojas de conveniência). O objetivo é substituir métodos manuais (cadernetas/planilhas) por uma solução computacional leve, de execução local (offline) e de baixo custo, prevenindo rupturas de estoque e perdas por vencimento de produtos.

## 🚀 Funcionalidades
- **Cadastro Estruturado**: Registro de produtos com código único, descrição, quantidades, preços e data de validade.
- **Controle de Movimentação**: Entrada e saída de mercadorias com validação rigorosa (impede saldo negativo e códigos duplicados).
- **Alertas Automáticos**: Relatórios proativos para itens com estoque ≤ 5 unidades e validade ≤ 7 dias.
- **Persistência Local**: Armazenamento de dados em arquivo `estoque.json`, garantindo portabilidade e funcionamento sem internet.
- **Tratamento de Exceções**: Validação de entradas para evitar travamentos por dados inválidos (ex: letras em campos numéricos).

## 🛠️ Requisitos Técnicos
- Python 3.8 ou superior.
- Nenhuma dependência externa (utiliza apenas bibliotecas nativas: `json`, `os`, `datetime`).

## 💻 Como Executar
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/gestao-estoque-microempresas.git
   cd gestao-estoque-microempresas
