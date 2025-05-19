````markdown
# 💳 Sistema Bancário em Python

Este projeto é uma simulação de um sistema bancário desenvolvido em Python, utilizando **Programação Orientada a Objetos (POO)**. Ele permite realizar operações como criação de clientes e contas, saques, depósitos e emissão de extrato bancário.

---

## 📌 Funcionalidades

- Criar clientes (pessoa física);
- Criar contas correntes com limite e controle de saques;
- Realizar **depósitos** e **saques** com histórico de transações;
- Emitir **extratos detalhados**;
- Listar contas cadastradas;
- Menu interativo no terminal.

---

## 🛠️ Tecnologias Utilizadas

- Python 3.x
- Programação Orientada a Objetos (POO)
- Módulos padrão: `abc`, `datetime`, `textwrap`

---

## ▶️ Como Executar

1. **Clone o repositório:**

```bash
git clone https://github.com/vfrancajr/desafio_bancario_2.git
cd sistema-bancario
````

2. **Execute o arquivo principal:**

```bash
python desafio_bancario_2.py
```

---

## 🧱 Estrutura do Projeto

* `Cliente` (classe base)
* `PessoaFisica` (subclasse de Cliente)
* `Conta` e `ContaCorrente`
* `Transacao`, `Saque` e `Deposito` (com uso de `ABC`)
* `Historico` (registra todas as transações por conta)

---

## ✅ Exemplo de uso

```
=============== MENU ===============
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuario
[q] Sair
=> 
```

---

## 🚧 Melhorias Futuras

* Persistência de dados em arquivo ou banco de dados;
* Interface gráfica (Tkinter ou Web com Flask);
* Autenticação de usuários;
* Suporte a contas poupança e jurídicas;
* Testes automatizados com `unittest` ou `pytest`.

---

## 👨‍💻 Autor

Desenvolvido por **Vandemberg de França Junior**
📧 Contato: \[[vfrancajr@gmail.com](mailto:vfrancajr@gmail.com)]
🔗 GitHub: [https://github.com/vfrancajr](https://github.com/vfrancajr)

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

```

