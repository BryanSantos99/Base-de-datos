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
        self.setup_add_patient_form()
        self.create_tab_eliminar_paciente()
        self.create_tab_modificar_paciente()

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
        tabview.add("Eliminar Paciente")  # Asegúrate de que esta línea esté presente
        tabview.add("Modificar Paciente")  # Asegúrate de que esta línea esté presente

        self.pacientes_frame = ctk.CTkScrollableFrame(tabview.tab("Pacientes"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.pacientes_frame.place(relwidth=1, relheight=1)
        
        self.agregar_paciente_frame = ctk.CTkFrame(tabview.tab("Agregar Paciente"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.agregar_paciente_frame.place(relwidth=1, relheight=1)
        
        self.modificar_paciente_frame = ctk.CTkFrame(tabview.tab("Modificar Paciente"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.modificar_paciente_frame.place(relwidth=1, relheight=1)
        
        self.eliminar_paciente_frame = ctk.CTkFrame(tabview.tab("Eliminar Paciente"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.eliminar_paciente_frame.place(relwidth=1, relheight=1)
    

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
        conn = conecta.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM paciente")
        pacientes = cursor.fetchall()
        conn.commit()
        conn.close()

        self.tabla_pacientes = ttk.Treeview(
            self.pacientes_frame,
            columns=("Codigo", "Nombre", "Direccion", "Telefono", "Fecha de Nacimiento", "Sexo", "Edad", "Estatura", "Generar PDF"),
            style="Treeview",
            show="headings",
            height=40
        )
        
        for col, col_name in zip(self.tabla_pacientes["columns"], ["Codigo", "Nombre", "Direccion", "Telefono", "Fecha de Nacimiento", "Sexo", "Edad", "Estatura"]):
            self.tabla_pacientes.heading(col, text=col_name)

       
        for paciente in pacientes:
            paciente_datos = paciente[:-1] 
            self.tabla_pacientes.insert("", "end", values=paciente_datos, tags=("pdf",))
        self.tabla_pacientes.pack()

    def create_tab_eliminar_paciente(self):
        
        
        ctk.CTkLabel(self.eliminar_paciente_frame, text="Código del Paciente a eliminar:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryCodigoEliminar = ctk.CTkEntry(self.eliminar_paciente_frame, placeholder_text="Código", width=200, height=30)
        self.entryCodigoEliminar.pack(pady=10)

        boton_eliminar = ctk.CTkButton(self.eliminar_paciente_frame, text="Eliminar Paciente", command=self.eliminar_paciente)
        boton_eliminar.pack(pady=10)

    def eliminar_paciente(self):
        codigo = self.entryCodigoEliminar.get()
        
        if not codigo:
            messagebox.showerror("Error", "Debe ingresar el código del paciente")
            return

        conn = conecta.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM paciente WHERE codigo = %s", (codigo,))
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "No se encontró el paciente con el código ingresado.")
            else:
                conn.commit()
                messagebox.showinfo("Éxito", "Paciente eliminado correctamente")
                self.entryCodigoEliminar.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar el paciente: {e}")
        finally:
            conn.close()
            
    def create_tab_modificar_paciente(self):
       
        
        ctk.CTkLabel( self.modificar_paciente_frame, text="Código del Paciente a modificar:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryCodigoModificar = ctk.CTkEntry( self.modificar_paciente_frame, placeholder_text="Código", width=200, height=30)
        self.entryCodigoModificar.pack(pady=10)
        
        ctk.CTkLabel(self.modificar_paciente_frame, text="Nombre:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryNombreModificar = ctk.CTkEntry(self.modificar_paciente_frame, placeholder_text="Nuevo Nombre", width=200, height=30)
        self.entryNombreModificar.pack(pady=10)

        ctk.CTkLabel(self.modificar_paciente_frame, text="Dirección:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryDireccionModificar = ctk.CTkEntry(self.modificar_paciente_frame, placeholder_text="Nueva Dirección", width=200, height=30)
        self.entryDireccionModificar.pack(pady=10)

        ctk.CTkLabel(self.modificar_paciente_frame, text="Teléfono:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryTelefonoModificar = ctk.CTkEntry(self.modificar_paciente_frame, placeholder_text="Nuevo Teléfono", width=200, height=30)
        self.entryTelefonoModificar.pack(pady=10)


        boton_modificar = ctk.CTkButton( self.modificar_paciente_frame, text="Modificar Paciente", command=self.modificar_paciente)
        boton_modificar.pack(pady=10)

    def modificar_paciente(self):
        codigo = self.entryCodigoModificar.get()
        
        if not codigo:
            messagebox.showerror("Error", "Debe ingresar el código del paciente")
            return

        conn = conecta.conectar()
        cursor = conn.cursor()
        try:
            nuevo_nombre = self.entryNombreModificar.get()
            nueva_direccion = self.entryDireccionModificar.get()
            nuevo_telefono = self.entryTelefonoModificar.get()

            # Actualizar todos los campos necesarios
            cursor.execute("UPDATE paciente SET nombre = %s, direccion = %s, telefono = %s WHERE codigo = %s", 
                           (nuevo_nombre, nueva_direccion, nuevo_telefono, codigo))
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "No se encontró el paciente con el código ingresado.")
            else:
                conn.commit()
                messagebox.showinfo("Éxito", "Paciente modificado correctamente")
                self.entryCodigoModificar.delete(0, "end")
                self.entryNombreModificar.delete(0, "end")
                self.entryDireccionModificar.delete(0, "end")
                self.entryTelefonoModificar.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar el paciente: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    pacientes = Pacientes(nombre="usuario_demo", rol="A")
    pacientes.mainloop()
