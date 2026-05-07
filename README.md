[README.md](https://github.com/user-attachments/files/27491091/README.md)
# 🧮 Calculadora Científica

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-FF6B6B?style=for-the-badge)
![License](https://img.shields.io/badge/Licença-MIT-00D4AA?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Concluído-00C851?style=for-the-badge)

**Calculadora científica desktop com interface gráfica moderna, tema cyberpunk e suporte a expressões matemáticas completas.**

![Demo](demo.gif)

</div>

---

## ✨ Funcionalidades

- ➕ Operações básicas: adição, subtração, multiplicação, divisão
- 🔬 Funções científicas: `sin`, `cos`, `tan`, `log`, `ln`, `sqrt`, `exp`, e muito mais
- 📐 Suporte a expressões completas: `2*sin(30) + log(100)`
- 🧮 Solver de equações lineares e quadráticas
- 💾 Sistema de memória: `M+`, `M-`, `MR`, `MC`, `MS`
- 📜 Histórico de cálculos (salvo automaticamente)
- ⌨️ Entrada por teclado
- 🎨 Troca de temas: Cyberpunk e Neon Purple
- 📋 Botão de copiar resultado

---

## 🖥️ Interface

![Demo](demo.gif)

---

## 🚀 Como executar

### Pré-requisitos

- Python 3.10 ou superior
- Tkinter (normalmente já vem com o Python)

### Instalação do Tkinter (se necessário)

**Windows:**
```bash
# Já vem instalado com o Python oficial (python.org)
```

**Ubuntu/Debian:**
```bash
sudo apt install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

### Rodando o projeto

```bash
# Clone o repositório
git clone https://github.com/Lucas-if-else/calculadora-cientifica.git

# Entre na pasta
cd calculadora-cientifica

# Execute
python main.py
```

---

## 📁 Estrutura do projeto

```
calculadora-cientifica/
├── main.py              # Ponto de entrada
├── engine/
│   ├── parser.py        # Parser matemático seguro (sem eval)
│   └── calculator.py    # Lógica: memória, histórico, solver
├── ui/
│   ├── window.py        # Interface gráfica (Tkinter)
│   └── theme.py         # Temas de cores
└── data/
    └── history.json     # Histórico salvo automaticamente
```

---

## ⌨️ Atalhos de teclado

| Tecla | Ação |
|-------|------|
| `0–9` e `.` | Digitar número |
| `+ - * /` | Operadores |
| `^` | Potência |
| `( )` | Parênteses |
| `Enter` | Calcular |
| `Backspace` | Apagar último caractere |
| `Delete` / `Esc` | Limpar tudo |

---

## 🛠️ Tecnologias utilizadas

- **Python 3** — Linguagem principal
- **Tkinter** — Interface gráfica
- **Parser próprio** — Sem uso de `eval()`, 100% seguro

---

## 👨‍💻 Autor

Feito por **Lucas Silva Santos**

[![GitHub](https://img.shields.io/badge/GitHub-Lucas--if--else-181717?style=for-the-badge&logo=github)](https://github.com/Lucas-if-else)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
