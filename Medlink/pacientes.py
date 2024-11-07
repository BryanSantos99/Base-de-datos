import customtkinter as ctk
from PIL import Image, ImageTk
import admin as admin
import tkinter as tk
from tkinter import ttk, messagebox
import conecta
from datetime import datetime
import empleadosadmin

class Pacientes(ctk.CTk):
    def __init__(self, nombre, rol):
        super().__init__()

        self.nombre = nombre
        self.rol = rol

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.title("MedLink")
        self.attributes("-fullscreen", True)

        self.load_images()
        self.setup_widgets()

    def load_images(self):
        try:
            doctor_image = Image.open("img/doctor_logo.png").resize((60, 60))
            self.doctor_logo_photo = ImageTk.PhotoImage(doctor_image)
            self.logo_image = Image.open("img/logo.png").resize((85, 85))
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
            self.header_image = Image.open("img/logo.png").resize((300, 300))
            self.header_photo = ImageTk.PhotoImage(self.header_image)
        except FileNotFoundError:
            print("Error: La imagen 'logo.png' no se encontró en la carpeta.")
            self.doctor_logo_photo = None

    def back_to_main(self):
        self.destroy()
        if self.rol == "A":
            admin.MainApp(self.nombre,self.rol)
        else:
            empleadosadmin.MainApp(self.nombre, self.rol)

    def setup_widgets(self):
        self.setup_header()
        self.setup_tabview()
        self.populate_patients_table()
        self.setup_add_patient_form()

    def setup_header(self):
        header_frame = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#1f6aa5")
        header_frame.place(relwidth=1.0, relx=0.5, rely=0.0, anchor='n')

        ctk.CTkButton(header_frame, text="Volver", width=100, height=30, fg_color="black", text_color="white", font=("Arial", 14), command=self.back_to_main).place(relx=0.85, rely=0.5, anchor="center")

        ctk.CTkLabel(header_frame, text="MedLink", font=("Arial", 24), text_color="white").place(relx=0.15, rely=0.5, anchor="center")
        ctk.CTkLabel(header_frame, text="Pacientes", font=("Arial", 34), text_color="white").place(relx=0.5, rely=0.5, anchor="center")

        if self.logo_photo:
            ctk.CTkLabel(header_frame, image=self.logo_photo, text="").place(relheight=1, relx=0.93, rely=0.5, anchor="w")

    def setup_tabview(self):
        tabview = ctk.CTkTabview(self, fg_color="white")
        tabview.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.89)

        tabview.add("Pacientes")
        tabview.add("Agregar Paciente")
        tabview.add("Eliminar Paciente")
        tabview.add("Modificar Paciente")

        # Frames for each tab
        self.pacientes_frame = ctk.CTkScrollableFrame(tabview.tab("Pacientes"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.pacientes_frame.place(relwidth=1, relheight=1)
        
        self.agregar_paciente_frame = ctk.CTkFrame(tabview.tab("Agregar Paciente"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.agregar_paciente_frame.place(relwidth=1, relheight=1)

    def populate_patients_table(self):
        conn = conecta.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM paciente")
        pacientes = cursor.fetchall()
        conn.commit()
        conn.close()

        tabla_pacientes = ttk.Treeview(self.pacientes_frame, columns=("Codigo", "Nombre", "Direccion", "Telefono", "Fecha de Nacimiento", "Sexo", "Edad", "Estatura"), style="Treeview", show="headings", height=40)
        for col, col_name in zip(tabla_pacientes["columns"], ["Codigo", "Nombre", "Direccion", "Telefono", "Fecha de Nacimiento", "Sexo", "Edad", "Estatura"]):
            tabla_pacientes.heading(col, text=col_name)

        for paciente in pacientes:
            tabla_pacientes.insert("", "end", values=paciente)

        tabla_pacientes.pack(expand=True, fill="both")

    def setup_add_patient_form(self):
        fields = [
            ("Codigo", "Codigo"), ("Nombre", "Nombre paciente"), ("Direccion", "Direccion"),
            ("Telefono", "Telefono"), ("Fecha Nacimiento", "AAAA-MM-DD"),
            ("Sexo", "F/M"), ("Edad", "Edad"), ("Estatura", "Estatura")
        ]
        
        self.entries = {}
        for label_text, placeholder in fields:
            label = ctk.CTkLabel(self.agregar_paciente_frame, text=label_text, font=("Arial", 14), text_color="black")
            label.pack(pady=(5, 5))
            entry = ctk.CTkEntry(self.agregar_paciente_frame, placeholder_text=placeholder, width=200, height=30)
            entry.pack(pady=5)
            self.entries[label_text.lower()] = entry
        
        ctk.CTkButton(self.agregar_paciente_frame, text="Agregar", command=self.agregar_paciente).pack(pady=10)

    def agregar_paciente(self):
        # Validación de campos
        if any(entry.get() == "" for entry in self.entries.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = conecta.conectar()
        cursor = conn.cursor()
        try:
            fecha_nac = datetime.strptime(self.entries["fecha nacimiento"].get(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Debe ser AAAA-MM-DD")
            return

        try:
            cursor.execute("""  
            INSERT INTO paciente 
            (codigo, nombre, direccion, telefono, fecha_nac, sexo, edad, estatura) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                self.entries["codigo"].get(),
                self.entries["nombre"].get(),
                self.entries["direccion"].get(),
                self.entries["telefono"].get(),
                fecha_nac,
                self.entries["sexo"].get(),
                self.entries["edad"].get(),
                self.entries["estatura"].get()
            ))
            conn.commit()
            messagebox.showinfo("Éxito", "Paciente agregado correctamente")
            for entry in self.entries.values():
                entry.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar paciente: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    pacientes = Pacientes(nombre="usuario_demo", rol="A")
    pacientes.mainloop()
