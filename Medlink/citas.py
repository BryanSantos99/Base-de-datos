import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import messagebox, ttk
from datetime import datetime
import conecta
import admin
import empleadosadmin

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
        self.tabview.add("Agregar Cita")
        self.tabview.add("Modificar Cita")
        self.tabview.add("Eliminar Cita")
        
        self.create_tab_cita()
        self.create_tab_agregar_cita()
        self.create_tab_modificar_cita()
        self.create_tab_eliminar_cita()

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

        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cita")
            empleados = cursor.fetchall()
            conn.close()
            for empleado in empleados:
                tabla_cita.insert("", "end", values=empleado)
        except Exception as e:
            messagebox.showerror("Error", "Error al cargar citas.")
            print(f"Error al cargar citas: {e}")

        
    def create_tab_agregar_cita(self):
        agregar_frame = ctk.CTkFrame(self.tabview.tab("Agregar Cita"), corner_radius=0, fg_color="lightgray", 
                                     border_width=1, border_color="black")
        agregar_frame.place(relwidth=1, relheight=1)
        
        ctk.CTkLabel(agregar_frame, text="Crear cita:", font=("Arial", 14),text_color="black").pack(pady=10)
        
        ctk.CTkLabel(agregar_frame, text="Id paciente:", font=("Arial", 14),text_color="black").pack(pady=10)
        self.entryPaciente = ctk.CTkEntry(agregar_frame, placeholder_text="ID Paciente", width=200, height=30)
        self.entryPaciente.pack(pady=5)
        
        ctk.CTkLabel(agregar_frame, text="Id Doctor:", font=("Arial", 14),text_color="black").pack(pady=10)
        self.entryMedico = ctk.CTkEntry(agregar_frame, placeholder_text="ID Médico", width=200, height=30)
        self.entryMedico.pack(pady=5)
        
        ctk.CTkLabel(agregar_frame, text="Seleccione la Fecha:", font=("Arial", 14),text_color="black").pack(pady=10)
        self.calendar = Calendar(agregar_frame, date_pattern="yyyy-mm-dd")
        self.calendar.pack(pady=10)
        
        ctk.CTkLabel(agregar_frame, text="Seleccione la Hora:", font=("Arial", 14),text_color="black").pack(pady=10)
        self.hour_combobox = ttk.Combobox(agregar_frame, values=self.get_available_hours())
        self.hour_combobox.set("Seleccione Hora")
        self.hour_combobox.pack(pady=5)
        
        boton_agregar = ctk.CTkButton(agregar_frame, text="Agregar Cita", command=self.agregar_cita)
        boton_agregar.pack(pady=10)

        
    def get_available_hours(self):
        return [f"{hour:02}:00" for hour in range(9, 21)]

    def agregar_cita(self):
        paciente_id = self.entryPaciente.get().strip()
        medico_id = self.entryMedico.get().strip()
        fecha = self.calendar.get_date()
        hora = self.hour_combobox.get().strip()

        if hora == "Seleccione Hora":
            messagebox.showerror("Error", "Debe seleccionar una hora válida.")
            return

        conn = conecta.conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 1 FROM cita WHERE fecha = %s AND hora = %s AND doctor_id = %s
        """, (fecha, hora,medico_id))
        if cursor.fetchone():
            messagebox.showerror("Error", "La hora seleccionada ya está ocupada.")
            conn.close()
            return
        conn.close()

        
        conn = conecta.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO cita (paciente_id, doctor_id, fecha, hora)
                VALUES (%s, %s, %s, %s)
            """, (paciente_id, medico_id, fecha, hora))
            conn.commit()
            messagebox.showinfo("Éxito", "Cita agregada correctamente")
            self.clear_input_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar la cita: {e}")
        finally:
            conn.close()


    def clear_input_fields(self):
        self.entryPaciente.delete(0, "end")
        self.entryMedico.delete(0, "end")
        self.hour_combobox.set("Seleccionar hora")

    # Modificar Cita Tab
    def create_tab_modificar_cita(self):
        modificar_frame = ctk.CTkFrame(self.tabview.tab("Modificar Cita"), corner_radius=0, fg_color="lightgray", 
                                       border_width=1, border_color="black")
        modificar_frame.place(relwidth=1, relheight=1)
        
        ctk.CTkLabel(modificar_frame, text="Código de la Cita a Modificar:", font=("Arial", 14),text_color="black").pack(pady=10)
        self.entryCodigoModificar2 = ctk.CTkEntry(modificar_frame, placeholder_text="Código", width=200, height=30)
        self.entryCodigoModificar2.pack(pady=10)
        
        ctk.CTkLabel(modificar_frame, text="Id Paciente:", font=("Arial", 14),text_color="black").pack(pady=10)
        self.entryPaciente2 = ctk.CTkEntry(modificar_frame, placeholder_text="ID Paciente", width=200, height=30)
        self.entryPaciente2.pack(pady=5)
        
        ctk.CTkLabel(modificar_frame, text="Id Doctor:", font=("Arial", 14),text_color="black").pack(pady=10)
        self.entryMedico2 = ctk.CTkEntry(modificar_frame, placeholder_text="ID Médico", width=200, height=30)
        self.entryMedico2.pack(pady=5)
        
        ctk.CTkLabel(modificar_frame, text="Seleccione la Fecha:", font=("Arial", 14),text_color="black").pack(pady=10)
        self.calendar2 = Calendar(modificar_frame, date_pattern="yyyy-mm-dd")
        self.calendar2.pack(pady=10)
        
        ctk.CTkLabel(modificar_frame, text="Seleccione la Hora:", font=("Arial", 14),text_color="black").pack(pady=10)
        self.hour_combobox2 = ttk.Combobox(modificar_frame, values=self.get_available_hours())
        self.hour_combobox2.set("Seleccione Hora")
        self.hour_combobox2.pack(pady=5)

        
        boton_modificar = ctk.CTkButton(modificar_frame, text="Modificar Cita", command=self.modificar_cita)
        boton_modificar.pack(pady=10)

    def modificar_cita(self):
        codigo = self.entryCodigoModificar2.get()
        paciente_id = self.entryPaciente2.get()
        medico_id = self.entryMedico2.get()
        fecha = self.calendar2.get_date()
        hora = self.hour_combobox2.get()

        if not codigo or not paciente_id or not medico_id or hora == "Seleccione Hora":
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = conecta.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE cita SET paciente_id = %s, doctor_id = %s, fecha = %s, hora = %s
                WHERE id_cita = %s
            """, (paciente_id, medico_id, fecha, hora, codigo))
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "No se encontró la cita con el código ingresado.")
            else:
                conn.commit()
                messagebox.showinfo("Éxito", "Cita modificada correctamente")
                
                codigo.delete(0, "end")
                self.clear_input_fields_mod()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar la cita: {e}")
        finally:
            self.clear_input_fields()
            conn.close()

    def clear_input_fields_mod(self):
        self.entryPaciente2.delete(0, "end")
        self.entryMedico2.delete(0, "end")
        self.hour_combobox2.set("Seleccionar hora")
        
    def create_tab_eliminar_cita(self):
        eliminar_frame = ctk.CTkFrame(self.tabview.tab("Eliminar Cita"), corner_radius=0, fg_color="lightgray", 
                                      border_width=1, border_color="black")
        eliminar_frame.place(relwidth=1, relheight=1)
        
        ctk.CTkLabel(eliminar_frame, text="Código de la Cita a Eliminar:", font=("Arial", 14),text_color="black").pack(pady=10)
        self.entryCodigoEliminar = ctk.CTkEntry(eliminar_frame, placeholder_text="Código", width=200, height=30)
        self.entryCodigoEliminar.pack(pady=10)
        
        boton_eliminar = ctk.CTkButton(eliminar_frame, text="Eliminar Cita", command=self.eliminar_cita)
        boton_eliminar.pack(pady=10)

    def eliminar_cita(self):
        codigo = self.entryCodigoEliminar.get()
        
        if not codigo:
            messagebox.showerror("Error", "Debe ingresar el código de la cita")
            return

        conn = conecta.conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM cita WHERE id_cita = %s", (codigo,))
            if cursor.rowcount == 0:
                messagebox.showerror("Error", "No se encontró la cita con el código ingresado.")
            else:
                conn.commit()
                messagebox.showinfo("Éxito", "Cita eliminada correctamente")
                self.entryCodigoEliminar.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar la cita: {e}")
        finally:
            conn.close()
            
    def back_to_main(self):
        self.destroy()
        if self.rol == "A":
            admin.MainApp(self.nombre,self.rol)
        else:
            empleadosadmin.MainApp(self.nombre, self.rol)


if __name__ == "__main__":
    app = Citas("admin", "A")
    app.mainloop()
