import tkinter as tk
from tkinter import ttk, messagebox
import datetime


def apply_custom_style():
    style = ttk.Style()

    style.theme_use("clam")

    primary_color = "#3498db"
    secondary_color = "#2ecc71"
    accent_color = "#9b59b6"
    text_color = "#2c3e50"
    bg_color = "#ecf0f1"

    style.configure("TFrame", background=bg_color)
    style.configure(
        "TLabelframe", background=bg_color, foreground=text_color, borderwidth=2
    )
    style.configure(
        "TLabelframe.Label",
        font=("Helvetica", 10, "bold"),
        foreground=primary_color,
        background=bg_color,
    )
    style.configure(
        "TLabel", background=bg_color, foreground=text_color, font=("Helvetica", 9)
    )
    style.configure(
        "TEntry", fieldbackground="white", foreground=text_color, font=("Helvetica", 9)
    )

    style.configure(
        "TButton",
        background=primary_color,
        foreground="white",
        font=("Helvetica", 9, "bold"),
        borderwidth=1,
        focusthickness=3,
        focuscolor=primary_color,
    )
    style.map(
        "TButton",
        background=[("active", accent_color), ("pressed", secondary_color)],
        foreground=[("active", "white"), ("pressed", "white")],
    )

    style.configure("Primary.TButton", background=primary_color)
    style.map(
        "Primary.TButton", background=[("active", "#2980b9"), ("pressed", "#2573a7")]
    )

    style.configure("Secondary.TButton", background=secondary_color)
    style.map(
        "Secondary.TButton", background=[("active", "#27ae60"), ("pressed", "#219955")]
    )

    style.configure("Warning.TButton", background="#e74c3c")
    style.map(
        "Warning.TButton", background=[("active", "#c0392b"), ("pressed", "#a93226")]
    )

    style.configure("TNotebook", background=bg_color, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background="#bdc3c7",
        foreground=text_color,
        padding=[10, 2],
        font=("Helvetica", 9, "bold"),
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", primary_color)],
        foreground=[("selected", "white")],
        expand=[("selected", [1, 1, 1, 0])],
    )

    style.configure(
        "Treeview",
        background="white",
        fieldbackground="white",
        foreground=text_color,
        font=("Helvetica", 9),
    )
    style.configure(
        "Treeview.Heading",
        font=("Helvetica", 9, "bold"),
        background=primary_color,
        foreground="white",
    )
    style.map(
        "Treeview",
        background=[("selected", primary_color)],
        foreground=[("selected", "white")],
    )


class Node:
    def __init__(self, titre, auteur, genre, statut):
        self.titre = titre
        self.auteur = auteur
        self.genre = genre
        self.statut = statut
        self.next = None


class Livre:
    def __init__(self):
        self.head = None

    def ajouter(self, titre, auteur, genre, statut):
        new_node = Node(titre, auteur, genre, statut)
        if not self.head:
            self.head = new_node
            return "Livre ajouté avec succès en tête de liste"
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        return "Livre ajouté avec succès"

    def supprimer(self, titre):
        if not self.head:
            return "la liste des livres est vide :) "
        if self.head.titre == titre:
            self.head = self.head.next
            return "Livre supprimé avec succès"
        current = self.head
        previous = None
        while current and current.titre != titre:
            previous = current
            current = current.next
        if current:
            previous.next = current.next
            return "Livre supprimé avec succès"
        else:
            return "le livre n'existe pas dans la liste"

    def afficher_livres(self):
        livres = []
        current = self.head
        if not current:
            return []
        while current:
            livres.append(
                {
                    "titre": current.titre,
                    "auteur": current.auteur,
                    "genre": current.genre,
                    "statut": current.statut,
                }
            )
            current = current.next
        return livres

    def modifier_statut(self, titre, nouveau_statut):
        current = self.head
        while current:
            if current.titre == titre:
                current.statut = nouveau_statut
                return True
            current = current.next
        return False


class EmpruntNode:
    def __init__(self, titre, date):
        self.titre = titre
        self.date = date
        self.next = None


