import customtkinter as ctk
from PIL import Image, ImageTk
import admin
import conecta
from tkinter import ttk, messagebox
from datetime import datetime
import empleadosadmin

class Empleados(ctk.CTk):
    def __init__(self, nombre, rol):
        super().__init__()

        self.nombre = nombre
        self.rol = rol
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.geometry("400x500")
        self.title("MedLink")
        self.attributes("-fullscreen", True)
        
        self.doctor_logo_photo = self.load_image("img/doctor_logo.png", (60, 60))
        self.logo_photo = self.load_image("img/logo.png", (85, 85))
        self.header_photo = self.load_image("img/logo.png", (300, 300))

        self.setup_widgets()

    def load_image(self, path, size):
        try:
            image = Image.open(path).resize(size)
            return ImageTk.PhotoImage(image)
        except FileNotFoundError:
            print(f"Error: La imagen '{path}' no se encontró en la carpeta.")
            return None

    def back_to_main(self):
        self.destroy()
        if self.rol == "A":
            admin.MainApp(self.nombre,self.rol)
        else:
            empleadosadmin.MainApp(self.nombre, self.rol)

    def setup_widgets(self):
        # Add header frame and buttons
        header_frame = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#1f6aa5")
        header_frame.place(relwidth=1.0, relx=0.5, rely=0.0, anchor='n')

        buttonBack = ctk.CTkButton(header_frame, text="Volver", width=100, height=30, fg_color="black", text_color="white", font=("Arial", 14), command=self.back_to_main)
        buttonBack.place(relx=0.85, rely=0.5, anchor="center")

        header_label = ctk.CTkLabel(header_frame, text="MedLink", font=("Arial", 24), text_color="white")
        header_label.place(relx=0.15, rely=0.5, anchor="center")

        header_label_empleados = ctk.CTkLabel(header_frame, text="Empleados", font=("Arial", 34), text_color="white")
        header_label_empleados.place(relx=0.5, rely=0.5, anchor="center")

        if self.logo_photo:
            logo_label = ctk.CTkLabel(header_frame, image=self.logo_photo, text="")
            logo_label.place(relheight=1, relx=0.93, rely=0.5, anchor="w")

        
        tabview = ctk.CTkTabview(self, fg_color="white")
        tabview.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.89)
        
        for tab_name in ["Empleados", "Agregar Empleado", "Eliminar Empleado", "Modificar Empleado"]:
            tabview.add(tab_name)

        self.setup_tabs(tabview)

    def setup_tabs(self, tabview):
        self.empleados_frame = ctk.CTkScrollableFrame(tabview.tab("Empleados"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.empleados_frame.place(relwidth=1, relheight=1)

        self.setup_empleados_table()

       
        self.agregar_empleado_frame = ctk.CTkFrame(tabview.tab("Agregar Empleado"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.agregar_empleado_frame.place(relwidth=1, relheight=1)

        self.setup_agregar_empleado_form()

    def setup_empleados_table(self):
        tabla_empleado = ttk.Treeview(self.empleados_frame, columns=("id", "nombres","direccion",'telefono','fecha_nac','sexo','sueldo','turno','contraseña'), show="headings", height=40)
        for col, title in zip(tabla_empleado["columns"], ["ID", "Nombres", "Dirección", "Teléfono", "Fecha Nacimiento", "Sexo", "Sueldo", "Turno", "Contraseña"]):
            tabla_empleado.heading(col, text=title)
        tabla_empleado.pack(expand=True, fill="both")

        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM empleado")
            empleados = cursor.fetchall()
            conn.close()
            for empleado in empleados:
                tabla_empleado.insert("", "end", values=empleado)
        except Exception as e:
            messagebox.showerror("Error", "Error al cargar empleados.")
            print(f"Error al cargar empleados: {e}")

    def setup_agregar_empleado_form(self):
        label_and_placeholder = [
            ("Id", "Id"), 
            ("Nombre", "Nombre empleado"), 
            ("Dirección", "Dirección"),
            ("Teléfono", "Teléfono"),
            ("Fecha Nacimiento", "AAAA-MM-DD"),
            ("Sexo", "Femenino/Masculino"),
            ("Sueldo", "Sueldo"),
            ("Turno", "Turno"),
            ("Contraseña", "Contraseña")
        ]
        for text, placeholder in label_and_placeholder:
            label = ctk.CTkLabel(self.agregar_empleado_frame, text=text, font=("Arial", 14), text_color="black")
            label.pack(pady=(5, 5))
            entry = ctk.CTkEntry(self.agregar_empleado_frame, placeholder_text=placeholder, width=200, height=30)
            entry.pack(pady=5)

        botonEnviar = ctk.CTkButton(self.agregar_empleado_frame, text="Agregar", command=self.agregar_empleado)
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
    empleados = Empleados(nombre="NombreEmpleado", rol="RolEmpleado")
    empleados.mainloop()
