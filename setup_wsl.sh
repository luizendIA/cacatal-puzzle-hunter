#!/bin/bash
# ══════════════════════════════════════════════════════════
# Caçatal Puzzle Hunter — Setup Script para WSL
# Cole este script no terminal do WSL/Ubuntu e execute
# ══════════════════════════════════════════════════════════

echo ""
echo "╔══════════════════════════════════════════════════╗"
echo "║   Caçatal Puzzle Hunter — Instalação WSL         ║"
echo "╚══════════════════════════════════════════════════╝"
echo ""

# Atualizar sistema
echo "[1/4] Atualizando sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependências
echo "[2/4] Instalando dependências..."
sudo apt install -y git build-essential libssl-dev libgmp-dev

# Clonar cacachave
echo "[3/4] Clonando cacachave..."
cd ~
if [ -d "cacachave" ]; then
    echo "  Pasta cacachave já existe. Atualizando..."
    cd cacachave
    git pull
else
    git clone https://github.com/lmajowka/cacachave.git
    cd cacachave
fi

# Compilar
echo "[4/4] Compilando..."
make

# Verificar
echo ""
if [ -f "./cacachave" ]; then
    echo "══════════════════════════════════════════════════"
    echo "  ✓ INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
    echo "  Agora abra o CacatalPuzzleHunter.exe no Windows"
    echo "══════════════════════════════════════════════════"
    echo ""
    echo "  Threads disponíveis: $(nproc)"
    echo ""
else
    echo "══════════════════════════════════════════════════"
    echo "  ✗ ERRO: Compilação falhou"
    echo "  Verifique as mensagens de erro acima"
    echo "══════════════════════════════════════════════════"
fi
