import customtkinter as ctk
from PIL import Image, ImageTk
import main_app
import psycopg2 as db

class Citas(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.geometry("400x500")
        self.title("MedLink")
        self.attributes("-fullscreen", True)
        
        try:
            self.logo_image = Image.open("img/logo.png").resize((85, 85))
            self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        except FileNotFoundError:
            print("Error: La imagen 'logo.png' no se encontró en la carpeta.")
            self.logo_photo = None
            
        self.setup_widgets()

    def back_to_main(self):
        self.destroy()
        main_app.MainApp()

    def setup_widgets(self):
        header_frame = ctk.CTkFrame(self, height=90, corner_radius=0, fg_color="#1f6aa5")
        header_frame.place(relwidth=1.0, relx=0.5, rely=0.0, anchor='n')
        
        buttonBack = ctk.CTkButton(header_frame, text="Volver", width=100, height=30, fg_color="black", text_color="white", font=("Arial", 14), command=self.back_to_main)
        buttonBack.place(relx=0.85, rely=0.5, anchor="center")
        
        header_label = ctk.CTkLabel(header_frame, text="MedLink", font=("Arial", 24), text_color="white")
        header_label.place(relx=0.15, rely=0.5, anchor="center")
        
        header_label = ctk.CTkLabel(header_frame, text="Citas", font=("Arial", 34), text_color="white")
        header_label.place(relx=0.5, rely=0.5, anchor="center")

        logo_label = ctk.CTkLabel(header_frame, image=self.logo_photo, text="")
        logo_label.place(relheight=1,relx=0.93, rely=0.5, anchor="w")
        
        tabview = ctk.CTkTabview(self,fg_color="white")
        tabview.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.89)
        
        tabview.add("Citas")
        tabview.add("Agregar Cita")
        tabview.add("Eliminar Cita")
        tabview.add("Modificar Cita")
        
        self.citas_frame = ctk.CTkScrollableFrame(tabview.tab("Citas"), corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.citas_frame.place(relwidth=1, relheight=1)
        
        self.agregar_cita_frame = ctk.CTkScrollableFrame(tabview.tab("Agregar Cita"), corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.agregar_cita_frame.place(relwidth=1, relheight=1)
        
        self.eliminar_cita_frame = ctk.CTkScrollableFrame(tabview.tab("Eliminar Cita"), corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.eliminar_cita_frame.place(relwidth=1, relheight=1)
        
        self.modificar_cita_frame = ctk.CTkScrollableFrame(tabview.tab("Modificar Cita"), corner_radius=0, fg_color="lightgray",border_width=1,border_color="black")
        self.modificar_cita_frame.place(relwidth=1, relheight=1)

if __name__ == "__main__":
    citas = Citas()
    citas.mainloop()
