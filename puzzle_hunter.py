"""
╔══════════════════════════════════════════════════════════╗
║          CAÇATAL PUZZLE HUNTER v1.0                      ║
║   Ferramenta da comunidade para o Bitcoin Puzzle         ║
║   Baseado no cacachave (keyhunt) por AlbertoBSD          ║
╚══════════════════════════════════════════════════════════╝

Distribuível para a comunidade.
Se encontrar a chave privada, envie 5% para o criador.

Requer: Windows 10/11 com WSL2 + Ubuntu instalado.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import subprocess
import threading
import time
import re
import os
import sys
import json
from datetime import timedelta

# ══════════════════════════════════════════════════════════
# CONFIGURAÇÃO DO CRIADOR — EDITE AQUI SEU ENDEREÇO BTC
# ══════════════════════════════════════════════════════════
CREATOR_BTC_ADDRESS = "bc1qcpc9jnmqml8lyfh0p3rak2xswu4l5s87c5n6v6"
CREATOR_NAME = "Comunidade Caçatal"
APP_VERSION = "1.0.0"

# ══════════════════════════════════════════════════════════
# DADOS DOS PUZZLES
# ══════════════════════════════════════════════════════════
PUZZLES = {
    "71": {
        "address": "1PWo3JeB9jrGwfHDNpdGK54CRas7fsVzXU",
        "reward": "~7.10 BTC",
        "bits": 71,
    },
    "69": {
        "address": "19vkiEajfhuZ8bs8Zu2jgmC6oqZbWqhxhG",
        "reward": "~6.90 BTC",
        "bits": 69,
    },
    "68": {
        "address": "1MVDYgVaSN6iKKEsbzRUAYFrYJadLYZvvZ",
        "reward": "~6.80 BTC",
        "bits": 68,
    },
}

# ══════════════════════════════════════════════════════════
# CORES DO TEMA
# ══════════════════════════════════════════════════════════
COLORS = {
    "bg_dark": "#0d1117",
    "bg_card": "#161b22",
    "bg_input": "#21262d",
    "border": "#30363d",
    "text_primary": "#e6edf3",
    "text_secondary": "#8b949e",
    "text_dim": "#484f58",
    "accent_orange": "#f7931a",  # Bitcoin orange
    "accent_green": "#3fb950",
    "accent_red": "#f85149",
    "accent_blue": "#58a6ff",
    "accent_gold": "#d4a017",
}

# ══════════════════════════════════════════════════════════
# CAMINHOS
# ══════════════════════════════════════════════════════════
SETTINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "hunter_settings.json")
CACACHAVE_WSL_PATH = "~/cacachave"


class PuzzleHunterApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Caçatal Puzzle Hunter v{APP_VERSION}")
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.geometry("720x820")
        self.root.minsize(620, 720)

        # State
        self.is_running = False
        self.process = None
        self.start_time = None
        self.total_keys = 0
        self.current_speed = 0
        self.session_keys = 0
        self.monitor_thread = None

        # Load settings
        self.settings = self.load_settings()

        # Build UI
        self.build_ui()

        # Check WSL on startup
        self.root.after(500, self.check_environment)

        # Handle close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ──────────────────────────────────────────────────
    # SETTINGS
    # ──────────────────────────────────────────────────
    def load_settings(self):
        defaults = {
            "threads": 4,
            "puzzle": "71",
            "total_keys_lifetime": 0,
            "total_time_seconds": 0,
        }
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, "r") as f:
                    saved = json.load(f)
                    defaults.update(saved)
        except Exception:
            pass
        return defaults

    def save_settings(self):
        try:
            self.settings["threads"] = int(self.thread_var.get())
            self.settings["puzzle"] = self.puzzle_var.get()
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self.settings, f, indent=2)
        except Exception:
            pass

    # ──────────────────────────────────────────────────
    # UI CONSTRUCTION
    # ──────────────────────────────────────────────────
    def build_ui(self):
        # Main container with padding
        main = tk.Frame(self.root, bg=COLORS["bg_dark"], padx=20, pady=12)
        main.pack(fill="both", expand=True)

        # ── HEADER ──
        header = tk.Frame(main, bg=COLORS["bg_dark"])
        header.pack(fill="x", pady=(0, 12))

        tk.Label(
            header,
            text="₿",
            font=("Segoe UI", 28, "bold"),
            fg=COLORS["accent_orange"],
            bg=COLORS["bg_dark"],
        ).pack(side="left", padx=(0, 10))

        title_frame = tk.Frame(header, bg=COLORS["bg_dark"])
        title_frame.pack(side="left")

        tk.Label(
            title_frame,
            text="CAÇATAL PUZZLE HUNTER",
            font=("Segoe UI", 18, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["bg_dark"],
        ).pack(anchor="w")

        tk.Label(
            title_frame,
            text=f"v{APP_VERSION} — Ferramenta da comunidade Bitcoin Puzzle",
            font=("Segoe UI", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_dark"],
        ).pack(anchor="w")

        # ── STATUS BAR ──
        self.status_frame = tk.Frame(main, bg=COLORS["bg_card"], padx=12, pady=8)
        self.status_frame.pack(fill="x", pady=(0, 12))

        self.status_dot = tk.Label(
            self.status_frame,
            text="●",
            font=("Segoe UI", 12),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_card"],
        )
        self.status_dot.pack(side="left", padx=(0, 8))

        self.status_label = tk.Label(
            self.status_frame,
            text="Pronto para iniciar",
            font=("Segoe UI", 10),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_card"],
        )
        self.status_label.pack(side="left")

        # ── CONFIG PANEL ──
        config_card = tk.Frame(main, bg=COLORS["bg_card"], padx=16, pady=14)
        config_card.pack(fill="x", pady=(0, 12))

        tk.Label(
            config_card,
            text="CONFIGURAÇÃO",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_card"],
        ).pack(anchor="w", pady=(0, 10))

        config_row = tk.Frame(config_card, bg=COLORS["bg_card"])
        config_row.pack(fill="x")

        # Puzzle selector
        pz_frame = tk.Frame(config_row, bg=COLORS["bg_card"])
        pz_frame.pack(side="left", padx=(0, 24))

        tk.Label(
            pz_frame,
            text="Puzzle alvo",
            font=("Segoe UI", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_card"],
        ).pack(anchor="w")

        self.puzzle_var = tk.StringVar(value=self.settings.get("puzzle", "71"))
        puzzle_combo = ttk.Combobox(
            pz_frame,
            textvariable=self.puzzle_var,
            values=list(PUZZLES.keys()),
            state="readonly",
            width=8,
            font=("Consolas", 11),
        )
        puzzle_combo.pack(anchor="w", pady=(4, 0))
        puzzle_combo.bind("<<ComboboxSelected>>", self.on_puzzle_change)

        # Reward display
        self.reward_label = tk.Label(
            pz_frame,
            text=f"Recompensa: {PUZZLES[self.puzzle_var.get()]['reward']}",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["accent_gold"],
            bg=COLORS["bg_card"],
        )
        self.reward_label.pack(anchor="w", pady=(4, 0))

        # Thread selector
        th_frame = tk.Frame(config_row, bg=COLORS["bg_card"])
        th_frame.pack(side="left", padx=(0, 24))

        tk.Label(
            th_frame,
            text="Threads (CPU)",
            font=("Segoe UI", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_card"],
        ).pack(anchor="w")

        self.thread_var = tk.StringVar(value=str(self.settings.get("threads", 4)))
        thread_spin = tk.Spinbox(
            th_frame,
            from_=1,
            to=128,
            textvariable=self.thread_var,
            width=6,
            font=("Consolas", 11),
            bg=COLORS["bg_input"],
            fg=COLORS["text_primary"],
            insertbackground=COLORS["text_primary"],
            buttonbackground=COLORS["bg_input"],
            highlightthickness=1,
            highlightcolor=COLORS["accent_orange"],
            relief="flat",
        )
        thread_spin.pack(anchor="w", pady=(4, 0))

        # Detect threads button
        detect_btn = tk.Button(
            th_frame,
            text="Auto-detectar",
            font=("Segoe UI", 8),
            fg=COLORS["accent_blue"],
            bg=COLORS["bg_card"],
            activeforeground=COLORS["accent_blue"],
            activebackground=COLORS["bg_input"],
            relief="flat",
            cursor="hand2",
            command=self.detect_threads,
        )
        detect_btn.pack(anchor="w", pady=(2, 0))

        # Address display
        addr_frame = tk.Frame(config_row, bg=COLORS["bg_card"])
        addr_frame.pack(side="left", fill="x", expand=True)

        tk.Label(
            addr_frame,
            text="Endereço alvo",
            font=("Segoe UI", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_card"],
        ).pack(anchor="w")

        self.addr_label = tk.Label(
            addr_frame,
            text=PUZZLES[self.puzzle_var.get()]["address"],
            font=("Consolas", 9),
            fg=COLORS["accent_orange"],
            bg=COLORS["bg_card"],
        )
        self.addr_label.pack(anchor="w", pady=(4, 0))

        # ── BIG BUTTON ──
        btn_frame = tk.Frame(main, bg=COLORS["bg_dark"], pady=4)
        btn_frame.pack(fill="x", pady=(0, 12))

        self.start_button = tk.Button(
            btn_frame,
            text="▶  INICIAR BUSCA",
            font=("Segoe UI", 16, "bold"),
            fg="#ffffff",
            bg=COLORS["accent_green"],
            activeforeground="#ffffff",
            activebackground="#2ea043",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=12,
            command=self.toggle_hunting,
        )
        self.start_button.pack(fill="x")

        # ── STATS PANEL ──
        stats_card = tk.Frame(main, bg=COLORS["bg_card"], padx=16, pady=14)
        stats_card.pack(fill="x", pady=(0, 12))

        tk.Label(
            stats_card,
            text="ESTATÍSTICAS EM TEMPO REAL",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_card"],
        ).pack(anchor="w", pady=(0, 10))

        stats_grid = tk.Frame(stats_card, bg=COLORS["bg_card"])
        stats_grid.pack(fill="x")

        # Speed
        self.speed_value = self._make_stat(stats_grid, "Velocidade", "0 keys/s", 0, 0)
        # Session keys
        self.session_value = self._make_stat(stats_grid, "Chaves (sessão)", "0", 0, 1)
        # Uptime
        self.uptime_value = self._make_stat(stats_grid, "Tempo ativo", "00:00:00", 1, 0)
        # Lifetime keys
        self.lifetime_value = self._make_stat(
            stats_grid,
            "Chaves (total histórico)",
            self._format_number(self.settings.get("total_keys_lifetime", 0)),
            1,
            1,
        )

        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)

        # ── LOG AREA ──
        log_card = tk.Frame(main, bg=COLORS["bg_card"], padx=12, pady=10)
        log_card.pack(fill="both", expand=True, pady=(0, 12))

        log_header = tk.Frame(log_card, bg=COLORS["bg_card"])
        log_header.pack(fill="x", pady=(0, 6))

        tk.Label(
            log_header,
            text="LOG",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_card"],
        ).pack(side="left")

        clear_btn = tk.Button(
            log_header,
            text="Limpar",
            font=("Segoe UI", 8),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_card"],
            activeforeground=COLORS["text_primary"],
            activebackground=COLORS["bg_input"],
            relief="flat",
            cursor="hand2",
            command=lambda: self.log_text.delete("1.0", "end"),
        )
        clear_btn.pack(side="right")

        self.log_text = scrolledtext.ScrolledText(
            log_card,
            font=("Consolas", 9),
            bg=COLORS["bg_dark"],
            fg=COLORS["text_secondary"],
            insertbackground=COLORS["text_primary"],
            relief="flat",
            height=8,
            state="disabled",
            wrap="word",
        )
        self.log_text.pack(fill="both", expand=True)

        # Configure log colors
        self.log_text.tag_configure("info", foreground=COLORS["text_secondary"])
        self.log_text.tag_configure("success", foreground=COLORS["accent_green"])
        self.log_text.tag_configure("warning", foreground=COLORS["accent_orange"])
        self.log_text.tag_configure("error", foreground=COLORS["accent_red"])
        self.log_text.tag_configure("found", foreground=COLORS["accent_gold"], font=("Consolas", 11, "bold"))

        # ── FOOTER — CREATOR INFO ──
        footer = tk.Frame(main, bg=COLORS["bg_card"], padx=16, pady=12)
        footer.pack(fill="x")

        tk.Label(
            footer,
            text="💰 ACORDO DA COMUNIDADE",
            font=("Segoe UI", 9, "bold"),
            fg=COLORS["accent_orange"],
            bg=COLORS["bg_card"],
        ).pack(anchor="w")

        tk.Label(
            footer,
            text="Se encontrar a chave privada, envie 5% da recompensa para o criador da ferramenta:",
            font=("Segoe UI", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["bg_card"],
            wraplength=650,
            justify="left",
        ).pack(anchor="w", pady=(4, 4))

        addr_copy_frame = tk.Frame(footer, bg=COLORS["bg_card"])
        addr_copy_frame.pack(anchor="w")

        self.creator_addr_label = tk.Label(
            addr_copy_frame,
            text=CREATOR_BTC_ADDRESS,
            font=("Consolas", 10, "bold"),
            fg=COLORS["accent_gold"],
            bg=COLORS["bg_card"],
        )
        self.creator_addr_label.pack(side="left")

        copy_btn = tk.Button(
            addr_copy_frame,
            text="📋 Copiar",
            font=("Segoe UI", 8),
            fg=COLORS["accent_blue"],
            bg=COLORS["bg_card"],
            activeforeground=COLORS["accent_blue"],
            activebackground=COLORS["bg_input"],
            relief="flat",
            cursor="hand2",
            command=self.copy_creator_address,
        )
        copy_btn.pack(side="left", padx=(10, 0))

        tk.Label(
            footer,
            text=f"Obrigado por participar, {CREATOR_NAME}! Juntos somos mais fortes. 🤝",
            font=("Segoe UI", 8),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_card"],
        ).pack(anchor="w", pady=(6, 0))

    def _make_stat(self, parent, label, initial_value, row, col):
        """Create a stat display widget."""
        frame = tk.Frame(parent, bg=COLORS["bg_card"], pady=4)
        frame.grid(row=row, column=col, sticky="w", padx=(0, 30), pady=(0, 6))

        tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 9),
            fg=COLORS["text_dim"],
            bg=COLORS["bg_card"],
        ).pack(anchor="w")

        value_label = tk.Label(
            frame,
            text=initial_value,
            font=("Consolas", 14, "bold"),
            fg=COLORS["text_primary"],
            bg=COLORS["bg_card"],
        )
        value_label.pack(anchor="w")

        return value_label

    # ──────────────────────────────────────────────────
    # ENVIRONMENT CHECKS
    # ──────────────────────────────────────────────────
    def check_environment(self):
        """Check if WSL and cacachave are available."""
        self.log("Verificando ambiente...", "info")

        def _check():
            # Check WSL
            try:
                result = subprocess.run(
                    ["wsl", "--status"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                )
                if result.returncode != 0:
                    self.log("⚠ WSL não detectado. Instale com: wsl --install", "error")
                    return
                self.log("✓ WSL detectado", "success")
            except FileNotFoundError:
                self.log("⚠ WSL não encontrado. Instale o WSL2 primeiro.", "error")
                return
            except Exception as e:
                self.log(f"⚠ Erro ao verificar WSL: {e}", "error")
                return

            # Check cacachave
            try:
                result = subprocess.run(
                    ["wsl", "-e", "bash", "-c", f"test -f {CACACHAVE_WSL_PATH}/cacachave && echo OK"],
                    capture_output=True,
                    text=True,
                    timeout=15,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                )
                if "OK" in result.stdout:
                    self.log("✓ Cacachave encontrado e compilado", "success")
                    self.log("Pronto! Clique em INICIAR BUSCA.", "success")
                    self.set_status("Pronto para iniciar", COLORS["accent_green"])
                else:
                    self.log("⚠ Cacachave não encontrado. Instalando...", "warning")
                    self.install_cacachave()
            except Exception as e:
                self.log(f"⚠ Erro ao verificar cacachave: {e}", "error")

        threading.Thread(target=_check, daemon=True).start()

    def install_cacachave(self):
        """Install cacachave in WSL."""
        install_script = (
            "sudo apt update && sudo apt install -y git build-essential libssl-dev libgmp-dev && "
            f"cd ~ && git clone https://github.com/lmajowka/cacachave.git && "
            f"cd cacachave && make"
        )

        self.log("Instalando dependências e compilando cacachave...", "warning")
        self.log("(isso pode levar alguns minutos na primeira vez)", "info")

        def _install():
            try:
                process = subprocess.Popen(
                    ["wsl", "-e", "bash", "-c", install_script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                )
                for line in process.stdout:
                    line = line.strip()
                    if line:
                        self.log(line, "info")
                process.wait()

                if process.returncode == 0:
                    self.log("✓ Cacachave instalado com sucesso!", "success")
                    self.log("Pronto! Clique em INICIAR BUSCA.", "success")
                    self.set_status("Pronto para iniciar", COLORS["accent_green"])
                else:
                    self.log("⚠ Erro na instalação. Tente manualmente no WSL.", "error")
            except Exception as e:
                self.log(f"⚠ Erro: {e}", "error")

        threading.Thread(target=_install, daemon=True).start()

    def detect_threads(self):
        """Detect available CPU threads via WSL."""
        def _detect():
            try:
                result = subprocess.run(
                    ["wsl", "-e", "bash", "-c", "nproc"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                )
                n = result.stdout.strip()
                if n.isdigit():
                    self.thread_var.set(n)
                    self.log(f"✓ Detectado: {n} threads disponíveis", "success")
            except Exception:
                self.log("Não foi possível detectar threads", "warning")

        threading.Thread(target=_detect, daemon=True).start()

    # ──────────────────────────────────────────────────
    # HUNTING CONTROL
    # ──────────────────────────────────────────────────
    def toggle_hunting(self):
        if self.is_running:
            self.stop_hunting()
        else:
            self.start_hunting()

    def start_hunting(self):
        puzzle = self.puzzle_var.get()
        threads = self.thread_var.get()

        if puzzle not in PUZZLES:
            messagebox.showerror("Erro", "Selecione um puzzle válido.")
            return

        if not threads.isdigit() or int(threads) < 1:
            messagebox.showerror("Erro", "Número de threads inválido.")
            return

        info = PUZZLES[puzzle]

        # Create puzzle address file in WSL
        setup_cmd = f'echo "{info["address"]}" > {CACACHAVE_WSL_PATH}/puzzle_target.txt'
        try:
            subprocess.run(
                ["wsl", "-e", "bash", "-c", setup_cmd],
                capture_output=True,
                timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
            )
        except Exception as e:
            self.log(f"Erro ao preparar arquivo alvo: {e}", "error")
            return

        # Build command
        hunt_cmd = (
            f"cd {CACACHAVE_WSL_PATH} && "
            f"./cacachave -m address -f puzzle_target.txt "
            f"-b {info['bits']} -l compress -R -t {threads} -q"
        )

        self.log(f"Iniciando busca — Puzzle #{puzzle} | {threads} threads", "success")
        self.log(f"Alvo: {info['address']}", "info")
        self.log(f"Recompensa: {info['reward']}", "warning")
        self.log("─" * 50, "info")

        self.is_running = True
        self.start_time = time.time()
        self.session_keys = 0

        # Update UI
        self.start_button.configure(
            text="■  PARAR BUSCA",
            bg=COLORS["accent_red"],
            activebackground="#da3633",
        )
        self.set_status("Buscando...", COLORS["accent_green"])

        # Start process
        def _run():
            try:
                self.process = subprocess.Popen(
                    ["wsl", "-e", "bash", "-c", hunt_cmd],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                )

                for line in self.process.stdout:
                    if not self.is_running:
                        break
                    line = line.strip()
                    if not line:
                        continue

                    # Parse output
                    self.parse_output(line)

                self.process.wait()

            except Exception as e:
                self.log(f"Erro no processo: {e}", "error")
            finally:
                if self.is_running:
                    self.root.after(0, self.stop_hunting)

        self.monitor_thread = threading.Thread(target=_run, daemon=True)
        self.monitor_thread.start()

        # Start uptime ticker
        self._tick_uptime()

        # Save settings
        self.save_settings()

    def stop_hunting(self):
        self.is_running = False

        # Kill the process
        if self.process:
            try:
                # Kill the WSL process
                subprocess.run(
                    ["wsl", "-e", "bash", "-c", "pkill -f cacachave"],
                    capture_output=True,
                    timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
                )
                self.process.terminate()
            except Exception:
                pass
            self.process = None

        # Update lifetime stats
        self.settings["total_keys_lifetime"] = self.settings.get("total_keys_lifetime", 0) + self.session_keys
        if self.start_time:
            elapsed = time.time() - self.start_time
            self.settings["total_time_seconds"] = self.settings.get("total_time_seconds", 0) + elapsed
        self.save_settings()

        # Update UI
        self.start_button.configure(
            text="▶  INICIAR BUSCA",
            bg=COLORS["accent_green"],
            activebackground="#2ea043",
        )
        self.set_status("Parado", COLORS["text_dim"])

        self.log("─" * 50, "info")
        self.log("Busca pausada.", "warning")
        self.log(f"Chaves verificadas nesta sessão: {self._format_number(self.session_keys)}", "info")

    def parse_output(self, line):
        """Parse cacachave output line for statistics."""
        # Log the raw line
        self.log(line, "info")

        # Check for FOUND KEY — the big prize!
        if "FOUND" in line.upper() or "Private Key" in line or "privkey" in line.lower():
            self.log("", "found")
            self.log("🎉🎉🎉 CHAVE ENCONTRADA!!! 🎉🎉🎉", "found")
            self.log(line, "found")
            self.log(f"Lembre-se: envie 5% para {CREATOR_BTC_ADDRESS}", "found")
            self.log("", "found")

            # Show popup
            self.root.after(0, lambda: messagebox.showinfo(
                "🎉 CHAVE ENCONTRADA!!!",
                f"PARABÉNS! A chave privada foi encontrada!\n\n"
                f"{line}\n\n"
                f"Lembre-se do acordo da comunidade:\n"
                f"Envie 5% para:\n{CREATOR_BTC_ADDRESS}\n\n"
                f"A chave também foi salva no arquivo Found.txt\n"
                f"dentro da pasta cacachave no WSL."
            ))
            return

        # Parse speed: ~3 Mkeys/s (3368209 keys/s)
        speed_match = re.search(r'~(\d+)\s*Mkeys/s', line)
        if speed_match:
            self.current_speed = int(speed_match.group(1)) * 1_000_000
            self.root.after(0, lambda s=self.current_speed: self.speed_value.configure(
                text=self._format_speed(s)
            ))

        # Parse total keys: Total 101046272 keys
        total_match = re.search(r'Total\s+(\d+)\s+keys', line)
        if total_match:
            self.session_keys = int(total_match.group(1))
            lifetime = self.settings.get("total_keys_lifetime", 0) + self.session_keys

            self.root.after(0, lambda sk=self.session_keys: self.session_value.configure(
                text=self._format_number(sk)
            ))
            self.root.after(0, lambda lt=lifetime: self.lifetime_value.configure(
                text=self._format_number(lt)
            ))

        # Also try parsing keys/s directly
        kps_match = re.search(r'\((\d+)\s*keys/s\)', line)
        if kps_match:
            self.current_speed = int(kps_match.group(1))
            self.root.after(0, lambda s=self.current_speed: self.speed_value.configure(
                text=self._format_speed(s)
            ))

    # ──────────────────────────────────────────────────
    # UI UPDATES
    # ──────────────────────────────────────────────────
    def _tick_uptime(self):
        """Update uptime display every second."""
        if not self.is_running:
            return

        elapsed = time.time() - self.start_time
        self.uptime_value.configure(text=str(timedelta(seconds=int(elapsed))))
        self.root.after(1000, self._tick_uptime)

    def set_status(self, text, color):
        self.status_dot.configure(fg=color)
        self.status_label.configure(text=text)

    def log(self, message, tag="info"):
        """Thread-safe log to the text area."""
        def _log():
            self.log_text.configure(state="normal")
            timestamp = time.strftime("%H:%M:%S")
            self.log_text.insert("end", f"[{timestamp}] {message}\n", tag)
            self.log_text.see("end")
            self.log_text.configure(state="disabled")

        self.root.after(0, _log)

    def on_puzzle_change(self, event=None):
        puzzle = self.puzzle_var.get()
        if puzzle in PUZZLES:
            self.addr_label.configure(text=PUZZLES[puzzle]["address"])
            self.reward_label.configure(text=f"Recompensa: {PUZZLES[puzzle]['reward']}")

    def copy_creator_address(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(CREATOR_BTC_ADDRESS)
        self.log("Endereço do criador copiado!", "success")

    def on_close(self):
        if self.is_running:
            if messagebox.askyesno(
                "Sair",
                "A busca está em andamento. Deseja realmente sair?\n"
                "O progresso da sessão será salvo."
            ):
                self.stop_hunting()
                self.root.destroy()
        else:
            self.root.destroy()

    # ──────────────────────────────────────────────────
    # FORMATTERS
    # ──────────────────────────────────────────────────
    @staticmethod
    def _format_number(n):
        if n >= 1_000_000_000_000:
            return f"{n / 1_000_000_000_000:.2f} T"
        elif n >= 1_000_000_000:
            return f"{n / 1_000_000_000:.2f} B"
        elif n >= 1_000_000:
            return f"{n / 1_000_000:.2f} M"
        elif n >= 1_000:
            return f"{n / 1_000:.1f} K"
        return str(n)

    @staticmethod
    def _format_speed(kps):
        if kps >= 1_000_000_000:
            return f"{kps / 1_000_000_000:.2f} Gkeys/s"
        elif kps >= 1_000_000:
            return f"{kps / 1_000_000:.1f} Mkeys/s"
        elif kps >= 1_000:
            return f"{kps / 1_000:.1f} Kkeys/s"
        return f"{kps} keys/s"


# ══════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = tk.Tk()

    # Set icon if available
    try:
        root.iconbitmap(default="icon.ico")
    except Exception:
        pass

    # Dark title bar on Windows 10/11
    try:
        import ctypes
        root.update()
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int)
        )
    except Exception:
        pass

    app = PuzzleHunterApp(root)
    root.mainloop()
