import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import messagebox, ttk
from datetime import datetime
import conecta
import admin
import empleadosadmin

class Medicamento(ctk.CTk):
    def __init__(self, nombre, rol):
        super().__init__()
        self.nombre = nombre
        self.rol = rol
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")
        self.geometry("800x600")
        self.title("MedLink - Gestión de Medicamentos")
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
        
        header_label = ctk.CTkLabel(header_frame, text="MedLink - Medicamentos", font=("Arial", 24), text_color="white")
        header_label.place(relx=0.15, rely=0.5, anchor="center")

    def create_tabs(self):
        self.tabview.add("Medicamentos")
        self.tabview.add("Agregar Medicamento")
        self.tabview.add("Modificar Medicamento")
        self.tabview.add("Eliminar Medicamento")
        
        self.create_tab_medicamento()
        self.create_tab_agregar_medicamento()
        self.create_tab_modificar_medicamento()
        self.create_tab_eliminar_medicamento()

    def create_tab_medicamento(self):
        medicamentos_frame = ctk.CTkFrame(self.tabview.tab("Medicamentos"), corner_radius=0, fg_color="lightgray", 
                                          border_width=1, border_color="black")
        medicamentos_frame.place(relwidth=1, relheight=1)
        
        self.setup_medicamentos_table(medicamentos_frame)
        
    def setup_medicamentos_table(self, frame):
        self.tabla_medicamentos = ttk.Treeview(frame, columns=("codigo", "nombre", "via_adm", "presentacion", "fecha_cad"), show="headings", height=40)
        for col, title in zip(self.tabla_medicamentos["columns"], ["Código", "Nombre", "Vía de Administración", "Presentación", "Fecha de Caducidad"]):
            self.tabla_medicamentos.heading(col, text=title)
        self.tabla_medicamentos.pack(expand=True, fill="both")

        self.load_medicamentos()

    def load_medicamentos(self):
        for row in self.tabla_medicamentos.get_children():
            self.tabla_medicamentos.delete(row)
        
        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM medicamento")
            medicamentos = cursor.fetchall()
            conn.close()
            for medicamento in medicamentos:
                self.tabla_medicamentos.insert("", "end", values=medicamento)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar medicamentos: {e}")

    def create_tab_agregar_medicamento(self):
        agregar_frame = ctk.CTkFrame(self.tabview.tab("Agregar Medicamento"), corner_radius=0, fg_color="lightgray", 
                                     border_width=1, border_color="black")
        agregar_frame.place(relwidth=1, relheight=1)
        
        ctk.CTkLabel(agregar_frame, text="Agregar Medicamento:", font=("Arial", 14), text_color="black").pack(pady=10)
        
        self.entryCodigo = ctk.CTkEntry(agregar_frame, placeholder_text="Código", width=200, height=30)
        self.entryCodigo.pack(pady=5)
        
        self.entryNombre = ctk.CTkEntry(agregar_frame, placeholder_text="Nombre", width=200, height=30)
        self.entryNombre.pack(pady=5)
        
        self.entryViaAdm = ctk.CTkEntry(agregar_frame, placeholder_text="Vía de Administración", width=200, height=30)
        self.entryViaAdm.pack(pady=5)
        
        self.entryPresentacion = ctk.CTkEntry(agregar_frame, placeholder_text="Presentación", width=200, height=30)
        self.entryPresentacion.pack(pady=5)
        
        self.calendarFechaCad = Calendar(agregar_frame, date_pattern="yyyy-mm-dd")
        self.calendarFechaCad.pack(pady=10)
        
        boton_agregar = ctk.CTkButton(agregar_frame, text="Agregar Medicamento", command=self.agregar_medicamento)
        boton_agregar.pack(pady=10)

    def agregar_medicamento(self):
        codigo = self.entryCodigo.get().strip()
        nombre = self.entryNombre.get().strip()
        via_adm = self.entryViaAdm.get().strip()
        presentacion = self.entryPresentacion.get().strip()
        fecha_cad = self.calendarFechaCad.get_date()

        if not codigo or not nombre or not via_adm or not presentacion:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO medicamento (codigo, nombre, via_adm, presentacion, fecha_cad)
                VALUES (%s, %s, %s, %s, %s)
            """, (codigo, nombre, via_adm, presentacion, fecha_cad))
            conn.commit()
            messagebox.showinfo("Éxito", "Medicamento agregado correctamente")
            self.load_medicamentos()
            self.clear_input_fields()
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar medicamento: {e}")
        finally:
            conn.close()

    def create_tab_modificar_medicamento(self):
        modificar_frame = ctk.CTkFrame(self.tabview.tab("Modificar Medicamento"), corner_radius=0, fg_color="lightgray", 
                                       border_width=1, border_color="black")
        modificar_frame.place(relwidth=1, relheight=1)
        
        ctk.CTkLabel(modificar_frame, text="Código del Medicamento a Modificar:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryCodigoModificar = ctk.CTkEntry(modificar_frame, placeholder_text="Código", width=200, height=30)
        self.entryCodigoModificar.pack(pady=10)
        
        self.entryNombreMod = ctk.CTkEntry(modificar_frame, placeholder_text="Nombre", width=200, height=30)
        self.entryNombreMod.pack(pady=5)
        
        self.entryViaAdmMod = ctk.CTkEntry(modificar_frame, placeholder_text="Vía de Administración", width=200, height=30)
        self.entryViaAdmMod.pack(pady=5)
        
        self.entryPresentacionMod = ctk.CTkEntry(modificar_frame, placeholder_text="Presentación", width=200, height=30)
        self.entryPresentacionMod.pack(pady=5)
        
        self.calendarFechaCadMod = Calendar(modificar_frame, date_pattern="yyyy-mm-dd")
        self.calendarFechaCadMod.pack(pady=10)
        
        boton_modificar = ctk.CTkButton(modificar_frame, text="Modificar Medicamento", command=self.modificar_medicamento)
        boton_modificar.pack(pady=10)

    def modificar_medicamento(self):
        codigo = self.entryCodigoModificar.get().strip()
        nombre = self.entryNombreMod.get().strip()
        via_adm = self.entryViaAdmMod.get().strip()
        presentacion = self.entryPresentacionMod.get().strip()
        fecha_cad = self.calendarFechaCadMod.get_date()

        if not codigo or not nombre or not via_adm or not presentacion:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE medicamento SET nombre = %s, via_adm = %s, presentacion = %s, fecha_cad = %s
                WHERE codigo = %s
            """, (nombre, via_adm, presentacion, fecha_cad, codigo))
            conn.commit()
            messagebox.showinfo("Éxito", "Medicamento modificado correctamente")
            self.load_medicamentos()
            self.clear_input_fields_mod()
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar medicamento: {e}")
        finally:
            conn.close()

    def create_tab_eliminar_medicamento(self):
        eliminar_frame = ctk.CTkFrame(self.tabview.tab("Eliminar Medicamento"), corner_radius=0, fg_color="lightgray", 
                                      border_width=1, border_color="black")
        eliminar_frame.place(relwidth=1, relheight=1)
        
        ctk.CTkLabel(eliminar_frame, text="Código del Medicamento a Eliminar:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryCodigoEliminar = ctk.CTkEntry(eliminar_frame, placeholder_text="Código", width=200, height=30)
        self.entryCodigoEliminar.pack(pady=10)
        
        boton_eliminar = ctk.CTkButton(eliminar_frame, text="Eliminar Medicamento", command=self.eliminar_medicamento)
        boton_eliminar.pack(pady=10)

    def eliminar_medicamento(self):
        codigo = self.entryCodigoEliminar.get().strip()

        if not codigo:
            messagebox.showerror("Error", "El código es obligatorio")
            return

        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM medicamento WHERE codigo = %s", (codigo,))
            conn.commit()
            messagebox.showinfo("Éxito", "Medicamento eliminado correctamente")
            self.load_medicamentos()
            self.entryCodigoEliminar.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar medicamento: {e}")
        finally:
            conn.close()

    def clear_input_fields(self):
        self.entryCodigo.delete(0, "end")
        self.entryNombre.delete(0, "end")
        self.entryViaAdm.delete(0, "end")
        self.entryPresentacion.delete(0, "end")

    def clear_input_fields_mod(self):
        self.entryCodigoModificar.delete(0, "end")
        self.entryNombreMod.delete(0, "end")
        self.entryViaAdmMod.delete(0, "end")
        self.entryPresentacionMod.delete(0, "end")

    def back_to_main(self):
        self.destroy()
        if self.rol == "A":
            admin.MainApp(self.nombre,self.rol)
        else:
            empleadosadmin.MainApp(self.nombre, self.rol)

if __name__ == "__main__":
    app = Medicamento()
    app.mainloop()