class Emprunts:
    def __init__(self):
        self.head = None

    def enregister(self, titre, date):
        new_node = EmpruntNode(titre, date)
        new_node.next = self.head
        self.head = new_node
        return f"Emprunt du livre '{titre}' enregistré avec succès à la date: {date}"

    def retour_livre(self):
        if not self.head:
            return "la liste des emprunts est vide"
        livre_retourne = self.head.titre
        self.head = self.head.next
        return f"Retour du livre '{livre_retourne}' effectué avec succès"

    def afficher_historique(self):
        historique = []
        current = self.head
        if not current:
            return []
        while current:
            historique.append({"titre": current.titre, "date": current.date})
            current = current.next
        return historique


class NodeArbre:
    def __init__(self, livre):
        self.livre = livre
        self.right = None
        self.left = None


class Arbre:
    def __init__(self):
        self.root = None

    def ajouter(self, livre):
        if not self.root:
            self.root = NodeArbre(livre)
            return f"Livre '{livre.titre}' ajouté comme racine de l'arbre"
        else:
            return self.ajouter_recursif(self.root, livre)

    def ajouter_recursif(self, current_node, livre):
        if livre.titre < current_node.livre.titre:
            if current_node.left is None:
                current_node.left = NodeArbre(livre)
                return f"Livre '{livre.titre}' ajouté à gauche de '{current_node.livre.titre}'"
            else:
                return self.ajouter_recursif(current_node.left, livre)
        else:
            if current_node.right is None:
                current_node.right = NodeArbre(livre)
                return f"Livre '{livre.titre}' ajouté à droite de '{current_node.livre.titre}'"
            else:
                return self.ajouter_recursif(current_node.right, livre)

    def rechercher(self, titre):
        result = self.rechercher_recursif(self.root, titre)
        if result:
            return result
        else:
            return None

    def rechercher_recursif(self, current_node, titre):
        if current_node is None:
            return None

        if current_node.livre.titre == titre:
            return current_node.livre

        if titre < current_node.livre.titre:
            return self.rechercher_recursif(current_node.left, titre)
        else:
            return self.rechercher_recursif(current_node.right, titre)

    def get_livres_alphabetique(self):
        result = []
        self.inorder_traversal(self.root, result)
        return result

    def inorder_traversal(self, node, result):
        if node:
            self.inorder_traversal(node.left, result)
            result.append(node.livre)
            self.inorder_traversal(node.right, result)


