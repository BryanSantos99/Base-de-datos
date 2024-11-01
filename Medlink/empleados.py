import customtkinter as ctk
from PIL import Image, ImageTk
import main_app
import conecta
from tkinter import ttk, messagebox
from datetime import datetime

class Empleados(ctk.CTk):
    def __init__(self,nombre):
        super().__init__()
        
        self.nombre=nombre
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.geometry("400x500")
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
        while True:
            try:
                self.setup_widgets()
                break
            except Exception as e:
                print(f"Error al cargar empleados: {e}")

    
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
        
        header_label = ctk.CTkLabel(header_frame, text="Empleados", font=("Arial", 34), text_color="white")
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        logo_label = ctk.CTkLabel(header_frame, image=self.logo_photo, text="")
        logo_label.place(relheight=1,relx=0.93, rely=0.5, anchor="w")
        
        tabview = ctk.CTkTabview(self,fg_color="white")
        tabview.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.89)
        
        tabview.add("Empleados")
        tabview.add("Agregar Empleado")
        tabview.add("Eliminar Empleado")
        tabview.add("Modificar Empleado")
        
        self.empleados_frame = ctk.CTkScrollableFrame(tabview.tab("Empleados"), corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.empleados_frame.place(relwidth=1, relheight=1)
        
        self.agregar_empleado_frame = ctk.CTkFrame(tabview.tab("Agregar Empleado"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.agregar_empleado_frame.place(relwidth=1, relheight=1)

        
        self.eliminar_empleado_frame = ctk.CTkScrollableFrame(tabview.tab("Eliminar Empleado"), corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.eliminar_empleado_frame.place(relwidth=1, relheight=1)
        
        self.modificar_empleado_frame = ctk.CTkScrollableFrame(tabview.tab("Modificar Empleado"), corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.modificar_empleado_frame.place(relwidth=1, relheight=1)
        
        while True:
            try:
                conn = conecta.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM empleado")
                empleados = cursor.fetchall()
                conn.commit()
                conn.close()
                break
            except Exception as e:
                print(f"Error al cargar empleados: {e}")
        
        
        tabla_empleado = ttk.Treeview(self.empleados_frame, columns=("id", "nombres","direccion",'telefono','fecha_nac','sexo','sueldo','turno','contraseña'), style="Treeview", show="headings", height=40)
        tabla_empleado.heading("id", text="Id")
        tabla_empleado.heading("nombres", text="Nombres")
        tabla_empleado.heading("direccion", text="Direccion")
        tabla_empleado.heading("telefono", text="Telefono")
        tabla_empleado.heading("fecha_nac", text="Fecha Nacimiento")
        tabla_empleado.heading("sexo", text="Sexo")
        tabla_empleado.heading("sueldo", text="Sueldo")
        tabla_empleado.heading("turno", text="Turno")
        tabla_empleado.heading("contraseña", text="Contraseña")
        while True:
            try:
                for empleado in empleados:
                    tabla_empleado.insert("", "end", values=empleado)
                break
            except Exception as e:

                messagebox.showerror("Error", "Al cargar datos")

                print(f"Error al cargar empleados: {e}")
            
        tabla_empleado.pack(expand=True, fill="both")
        
        labelId = ctk.CTkLabel(self.agregar_empleado_frame, text="Id", font=("Arial", 14), text_color="black")
        labelId.pack(pady=(5, 5))
        
        self.entryId = ctk.CTkEntry(self.agregar_empleado_frame, placeholder_text="Id", width=200, height=30)
        self.entryId.pack(pady=5)
        
        labelNombre = ctk.CTkLabel(self.agregar_empleado_frame, text="Nombre", font=("Arial", 14), text_color="black")
        labelNombre.pack(pady=(5, 5))
        
        self.entryNombre = ctk.CTkEntry(self.agregar_empleado_frame, placeholder_text="Nombre empleado", width=200, height=30)
        self.entryNombre.pack(pady=5)
        
        labelDireccion = ctk.CTkLabel(self.agregar_empleado_frame, text="Direccion", font=("Arial", 14), text_color="black")
        labelDireccion.pack(pady=(5, 5))
        
        self.entryDireccion = ctk.CTkEntry(self.agregar_empleado_frame, placeholder_text="Direccion", width=200, height=30)
        self.entryDireccion.pack(pady=5)

        labelNss = ctk.CTkLabel(self.agregar_empleado_frame, text="Telefono", font=("Arial", 14), text_color="black")
        labelNss.pack(pady=(5, 5))
        
        self.entryTelefono = ctk.CTkEntry(self.agregar_empleado_frame, placeholder_text="Telefono", width=200, height=30)
        self.entryTelefono.pack(pady=5)
        
        labelFecha = ctk.CTkLabel(self.agregar_empleado_frame, text="Fecha Nacimiento", font=("Arial", 14), text_color="black")
        labelFecha.pack(pady=(5, 5))
        
        
        self.entryFecha = ctk.CTkEntry(self.agregar_empleado_frame, placeholder_text="AAAA-MM-DD", width=200, height=30)
        self.entryFecha.pack(pady=5)
        
        labelSexo = ctk.CTkLabel(self.agregar_empleado_frame, text="Sexo", font=("Arial", 14), text_color="black")
        labelSexo.pack(pady=(5, 5))
        
        self.entrySexo = ctk.CTkEntry(self.agregar_empleado_frame, placeholder_text="FEMENINO/MASCULINO", width=200, height=30)
        self.entrySexo.pack(pady=5)

        
        labelSueldo = ctk.CTkLabel(self.agregar_empleado_frame, text="Sueldo", font=("Arial", 14), text_color="black")
        labelSueldo.pack(pady=(5, 5))
        
        self.entrySueldo = ctk.CTkEntry(self.agregar_empleado_frame, placeholder_text="Sueldo", width=200, height=30)
        self.entrySueldo.pack(pady=5)
        
        labelTurno = ctk.CTkLabel(self.agregar_empleado_frame, text="Turno", font=("Arial", 14), text_color="black")
        labelTurno.pack(pady=(5, 5))
        
        self.entryTurno = ctk.CTkEntry(self.agregar_empleado_frame, placeholder_text="Turno", width=200, height=30)
        self.entryTurno.pack(pady=5)
        
        labelContrasena = ctk.CTkLabel(self.agregar_empleado_frame, text="Contrasena", font=("Arial", 14), text_color="black")
        labelContrasena.pack(pady=(5, 5))
        
        self.entryContrasena = ctk.CTkEntry(self.agregar_empleado_frame, placeholder_text="Contrasena", width=200, height=30)
        self.entryContrasena.pack(pady=5)
        
        botonEnviar = ctk.CTkButton(self.agregar_empleado_frame, text="Agregar",command=self.agregar_empleado)
        botonEnviar.pack(pady=10)
        
    def agregar_empleado(self):
        if self.entryId.get() == "" or self.entryNombre.get() == "" or self.entryDireccion.get() == "" or self.entryTelefono.get() == "" or self.entryFecha.get() == "" or self.entrySexo.get() == "" or self.entrySueldo.get() == "" or self.entryTurno.get() == "" or self.entryContrasena.get() == "":
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        else:       
            try:
                conn = conecta.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM empleado WHERE codigo = %s", (self.entryId.get(),))
                if cursor.fetchone():
                    messagebox.showerror("Error", "El id ya existe")
                    self.entryId.delete(0, "end")
                    conn.commit()
                    conn.close()
                    return
                
                else:
                    conn = conecta.conectar()
                    cursor = conn.cursor()
                    try:
                        fecha_nac = datetime.strptime(self.entryFecha.get(), "%Y-%m-%d")
                    except ValueError:
                        messagebox.showerror("Error", "Formato de fecha incorrecto")
                        return
                    
                    cursor.execute("""
                    INSERT INTO empleado 
                    (codigo, nombre, direccion, telefono, fecha_nac, sexo, sueldo, turno, contraseña) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                     """, (
                    self.entryId.get(), 
                    self.entryNombre.get(), 
                    self.entryDireccion.get(), 
                    self.entryTelefono.get(), 
                    fecha_nac, 
                    self.entrySexo.get(), 
                    self.entrySueldo.get(), 
                    self.entryTurno.get(), 
                    self.entryContrasena.get()
                    ))
                    
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Exito", "Empleado agregado correctamente")
                    self.entryId.delete(0, "end")
                    self.entryNombre.delete(0, "end")
                    self.entryDireccion.delete(0, "end")
                    self.entryTelefono.delete(0, "end")
                    self.entryFecha.delete(0, "end")
                    self.entrySexo.delete(0, "end")
                    self.entrySueldo.delete(0, "end")
                    self.entryTurno.delete(0, "end")
                    self.entryContrasena.delete(0, "end")
                    
            except Exception as e:
                messagebox.showerror("Error", "En la operacion")

                print(f"Error al agregar empleado: {e}")

    

if __name__ == "__main__":
    empleados = Empleados()
    empleados.mainloop()
