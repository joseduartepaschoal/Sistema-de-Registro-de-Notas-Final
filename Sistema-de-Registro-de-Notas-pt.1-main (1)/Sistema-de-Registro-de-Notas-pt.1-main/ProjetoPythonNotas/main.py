import tkinter as tk
from tkinter import ttk, messagebox
from database import SistemaNotasDB


class SistemaNotas:
    CURSOS = (
        "Ciência da Computação",
        "Engenharia de Software",
        "Sistemas de Informação",
        "Análise e Desenvolvimento de Sistemas",
        "Engenharia da Computação",
    )

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Acadêmico de Registro de Notas")
        self.root.geometry("940x640")
        self.root.minsize(900, 600)

        self.db = SistemaNotasDB()
        self.db.criar_tabela()
        self.id_em_edicao = None
        self.modo_escuro = False

        self.style = ttk.Style()
        self._configurar_estilos()
        self._centralizar_janela()
        self._build_ui()
        self.listar()

    def _centralizar_janela(self):
        self.root.update_idletasks()
        largura = 940
        altura = 640
        x = (self.root.winfo_screenwidth() // 2) - (largura // 2)
        y = (self.root.winfo_screenheight() // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    def _configurar_estilos(self):
        self.temas = {
            "claro": {
                "bg": "#f3f5f8",
                "surface": "#ffffff",
                "surface_alt": "#eef2f7",
                "text": "#172033",
                "muted": "#667085",
                "border": "#d0d5dd",
                "primary": "#1d4ed8",
                "primary_hover": "#1e40af",
                "primary_text": "#ffffff",
                "disabled_bg": "#e5e7eb",
                "disabled_text": "#98a2b3",
                "entry": "#ffffff",
                "tree": "#ffffff",
                "tree_alt": "#f8fafc",
                "heading": "#e9eef5",
                "select": "#dbeafe",
                "success": "#dcfce7",
                "warning": "#fef9c3",
                "danger": "#fee2e2",
            },
            "escuro": {
                "bg": "#101827",
                "surface": "#182234",
                "surface_alt": "#111827",
                "text": "#f8fafc",
                "muted": "#cbd5e1",
                "border": "#334155",
                "primary": "#60a5fa",
                "primary_hover": "#93c5fd",
                "primary_text": "#0f172a",
                "disabled_bg": "#243044",
                "disabled_text": "#7f8da3",
                "entry": "#0f172a",
                "tree": "#111827",
                "tree_alt": "#1e293b",
                "heading": "#253247",
                "select": "#1d4ed8",
                "success": "#14532d",
                "warning": "#713f12",
                "danger": "#7f1d1d",
            },
        }
        self._aplicar_tema()

    def _aplicar_tema(self):
        tema = self.temas["escuro" if self.modo_escuro else "claro"]
        self.root.configure(bg=tema["bg"])
        self.style.theme_use("clam")

        self.style.configure(".", font=("Segoe UI", 10), background=tema["bg"], foreground=tema["text"])
        self.style.configure("TFrame", background=tema["bg"])
        self.style.configure("Surface.TFrame", background=tema["surface"])
        self.style.configure("Header.TFrame", background=tema["bg"])
        self.style.configure("TLabel", background=tema["bg"], foreground=tema["text"])
        self.style.configure("Surface.TLabel", background=tema["surface"], foreground=tema["text"])
        self.style.configure("Muted.TLabel", background=tema["bg"], foreground=tema["muted"])
        self.style.configure("HeaderTitle.TLabel", font=("Segoe UI", 20, "bold"), background=tema["bg"], foreground=tema["text"])
        self.style.configure("HeaderSub.TLabel", font=("Segoe UI", 10), background=tema["bg"], foreground=tema["muted"])
        self.style.configure("Status.TLabel", background=tema["surface"], foreground=tema["muted"], padding=(16, 7))

        self.style.configure(
            "TLabelframe",
            background=tema["surface"],
            foreground=tema["text"],
            bordercolor=tema["border"],
            relief="solid",
        )
        self.style.configure("TLabelframe.Label", background=tema["surface"], foreground=tema["text"], font=("Segoe UI", 10, "bold"))

        self.style.configure(
            "TEntry",
            fieldbackground=tema["entry"],
            foreground=tema["text"],
            insertcolor=tema["text"],
            bordercolor=tema["border"],
            lightcolor=tema["border"],
            darkcolor=tema["border"],
            padding=(10, 8),
        )
        self.style.configure(
            "TCombobox",
            fieldbackground=tema["entry"],
            background=tema["entry"],
            foreground=tema["text"],
            arrowcolor=tema["muted"],
            bordercolor=tema["border"],
            lightcolor=tema["border"],
            darkcolor=tema["border"],
            padding=(10, 8),
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", tema["entry"])],
            foreground=[("readonly", tema["text"])],
            selectbackground=[("readonly", tema["entry"])],
            selectforeground=[("readonly", tema["text"])],
            arrowcolor=[("active", tema["primary"]), ("readonly", tema["muted"])],
        )
        self.root.option_add("*TCombobox*Listbox.background", tema["entry"])
        self.root.option_add("*TCombobox*Listbox.foreground", tema["text"])
        self.root.option_add("*TCombobox*Listbox.selectBackground", tema["primary"])
        self.root.option_add("*TCombobox*Listbox.selectForeground", tema["primary_text"])

        self.style.configure("TNotebook", background=tema["bg"], borderwidth=0, tabmargins=(0, 0, 0, 0))
        self.style.configure(
            "TNotebook.Tab",
            background=tema["surface_alt"],
            foreground=tema["muted"],
            padding=(22, 11),
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", tema["surface"]), ("active", tema["heading"])],
            foreground=[("selected", tema["text"]), ("active", tema["text"])],
            padding=[("selected", (26, 14)), ("!selected", (22, 10))],
        )

        self.style.configure(
            "TButton",
            background=tema["surface"],
            foreground=tema["text"],
            bordercolor=tema["border"],
            lightcolor=tema["border"],
            darkcolor=tema["border"],
            padding=(14, 8),
            font=("Segoe UI", 10),
            borderwidth=1,
        )
        self.style.map(
            "TButton",
            background=[("disabled", tema["disabled_bg"]), ("active", tema["heading"])],
            foreground=[("disabled", tema["disabled_text"]), ("active", tema["text"])],
            bordercolor=[("disabled", tema["border"])],
            lightcolor=[("disabled", tema["border"])],
            darkcolor=[("disabled", tema["border"])],
        )
        self.style.configure("Primary.TButton", background=tema["primary"], foreground=tema["primary_text"])
        self.style.map(
            "Primary.TButton",
            background=[("disabled", tema["disabled_bg"]), ("active", tema["primary_hover"])],
            foreground=[("active", tema["primary_text"]), ("disabled", tema["muted"])],
            bordercolor=[("disabled", tema["border"])],
            lightcolor=[("disabled", tema["border"])],
            darkcolor=[("disabled", tema["border"])],
        )
        self.style.configure(
            "Theme.TButton",
            background=tema["surface"],
            foreground=tema["text"],
            bordercolor=tema["border"],
            padding=(16, 9),
            font=("Segoe UI", 10, "bold"),
        )
        self.style.map(
            "Theme.TButton",
            background=[("disabled", tema["disabled_bg"]), ("active", tema["heading"])],
            foreground=[("disabled", tema["disabled_text"]), ("active", tema["text"])],
            bordercolor=[("disabled", tema["border"])],
            lightcolor=[("disabled", tema["border"])],
            darkcolor=[("disabled", tema["border"])],
        )

        self.style.configure(
            "Treeview",
            background=tema["tree"],
            foreground=tema["text"],
            fieldbackground=tema["tree"],
            rowheight=32,
            bordercolor=tema["border"],
            lightcolor=tema["border"],
            darkcolor=tema["border"],
        )
        self.style.configure(
            "Treeview.Heading",
            background=tema["heading"],
            foreground=tema["text"],
            font=("Segoe UI", 10, "bold"),
            padding=(10, 9),
            relief="flat",
        )
        self.style.map("Treeview", background=[("selected", tema["select"])], foreground=[("selected", tema["text"])])

        if hasattr(self, "tree"):
            self._configurar_tags_tabela()

    def _build_ui(self):
        container = ttk.Frame(self.root, padding=(20, 18, 20, 14))
        container.pack(fill="both", expand=True)

        topo = ttk.Frame(container, style="Header.TFrame")
        topo.pack(fill="x", pady=(0, 16))
        textos_topo = ttk.Frame(topo, style="Header.TFrame")
        textos_topo.pack(side="left", fill="x", expand=True)
        ttk.Label(textos_topo, text="Sistema Acadêmico", style="HeaderTitle.TLabel").pack(anchor="w")
        ttk.Label(textos_topo, text="Registro de notas, cursos e matrículas", style="HeaderSub.TLabel").pack(anchor="w", pady=(2, 0))

        self.btn_tema = ttk.Button(topo, text="Modo Escuro", style="Theme.TButton", command=self.alternar_tema)
        self.btn_tema.pack(side="right", padx=(16, 0))

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        self.aba_cadastro = ttk.Frame(self.notebook, padding=18, style="Surface.TFrame")
        self.aba_busca = ttk.Frame(self.notebook, padding=18, style="Surface.TFrame")
        self.notebook.add(self.aba_cadastro, text="Cadastro")
        self.notebook.add(self.aba_busca, text="Busca")

        self._build_aba_cadastro()
        self._build_aba_busca()

        self.lbl_status_bar = ttk.Label(self.root, text="Pronto.", style="Status.TLabel", anchor="w")
        self.lbl_status_bar.pack(fill="x", side="bottom")

    def _build_aba_cadastro(self):
        form = ttk.LabelFrame(self.aba_cadastro, text="Dados do Aluno", padding=18)
        form.pack(fill="x", anchor="n")
        form.columnconfigure(1, weight=1)
        form.columnconfigure(3, weight=1)

        ttk.Label(form, text="Matrícula:", style="Surface.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=9)
        self.ent_matricula = ttk.Entry(form)
        self.ent_matricula.grid(row=0, column=1, sticky="ew", padx=(0, 20), pady=9)

        ttk.Label(form, text="Nome:", style="Surface.TLabel").grid(row=0, column=2, sticky="w", padx=(0, 10), pady=9)
        self.ent_nome = ttk.Entry(form)
        self.ent_nome.grid(row=0, column=3, sticky="ew", pady=9)

        ttk.Label(form, text="Curso:", style="Surface.TLabel").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=9)
        self.cmb_curso = ttk.Combobox(form, values=self.CURSOS, state="readonly")
        self.cmb_curso.grid(row=1, column=1, sticky="ew", padx=(0, 20), pady=9)

        ttk.Label(form, text="Nota:", style="Surface.TLabel").grid(row=1, column=2, sticky="w", padx=(0, 10), pady=9)
        self.ent_nota = ttk.Entry(form)
        self.ent_nota.grid(row=1, column=3, sticky="ew", pady=9)

        self.lbl_status = ttk.Label(form, text="", style="Surface.TLabel")
        self.lbl_status.grid(row=2, column=0, columnspan=4, sticky="w", pady=(8, 0))

        btn_frame = ttk.Frame(self.aba_cadastro, padding=(0, 18, 0, 0), style="Surface.TFrame")
        btn_frame.pack(fill="x")

        self.btn_cadastrar = ttk.Button(btn_frame, text="Cadastrar", style="Primary.TButton", command=self.cadastrar)
        self.btn_cadastrar.pack(side="left", padx=(0, 8))

        self.btn_salvar = ttk.Button(btn_frame, text="Salvar Edição", command=self.salvar, state="disabled")
        self.btn_salvar.pack(side="left", padx=8)

        ttk.Button(btn_frame, text="Editar", command=self.carregar).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar).pack(side="left", padx=8)

    def _build_aba_busca(self):
        filtros = ttk.LabelFrame(self.aba_busca, text="Filtros de Busca", padding=16)
        filtros.pack(fill="x")
        filtros.columnconfigure(1, weight=1)
        filtros.columnconfigure(3, weight=1)
        filtros.columnconfigure(5, weight=1)

        ttk.Label(filtros, text="Buscar por nome:", style="Surface.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=7)
        self.ent_busca = ttk.Entry(filtros)
        self.ent_busca.grid(row=0, column=1, sticky="ew", padx=(0, 14), pady=7)

        ttk.Label(filtros, text="Buscar por matrícula:", style="Surface.TLabel").grid(row=0, column=2, sticky="w", padx=(0, 8), pady=7)
        self.ent_busca_matricula = ttk.Entry(filtros)
        self.ent_busca_matricula.grid(row=0, column=3, sticky="ew", padx=(0, 14), pady=7)

        ttk.Label(filtros, text="Filtro por curso:", style="Surface.TLabel").grid(row=0, column=4, sticky="w", padx=(0, 8), pady=7)
        self.cmb_busca_curso = ttk.Combobox(filtros, values=self.CURSOS, state="readonly")
        self.cmb_busca_curso.grid(row=0, column=5, sticky="ew", pady=7)

        for campo in (self.ent_busca, self.ent_busca_matricula, self.cmb_busca_curso):
            campo.bind("<Return>", lambda _event: self.buscar())

        botoes = ttk.Frame(self.aba_busca, padding=(0, 12, 0, 8), style="Surface.TFrame")
        botoes.pack(fill="x")
        ttk.Button(botoes, text="Buscar", style="Primary.TButton", command=self.buscar).pack(side="left", padx=(0, 8))
        ttk.Button(botoes, text="Limpar filtros", command=self.limpar_filtros).pack(side="left", padx=8)

        tabela_frame = ttk.Frame(self.aba_busca, style="Surface.TFrame")
        tabela_frame.pack(fill="both", expand=True, pady=(8, 0))

        colunas = ("Matrícula", "Nome", "Curso", "Nota", "Situação")
        self.tree = ttk.Treeview(tabela_frame, columns=colunas, show="headings", height=12)

        larguras = {
            "Matrícula": 120,
            "Nome": 250,
            "Curso": 285,
            "Nota": 85,
            "Situação": 130,
        }
        for coluna in colunas:
            self.tree.heading(coluna, text=coluna)
            anchor = "center" if coluna in ("Matrícula", "Nota", "Situação") else "w"
            self.tree.column(coluna, width=larguras[coluna], minwidth=80, anchor=anchor, stretch=True)

        scroll_y = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(tabela_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        tabela_frame.rowconfigure(0, weight=1)
        tabela_frame.columnconfigure(0, weight=1)

        rodape_tabela = ttk.Frame(self.aba_busca, padding=(0, 8, 0, 0), style="Surface.TFrame")
        rodape_tabela.pack(fill="x")
        self.lbl_total = ttk.Label(rodape_tabela, text="Total: 0 aluno(s)", style="Muted.TLabel")
        self.lbl_total.pack(side="right")

    def _validar(self):
        matricula = self.ent_matricula.get().strip()
        nome = self.ent_nome.get().strip()
        curso = self.cmb_curso.get().strip()
        nota_str = self.ent_nota.get().strip()

        if not matricula or not nome or not curso or not nota_str:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            if not matricula:
                self.ent_matricula.focus()
            elif not nome:
                self.ent_nome.focus()
            elif not curso:
                self.cmb_curso.focus()
            else:
                self.ent_nota.focus()
            return None, None, None, None

        if not curso:
            messagebox.showwarning("Atenção", "Selecione um curso.")
            self.cmb_curso.focus()
            return None, None, None, None

        try:
            nota = float(nota_str.replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Informe uma nota válida.")
            self.ent_nota.focus()
            return None, None, None, None

        if not (0 <= nota <= 10):
            messagebox.showerror("Erro", "A nota deve estar entre 0 e 10.")
            self.ent_nota.focus()
            return None, None, None, None

        return matricula, nome, curso, nota

    def _situacao(self, nota):
        if nota >= 7:
            return "Aprovado"
        elif nota >= 5:
            return "Recuperação"
        else:
            return "Reprovado"

    def _atualizar_status(self, texto):
        self.lbl_status_bar.config(text=texto)

    def cadastrar(self):
        matricula, nome, curso, nota = self._validar()
        if nome is None:
            return
        self.db.inserir_aluno(matricula, nome, curso, nota)
        messagebox.showinfo("Sucesso", f"Aluno '{nome}' cadastrado com nota {nota:.1f}!")
        self._atualizar_status("Cadastro realizado com sucesso.")
        self.limpar()
        self.listar()

    def listar(self):
        self._preencher_tabela(self.db.listar_alunos())

    def buscar(self):
        termo_nome = self.ent_busca.get().strip()
        termo_matricula = self.ent_busca_matricula.get().strip()
        curso = self.cmb_busca_curso.get().strip()

        if not termo_nome and not termo_matricula and not curso:
            messagebox.showwarning("Atenção", "Informe pelo menos um filtro para buscar.")
            return

        resultados = self.db.buscar_aluno(termo_nome, termo_matricula, curso)
        if not resultados:
            messagebox.showinfo("Busca", "Nenhum aluno encontrado.")
        self._preencher_tabela(resultados)
        self._atualizar_status("Busca concluída. Filtro aplicado.")

    def carregar(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno na tabela para editar.")
            return
        aluno_id = int(item[0])
        dados = self.tree.item(item)["values"]
        self.id_em_edicao = aluno_id

        self.ent_matricula.delete(0, tk.END)
        self.ent_matricula.insert(0, dados[0])
        self.ent_nome.delete(0, tk.END)
        self.ent_nome.insert(0, dados[1])
        self.cmb_curso.set(dados[2])
        self.ent_nota.delete(0, tk.END)
        self.ent_nota.insert(0, dados[3])

        self.notebook.select(self.aba_cadastro)
        self.btn_cadastrar.config(state="disabled")
        self.btn_salvar.config(state="normal")
        self.lbl_status.config(text=f"Editando aluno matrícula {dados[0]}")
        self.ent_nome.focus()

    def salvar(self):
        matricula, nome, curso, nota = self._validar()
        if nome is None:
            return
        self.db.atualizar_aluno(self.id_em_edicao, matricula, nome, curso, nota)
        messagebox.showinfo("Sucesso", f"Aluno matrícula {matricula} atualizado!")
        self._atualizar_status("Registro atualizado.")
        self.limpar()
        self.listar()

    def excluir(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um aluno na tabela para excluir.")
            return
        aluno_id = int(item[0])
        dados = self.tree.item(item)["values"]
        if messagebox.askyesno("Confirmar", f"Deseja excluir o aluno '{dados[1]}'?"):
            self.db.deletar_aluno(aluno_id)
            self._atualizar_status("Registro removido.")
            self.limpar()
            self.listar()

    def limpar(self):
        self.ent_matricula.delete(0, tk.END)
        self.ent_nome.delete(0, tk.END)
        self.cmb_curso.set("")
        self.ent_nota.delete(0, tk.END)
        self.id_em_edicao = None
        self.btn_cadastrar.config(state="normal")
        self.btn_salvar.config(state="disabled")
        self.lbl_status.config(text="")

    def limpar_filtros(self):
        self.ent_busca.delete(0, tk.END)
        self.ent_busca_matricula.delete(0, tk.END)
        self.cmb_busca_curso.set("")
        self.listar()
        self._atualizar_status("Filtros limpos.")

    def alternar_tema(self):
        self.modo_escuro = not self.modo_escuro
        self.btn_tema.config(text="Modo Claro" if self.modo_escuro else "Modo Escuro")
        self._aplicar_tema()

    def _configurar_tags_tabela(self):
        tema = self.temas["escuro" if self.modo_escuro else "claro"]
        self.tree.tag_configure("aprovado", background=tema["success"])
        self.tree.tag_configure("recuperacao", background=tema["warning"])
        self.tree.tag_configure("reprovado", background=tema["danger"])
        self.tree.tag_configure("alternada", background=tema["tree_alt"])

    def _preencher_tabela(self, alunos):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for indice, aluno in enumerate(alunos):
            aluno_id, matricula, nome, curso, nota_valor = aluno
            try:
                nota = float(nota_valor)
            except (ValueError, TypeError):
                nota = 0
            situacao = self._situacao(nota)
            tag_situacao = "aprovado" if nota >= 7 else ("recuperacao" if nota >= 5 else "reprovado")
            tags = (tag_situacao,) if indice % 2 == 0 else ("alternada",)

            self.tree.insert(
                "",
                tk.END,
                iid=str(aluno_id),
                values=(matricula, nome, curso, f"{nota:.1f}", situacao),
                tags=tags,
            )

        self._configurar_tags_tabela()
        self.lbl_total.config(text=f"Total: {len(self.tree.get_children())} aluno(s)")


root = tk.Tk()
app = SistemaNotas(root)
root.mainloop()
