import customtkinter as ctk
from PIL import Image, ImageTk
import app
import empleados
import pacientes
import doctores
import citas

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

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
            
        self.setup_widgets()

   
   
    def cerrar_sesion(self):
        print("cerrar sesion")
        self.destroy()
        login_window = app.LoginApp()
        login_window.mainloop()
        
    
    def setup_widgets(self):
      
        header_frame = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#1f6aa5")
        header_frame.place(relwidth=1.0, relx=0.5, rely=0.0, anchor='n')
        

        header_label = ctk.CTkLabel(header_frame, text="MedLink", font=("Arial", 24), text_color="white")
        header_label.place(relx=0.15, rely=0.5, anchor="center")
        
        header_label = ctk.CTkLabel(header_frame, text="Inicio", font=("Arial", 34), text_color="white")
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        logo_label = ctk.CTkLabel(header_frame, image=self.logo_photo, text="")
        logo_label.place(relheight=1,relx=0.93, rely=0.5, anchor="w")
        
        header_img = ctk.CTkFrame(self, height=300,width=300, corner_radius=0, fg_color="#1f6aa5")
        header_img.place(relx=0.39, rely=0.60)

        logo_main = ctk.CTkLabel(header_img, image=self.header_photo, text="")
        logo_main.place(relheight=1, rely=0.5, relx=.5, anchor="center")
        
        self.crear_boton(0.2, 0.4, "Pacientes",self.logo_photo,self.abrir_pacientes)
        self.crear_boton(0.4, 0.4, "Citas",self.logo_photo,self.abrir_citas)
        self.crear_boton(0.6, 0.4, "Empleados",self.logo_photo,self.abrir_empleados)
        self.crear_boton(0.8, 0.4, "Doctores",self.logo_photo,self.abrir_doctores)
        self.crear_boton(0.95, 0.16, "Cerrar Sesion",None,self.cerrar_sesion)

    def crear_boton(self, x, y, nombre,image,com):
        button = ctk.CTkButton(
            self, 
            text=nombre, 
            image=image, 
            compound="right", 
            width=100, 
            height=90,
            command=com
        )
        button.place(relx=x, rely=y, anchor="center")
    
    def abrir_pacientes(self):
        self.destroy()
        pacientes.Pacientes()
        
    def abrir_empleados(self):
        self.destroy()
        empleados.Empleados()
    
    def abrir_doctores(self):
        self.destroy()
        doctores.Doctores()
        
    def abrir_citas(self):
        self.destroy()
        citas.Citas()
        

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
