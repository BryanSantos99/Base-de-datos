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
        
        self.eliminar_empleado_frame = ctk.CTkFrame(tabview.tab("Eliminar Empleado"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.eliminar_empleado_frame.place(relwidth=1, relheight=1)

        self.eliminar_empleado_form()
        
        self.modificar_empleado_frame = ctk.CTkFrame(tabview.tab("Modificar Empleado"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.modificar_empleado_frame.place(relwidth=1, relheight=1)

        self.modificar_empleado_form()

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

    def modificar_empleado_form(self):
        
        ctk.CTkLabel(self.modificar_empleado_frame, text="Código del Empleado a modificar:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryCodigoModificar2 = ctk.CTkEntry(self.modificar_empleado_frame, placeholder_text="Código", width=200, height=30)
        self.entryCodigoModificar2.pack(pady=10)

        self.entryNombreModificar = ctk.CTkEntry(self.modificar_empleado_frame, placeholder_text="Nuevo Nombre", width=200, height=30)
        self.entryNombreModificar.pack(pady=5)
        
        self.entryDireccionModificar = ctk.CTkEntry(self.modificar_empleado_frame, placeholder_text="Nueva Dirección", width=200, height=30)
        self.entryDireccionModificar.pack(pady=5)

        self.entryTelefonoModificar = ctk.CTkEntry(self.modificar_empleado_frame, placeholder_text="Nuevo Teléfono", width=200, height=30)
        self.entryTelefonoModificar.pack(pady=5)

        boton_modificar = ctk.CTkButton(self.modificar_empleado_frame, text="Modificar Empleado", command=self.modificar_empleado)
        boton_modificar.pack(pady=10)

    def modificar_empleado(self):
        codigo = self.entryCodigoModificar2.get()
        nuevo_nombre = self.entryNombreModificar.get()
        nueva_direccion = self.entryDireccionModificar.get()
        nuevo_telefono = self.entryTelefonoModificar.get()

        if not codigo or not nuevo_nombre or not nueva_direccion or not nuevo_telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = conecta.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE empleado 
                SET nombre = %s, direccion = %s, telefono = %s 
                WHERE codigo = %s
            """, (nuevo_nombre, nueva_direccion, nuevo_telefono, codigo))
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "No se encontró el empleado con el código ingresado.")
            else:
                conn.commit()
                messagebox.showinfo("Éxito", "Empleado modificado correctamente")
                self.entryCodigoModificar2.delete(0, "end")
                self.entryNombreModificar.delete(0, "end")
                self.entryDireccionModificar.delete(0, "end")
                self.entryTelefonoModificar.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar el empleado: {e}")
        finally:
            conn.close()

    
    def clear_input_fields_mod(self):
        self.entryPaciente2.delete(0, "end")
        self.entryMedico2.delete(0, "end")
        self.hour_combobox2.set("Seleccionar hora")
        
    def eliminar_empleado_form(self):
       
        
        ctk.CTkLabel(self.eliminar_empleado_frame, text="Código del Empleado a eliminar:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryCodigoEliminar = ctk.CTkEntry(self.eliminar_empleado_frame, placeholder_text="Código", width=200, height=30)
        self.entryCodigoEliminar.pack(pady=10)

        boton_eliminar = ctk.CTkButton(self.eliminar_empleado_frame, text="Eliminar Empleado", command=self.eliminar_empleado)
        boton_eliminar.pack(pady=10)

    def eliminar_empleado(self):
        codigo = self.entryCodigoEliminar.get()
        
        if not codigo:
            messagebox.showerror("Error", "Debe ingresar el código del empleado")
            return

        conn = conecta.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM empleado WHERE codigo = %s", (codigo,))
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "No se encontró el empleado con el código ingresado.")
            else:
                conn.commit()
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente")
                self.entryCodigoEliminar.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el empleado: {e}")
        finally:
            conn.close()
            
if __name__ == "__main__":
    empleados = Empleados(nombre="Admin", rol="A")
    empleados.mainloop()
