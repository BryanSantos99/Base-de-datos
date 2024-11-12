import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import messagebox, ttk
import conecta

class Consultas(ctk.CTk):
    def __init__(self, nombre, rol):
        super().__init__()
        self.nombre = nombre
        self.rol = rol
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.geometry("800x600")
        self.title("MedLink - Gestión de Consultas")
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
        
        header_label = ctk.CTkLabel(header_frame, text="MedLink - Consultas", font=("Arial", 24), text_color="white")
        header_label.place(relx=0.15, rely=0.5, anchor="center")

    def create_tabs(self):
        self.tabview.add("Consultas")
        self.tabview.add("Agregar Consulta")
        
        self.create_tab_consulta()
        self.create_tab_agregar_consulta()

    def create_tab_consulta(self):
        consulta_frame = ctk.CTkFrame(self.tabview.tab("Consultas"), corner_radius=0, fg_color="lightgray", 
                                      border_width=1, border_color="black")
        consulta_frame.place(relwidth=1, relheight=1)
        
        self.setup_consultas_table(consulta_frame)
        
    def setup_consultas_table(self, frame):
        tabla_consulta = ttk.Treeview(frame, columns=("id", "Paciente", "Doctor", "Fecha", "Diagnóstico"), show="headings", height=40)
        for col, title in zip(tabla_consulta["columns"], ["ID", "Paciente", "Doctor", "Fecha", "Diagnóstico"]):
            tabla_consulta.heading(col, text=title)
        tabla_consulta.pack(expand=True, fill="both")

        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM consulta")
            consultas = cursor.fetchall()
            conn.close()
            for consulta in consultas:
                tabla_consulta.insert("", "end", values=consulta)
        except Exception as e:
            messagebox.showerror("Error", "Error al cargar consultas.")
            print(f"Error al cargar consultas: {e}")

    def create_tab_agregar_consulta(self):
        agregar_frame = ctk.CTkFrame(self.tabview.tab("Agregar Consulta"), corner_radius=0, fg_color="lightgray", 
                                     border_width=1, border_color="black")
        agregar_frame.place(relwidth=1, relheight=1)
        
        ctk.CTkLabel(agregar_frame, text="Crear consulta:", font=("Arial", 14), text_color="black").pack(pady=10)
        
        ctk.CTkLabel(agregar_frame, text="Id paciente:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryPaciente = ctk.CTkEntry(agregar_frame, placeholder_text="ID Paciente", width=200, height=30)
        self.entryPaciente.pack(pady=5)
        
        ctk.CTkLabel(agregar_frame, text="Id Doctor:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryMedico = ctk.CTkEntry(agregar_frame, placeholder_text="ID Médico", width=200, height=30)
        self.entryMedico.pack(pady=5)
        
        ctk.CTkLabel(agregar_frame, text="Fecha de la Consulta:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.calendar = Calendar(agregar_frame, date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=10)
        
        # Lista desplegable para seleccionar medicamentos
        ctk.CTkLabel(agregar_frame, text="Seleccione Medicamento:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.medicamento_combobox = ttk.Combobox(agregar_frame, values=self.get_medicamentos())
        self.medicamento_combobox.set("Seleccione Medicamento")
        self.medicamento_combobox.pack(pady=5)
        
        boton_agregar = ctk.CTkButton(agregar_frame, text="Agregar Consulta", command=self.agregar_consulta)
        boton_agregar.pack(pady=10)

    def get_medicamentos(self):
        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT nombre FROM medicamento")
            medicamentos = [med[0] for med in cursor.fetchall()]
            conn.close()
            return medicamentos
        except Exception as e:
            messagebox.showerror("Error", "Error al cargar medicamentos.")
            print(f"Error al cargar medicamentos: {e}")
            return []

    def agregar_consulta(self):
        paciente_id = self.entryPaciente.get().strip()
        medico_id = self.entryMedico.get().strip()
        fecha = self.calendar.get_date()
        medicamento = self.medicamento_combobox.get().strip()

        if not paciente_id or not medico_id or medicamento == "Seleccione Medicamento":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO consulta (paciente_id, doctor_id, fecha, diagnostico)
                VALUES (%s, %s, %s, %s)
            """, (paciente_id, medico_id, fecha, f"Recetar {medicamento}"))
            conn.commit()
            messagebox.showinfo("Éxito", "Consulta agregada correctamente")
            self.clear_input_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar la consulta: {e}")
        finally:
            conn.close()

    def clear_input_fields(self):
        self.entryPaciente.delete(0, "end")
        self.entryMedico.delete(0, "end")
        self.medicamento_combobox.set("Seleccione Medicamento")

    def back_to_main(self):
        self.destroy()

if __name__ == "__main__":
    app = Consultas("admin", "A")
    app.mainloop()
