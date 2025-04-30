import customtkinter
from customtkinter import StringVar, CTkLabel, CTkEntry, CTkComboBox, CTkButton, CTkFrame, CTk, set_appearance_mode, set_default_color_theme
from tkinter import ttk, messagebox, TOP, X, LEFT, YES, BOTH, NO, CENTER
import tkinter as tk
import datetime
import database

# Set light appearance mode and custom light color theme
set_appearance_mode("light")
set_default_color_theme("blue")

def add_to_treeview(tree):
    """
    Populate the given treeview widget with visit data from the database.
    """
    visitas = database.fetch_visitas()
    tree.delete(*tree.get_children())
    for row in visitas:
        tree.insert('', 'end', values=row)
    tree.pack()

class CadastroFrame(CTkFrame):
    """
    Frame for visitor registration form and related actions.
    """

    def __init__(self, master, border_color=None):
        super().__init__(master, border_color=border_color)

        self.visita_var = StringVar(value="Entregador")
        self.veiculo_var = StringVar(value="Carro")

        self.pack(padx=20, pady=20, fill="both", expand=None)

        self._create_widgets()

    def _create_widgets(self):
        """
        Create and place all widgets for the registration form.
        """
        self.label_nome = CTkLabel(self, text="Nome:", font=("Helvetica", 18), text_color="#2E3B4E")
        self.label_nome.place(x=50, y=40)

        self.entry_nome = CTkEntry(self, font=("Helvetica", 18), width=200, fg_color="#F0F4F8",
                                   text_color="#2E3B4E", border_color="#A9B7C6")
        self.entry_nome.place(x=120, y=40)

        self.label_documento = CTkLabel(self, text="Documento:", font=("Helvetica", 18), text_color="#2E3B4E")
        self.label_documento.place(x=340, y=40)

        vcmd = (self.register(self._validate_documento), '%P')
        self.entry_documento = CTkEntry(self, font=("Helvetica", 18), width=200, fg_color="#F0F4F8",
                                       text_color="#2E3B4E", border_color="#A9B7C6", validate="key",
                                       validatecommand=vcmd)
        self.entry_documento.place(x=450, y=40)

        self.label_morador = CTkLabel(self, text="Morador: ", font=("Helvetica", 18), text_color="#2E3B4E")
        self.label_morador.place(x=670, y=40)

        self.entry_morador = CTkEntry(self, font=("Helvetica", 18), width=200, fg_color="#F0F4F8",
                                     text_color="#2E3B4E", border_color="#A9B7C6")
        self.entry_morador.place(x=760, y=40)

        self.label_Tvisita = CTkLabel(self, text="Selecione o tipo de visita:", font=("Helvetica", 18),
                                     text_color="#2E3B4E")
        self.label_Tvisita.place(x=50, y=100)

        tipo_visita = ["Entregador", "Prestador de Serviço", "Familiar ou amigo"]
        self.combo_visita = CTkComboBox(self, values=tipo_visita, font=("Helvetica", 18), width=220,
                                        variable=self.visita_var, dropdown_font=("Helvetica", 18), fg_color="#F0F4F8",
                                        button_color="#A9B7C6", text_color="#2E3B4E")
        self.combo_visita.place(x=270, y=100)

        self.label_veiculo = CTkLabel(self, text="Veiculo:", font=("Helvetica", 18), text_color="#2E3B4E")
        self.label_veiculo.place(x=500, y=100)

        veiculos = ["Carro", "Moto", "Pedestre"]
        self.combo_veiculo = CTkComboBox(self, values=veiculos, font=("Helvetica", 18),
                                         variable=self.veiculo_var, dropdown_font=("Helvetica", 18), fg_color="#F0F4F8",
                                         button_color="#A9B7C6", text_color="#2E3B4E")
        self.combo_veiculo.place(x=580, y=100)

        self.label_placa = CTkLabel(self, text="Placa:", font=("Helvetica", 18), text_color="#2E3B4E")
        self.label_placa.place(x=750, y=100)

        self.entry_placa = CTkEntry(self, font=("Helvetica", 18), width=100, fg_color="#F0F4F8",
                                   text_color="#2E3B4E", border_color="#A9B7C6")
        self.entry_placa.place(x=810, y=100)

        self.gravar = CTkButton(self, text="Salvar", command=self.insert, font=("Helvetica", 18), fg_color='#00AEF2',
                                hover_color="#0a85b2", text_color="white")
        self.gravar.place(x=800, y=150)

    def _validate_documento(self, new_value):
        """
        Validation callback for the 'Documento' entry field.
        Allows only digits up to length 8 or empty string.
        """
        if new_value == "":
            return True
        if new_value.isdigit() and len(new_value) <= 8:
            return True
        return False

    def insert(self):
        """
        Insert a new visit record into the database after validation.
        """
        nome = self.entry_nome.get().strip()
        documento = self.entry_documento.get().strip()
        tentrada = self.visita_var.get()
        morador = self.entry_morador.get().strip()
        veiculo = self.veiculo_var.get()
        placa = self.entry_placa.get().strip()
        entrada = datetime.datetime.now().strftime("%d/%m  %H:%M:%S")
        saida = "aguardando"

        if not nome:
            messagebox.showerror("Erro", "O campo Nome é obrigatório.")
            return
        if not documento:
            messagebox.showerror("Erro", "O campo Documento é obrigatório.")
            return

        database.insert_visitas(nome, documento, tentrada, morador, veiculo, placa, entrada, saida)
        add_to_treeview(self.master.tree)
        messagebox.showinfo('Dados inseridos',
                            f"Visitante: {nome} \nDocumento: {documento}\nTipo de Visita: {tentrada}\nMorador: {morador}")

        self._clear_fields()

    def _clear_fields(self):
        """
        Clear all input fields and reset combo boxes to default values.
        """
        self.entry_nome.delete(0, tk.END)
        self.entry_documento.delete(0, tk.END)
        self.visita_var.set("Entregador")
        self.entry_morador.delete(0, tk.END)
        self.veiculo_var.set("Carro")
        self.entry_placa.delete(0, tk.END)

    def on_treeview_click(self, event):
        """
        Handle click event on the treeview to update 'saida' time or show visit data.
        """
        selected_item = self.master.tree.focus()
        if not selected_item:
            return
        values = self.master.tree.item(selected_item, 'values')
        saida_value = values[8]  # 'Saida' column index
        if saida_value == "aguardando":
            confirm = messagebox.askokcancel("Confirmação", "Deseja adicionar a hora atual para saída?")
            if confirm:
                current_time = datetime.datetime.now().strftime("%d/%m  %H:%M:%S")
                id_value = values[0]  # Assuming first column is ID or unique identifier
                database.update_saida(id_value, current_time)
                add_to_treeview(self.master.tree)
                messagebox.showinfo("Saida Atualizada", f"Hora de saída atualizada para {current_time}")
        else:
            messagebox.showinfo("Dados da Visita",
                                f"Dados:\nN°: {values[0]}\nNome: {values[1]}\nDocumento: {values[2]}\nTipo de entrada: {values[3]}"
                                f"\nMorador: {values[4]}\nVeiculo: {values[5]}\nPlaca: {values[6]}\nEntrada: {values[7]}\nSaida: {values[8]}")

