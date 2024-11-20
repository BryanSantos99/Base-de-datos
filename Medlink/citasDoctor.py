import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import messagebox, ttk
from datetime import datetime
import conecta
import admin
import empleadosadmin
import doctoresadmin

class Citas(ctk.CTk):
    def __init__(self, nombre, rol):
        super().__init__()
        self.nombre = nombre
        self.rol = rol
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.geometry("800x600")
        self.title("MedLink - Gestión de Citas")
        self.attributes("-fullscreen", True)
        
        self.setup_widgets()
        
    def setup_widgets(self):
        self.create_header()
        self.tabview = ctk.CTkTabview(self, fg_color="white")
        self.tabview.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.89)
        self.create_tabs()

    def create_header(self):
        header_frame = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#1f6aa5")
        header_frame.place(relwidth=1.0, relx=0.5, rely=0.0, anchor='n')
        
        buttonBack = ctk.CTkButton(header_frame, text="Volver", width=100, height=30, fg_color="black", 
                                   text_color="white", font=("Arial", 14), command=self.back_to_main)
        buttonBack.place(relx=0.85, rely=0.5, anchor="center")
        
        header_label = ctk.CTkLabel(header_frame, text="MedLink - Citas", font=("Arial", 24), text_color="white")
        header_label.place(relx=0.15, rely=0.5, anchor="center")

    def create_tabs(self):
        self.tabview.add("Citas")
        
        self.create_tab_cita()
        
        
    def create_tab_cita(self):
        agregar_frame = ctk.CTkFrame(self.tabview.tab("Citas"), corner_radius=0, fg_color="lightgray", 
                                     border_width=1, border_color="black")
        agregar_frame.place(relwidth=1, relheight=1)
        
        self.setup_citas_table(agregar_frame)
        
    def setup_citas_table(self,frame):
        tabla_cita = ttk.Treeview(frame, columns=("id", "Paciente","Doctor",'Fecha','hora'), show="headings", height=40)
        for col, title in zip(tabla_cita["columns"], ["ID", "Paciente", "Doctor", "Fecha", "Hora"]):
            tabla_cita.heading(col, text=title)
        tabla_cita.pack(expand=True, fill="both")
        id_d=0
        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            print(self.nombre)
            cursor.execute(f"SELECT codigo FROM doctor WHERE nombre='{self.nombre}'")
            doctor = cursor.fetchone()
            if doctor is not None:  # Verifica si se encontró un doctor
                id_d = doctor[0]
                print(id_d)
            else:
                messagebox.showerror("Error", "No se encontró el doctor.")
            
        except Exception as e:
            messagebox.showerror("Error", "Error al doctor.")
            print(f"Error al cargar citas: {e}")
            
        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM cita WHERE doctor_id = '{id_d}'")
            empleados = cursor.fetchall()
            conn.close()
            for empleado in empleados:
                tabla_cita.insert("", "end", values=empleado)
        except Exception as e:
            messagebox.showerror("Error", "Error al cargar citas.")
            print(f"Error al cargar citas: {e}")

        

    def back_to_main(self):
        self.destroy()
        if self.rol == "A":
            admin.MainApp(self.nombre,self.rol)
        elif self.rol=='E':
            empleadosadmin.MainApp(self.nombre, self.rol)
        else:
            doctoresadmin.MainApp(self.nombre, self.rol)

if __name__ == "__main__":
    app = Citas("admin", "A")
    app.mainloop()
