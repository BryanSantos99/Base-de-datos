import customtkinter as ctk
from PIL import Image, ImageTk
import admin as admin
import empleadosadmin
import conecta
from tkinter import ttk, messagebox
from datetime import datetime

class Doctores(ctk.CTk):

    def __init__(self, nombre, rol):
        super().__init__()
        self.nombre = nombre
        self.rol = rol
        self.configure_window()
        self.load_images()
        self.setup_widgets()

    def configure_window(self):
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.geometry("400x500")
        self.title("MedLink")
        self.attributes("-fullscreen", True)

    def load_images(self):
        try:
            self.logo_image = Image.open("img/logo.png").resize((85, 85))
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except FileNotFoundError:
            print("Error: La imagen 'logo.png' no se encontró en la carpeta.")
            self.logo_photo = None

    def back_to_main(self):
        self.destroy()
        if self.rol == "A":
            admin.MainApp(self.nombre,self.rol)
        else:
            empleadosadmin.MainApp(self.nombre, self.rol)

    def setup_widgets(self):
        self.setup_header()
        self.setup_tabview()
        self.populate_doctors_table()
        self.setup_add_doctor_form()

    def setup_header(self):
        header_frame = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#1f6aa5")
        header_frame.place(relwidth=1.0, relx=0.5, rely=0.0, anchor='n')
        
        ctk.CTkButton(header_frame, text="Volver", width=100, height=30, fg_color="black", text_color="white", font=("Arial", 14), command=self.back_to_main).place(relx=0.85, rely=0.5, anchor="center")
        
        ctk.CTkLabel(header_frame, text="MedLink", font=("Arial", 24), text_color="white").place(relx=0.15, rely=0.5, anchor="center")
        ctk.CTkLabel(header_frame, text="Doctores", font=("Arial", 34), text_color="white").place(relx=0.5, rely=0.5, anchor="center")
        
        if self.logo_photo:
            ctk.CTkLabel(header_frame, image=self.logo_photo, text="").place(relheight=1, relx=0.93, rely=0.5, anchor="w")

    def setup_tabview(self):
        tabview = ctk.CTkTabview(self, fg_color="white")
        tabview.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.89)

        # Add tabs
        for tab_name in ["Doctores", "Agregar Doctor", "Eliminar Doctor", "Modificar Doctor"]:
            tabview.add(tab_name)
        
        # Create frames for each tab
        self.doctores_frame = ctk.CTkScrollableFrame(tabview.tab("Doctores"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.agregar_doctor_frame = ctk.CTkScrollableFrame(tabview.tab("Agregar Doctor"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.eliminar_doctor_frame = ctk.CTkScrollableFrame(tabview.tab("Eliminar Doctor"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")
        self.modificar_doctor_frame = ctk.CTkScrollableFrame(tabview.tab("Modificar Doctor"), corner_radius=0, fg_color="lightgray", border_width=1, border_color="black")

        # Set frames to fill tab space
        for frame in [self.doctores_frame, self.agregar_doctor_frame, self.eliminar_doctor_frame, self.modificar_doctor_frame]:
            frame.place(relwidth=1, relheight=1)

    def populate_doctors_table(self):
        conn = conecta.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctor")
        doctores = cursor.fetchall()
        conn.commit()
        conn.close()

        # Table
        tabla_doctores = ttk.Treeview(self.doctores_frame, columns=("id", "nombres", "direccion", 'telefono', 'fecha_nac', 'sexo', 'especialidad', 'contraseña'), style="Treeview", show="headings", height=40)
        for col, col_name in zip(tabla_doctores["columns"], ["Id", "Nombres", "Direccion", "Telefono", "Fecha Nacimiento", "Sexo", "Especialidad", "Contraseña"]):
            tabla_doctores.heading(col, text=col_name)

        for doctor in doctores:
            tabla_doctores.insert("", "end", values=doctor)

        tabla_doctores.pack(expand=True, fill="both")

    def setup_add_doctor_form(self):
        fields = [
            ("Codigo", "Codigo"), ("Nombre", "Nombre empleado"), ("Direccion", "Direccion"),
            ("Telefono", "Telefono"), ("Fecha Nacimiento", "AAAA-MM-DD"),
            ("Sexo", "FEMENINO/MASCULINO"), ("Especialidad", "Especialidad"), ("Contrasena", "Contrasena")
        ]
        
        self.entries = {}
        for label_text, placeholder in fields:
            label = ctk.CTkLabel(self.agregar_doctor_frame, text=label_text, font=("Arial", 14), text_color="black")
            label.pack(pady=(5, 5))
            entry = ctk.CTkEntry(self.agregar_doctor_frame, placeholder_text=placeholder, width=200, height=30)
            entry.pack(pady=5)
            self.entries[label_text.lower()] = entry
        
        ctk.CTkButton(self.agregar_doctor_frame, text="Agregar", command=self.agregar_doctor).pack(pady=10)

    def agregar_doctor(self):
        # Check if any field is empty
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
            INSERT INTO doctor 
            (codigo, nombre, direccion, telefono, fecha_nac, sexo, especialidad, contraseña) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                self.entries["codigo"].get(),
                self.entries["nombre"].get(),
                self.entries["direccion"].get(),
                self.entries["telefono"].get(),
                fecha_nac,
                self.entries["sexo"].get(),
                self.entries["especialidad"].get(),
                self.entries["contrasena"].get()
            ))
            conn.commit()
            messagebox.showinfo("Exito", "Doctor agregado correctamente")
            for entry in self.entries.values():
                entry.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar doctor: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    doctores = Doctores(nombre="usuario_demo", rol="A")
    doctores.mainloop()
