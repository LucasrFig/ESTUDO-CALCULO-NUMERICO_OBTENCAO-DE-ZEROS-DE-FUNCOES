import tkinter as tk
from tkinter import ttk, messagebox
import math

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import metodos


# -------------------- Aparência --------------------
FUNDO = "#EEF2F8"
PAINEL = "#FFFFFF"
BORDA = "#D5DEEA"
TEXTO = "#1E293B"
SECUNDARIO = "#5B6B82"
DESTAQUE = "#2563EB"
DESTAQUE_HOVER = "#1D4ED8"
ERRO = "#B42332"
SUCESSO = "#16805D"


class InterfaceMetodos:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title("Análise comparativa dos métodos numéricos")
        self.raiz.geometry("1420x900")
        self.raiz.minsize(1120, 740)
        self.raiz.configure(bg=FUNDO)

        self.resultados = {}
        self.funcao_numerica = None
        self.expressao = None
        self.simbolo_x = sp.Symbol("x")
        self.tipo_grafico = "funcao"

        plt.rcParams.update({
            "font.family": "Segoe UI",
            "font.size": 12,
            "axes.titlesize": 15,
            "axes.labelsize": 12,
            "xtick.labelsize": 11,
            "ytick.labelsize": 11,
            "legend.fontsize": 10
        })

        self._configurar_estilos()
        self._montar_interface()
        self._desenhar_grafico_inicial()

    def _configurar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure(
            "TLabel", background=PAINEL, foreground=TEXTO,
            font=("Segoe UI", 11)
        )
        estilo.configure(
            "TButton", background="#E6EDF7", foreground=TEXTO,
            padding=(12, 9), font=("Segoe UI", 11, "bold"),
            borderwidth=0
        )
        estilo.map(
            "TButton",
            background=[("active", "#D7E5F8"), ("pressed", "#C7D9F2")],
            foreground=[("disabled", "#8A96A8")]
        )
        estilo.configure(
            "Primary.TButton", background=DESTAQUE, foreground="#FFFFFF",
            padding=(14, 11), font=("Segoe UI", 12, "bold"), borderwidth=0
        )
        estilo.map(
            "Primary.TButton",
            background=[("active", DESTAQUE_HOVER), ("pressed", DESTAQUE_HOVER)]
        )
        estilo.configure(
            "TEntry", fieldbackground="#F8FAFC", foreground=TEXTO,
            insertcolor=TEXTO, padding=(8, 7), bordercolor=BORDA
        )
        estilo.configure(
            "TLabelframe", background=PAINEL, foreground=TEXTO,
            bordercolor=BORDA, relief="solid", borderwidth=1
        )
        estilo.configure(
            "TLabelframe.Label", background=PAINEL, foreground=TEXTO,
            font=("Segoe UI", 12, "bold")
        )
        estilo.configure(
            "TCheckbutton", background=PAINEL, foreground=TEXTO,
            font=("Segoe UI", 11)
        )

    def _painel(self, pai, titulo):
        quadro = ttk.LabelFrame(pai, text=titulo, padding=14)
        return quadro

    def _montar_interface(self):
        # Cabeçalho compacto para dar identidade visual e orientar o usuário.
        cabecalho = tk.Frame(self.raiz, bg="#172B4D", padx=22, pady=13)
        cabecalho.pack(fill="x")
        tk.Label(
            cabecalho, text="Análise comparativa",
            bg="#172B4D", fg="#FFFFFF",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w")
        tk.Label(
            cabecalho,
            text="Métodos numéricos para obtenção de zeros de funções",
            bg="#172B4D", fg="#D8E4F5",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(2, 0))

        principal = tk.Frame(self.raiz, bg=FUNDO, padx=16, pady=14)
        principal.pack(fill="both", expand=True)

        principal.columnconfigure(0, weight=4, uniform="top")
        principal.columnconfigure(1, weight=1, uniform="top")
        principal.columnconfigure(2, weight=5, uniform="top")
        principal.rowconfigure(0, weight=3, minsize=390)
        principal.rowconfigure(1, weight=2, minsize=220)

        # Função e parâmetros, lado esquerdo
        topo_esquerdo = tk.Frame(principal, bg=FUNDO)
        topo_esquerdo.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        topo_esquerdo.columnconfigure(0, weight=1)
        topo_esquerdo.rowconfigure(1, weight=1)

        quadro_funcao = self._painel(topo_esquerdo, "Função f(x)")
        quadro_funcao.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        quadro_funcao.columnconfigure(0, weight=1)

        self.entrada_funcao = ttk.Entry(quadro_funcao, font=("Cascadia Code", 13))
        self.entrada_funcao.insert(0, "x**3 - 2*x - 5")
        self.entrada_funcao.grid(row=0, column=0, sticky="ew", padx=3, pady=3)

        quadro_parametros = self._painel(topo_esquerdo, "Parâmetros")
        quadro_parametros.grid(row=1, column=0, sticky="nsew")
        quadro_parametros.columnconfigure(1, weight=1)
        quadro_parametros.columnconfigure(3, weight=1)

        campos = [
            ("Limite A (Bissecção/Falsa Posição)", "limite_a", "0"),
            ("Limite B (Bissecção/Falsa Posição)", "limite_b", "3"),
            ("Chute X0 (Newton-Raphson)", "x0_newton", "2"),
            ("Chute X0 (Secante)", "x0_secante", "1"),
            ("Chute X1 (Secante)", "x1_secante", "3"),
            ("Tolerância", "tolerancia", "0.000001"),
            ("Limite de iterações", "limite_iteracoes", "1000"),
        ]
        self.entradas = {}
        for i, (rotulo, chave, valor) in enumerate(campos):
            linha = i // 2
            coluna = (i % 2) * 2
            ttk.Label(quadro_parametros, text=rotulo, wraplength=205).grid(
                row=linha, column=coluna, sticky="w", padx=6, pady=9
            )
            entrada = ttk.Entry(quadro_parametros, width=14, font=("Segoe UI", 11))
            entrada.insert(0, valor)
            entrada.grid(row=linha, column=coluna + 1, sticky="ew", padx=6, pady=9)
            self.entradas[chave] = entrada

        botao_executar = ttk.Button(
            quadro_parametros, text="▶  Executar análise",
            command=self.executar, style="Primary.TButton"
        )
        botao_executar.grid(
            row=4, column=0, columnspan=4, sticky="ew", padx=4, pady=(12, 4)
        )

        # Botões para trocar o gráfico
        controles = tk.Frame(principal, bg=FUNDO)
        controles.grid(row=0, column=1, sticky="ns", padx=4)
        ttk.Label(
            controles, text="VISUALIZAÇÃO", background=FUNDO,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="center", pady=(8, 12))
        botoes = [
            ("f(x) e raízes", "funcao"),
            ("Tempo", "tempo_ms"),
            ("Iterações", "iteracoes"),
            ("Resíduo", "residuo"),
        ]
        for texto, tipo in botoes:
            ttk.Button(
                controles, text=texto, command=lambda t=tipo: self.mudar_grafico(t)
            ).pack(fill="x", pady=5)

        # Área de gráfico
        quadro_grafico = self._painel(principal, "Visualização")
        quadro_grafico.grid(row=0, column=2, sticky="nsew", padx=(8, 0))
        quadro_grafico.rowconfigure(0, weight=1)
        quadro_grafico.columnconfigure(0, weight=1)

        self.figura, self.eixo = plt.subplots(figsize=(7, 4.5), dpi=100)
        self.figura.patch.set_facecolor(PAINEL)
        self.eixo.set_facecolor(PAINEL)
        self.canvas = FigureCanvasTkAgg(self.figura, master=quadro_grafico)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        # Quatro cartões inferiores
        inferior = tk.Frame(principal, bg=FUNDO)
        inferior.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(14, 0))
        for coluna in range(4):
            inferior.columnconfigure(coluna, weight=1, uniform="metodos")
        inferior.rowconfigure(0, weight=1)

        nomes = [
            ("Bissecção", "bisseccao"),
            ("Falsa Posição", "falsa_pos"),
            ("Newton-Raphson", "newton"),
            ("Secante", "secante"),
        ]
        self.cartoes = {}
        for coluna, (nome, chave) in enumerate(nomes):
            quadro = self._painel(inferior, nome)
            quadro.grid(row=0, column=coluna, sticky="nsew", padx=5)
            texto = tk.Text(
                quadro, height=8, wrap="word", bg=PAINEL, fg=TEXTO,
                insertbackground=TEXTO, relief="flat",
                font=("Segoe UI", 11),
                padx=10, pady=10,
                state="disabled"
            )
            texto.pack(fill="both", expand=True)
            self.cartoes[chave] = texto
            self._atualizar_cartao(chave, None)

    
    def _atualizar_cartao(self, chave, resultado):
        widget = self.cartoes[chave]
        widget.configure(state="normal")
        widget.delete("1.0", "end")

        # Estilos para diferenciar os rótulos dos valores
        widget.tag_configure(
            "rotulo",
            font=("Segoe UI", 11, "bold"),
            foreground=DESTAQUE
        )
        widget.tag_configure(
            "valor",
            font=("Segoe UI", 11),
            foreground=TEXTO
        )
        widget.tag_configure(
            "erro",
            font=("Segoe UI", 11, "bold"),
            foreground=ERRO
        )

        if resultado is None:
            widget.insert("end", "Aguardando execução.", "valor")

        elif resultado.get("erro"):
            widget.insert("end", "Erro ao calcular\n\n", "erro")
            widget.insert("end", resultado.get("mensagem", ""), "valor")

        else:
            raiz = format(resultado["raiz"], ".15g")
            residuo = format(resultado["residuo"], ".15g")
            tempo = format(resultado["tempo_ms"], ".8g")

            campos = [
                ("Raiz encontrada [x]", raiz),
                ("Nº de iterações", str(resultado["iteracoes"])),
                ("Tempo de execução", f"{tempo} ms"),
                ("Resíduo final |f(x)|", residuo),
                ("Convergiu", "Sim" if resultado["convergiu"] else "Não"),
            ]

            for i, (rotulo, valor) in enumerate(campos):
                widget.insert("end", rotulo + ": ", "rotulo")
                widget.insert("end", valor + "\n", "valor")

                # Espaço menor entre os campos
                if i < len(campos) - 1:
                    widget.insert("end", "\n")

        widget.configure(state="disabled")


    def _desenhar_grafico_inicial(self):
        self.eixo.clear()
        self.eixo.set_facecolor(PAINEL)
        self.eixo.text(
            0.5, 0.5, "Digite uma função e clique em\nExecutar análise",
            color=TEXTO, ha="center", va="center",
            transform=self.eixo.transAxes
        )
        self._estilizar_eixo()
        self.canvas.draw()

    def _estilizar_eixo(self):
        self.eixo.tick_params(colors=TEXTO)
        self.eixo.xaxis.label.set_color(TEXTO)
        self.eixo.yaxis.label.set_color(TEXTO)
        self.eixo.title.set_color(TEXTO)
        for borda in self.eixo.spines.values():
            borda.set_color(BORDA)
        self.eixo.grid(True, color="#D8E1ED", alpha=0.8, linewidth=0.8)
        self.eixo.set_axisbelow(True)

    def executar(self):
        texto = self.entrada_funcao.get().strip()
        p = {chave: entrada.get().strip() for chave, entrada in self.entradas.items()}

        # Entradas inválidas ou expressão inválida são erros gerais da configuração.
        try:
            expressao = sp.sympify(texto)
            funcao = sp.lambdify(self.simbolo_x, expressao, modules=["math"])
            limite_a = float(p["limite_a"].replace(",", "."))
            limite_b = float(p["limite_b"].replace(",", "."))
            x0_newton = float(p["x0_newton"].replace(",", "."))
            x0_secante = float(p["x0_secante"].replace(",", "."))
            x1_secante = float(p["x1_secante"].replace(",", "."))
            tolerancia = float(p["tolerancia"].replace(",", "."))
            limite_iteracoes = int(p["limite_iteracoes"])
            if tolerancia <= 0 or limite_iteracoes < 1:
                raise ValueError("A tolerância deve ser positiva e o limite de iterações deve ser maior que zero.")
        except Exception as erro:
            messagebox.showerror("Dados inválidos", f"Verifique a função e os parâmetros.\n\nDetalhe: {erro}")
            return

        derivada_expr = sp.diff(expressao, self.simbolo_x)
        derivada = sp.lambdify(self.simbolo_x, derivada_expr, modules=["math"])

        self.expressao = expressao
        self.funcao_numerica = funcao
        configuracoes = [
            ("bisseccao", lambda: metodos.metodo_bisseccao(
                funcao, limite_a, limite_b, tolerancia, limite_iteracoes
            )),
            ("falsa_pos", lambda: metodos.metodo_falsa_pos(
                funcao, limite_a, limite_b, tolerancia, limite_iteracoes
            )),
            ("newton", lambda: metodos.metodo_newton_raphson(
                funcao, derivada, x0_newton, tolerancia, limite_iteracoes
            )),
            ("secante", lambda: metodos.metodo_secante(
                funcao, x0_secante, x1_secante, tolerancia, limite_iteracoes
            )),
        ]

        self.resultados = {}
        for chave, executar_metodo in configuracoes:
            try:
                resultado = executar_metodo()
                if resultado["raiz"] is None or not math.isfinite(float(resultado["raiz"])):
                    raise ValueError("O método não produziu uma raiz válida.")
                if resultado["residuo"] is None or not math.isfinite(float(resultado["residuo"])):
                    raise ValueError("O método não produziu um resíduo válido.")
                self.resultados[chave] = resultado
            except Exception as erro:
                self.resultados[chave] = {
                    "erro": True,
                    "mensagem": str(erro) or "Falha durante o cálculo."
                }
            self._atualizar_cartao(chave, self.resultados[chave])

        self.mudar_grafico(self.tipo_grafico)

    def mudar_grafico(self, tipo):
        self.tipo_grafico = tipo
        self.eixo.clear()
        self.eixo.set_facecolor(PAINEL)

        if tipo == "funcao":
            self._plotar_funcao()
        else:
            self._plotar_comparacao(tipo)

        self._estilizar_eixo()
        self.figura.tight_layout()
        self.canvas.draw()

    def _plotar_funcao(self):
        self.eixo.set_title(f"f(x) = {sp.sstr(self.expressao)}")
        self.eixo.set_xlabel("x")
        self.eixo.set_ylabel("f(x)")

        valores_x = []
        for chave in ("bisseccao", "falsa_pos", "newton", "secante"):
            if chave in self.resultados and not self.resultados[chave].get("erro"):
                valores_x.append(float(self.resultados[chave]["raiz"]))

        try:
            a = float(self.entradas["limite_a"].get().replace(",", "."))
            b = float(self.entradas["limite_b"].get().replace(",", "."))
            pontos_base = [a, b]
        except ValueError:
            pontos_base = [-10, 10]
        pontos_base += valores_x
        xmin, xmax = min(pontos_base), max(pontos_base)
        largura = xmax - xmin
        if largura == 0:
            largura = max(abs(xmin) * 0.2, 2)
        xmin -= largura * 0.25
        xmax += largura * 0.25

        xs = np.linspace(xmin, xmax, 800)
        ys = []
        xs_validos = []
        for valor in xs:
            try:
                y = float(self.funcao_numerica(float(valor)))
                if math.isfinite(y) and abs(y) < 1e12:
                    xs_validos.append(valor)
                    ys.append(y)
                else:
                    xs_validos.append(valor)
                    ys.append(np.nan)
            except (ValueError, OverflowError, ZeroDivisionError):
                xs_validos.append(valor)
                ys.append(np.nan)

        self.eixo.plot(xs_validos, ys, color=DESTAQUE, label="f(x)")
        self.eixo.axhline(0, color="#9AA8BA", linewidth=1)

        raizes_plotadas = set()
        for chave, resultado in self.resultados.items():
            if resultado.get("erro"):
                continue
            raiz = float(resultado["raiz"])
            if raiz in raizes_plotadas:
                continue
            raizes_plotadas.add(raiz)
            try:
                y = float(self.funcao_numerica(raiz))
            except Exception:
                y = 0.0
            self.eixo.scatter([raiz], [y], s=45, label=f"Raiz ({chave})")
            self.eixo.axvline(raiz, color="#AAB8CA", alpha=0.35, linestyle="--")

        self.eixo.legend(facecolor=PAINEL, labelcolor=TEXTO, fontsize=9, frameon=False)

    def _plotar_comparacao(self, tipo):
        nomes = {
            "tempo_ms": ("Tempo de execução (ms)", "tempo_ms"),
            "iteracoes": ("Número de iterações", "iteracoes"),
            "residuo": ("Resíduo final |f(x)| (menor é melhor)", "residuo"),
        }
        titulo, campo = nomes[tipo]
        validos = [
            (chave, resultado) for chave, resultado in self.resultados.items()
            if not resultado.get("erro")
        ]
        self.eixo.set_title(titulo)
        if not validos:
            self.eixo.text(
                0.5, 0.5, "Nenhum método calculou uma raiz.",
                color=TEXTO, ha="center", va="center",
                transform=self.eixo.transAxes
            )
            return

        rotulos = [resultado["metodo"] for _, resultado in validos]
        valores = [float(resultado[campo]) for _, resultado in validos]
        barras = self.eixo.bar(rotulos, valores, color=DESTAQUE)
        self.eixo.set_ylabel(titulo)
        self.eixo.tick_params(axis="x", labelrotation=15)
        for barra, valor in zip(barras, valores):
            texto = format(valor, ".8g")
            self.eixo.annotate(
                texto,
                (barra.get_x() + barra.get_width() / 2, barra.get_height()),
                xytext=(0, 4), textcoords="offset points",
                ha="center", va="bottom", color=TEXTO, fontsize=10
            )


if __name__ == "__main__":
    janela = tk.Tk()
    app = InterfaceMetodos(janela)
    janela.mainloop()
