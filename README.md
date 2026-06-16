# ₿ Caçatal Puzzle Hunter v1.0

**Ferramenta da comunidade para buscar as chaves privadas do Bitcoin Puzzle.**

Inspirado pelo canal [Mestre Caçatal](https://www.youtube.com/@mestrecacatal) e baseado no [cacachave](https://github.com/lmajowka/cacachave) (tradução do keyhunt por AlbertoBSD).

---

## 🎯 O que é?

O Bitcoin Puzzle é um desafio criado anonimamente contendo ~1000 BTC distribuídos em 160 endereços. O objetivo é encontrar a chave privada correta dentro de um intervalo de bits conhecido. Este programa usa o poder do seu processador (CPU) para fazer busca por força bruta.

**Puzzle atual: #71** (~7.10 BTC de recompensa)

---

## 📋 Requisitos

- **Windows 10 ou 11** (64 bits)
- **WSL2 com Ubuntu** instalado
- Conexão com internet (apenas na primeira execução, para instalar o cacachave)

### Como instalar o WSL (se ainda não tem):

1. Abra o **PowerShell como Administrador**
2. Execute: `wsl --install`
3. Reinicie o computador
4. Abra o Ubuntu pelo menu iniciar e crie um usuário

---

## 🚀 Como usar

### Opção 1 — Executar direto (precisa de Python)

1. Instale o [Python](https://www.python.org/downloads/) (marque "Add to PATH")
2. Dê duplo clique em `puzzle_hunter.py`
3. Ou abra o terminal e rode: `python puzzle_hunter.py`

### Opção 2 — Usar o .exe pronto

1. Baixe o `CacatalPuzzleHunter.exe`
2. Dê duplo clique para abrir
3. Na primeira vez, o programa vai instalar o cacachave automaticamente no WSL
4. Clique em **INICIAR BUSCA** e pronto!

### Opção 3 — Compilar o .exe você mesmo

1. Instale o Python
2. Dê duplo clique em `BUILD.bat`
3. O .exe será criado na pasta `dist/`

---

## ⚙️ Configurações

- **Puzzle alvo**: Escolha qual puzzle buscar (71, 69, 68)
- **Threads**: Quantos núcleos da CPU usar. Clique em "Auto-detectar" para ver o máximo.
  - Use o máximo para velocidade total
  - Use menos (ex: metade) se quiser continuar usando o PC normalmente
- As configurações são salvas automaticamente entre sessões

---

## 💰 Acordo da Comunidade

Este programa é **gratuito e open-source**. Se você encontrar a chave privada de um dos puzzles, pedimos que envie **5% da recompensa** para o endereço BTC do criador da ferramenta, exibido no rodapé do programa.

Isso é baseado em confiança e honra — não é automático nem obrigatório. É a forma da comunidade agradecer pelo trabalho de desenvolvimento e manutenção.

---

## 📊 Expectativas realistas

Seja honesto consigo mesmo: encontrar a chave é como ganhar na loteria. O Puzzle #71 tem um espaço de chaves de 2^70 (~1.18 sextilhão de chaves). Mesmo uma RTX 4090 (~1.5 GKeys/s) levaria ~25.000 anos sozinha.

**Mas alguém vai encontrar** — e quanto mais gente buscando, mais rápido o espaço é coberto. Cada chave que você testa é uma chance real.

---

## 🔧 Problemas comuns

| Problema | Solução |
|----------|---------|
| "WSL não detectado" | Instale com `wsl --install` no PowerShell (Admin) |
| "Cacachave não encontrado" | O programa tenta instalar automaticamente. Se falhar, abra o WSL e rode: `sudo apt install -y git build-essential libssl-dev libgmp-dev && cd ~ && git clone https://github.com/lmajowka/cacachave.git && cd cacachave && make` |
| Velocidade muito baixa | Aumente o número de threads nas configurações |
| PC travando | Reduza o número de threads (deixe 2-4 livres pro sistema) |

---

## 🙏 Créditos

- **AlbertoBSD** — criador do [keyhunt](https://github.com/albertobsd/keyhunt) original
- **lmajowka** — tradução para português ([cacachave](https://github.com/lmajowka/cacachave))
- **Mestre Caçatal** — divulgação e educação da comunidade brasileira
- **Comunidade Bitcoin Puzzle Brasil** — força coletiva!

---

## ⚠️ Aviso Legal

Este programa é fornecido "como está", sem garantias. Use por sua própria conta e risco. O Bitcoin Puzzle é um desafio matemático legítimo — não há garantia de retorno financeiro. Nunca invista mais recursos (eletricidade, hardware) do que pode perder.

---

*Feito com ❤️ para a comunidade brasileira de Bitcoin Puzzle*
