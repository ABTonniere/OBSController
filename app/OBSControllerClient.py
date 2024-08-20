import customtkinter as ctk
import getmac
import asyncio
import json
import websockets



SERVER_IP = "127.0.0.1"
SERVER_PORT = 6059

message = { "id" : getmac.get_mac_address(),
    "data" : {
    "command" : "",
    "args" : ""
}}

class App(ctk.CTk):

    

    def __init__(self):
        super().__init__()

        self.title("OBS Controller")
        self.geometry("800x600")

        # Créer un conteneur pour les pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        # Configurer la grille de la fenêtre principale pour le redimensionnement
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Dictionnaire pour garder la trace des frames/pages
        self.frames = {}

        for F in (LoginPage, PannelPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame

            # Mettre toutes les pages à la même position (0, 0) et les faire s'étendre
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")


    def show_frame(self, page_name):
        '''Montrer un frame spécifique en fonction du nom de la page'''
        frame = self.frames[page_name]
        frame.tkraise()
        frame.on_show_sync()
    



###########################
#                         #
#         FRAMES          #
#                         #
###########################



class LoginPage(ctk.CTkFrame):



    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        

        # Configurer la grille pour que le contenu s'étende
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Titre de la page de connexion
        title_label = ctk.CTkLabel(self, text="Connexion", font=("Arial", 32, "bold"))
        title_label.grid(row=0, column=1, pady=20, sticky="n")

        # Champ du nom d'utilisateur avec icône
        username_icon = ctk.CTkLabel(self, text="👤", font=("Arial", 20))
        username_icon.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nom d'utilisateur")
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Bouton de connexion stylisé
        login_button = ctk.CTkButton(self, text="S'identifier", command=self.login_button_click, 
                                     fg_color="#1f6aa5", hover_color="#144e7a", 
                                     text_color="white", font=("Arial", 16, "bold"))
        login_button.grid(row=3, column=1, padx=10, pady=20, sticky="n")

    def on_show_sync(self):
        asyncio.run(self.on_show())

    async def on_show(self):

        #Verify if the user is already connected

        connected = False

        async with websockets.connect("ws://" + SERVER_IP + ":" + str(SERVER_PORT)) as websocket:

            message["data"]["command"] = "connected"
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            response = json.loads(response)

            if response == "Connected":
                connected = True
                print("Already connected")
                self.controller.show_frame("PannelPage")
            else:
                print("Not connected")
        

        # Get the username if connected
        if connected:
            async with websockets.connect("ws://" + SERVER_IP + ":" + str(SERVER_PORT)) as websocket:
                message["data"]["command"] = "getUsername"
                await websocket.send(json.dumps(message))
                response = await websocket.recv()
                response = json.loads(response)
                print("Username:", response)



    def login_button_click(self):
        asyncio.run(self.login())

    async def login(self):
        async with websockets.connect("ws://" + SERVER_IP + ":" + str(SERVER_PORT)) as websocket:

            message["data"]["command"] = "signUp"
            message["data"]["args"] = self.username_entry.get()

            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            response = json.loads(response)

            if response == "Signed up":
                print("Signed in successfully as", self.username_entry.get())
                self.controller.show_frame("PannelPage")

        




class PannelPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Configurer la grille pour que le contenu s'étende
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text="Bienvenue dans l'application !", font=("Arial", 24))
        self.label.grid(row=0, column=0, pady=20)

        logout_button = ctk.CTkButton(self, text="Quitter", command=lambda: controller.quit())
        logout_button.grid(row=1, column=0, pady=20)
    


    def on_show_sync(self):
        pass
        #asyncio.create_task(self.on_show())

    async def on_show(self):
        async with websockets.connect("ws://" + SERVER_IP + ":" + str(SERVER_PORT)) as websocket:

            message["data"]["command"] = "getUsername"
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            response = json.loads(response)
            self.label.configure(text="Bienvenue dans l'application, " + response)


###########################
#                         #
#          MAIN           #
#                         #
###########################



if __name__ == "__main__":
    print("Starting OBS Controller Client")
    app = App()
    app.mainloop()
