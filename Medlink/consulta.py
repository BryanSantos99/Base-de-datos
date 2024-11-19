import customtkinter as ctk
from tkcalendar import Calendar
from tkinter import messagebox, ttk
import conecta
import empleadosadmin
from fpdf import FPDF
from datetime import datetime
import random
import doctoresadmin

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
        agregar_frame = ctk.CTkScrollableFrame(self.tabview.tab("Agregar Consulta"), corner_radius=0, fg_color="lightgray", 
                                     border_width=1, border_color="black")
        agregar_frame.place(relwidth=1, relheight=1)
        
        ctk.CTkLabel(agregar_frame, text="Crear consulta:", font=("Arial", 14), text_color="black").pack(pady=10)
        
        ctk.CTkLabel(agregar_frame, text="Id De la cita:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.entryCita = ctk.CTkEntry(agregar_frame, placeholder_text="ID Paciente", width=200, height=30)
        self.entryCita.pack(pady=5)
        
        ctk.CTkLabel(agregar_frame, text="Seleccione Medicamento:", font=("Arial", 14), text_color="black").pack(pady=10)
        self.medicamento_combobox = ttk.Combobox(agregar_frame, values=self.get_medicamentos())
        self.medicamento_combobox.set("Seleccione Medicamento")
        self.medicamento_combobox.pack(pady=5)
        
 
        boton_agregar_medicamento = ctk.CTkButton(agregar_frame, text="Agregar Medicamento", command=self.agregar_medicamento)
        boton_agregar_medicamento.pack(pady=10)

    
        self.lista_medicamentos = ttk.Treeview(agregar_frame, columns=("Medicamento"), show="headings", height=8)
        self.lista_medicamentos.heading("Medicamento", text="Medicamento")
        self.lista_medicamentos.pack(pady=10)

       
        boton_eliminar_medicamento = ctk.CTkButton(agregar_frame, text="Eliminar Medicamento", command=self.eliminar_medicamento)
        boton_eliminar_medicamento.pack(pady=10)
            
        boton_agregar = ctk.CTkButton(agregar_frame, text="Agregar Consulta", command=self.agregar_consulta)
        boton_agregar.pack(pady=10)


    def agregar_medicamento(self):
        medicamento = self.medicamento_combobox.get()
        medicamentos = [self.lista_medicamentos.item(item, 'values')[0] for item in self.lista_medicamentos.get_children()]
        if not medicamento or medicamento == "Seleccione Medicamento":
            messagebox.showerror("Error", "Seleccione un Medicamento.")
            return
        for m in medicamentos:
            if m in medicamento:
                messagebox.showerror("Error", "Medicamento Duplicado.")
                return
        self.lista_medicamentos.insert("", "end", values=(medicamento))

    def eliminar_medicamento(self):
        selected_item = self.lista_medicamentos.selection()
        if selected_item:
            self.lista_medicamentos.delete(selected_item)
        else:
            messagebox.showerror("Error", "Seleccione un medicamento para eliminar.")
        
    def get_medicamentos(self):
            meds=[]
            try:
                conn = conecta.conectar()
                cursor = conn.cursor()
                cursor.execute("SELECT nombre, via_adm, presentacion FROM medicamento")
                medicamentos = cursor.fetchall()
                conn.close()
                for med in medicamentos:
                    strin=" ".join(med)
                    meds.append(strin)
                return meds
            except Exception as e:
                messagebox.showerror("Error", "Error al cargar medicamentos.")
                print(f"Error al cargar medicamentos: {e}")
                return []

    def agregar_consulta(self):
        cita = self.entryCita.get()
        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM cita WHERE id_cita = {cita}")
            datos_cita = cursor.fetchone()
            print(cita)
            conn.close()

            if datos_cita:
                paciente_id = datos_cita[1]
                medico_id = datos_cita[2]
                fecha = datos_cita[3]
                hora = datos_cita[4]
            else:
                messagebox.showerror("Error", "Paciente no encontrado.")
                return
        except Exception as e:
            messagebox.showerror("Error", "Error al cargar datos del paciente.")
            print(f"Error al cargar datos del paciente: {e}")
            return
        
        medicamento = self.medicamento_combobox.get()
        medicamentos = [self.lista_medicamentos.item(item, 'values')[0] for item in self.lista_medicamentos.get_children()]
        print(medicamentos)
        meds=""
        if not cita or medicamento == "Seleccione Medicamento":
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        for med in medicamentos:
            meds+=","+med
        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO consulta (paciente_id, doctor_id, fecha, diagnostico)
                VALUES (%s, %s, %s, %s)
            """, (paciente_id, medico_id, fecha, f"{meds}"))
            conn.commit()
            messagebox.showinfo("Éxito", "Consulta agregada correctamente")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar la consulta: {e}")
        finally:
            self.generar_factura(paciente_id,medico_id,fecha,hora)
            conn.close()
            self.clear_input_fields()
        
       

        
    def generar_factura(self,p,me,f,h):
        
        medicamentos = [self.lista_medicamentos.item(item, 'values')[0] for item in self.lista_medicamentos.get_children()]
        meds=[]
        try:
                
                
                for med in medicamentos:
                    conn = conecta.conectar()
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT nombre, via_adm, presentacion FROM medicamento WHERE nombre LIKE '%{med}%'")
                    medicamento = cursor.fetchone()
                    meds.append(medicamento)
                conn.close()
                
        except Exception as e:
                messagebox.showerror("Error", "Error al cargar medicamentos.")
                print(f"Error al cargar medicamentos: {e}")

  
        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute(f"SELECT nombre FROM paciente WHERE codigo = {p}")
            datos_paciente = cursor.fetchone()
            conn.close()

            if datos_paciente:
                nombre_cliente = datos_paciente[0]
            else:
                messagebox.showerror("Error", "Paciente no encontrado.")
                return
        except Exception as e:
            messagebox.showerror("Error", "Error al cargar datos del paciente.")
            print(f"Error al cargar datos del paciente: {e}")
            return
        try:
            conn = conecta.conectar()
            cursor = conn.cursor()
            cursor.execute(f"SELECT nombre FROM doctor WHERE codigo = {me}")
            datos_doctor = cursor.fetchone()
            conn.close()

            if datos_doctor:
                nombre_doctor = datos_doctor[0]
            else:
                messagebox.showerror("Error", "Doctor no encontrado.")
                return
        except Exception as e:
            messagebox.showerror("Error", "Error al cargar datos del Doctor.")
            print(f"Error al cargar datos del doctor: {e}")
            return

        identificador_factura = random.randint(10000, 99999)

        pdf = FPDF()
        pdf.add_page()

        logo_path = 'img/logo.png'
        pdf.image(logo_path, x=160, y=8, w=40)

        pdf.set_xy(10, 10)
        pdf.set_font('Arial', size=12)
        pdf.cell(0, 10, 'La salud es lo primero', ln=True)
        pdf.cell(0, 10, 'Calle #N30 CP 21020', ln=True)
        pdf.cell(0, 10, 'B32312312', ln=True)
        pdf.cell(0, 10, f'Fecha: {f}', ln=True)
        pdf.cell(0, 10, f'Hora: {h}', ln=True)

        pdf.ln(10)

        pdf.set_font('Arial', size=16)
        pdf.cell(0, 10, txt='RECETA', ln=True, align='C')

        pdf.set_font('Arial', size=12)
        pdf.cell(0, 10, f'Numero Receta: {identificador_factura}', ln=True, align='C')

        pdf.cell(0, 10, 'Datos del Doctor(a)', ln=True, align='L')
        pdf.cell(0, 10, f'Nombre: {nombre_doctor}', ln=True, align='L')
        
        pdf.set_font('Arial', size=12)
        pdf.cell(0, 10, '------------------------------------', ln=True, align='L')

        pdf.cell(0, 10, 'Datos del Paciente', ln=True, align='L')
        pdf.cell(0, 10, f'Nombre: {nombre_cliente}', ln=True, align='L')

        

        pdf.cell(0, 10, '---------------------------------', ln=True, align='L')
        pdf.cell(0, 10, 'Detalles de la consulta', ln=True, align='L')
        pdf.cell(160, 10, 'Nombre del Medicamento | via de Administracion | Tipo presentacion :', border=1,ln=True)

      
        for m in meds:
            strr=" | ".join(m)
            pdf.cell(160,10,strr, border=1, ln=True)
        


        pdf.cell(0, 10, '================================================', ln=True, align='L')
        pdf.cell(0, 10, 'Que se alivie pronto!', ln=True, align='C')

        pdf_file = f'recetas/Factura_{nombre_cliente+str(identificador_factura)}.pdf'
        pdf.output(pdf_file, 'F')

    def clear_input_fields(self):
        self.entryCita.delete(0, "end")
        self.medicamento_combobox.set("Seleccione Medicamento")
        self.lista_medicamentos.delete(*self.lista_medicamentos.get_children())

    def back_to_main(self):
        self.destroy()
        if self.rol=='E':
            empleadosadmin.MainApp(self.nombre, self.rol)
        else:
            doctoresadmin.MainApp(self.nombre, self.rol)


if __name__ == "__main__":
    app = Consultas("admin", "A")
    app.mainloop()