class CustomDialog:
    def show_success(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        messagebox.showinfo(title, message)


class BibliothequeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Système de Gestion de Bibliothèque")
        self.master.geometry("800x600")
        self.master.minsize(800, 600)

        self.master.configure(bg="#ecf0f1")

        apply_custom_style()

        self.dialog = CustomDialog()

        self.livres = Livre()
        self.emprunts = Emprunts()
        self.arbre = Arbre()

        self.create_header()

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_gestion = ttk.Frame(self.notebook)
        self.tab_emprunts = ttk.Frame(self.notebook)
        self.tab_recherche = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_gestion, text="Gestion des Livres")
        self.notebook.add(self.tab_emprunts, text="Gestion des Emprunts")
        self.notebook.add(self.tab_recherche, text="Recherche")

        self.init_gestion_tab()
        self.init_emprunts_tab()
        self.init_recherche_tab()

        self.create_footer()

        self.add_sample_data()

    def create_header(self):
        header_frame = tk.Frame(self.master, bg="#3498db", height=60)
        header_frame.pack(fill="x")

        title_label = tk.Label(
            header_frame,
            text="BIBLIOTHÈQUE MANAGER",
            font=("Helvetica", 16, "bold"),
            bg="#3498db",
            fg="white",
        )
        title_label.pack(side="left", padx=20, pady=15)

        date_str = datetime.datetime.now().strftime("%d %B %Y")
        date_label = tk.Label(
            header_frame,
            text=date_str,
            font=("Helvetica", 10),
            bg="#3498db",
            fg="white",
        )
        date_label.pack(side="right", padx=20, pady=15)

    def create_footer(self):
        footer_frame = tk.Frame(self.master, bg="#2c3e50", height=30)
        footer_frame.pack(fill="x", side="bottom")

        footer_text = tk.Label(
            footer_frame,
            text="© 2025 Système de Gestion de Bibliothèque",
            font=("Helvetica", 8),
            bg="#2c3e50",
            fg="white",
        )
        footer_text.pack(side="right", padx=10, pady=5)

    def add_sample_data(self):
        self.livres.ajouter("Python Basics", "John Smith", "Informatique", "Disponible")
        self.livres.ajouter(
            "L'Histoire de l'Humanité", "Anne Dubois", "Histoire", "Disponible"
        )
        self.livres.ajouter(
            "Le Petit Prince", "Antoine de Saint-Exupéry", "Fiction", "Disponible"
        )
        self.livres.ajouter("1984", "George Orwell", "Science-Fiction", "Disponible")
        self.update_tree(self.livres_tree)

        current = self.livres.head
        while current:
            node_for_tree = Node(
                current.titre, current.auteur, current.genre, current.statut
            )
            self.arbre.ajouter(node_for_tree)
            current = current.next

    def init_gestion_tab(self):
        padding_frame = ttk.Frame(self.tab_gestion)
        padding_frame.pack(fill="both", expand=True, padx=10, pady=10)

        form_frame = ttk.LabelFrame(padding_frame, text="Ajouter un Livre")
        form_frame.pack(fill="x", padx=5, pady=10)

        form_grid = ttk.Frame(form_frame)
        form_grid.pack(fill="x", padx=10, pady=10)

        ttk.Label(form_grid, text="Titre:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.titre_entry = ttk.Entry(form_grid, width=30)
        self.titre_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_grid, text="Auteur:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.auteur_entry = ttk.Entry(form_grid, width=30)
        self.auteur_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(form_grid, text="Genre:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.genre_entry = ttk.Entry(form_grid, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        button_frame = ttk.Frame(form_grid)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        add_button = ttk.Button(
            button_frame, text="Ajouter", command=self.add_book, style="Primary.TButton"
        )
        add_button.pack(side="left", padx=5)

        clear_button = ttk.Button(button_frame, text="Effacer", command=self.clear_form)
        clear_button.pack(side="left", padx=5)

        list_frame = ttk.LabelFrame(padding_frame, text="Liste des Livres")
        list_frame.pack(fill="both", expand=True, padx=5, pady=10)

        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")

        self.livres_tree = ttk.Treeview(
            tree_frame,
            columns=("Titre", "Auteur", "Genre", "Statut"),
            show="headings",
            yscrollcommand=scrollbar.set,
        )

        scrollbar.config(command=self.livres_tree.yview)

        self.livres_tree.heading("Titre", text="Titre")
        self.livres_tree.heading("Auteur", text="Auteur")
        self.livres_tree.heading("Genre", text="Genre")
        self.livres_tree.heading("Statut", text="Statut")

        self.livres_tree.column("Titre", width=200)
        self.livres_tree.column("Auteur", width=150)
        self.livres_tree.column("Genre", width=100)
        self.livres_tree.column("Statut", width=100)

        self.livres_tree.pack(fill="both", expand=True)

        self.livres_tree.tag_configure("odd", background="#f5f5f5")
        self.livres_tree.tag_configure("even", background="white")

        actions_frame = ttk.Frame(list_frame)
        actions_frame.pack(fill="x", padx=10, pady=5)

        delete_button = ttk.Button(
            actions_frame,
            text="Supprimer le livre sélectionné",
            command=self.delete_book,
            style="Warning.TButton",
        )
        delete_button.pack(side="right", padx=5)

    def init_emprunts_tab(self):
        padding_frame = ttk.Frame(self.tab_emprunts)
        padding_frame.pack(fill="both", expand=True, padx=10, pady=10)

        borrow_frame = ttk.LabelFrame(padding_frame, text="Emprunter un Livre")
        borrow_frame.pack(fill="x", padx=5, pady=10)

        borrow_grid = ttk.Frame(borrow_frame)
        borrow_grid.pack(fill="x", padx=10, pady=10)

        ttk.Label(borrow_grid, text="Titre du livre:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.emprunt_titre_entry = ttk.Entry(borrow_grid, width=30)
        self.emprunt_titre_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        borrow_button = ttk.Button(
            borrow_grid,
            text="Emprunter",
            command=self.borrow_book,
            style="Primary.TButton",
        )
        borrow_button.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        return_frame = ttk.LabelFrame(padding_frame, text="Retourner un Livre")
        return_frame.pack(fill="x", padx=5, pady=10)

        return_button = ttk.Button(
            return_frame,
            text="Retourner le dernier livre emprunté",
            command=self.return_book,
            style="Secondary.TButton",
        )
        return_button.pack(pady=10, padx=10)

        history_frame = ttk.LabelFrame(padding_frame, text="Historique des Emprunts")
        history_frame.pack(fill="both", expand=True, padx=5, pady=10)

        tree_container = ttk.Frame(history_frame)
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)

        history_scrollbar = ttk.Scrollbar(tree_container)
        history_scrollbar.pack(side="right", fill="y")

        self.emprunts_tree = ttk.Treeview(
            tree_container,
            columns=("Titre", "Date"),
            show="headings",
            yscrollcommand=history_scrollbar.set,
        )

        history_scrollbar.config(command=self.emprunts_tree.yview)

        self.emprunts_tree.heading("Titre", text="Titre")
        self.emprunts_tree.heading("Date", text="Date d'emprunt")

        self.emprunts_tree.column("Titre", width=300)
        self.emprunts_tree.column("Date", width=150)

        self.emprunts_tree.pack(fill="both", expand=True)

        self.emprunts_tree.tag_configure("odd", background="#f5f5f5")
        self.emprunts_tree.tag_configure("even", background="white")

    def init_recherche_tab(self):
        padding_frame = ttk.Frame(self.tab_recherche)
        padding_frame.pack(fill="both", expand=True, padx=10, pady=10)

        search_frame = ttk.LabelFrame(padding_frame, text="Rechercher un Livre")
        search_frame.pack(fill="x", padx=5, pady=10)

        search_grid = ttk.Frame(search_frame)
        search_grid.pack(fill="x", padx=10, pady=10)

        ttk.Label(search_grid, text="Titre:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.search_entry = ttk.Entry(search_grid, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        button_container = ttk.Frame(search_grid)
        button_container.grid(row=1, column=0, columnspan=2, pady=10)

        search_button = ttk.Button(
            button_container,
            text="Rechercher",
            command=self.search_book,
            style="Primary.TButton",
        )
        search_button.pack(side="left", padx=5)

        sort_button = ttk.Button(
            button_container,
            text="Afficher par ordre alphabétique",
            command=self.show_alphabetical,
            style="Secondary.TButton",
        )
        sort_button.pack(side="left", padx=5)

        results_frame = ttk.LabelFrame(padding_frame, text="Résultats de la Recherche")
        results_frame.pack(fill="both", expand=True, padx=5, pady=10)

        tree_container = ttk.Frame(results_frame)
        tree_container.pack(fill="both", expand=True, padx=10, pady=10)

        results_scrollbar = ttk.Scrollbar(tree_container)
        results_scrollbar.pack(side="right", fill="y")

        self.results_tree = ttk.Treeview(
            tree_container,
            columns=("Titre", "Auteur", "Genre", "Statut"),
            show="headings",
            yscrollcommand=results_scrollbar.set,
        )

        results_scrollbar.config(command=self.results_tree.yview)

        self.results_tree.heading("Titre", text="Titre")
        self.results_tree.heading("Auteur", text="Auteur")
        self.results_tree.heading("Genre", text="Genre")
        self.results_tree.heading("Statut", text="Statut")

        self.results_tree.column("Titre", width=200)
        self.results_tree.column("Auteur", width=150)
        self.results_tree.column("Genre", width=100)
        self.results_tree.column("Statut", width=100)

        self.results_tree.pack(fill="both", expand=True)

        self.results_tree.tag_configure("odd", background="#f5f5f5")
        self.results_tree.tag_configure("even", background="white")

    def clear_form(self):
        self.titre_entry.delete(0, tk.END)
        self.auteur_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)

    def add_book(self):
        titre = self.titre_entry.get()
        auteur = self.auteur_entry.get()
        genre = self.genre_entry.get()

        if not titre or not auteur or not genre:
            self.dialog.show_error("Erreur", "Tous les champs sont obligatoires!")
            return

        statut = "Disponible"
        result = self.livres.ajouter(titre, auteur, genre, statut)

        node_for_tree = Node(titre, auteur, genre, statut)
        self.arbre.ajouter(node_for_tree)

        self.update_tree(self.livres_tree)
        self.clear_form()

        self.dialog.show_success("Succès", result)

    def delete_book(self):
        selected_item = self.livres_tree.selection()
        if not selected_item:
            self.dialog.show_error("Erreur", "Aucun livre sélectionné!")
            return

        titre = self.livres_tree.item(selected_item, "values")[0]

        result = self.livres.supprimer(titre)

        self.update_tree(self.livres_tree)
        self.rebuild_tree()

        self.dialog.show_success("Succès", result)

    def borrow_book(self):
        titre = self.emprunt_titre_entry.get()

        if not titre:
            self.dialog.show_error("Erreur", "Veuillez entrer le titre du livre!")
            return

        book_found = False
        current = self.livres.head
        while current:
            if current.titre == titre:
                book_found = True
                if current.statut == "Disponible":
                    current.statut = "Emprunté"
                    date_emprunt = datetime.datetime.now().strftime("%Y-%m-%d")
                    result = self.emprunts.enregister(titre, date_emprunt)

                    self.update_tree(self.livres_tree)
                    self.update_emprunts_tree()
                    self.rebuild_tree()

                    self.dialog.show_success("Succès", result)
                    self.emprunt_titre_entry.delete(0, tk.END)
                    return
                else:
                    self.dialog.show_error(
                        "Erreur", f"Le livre '{titre}' n'est pas disponible!"
                    )
                    return
            current = current.next

        if not book_found:
            self.dialog.show_error(
                "Erreur", f"Le livre '{titre}' n'existe pas dans la bibliothèque!"
            )

    def return_book(self):
        if not self.emprunts.head:
            self.dialog.show_error("Erreur", "Aucun livre à retourner!")
            return

        titre_retourne = self.emprunts.head.titre

        current = self.livres.head
        while current:
            if current.titre == titre_retourne:
                current.statut = "Disponible"
                break
            current = current.next

        result = self.emprunts.retour_livre()

        self.update_tree(self.livres_tree)
        self.update_emprunts_tree()
        self.rebuild_tree()

        self.dialog.show_success("Succès", result)

    def search_book(self):
        titre = self.search_entry.get()

        if not titre:
            self.dialog.show_error("Erreur", "Veuillez entrer un titre à rechercher!")
            return

        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        result = self.arbre.rechercher(titre)

        if result:
            self.results_tree.insert(
                "",
                "end",
                values=(result.titre, result.auteur, result.genre, result.statut),
                tags=("odd",),
            )
            self.dialog.show_success("Succès", f"Livre trouvé: '{result.titre}'")
        else:
            self.dialog.show_info(
                "Information", f"Aucun livre avec le titre '{titre}' n'a été trouvé."
            )

    def show_alphabetical(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)

        livres = self.arbre.get_livres_alphabetique()

        if not livres:
            self.dialog.show_info("Information", "Aucun livre dans la bibliothèque")
            return

        for i, livre in enumerate(livres):
            tag = "odd" if i % 2 == 0 else "even"
            self.results_tree.insert(
                "",
                "end",
                values=(livre.titre, livre.auteur, livre.genre, livre.statut),
                tags=(tag,),
            )

    def update_tree(self, tree_widget):
        for item in tree_widget.get_children():
            tree_widget.delete(item)

        livres = self.livres.afficher_livres()

        for i, livre in enumerate(livres):
            tag = "odd" if i % 2 == 0 else "even"
            tree_widget.insert(
                "",
                "end",
                values=(
                    livre["titre"],
                    livre["auteur"],
                    livre["genre"],
                    livre["statut"],
                ),
                tags=(tag,),
            )

    def update_emprunts_tree(self):
        for item in self.emprunts_tree.get_children():
            self.emprunts_tree.delete(item)

        historique = []
        current = self.emprunts.head
        while current:
            historique.append({"titre": current.titre, "date": current.date})
            current = current.next

        for i, emprunt in enumerate(historique):
            tag = "odd" if i % 2 == 0 else "even"
            self.emprunts_tree.insert(
                "", "end", values=(emprunt["titre"], emprunt["date"]), tags=(tag,)
            )

    def rebuild_tree(self):
        self.arbre = Arbre()
        current = self.livres.head
        while current:
            node_for_tree = Node(
                current.titre, current.auteur, current.genre, current.statut
            )
            self.arbre.ajouter(node_for_tree)
            current = current.next


root = tk.Tk()
app = BibliothequeApp(root)
root.mainloop()