class App(CTk):
    """
    Main application window class.
    """

    font1 = ('Arial', 20, 'bold')
    font2 = ('Arial', 12, 'bold')

    def __init__(self):
        super().__init__()

        self.title("Cadastro de Visitantes")
        self.geometry("1200x1150")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.label_nome = CTkLabel(self, text="Cadastro de Visitantes Parque Imperador:", font=("Helvetica", 24),
                                   text_color="#2E3B4E")
        self.label_nome.pack(pady=10)

        self.cadastro_frame = CadastroFrame(self)
        self.cadastro_frame.configure(border_color='#00AEF2')
        self.cadastro_frame.place()

        self._create_search_frame()
        self._create_treeview()
        add_to_treeview(self.tree)

        self.tree.bind("<ButtonRelease-1>", self.cadastro_frame.on_treeview_click)

    def _create_search_frame(self):
        """
        Create the search frame with entry and button.
        """
        self.search_frame = CTkFrame(self, fg_color="#F0F4F8")
        self.search_frame.pack(side=TOP, fill=X, padx=10, pady=5)

        self.button1 = CTkButton(self.search_frame, text="Buscar", width=100, font=("Helvetica", 18), fg_color='#00AEF2',
                                 hover_color="#0a85b2", text_color="white")
        self.button1.pack(side=LEFT, padx=12)

        self.entry_busca = CTkEntry(self.search_frame, font=("Helvetica", 18), width=200, fg_color="#F0F4F8",
                                    text_color="#2E3B4E", border_color='#00AEF2')
        self.entry_busca.pack(side=LEFT, padx=5, fill=X, expand=YES)

        self.button1.configure(command=self.buscar)

    def _create_treeview(self):
        """
        Create and style the treeview widget for displaying visit data.
        """
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.style.configure("Treeview",
                             background="#D9E4F5",
                             foreground="#1B365D",
                             rowheight=25,
                             font=("Helvetica", 12, 'bold'),
                             fieldbackground='#B0C4DE')

        self.style.map('Treeview',
                       background=[('selected', '#4A6FA5')],
                       foreground=[('selected', 'white')])

        self.style.configure("Treeview.Heading",
                             
                             background='#00AEF2',
                             foreground="white",
                             font=("Helvetica", 15, 'bold'))

        self.tree = ttk.Treeview(self, height=15)

        self.tree['columns'] = ('N°', 'Nome', 'Documento', 'Tipo de Visita', 'Morador', 'veiculo', 'Placa', 'Entrada', 'Saida')

        self.tree.column('#0', width=0, stretch=NO)
        self.tree.column('N°', anchor=CENTER, width=50)
        self.tree.column('Entrada', anchor=CENTER, width=120)
        self.tree.column('Nome', anchor=CENTER, width=120)
        self.tree.column('Morador', anchor=CENTER, width=120)
        self.tree.column('Tipo de Visita', anchor=CENTER, width=150)
        self.tree.column('veiculo', anchor=CENTER, width=120)
        self.tree.column('Placa', anchor=CENTER, width=120)
        self.tree.column('Documento', anchor=CENTER, width=120)
        self.tree.column('Saida', anchor=CENTER, width=120)

        self.tree.heading('N°', text='N°')
        self.tree.heading('Entrada', text='Entrada')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Morador', text='Morador')
        self.tree.heading('Tipo de Visita', text='Tipo de Visita')
        self.tree.heading('veiculo', text='veiculo')
        self.tree.heading('Placa', text='Placa')
        self.tree.heading('Documento', text='Documento')
        self.tree.heading('Saida', text='Saida')

        self.tree.tag_configure('oddrow', background='#D9E4F5')
        self.tree.tag_configure('evenrow', background='#B0C4DE')

        self.tree.pack(side=TOP, fill=BOTH, expand=YES, padx=10, pady=10)

    def buscar(self):
        """
        Search visit records by term and update the treeview.
        """
        term = self.entry_busca.get().strip()
        if term == "":
            results = database.fetch_visitas()
        else:
            results = database.search_visitas(term)
        self.tree.delete(*self.tree.get_children())
        for row in results:
            self.tree.insert('', 'end', values=row)


app = App()
app.mainloop()
