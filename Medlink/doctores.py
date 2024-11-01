import customtkinter as ctk
from PIL import Image, ImageTk
import main_app
import conecta
from tkinter import ttk, messagebox
from datetime import datetime
class Doctores(ctk.CTk):
<<<<<<< HEAD
    def __init__(self,nombre):
        super().__init__()
        self.nombre=nombre
=======
    def __init__(self):
        super().__init__()

>>>>>>> main
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.geometry("400x500")
        self.title("MedLink")
        self.attributes("-fullscreen", True)
        
        try:
            self.logo_image = Image.open("img/logo.png").resize((85, 85))
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except FileNotFoundError:
            print("Error: La imagen 'logo.png' no se encontró en la carpeta.")
            self.logo_photo = None
            
        self.setup_widgets()



    def back_to_main(self):
        self.destroy()
<<<<<<< HEAD
        main_app.MainApp(self.nombre)
=======
        main_app.MainApp()
>>>>>>> main

    def setup_widgets(self):
        header_frame = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#1f6aa5")
        header_frame.place(relwidth=1.0, relx=0.5, rely=0.0, anchor='n')
        
        buttonBack = ctk.CTkButton(header_frame, text="Volver", width=100, height=30, fg_color="black", text_color="white", font=("Arial", 14), command=self.back_to_main)
        buttonBack.place(relx=0.85, rely=0.5, anchor="center")
        
        header_label = ctk.CTkLabel(header_frame, text="MedLink", font=("Arial", 24), text_color="white")
        header_label.place(relx=0.15, rely=0.5, anchor="center")
        
        header_label = ctk.CTkLabel(header_frame, text="Doctores", font=("Arial", 34), text_color="white")
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        logo_label = ctk.CTkLabel(header_frame, image=self.logo_photo, text="")
        logo_label.place(relheight=1,relx=0.93, rely=0.5, anchor="w")
        
        tabview = ctk.CTkTabview(self,fg_color="white")
        tabview.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.89)
        
        tabview.add("Doctores")
        tabview.add("Agregar Doctor")
        tabview.add("Eliminar Doctor")
        tabview.add("Modificar Doctor")
        
        self.doctores_frame = ctk.CTkScrollableFrame(tabview.tab("Doctores"), corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.doctores_frame.place(relwidth=1, relheight=1)
        
        self.agregar_doctor_frame = ctk.CTkScrollableFrame(tabview.tab("Agregar Doctor"), corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.agregar_doctor_frame.place(relwidth=1, relheight=1)
        
        self.eliminar_doctor_frame = ctk.CTkScrollableFrame(tabview.tab("Eliminar Doctor"), corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.eliminar_doctor_frame.place(relwidth=1, relheight=1)
        
        self.modificar_doctor_frame = ctk.CTkScrollableFrame(tabview.tab("Modificar Doctor"), corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.modificar_doctor_frame.place(relwidth=1, relheight=1)
        
        conn = conecta.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctor")
        doctores = cursor.fetchall()
        conn.commit()
        conn.close()
        
        

        tabla_doctores = ttk.Treeview(self.doctores_frame, columns=("id", "nombres","direccion",'telefono','fecha_nac','sexo','especialidad','contraseña'), style="Treeview", show="headings", height=40)
        tabla_doctores.heading("id", text="Id")
        tabla_doctores.heading("nombres", text="Nombres")
        tabla_doctores.heading("direccion", text="Direccion")
        tabla_doctores.heading("telefono", text="Telefono")
        tabla_doctores.heading("fecha_nac", text="Fecha Nacimiento")
        tabla_doctores.heading("sexo", text="Sexo")
        tabla_doctores.heading("especialidad", text="Especialidad")
        tabla_doctores.heading("contraseña", text="Contraseña")

        for doctor in doctores:
            tabla_doctores.insert("", "end", values=doctor)

        tabla_doctores.pack(expand=True, fill="both")
        
        labelCodigo = ctk.CTkLabel(self.agregar_doctor_frame, text="Codigo", font=("Arial", 14), text_color="black")
        labelCodigo.pack(pady=(5, 5))
        
        self.entryCodigo = ctk.CTkEntry(self.agregar_doctor_frame, placeholder_text="Codigo", width=200, height=30)
        self.entryCodigo.pack(pady=5)
        
        labelNombre = ctk.CTkLabel(self.agregar_doctor_frame, text="Nombre", font=("Arial", 14), text_color="black")
        labelNombre.pack(pady=(5, 5))
        
        self.entryNombre = ctk.CTkEntry(self.agregar_doctor_frame, placeholder_text="Nombre empleado", width=200, height=30)
        self.entryNombre.pack(pady=5)
        
        labelDireccion = ctk.CTkLabel(self.agregar_doctor_frame, text="Direccion", font=("Arial", 14), text_color="black")
        labelDireccion.pack(pady=(5, 5))
        
        self.entryDireccion = ctk.CTkEntry(self.agregar_doctor_frame, placeholder_text="Direccion", width=200, height=30)
        self.entryDireccion.pack(pady=5)
        
        
        labelTelefono = ctk.CTkLabel(self.agregar_doctor_frame, text="Telefono", font=("Arial", 14), text_color="black")
        labelTelefono.pack(pady=(5, 5))
        
        self.entryTelefono = ctk.CTkEntry(self.agregar_doctor_frame, placeholder_text="Telefono", width=200, height=30)
        self.entryTelefono.pack(pady=5)
        
        
        labelFecha = ctk.CTkLabel(self.agregar_doctor_frame, text="Fecha Nacimiento", font=("Arial", 14), text_color="black")
        labelFecha.pack(pady=(5, 5))
        
        
        self.entryFecha = ctk.CTkEntry(self.agregar_doctor_frame, placeholder_text="AAAA-MM-DD", width=200, height=30)
        self.entryFecha.pack(pady=5)
        
        labelSexo = ctk.CTkLabel(self.agregar_doctor_frame, text="Sexo", font=("Arial", 14), text_color="black")
        labelSexo.pack(pady=(5, 5))
        
        self.entrySexo = ctk.CTkEntry(self.agregar_doctor_frame, placeholder_text="FEMENINO/MASCULINO", width=200, height=30)
        self.entrySexo.pack(pady=5)

        
        labelEspecialidad = ctk.CTkLabel(self.agregar_doctor_frame, text="Especialidad", font=("Arial", 14), text_color="black")
        labelEspecialidad.pack(pady=(5, 5))
        
        self.entryEspecialidad = ctk.CTkEntry(self.agregar_doctor_frame, placeholder_text="Especialidad", width=200, height=30)
        self.entryEspecialidad.pack(pady=5)
        
        labelContrasena = ctk.CTkLabel(self.agregar_doctor_frame, text="Contrasena", font=("Arial", 14), text_color="black")
        labelContrasena.pack(pady=(5, 5))
        
        self.entryContrasena = ctk.CTkEntry(self.agregar_doctor_frame, placeholder_text="Contrasena", width=200, height=30)
        self.entryContrasena.pack(pady=5)
        
        
        botonEnviar = ctk.CTkButton(self.agregar_doctor_frame, text="Agregar",command=self.agregar_doctor)
        botonEnviar.pack(pady=10)
        
    def agregar_doctor(self):
        if (self.entryCodigo.get() == "" or self.entryNombre.get() == "" or self.entryDireccion.get() == "" or 
            self.entryTelefono.get() == "" or self.entryFecha.get() == "" or 
            self.entrySexo.get() == "" or self.entryEspecialidad.get() == "" or 
            self.entryContrasena.get() == ""):
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
                (codigo, nombre, direccion, telefono, fecha_nac, sexo, especialidad, contraseña) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                self.entryCodigo.get(),
                self.entryNombre.get(), 
                self.entryDireccion.get(), 
                self.entryTelefono.get(),
                fecha_nac, 
                self.entrySexo.get(), 
                self.entryEspecialidad.get(), 
                self.entryContrasena.get()
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
                self.entryEspecialidad.delete(0, "end")
                self.entryContrasena.delete(0, "end")
            except Exception as e:
                messagebox.showerror("Error", f"Error al agregar doctor: {e}")
            
    
if __name__ == "__main__":
    doctores = Doctores()
    doctores.mainloop()
