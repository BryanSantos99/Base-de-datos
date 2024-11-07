
import customtkinter as ctk
from PIL import Image, ImageTk
import admin
import empleadosadmin
import conecta
from tkinter import messagebox


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.geometry("400x500")
        self.title("MedLink")

        
        window_width = 400
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        self.resizable(False, False)

        try:
            self.logo_image = Image.open("img/logo.png").resize((60, 60))
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except FileNotFoundError:
            print("Error: La imagen 'logo.png' no se encontró en la carpeta.")
            self.logo_photo = None
        self.create_widgets()


    def create_widgets(self):
        header_frame = ctk.CTkFrame(self, width=400, height=50, corner_radius=0, fg_color="#1f6aa5")
        header_frame.place(relx=0.5, rely=0, anchor="n")

        header_label = ctk.CTkLabel(header_frame, text="Inicio de sesión", font=("Arial", 24), text_color="white")
        header_label.place(relx=0.22, rely=0.5, anchor="center")

        logo_label = ctk.CTkLabel(header_frame, image=self.logo_photo, text="")
        logo_label.place(relx=0.91, rely=0.5, anchor="center")

        usr_label = ctk.CTkLabel(self, text="Usuario:", font=("Arial", 14))
        usr_label.place(relx=0.5, rely=0.3, anchor="center")

        self.usr_entry = ctk.CTkEntry(master=self, placeholder_text="Usuario", width=200, height=35, corner_radius=10)
        self.usr_entry.place(relx=0.5, rely=0.37, anchor="center")

        psw_label = ctk.CTkLabel(self, text="Contraseña:", font=("Arial", 14))
        psw_label.place(relx=0.5, rely=0.45, anchor="center")

        self.psw_entry = ctk.CTkEntry(master=self, placeholder_text="Contraseña", show="*", width=200, height=35, corner_radius=10)
        self.psw_entry.place(relx=0.5, rely=0.52, anchor="center")

        login_button = ctk.CTkButton(master=self, text="Ingresar", command=self.button_event, width=100, height=35, corner_radius=10)
        login_button.place(relx=0.35, rely=0.65, anchor="center")

        cancel_button = ctk.CTkButton(master=self, text="Cancelar", command=self.cancel_event, width=100, height=35, corner_radius=10)
        cancel_button.place(relx=0.65, rely=0.65, anchor="center")
        
        
        
        change_theme = ctk.CTkLabel(self, text="Tema:", anchor="w")
        change_theme.place(relx=0.28, rely=0.95, anchor="center")
        cm=ctk.appearance_mode_optionemenu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"],command=self.change_theme)
        cm.place(relx=0.55, rely=0.95, anchor="center")

    def change_theme(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
    
    def button_event(self):
       
        nombre_usuario=""
    
        entered_psw = self.psw_entry.get()
        entered_user = self.usr_entry.get()

        admin="admin"
        con="12345"

        if entered_user == admin and entered_psw == con:
            nombre_usuario="admin"
            rol="A"
            self.open_main_app(nombre_usuario,rol)
        else:
            conn = conecta.conectar()
            cursor = conn.cursor()
        
            cursor.execute("SELECT nombre FROM empleado WHERE codigo=%s AND contraseña=%s", (int(entered_user), entered_psw))
            resultado = cursor.fetchone()

            
            if resultado:
                nombre_usuario = resultado[0]
                rol="E"
                self.mostrar_pantalla_empleado(nombre_usuario,rol)
                
            else:
                cursor.execute("SELECT nombre FROM doctor WHERE codigo=%s AND contraseña=%s", (int(entered_user), entered_psw))
                resultado = cursor.fetchone()
                if resultado:
                    nombre_usuario = resultado[0]
                    rol="E"
                    self.mostrar_pantalla_empleado(nombre_usuario,rol)
                else:
                    messagebox.showerror("Error", "Usuario o contraseña incorrectos")

            cursor.close()
            


    def open_main_app(self,n,r):
        self.destroy()
        mainApp = admin.MainApp(n,r)
        mainApp.mainloop()
        
    def mostrar_pantalla_empleado(self,n,r):
        self.destroy()
        empleadoApp = empleadosadmin.MainApp(n,r)
        empleadoApp.mainloop()

    def cancel_event(self):
        print("datos borrados")
        self.usr_entry.delete(0, 'end')  
        self.psw_entry.delete(0, 'end')

