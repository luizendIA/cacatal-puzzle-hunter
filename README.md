# ₿ Caçatal Puzzle Hunter v1.0

**Ferramenta da comunidade para buscar as chaves privadas do Bitcoin Puzzle.**

---

## ⬇️ DOWNLOAD

### 👉 [CLIQUE AQUI PARA BAIXAR O PROGRAMA (.exe)](https://github.com/luizendIA/cacatal-puzzle-hunter/releases/download/v1.0.0/CacatalPuzzleHunter.exe)

*(Windows 10/11 — requer WSL2 com Ubuntu)*

---

## 🎯 O que é?

O Bitcoin Puzzle é um desafio criado anonimamente contendo ~1000 BTC distribuidos em 160 enderecos. O objetivo é encontrar a chave privada correta dentro de um intervalo de bits conhecido. Este programa usa o poder do seu processador (CPU) para fazer busca por forca bruta.

**Puzzle atual: #71** (~7.10 BTC de recompensa)

## 📋 Requisitos

- **Windows 10 ou 11** (64 bits)
- **WSL2 com Ubuntu** instalado
- Conexao com internet (apenas na primeira execucao, para instalar o cacachave)

### Como instalar o WSL (se ainda nao tem):

1. Abra o **PowerShell como Administrador**
2. Execute: `wsl --install`
3. Reinicie o computador
4. Abra o Ubuntu pelo menu iniciar e crie um usuario

## 🚀 Como usar

1. Baixe o **CacatalPuzzleHunter.exe** pelo link acima
2. Execute o programa
3. Na primeira vez, ele instala o cacachave automaticamente no WSL
4. Clique em **INICIAR BUSCA** e pronto!
5. Ajuste o numero de **threads** para usar mais nucleos do seu CPU

## ⚙️ Configuracoes

- **Puzzle alvo**: Escolha qual puzzle buscar (71, 69, 68)
- **Threads**: Quantos nucleos da CPU usar. Clique em "Auto-detectar" para ver o maximo
  - Use o maximo para velocidade total
  - Use menos se quiser continuar usando o PC normalmente

## 💰 Acordo da Comunidade

Este programa e **gratuito e open-source**. Se voce encontrar a chave privada de um dos puzzles, pedimos que envie **5% da recompensa** para o endereco BTC do criador da ferramenta, exibido no rodape do programa.

Isso e baseado em confianca e honra. E a forma da comunidade agradecer pelo trabalho de desenvolvimento.

## 📊 Expectativas realistas

Encontrar a chave e como ganhar na loteria. O Puzzle #71 tem um espaco de chaves de 2^70 (~1.18 sextilhao de chaves). Mas alguem vai encontrar — e quanto mais gente buscando, mais rapido o espaco e coberto.

## 🔧 Problemas comuns

| Problema | Solucao |
|----------|---------|
| "WSL nao detectado" | Instale com `wsl --install` no PowerShell (Admin) |
| "Cacachave nao encontrado" | O programa tenta instalar automaticamente. Se falhar, abra o WSL e rode o script `setup_wsl.sh` |
| Velocidade muito baixa | Aumente o numero de threads |
| PC travando | Reduza o numero de threads |

## 🙏 Creditos

- **AlbertoBSD** — criador do [keyhunt](https://github.com/albertobsd/keyhunt) original
- **lmajowka** — traducao para portugues ([cacachave](https://github.com/lmajowka/cacachave))
- **Mestre Cacatal** — divulgacao e educacao da comunidade brasileira
- **Comunidade Bitcoin Puzzle Brasil**

## ⚠️ Aviso Legal

Este programa e fornecido "como esta", sem garantias. Use por sua propria conta e risco. Nunca invista mais recursos (eletricidade, hardware) do que pode perder.

---

*Feito com ❤️ para a comunidade brasileira de Bitcoin Puzzle*
