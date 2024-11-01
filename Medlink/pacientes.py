import customtkinter as ctk
from PIL import Image, ImageTk
import main_app
import tkinter as tk
from tkinter import ttk ,messagebox
import conecta
from datetime import datetime


class Pacientes(ctk.CTk):
    def __init__(self,nombre):
        super().__init__()

        self.nombre=nombre
        
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
        main_app.MainApp(self.nombre)
        

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
        
        

        tabla_pacientes = ttk.Treeview(self.pacientes_frame, columns=("Codigo", "Nombre", "Direccion","Telefono","Fecha de Nacimiento", "Sexo" ,"Edad","Estatura"), style="Treeview", show="headings", height=40)
        tabla_pacientes.heading("Codigo", text="Codigo")
        tabla_pacientes.heading("Nombre", text="Nombre")
        tabla_pacientes.heading("Direccion", text="Direccion")
        tabla_pacientes.heading("Telefono", text="Telefono")
        tabla_pacientes.heading("Fecha de Nacimiento", text="Fecha De Nacimiente")
        tabla_pacientes.heading("Sexo", text="Sexo")
        tabla_pacientes.heading("Edad", text="Edad")
        tabla_pacientes.heading("Estatura", text="Estatura")

        for paciente in pacientes:
            tabla_pacientes.insert("", "end", values=paciente)

        tabla_pacientes.pack(expand=True, fill="both")
        
        labelCodigo = ctk.CTkLabel(self.agregar_paciente_frame, text="Codigo", font=("Arial", 14), text_color="black")
        labelCodigo.pack(pady=(5, 5))
        
        self.entryCodigo = ctk.CTkEntry(self.agregar_paciente_frame, placeholder_text="Codigo", width=200, height=30)
        self.entryCodigo.pack(pady=5)
        
        labelNombre = ctk.CTkLabel(self.agregar_paciente_frame, text="Nombre", font=("Arial", 14), text_color="black")
        labelNombre.pack(pady=(5, 5))
        
        self.entryNombre = ctk.CTkEntry(self.agregar_paciente_frame, placeholder_text="Nombre empleado", width=200, height=30)
        self.entryNombre.pack(pady=5)
        
        labelDireccion = ctk.CTkLabel(self.agregar_paciente_frame, text="Direccion", font=("Arial", 14), text_color="black")
        labelDireccion.pack(pady=(5, 5))
        
        self.entryDireccion = ctk.CTkEntry(self.agregar_paciente_frame, placeholder_text="Direccion", width=200, height=30)
        self.entryDireccion.pack(pady=5)
        
        
        labelTelefono = ctk.CTkLabel(self.agregar_paciente_frame, text="Telefono", font=("Arial", 14), text_color="black")
        labelTelefono.pack(pady=(5, 5))
        
        self.entryTelefono = ctk.CTkEntry(self.agregar_paciente_frame, placeholder_text="Telefono", width=200, height=30)
        self.entryTelefono.pack(pady=5)
        
        
        labelFecha = ctk.CTkLabel(self.agregar_paciente_frame, text="Fecha Nacimiento", font=("Arial", 14), text_color="black")
        labelFecha.pack(pady=(5, 5))
        
        
        self.entryFecha = ctk.CTkEntry(self.agregar_paciente_frame, placeholder_text="AAAA-MM-DD", width=200, height=30)
        self.entryFecha.pack(pady=5)
        
        labelSexo = ctk.CTkLabel(self.agregar_paciente_frame, text="Sexo", font=("Arial", 14), text_color="black")
        labelSexo.pack(pady=(5, 5))
        
        self.entrySexo = ctk.CTkEntry(self.agregar_paciente_frame, placeholder_text="F/M", width=200, height=30)
        self.entrySexo.pack(pady=5)

        
        labelEdad = ctk.CTkLabel(self.agregar_paciente_frame, text="Edad", font=("Arial", 14), text_color="black")
        labelEdad.pack(pady=(5, 5))
        
        self.entryEdad = ctk.CTkEntry(self.agregar_paciente_frame, placeholder_text="Edad", width=200, height=30)
        self.entryEdad.pack(pady=5)
        
        labelEstatura = ctk.CTkLabel(self.agregar_paciente_frame, text="Estatura", font=("Arial", 14), text_color="black")
        labelEstatura.pack(pady=(5, 5))
        
        self.entryEstatura = ctk.CTkEntry(self.agregar_paciente_frame, placeholder_text="Estatura", width=200, height=30)
        self.entryEstatura.pack(pady=5)
        
        
        botonEnviar = ctk.CTkButton(self.agregar_paciente_frame, text="Agregar",command=self.agregar_doctor)
        botonEnviar.pack(pady=10)
        
    def agregar_doctor(self):
        if (self.entryCodigo.get() == "" or self.entryNombre.get() == "" or self.entryDireccion.get() == "" or 
            self.entryTelefono.get() == "" or self.entryFecha.get() == "" or 
            self.entrySexo.get() == "" or self.entryEdad.get() == "" or 
            self.entryEstatura.get() == ""):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        else:
            conn = conecta.conectar()
            cursor = conn.cursor() 
            try:
                try:
                    fecha_nac = datetime.strptime(self.entryFecha.get(), "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Error", "Formato de fecha inválido. Debe ser AAAA-MM-DD")
                    return
                cursor.execute("""  
                INSERT INTO doctor 
                (codigo, nombre, direccion, telefono, fecha_nac, sexo, edad, estatura) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                self.entryCodigo.get(),
                self.entryNombre.get(), 
                self.entryDireccion.get(), 
                self.entryTelefono.get(),
                fecha_nac, 
                self.entrySexo.get(), 
                self.entryEdad.get(), 
                self.entryEstatura.get()
                ))
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Exito", "Doctor agregado correctamente")
                self.entryCodigo.delete(0, "end")
                self.entryNombre.delete(0, "end")
                self.entryDireccion.delete(0, "end")
                self.entryTelefono.delete(0, "end")
                self.entryFecha.delete(0, "end")
                self.entrySexo.delete(0, "end")
                self.entryEdad.delete(0, "end")
                self.entryEstatura.delete(0, "end")
            except Exception as e:
                messagebox.showerror("Error", f"Error al agregar doctor: {e}")
            
        
        

if __name__ == "__main__":
    pacientes = Pacientes(None)
    pacientes.mainloop()
    
    
