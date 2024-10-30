import customtkinter as ctk
from PIL import Image, ImageTk
import main_app
import tkinter as tk
from tkinter import ttk
import conecta


class Pacientes(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.title("MedLink")
        self.attributes("-fullscreen", True)

        
        
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
            
        self.setup_widgets()
        
    def back_to_main(self):
        self.destroy()
        main_app.MainApp()
        

    def setup_widgets(self):
        header_frame = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#1f6aa5")
        header_frame.place(relwidth=1.0, relx=0.5, rely=0.0, anchor='n')
        
        buttonBack = ctk.CTkButton(header_frame, text="Volver", width=100, height=30, fg_color="black", text_color="white", font=("Arial", 14), command=self.back_to_main)
        buttonBack.place(relx=0.85, rely=0.5, anchor="center")
        
        header_label = ctk.CTkLabel(header_frame, text="MedLink", font=("Arial", 24), text_color="white")
        header_label.place(relx=0.15, rely=0.5, anchor="center")
        
        header_label = ctk.CTkLabel(header_frame, text="Pacientes", font=("Arial", 34), text_color="white")
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        logo_label = ctk.CTkLabel(header_frame, image=self.logo_photo, text="")
        logo_label.place(relheight=1,relx=0.93, rely=0.5, anchor="w")
        
        tabview = ctk.CTkTabview(self,fg_color="white")
        tabview.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.89)
        
        pacientes_tab=tabview.add("Pacientes")
        agregar_paciente_tab=tabview.add("Agregar Paciente")
        eliminar_paciente_tab=tabview.add("Eliminar Paciente")
        modificar_paciente_tab=tabview.add("Modificar Paciente")
        
        self.pacientes_frame = ctk.CTkScrollableFrame(pacientes_tab, corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.pacientes_frame.place(relwidth=1, relheight=1)
        
        self.agregar_paciente_frame = ctk.CTkFrame(agregar_paciente_tab, corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.agregar_paciente_frame.place(relwidth=1, relheight=1)
        
        self.eliminar_paciente_frame = ctk.CTkScrollableFrame(eliminar_paciente_tab, corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.eliminar_paciente_frame.place(relwidth=1, relheight=1)
        
        self.modificar_paciente_frame = ctk.CTkScrollableFrame(modificar_paciente_tab, corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.modificar_paciente_frame.place(relwidth=1, relheight=1)
        
        
        conn = conecta.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM paciente")
        pacientes = cursor.fetchall()
        conn.commit()
        conn.close()
        
        

        tabla_pacientes = ttk.Treeview(self.pacientes_frame, columns=("id", "nombres", "apellidos", "salario"), style="Treeview", show="headings", height=40)
        tabla_pacientes.heading("id", text="ID")
        tabla_pacientes.heading("nombres", text="Nombres")
        tabla_pacientes.heading("apellidos", text="Apellidos")
        tabla_pacientes.heading("salario", text="Salario")

        for paciente in pacientes:
            tabla_pacientes.insert("", "end", values=paciente)

        tabla_pacientes.pack(expand=True, fill="both")
        
        labelNombre = ctk.CTkLabel(self.agregar_paciente_frame, text="Nombre", font=("Arial", 14), text_color="black")
        labelNombre.place(relx=0.48, rely=0.1, anchor="w")
        
        entryNombre = ctk.CTkEntry(self.agregar_paciente_frame, placeholder_text="Nombre paciente", width=200, height=30)
        entryNombre.place(relx=0.43, rely=0.15, anchor="w")

        boton_prueba = ctk.CTkButton(self.agregar_paciente_frame, text="Botón de prueba")
        boton_prueba.place(relx=0.45, rely=0.2, anchor="w")

if __name__ == "__main__":
    pacientes = Pacientes()
    pacientes.mainloop()
    
    
