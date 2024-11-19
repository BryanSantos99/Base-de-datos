import customtkinter as ctk
from PIL import Image, ImageTk
import admin as admin
import tkinter as tk
from tkinter import ttk, messagebox
import conecta
from datetime import datetime
import empleadosadmin
import doctoresadmin

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
        elif self.rol=='E':
            empleadosadmin.MainApp(self.nombre, self.rol)
        else:
            doctoresadmin.MainApp(self.nombre, self.rol)

    def setup_widgets(self):
        self.setup_header()
        self.setup_tabview()
        self.populate_patients_table()
        self.setup_patient()
        
        

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
        self.tab=tabview.add("Paciente")
        

        self.pacientes_frame = ctk.CTkScrollableFrame(tabview.tab("Pacientes"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.pacientes_frame.place(relwidth=1, relheight=1)
        
        self.paciente_frame = ctk.CTkFrame(tabview.tab("Paciente"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.paciente_frame.place(relwidth=1, relheight=1)
        
        

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

    def setup_patient(self):
        
        
        ctk.CTkLabel( self.paciente_frame, text="Código del Paciente para ver detalles", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryCodigo = ctk.CTkEntry( self.paciente_frame, placeholder_text="Código", width=200, height=30)
        self.entryCodigo.pack(pady=10)
        

        boton_modificar = ctk.CTkButton( self.paciente_frame, text="Ver Paciente", command=self.ver_paciente)
        boton_modificar.pack(pady=10)


    def ver_paciente(self):
        codigo_paciente = self.entryCodigo.get()
        self.paciente_frame.destroy()
        self.setup_patient2(codigo_paciente)
        
        
    def setup_patient2(self, codigo_paciente):
        print("Codigo:", codigo_paciente)
        
        self.pacientes_frame2 = ctk.CTkScrollableFrame(self.tab, corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.pacientes_frame2.place(relwidth=1, relheight=1)
        
        # Cambié el frame donde se colocan los detalles del paciente
        conn = conecta.conectar()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM paciente WHERE codigo = {codigo_paciente}")
        paciente = cursor.fetchone()
        conn.close()

        if paciente:
            ctk.CTkLabel(self.pacientes_frame2, text="Detalles del Paciente", font=("Arial", 24), text_color="black").pack(pady=10)
            ctk.CTkLabel(self.pacientes_frame2, text=f"Código: {paciente[0]}", font=("Arial", 14),text_color="black").pack(pady=5)
            ctk.CTkLabel(self.pacientes_frame2, text=f"Nombre: {paciente[1]}", font=("Arial", 14),text_color="black").pack(pady=5)
            ctk.CTkLabel(self.pacientes_frame2, text=f"Dirección: {paciente[2]}", font=("Arial", 14),text_color="black").pack(pady=5)
            ctk.CTkLabel(self.pacientes_frame2, text=f"Teléfono: {paciente[3]}", font=("Arial", 14),text_color="black").pack(pady=5)
            ctk.CTkLabel(self.pacientes_frame2, text=f"Fecha de Nacimiento: {paciente[4]}", font=("Arial", 14),text_color="black").pack(pady=5)
            ctk.CTkLabel(self.pacientes_frame2, text=f"Sexo: {paciente[5]}", font=("Arial", 14),text_color="black").pack(pady=5)
            ctk.CTkLabel(self.pacientes_frame2, text=f"Edad: {paciente[6]}", font=("Arial", 14),text_color="black").pack(pady=5)
            ctk.CTkLabel(self.pacientes_frame2, text=f"Estatura: {paciente[7]}", font=("Arial", 14),text_color="black").pack(pady=5)
        else:
            ctk.CTkLabel(self.pacientes_frame2, text="Paciente no encontrado", font=("Arial", 14), text_color="red").pack(pady=10)
        
if __name__ == "__main__":
    pacientes = Pacientes(nombre="Doctor", rol="D")
    pacientes.mainloop()
