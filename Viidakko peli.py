import tkinter as tk
import random
import math
import time
import winsound

#Tehdään viidakko
VIIDAKKO_SIZE = 100
viidakko = [[0 for _ in range(VIIDAKKO_SIZE) for _ in range(VIIDAKKO_SIZE)]]

#Tehdään Ernesti ja Kernesti
Ernesti = {
    "position":None,
    "id":None,
    
}

Kernesti = {
    "position":None,
    "id":None,
    
}

Leijonat = []
#Luodaan käyttöliittymä ja ikkuna
root = tk.Tk()
root.title("Ernestin ja Kernestin seikkailu")

canvas = tk.Canvas(root,width=800,height=800,bg="green")
canvas.pack(side=tk.LEFT)

text_id = canvas.create_text(400,20,text="",fill="white",font=("Arial",16))

ERNESTI_SYMBOL = "E"
KERNESTI_SYMBOL = "K"
LEIJONAT_SYMBOL = "L"

def  show_message(message):
    canvas.itemconfig(text_id,text=message)
    root.update()

def create_symbol(symbol, position):
    x, y = position
    return canvas.create_text(x * 8 + 4, y * 8 + 4, text=symbol, fill="white", font=("Arial", 12), anchor=tk.CENTER)
def update_position(character):
    x, y = character["position"]
    if character["id"]:
        canvas.coords(character["id"], x * 8 + 4, y * 8 + 4)

def move_character(character):
    x,y = character ["position"]
    direction = random.choice(['up','down','left','right'])
    if direction == 'up' and y < VIIDAKKO_SIZE - 1:
        y += 1

    elif direction == 'down' and y > 0:
        y -= 1

    elif direction == 'left' and y > 0:
        y -= 1

    elif direction == 'right' and y < VIIDAKKO_SIZE - 1:
        y += 1

    character["position"] = (x,y)
    update_position(character)

def distance(p1,p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def simulate_movement():
    while True:
        move_character(Ernesti)
        move_character(Kernesti)

        if distance(Ernesti["position"],Kernesti["position"]) <= 5:
            winsound.Beep(300,200)
            show_message("Vau ompa mukava nähdä taas")
            return "encounter"
        
        if not move_lions():
            return "lion"
        
        root.update()
        time.sleep(1)

def add_lion():
    lion = {
        "position":
            (random.randint(0,VIIDAKKO_SIZE - 1),random.randint(0,VIIDAKKO_SIZE - 1)),
        "id":
            None
    }

    lion["id"] = create_symbol(LEIJONAT_SYMBOL,lion["position"])
    Leijonat.append(lion)
    move_lions()

def move_lions():
    for lion in Leijonat:
        lx, ly = lion["position"]
        ex, ey = Ernesti["position"]
        kx, ky = Kernesti["position"]

        distance_to_ernesti = distance((lx,ly),(ex,ey))
        distance_to_kernesti = distance((lx,ly),(kx,ky))
        if distance_to_ernesti <= distance_to_kernesti:
            target = Ernesti

        else: target = Kernesti

        tx, ty = target["position"]
        if lx < tx:
            lx += 1

        elif lx > tx:
            lx -= 1

        if ly < ty:
            ly += 1

        elif ly > ty:
            ly -= 1    

        lion["position"] = (lx, ly)
        update_position(lion)
        
        if lion["position"] == target["position"]:
            show_message("Slurps, olipa hyvä ohjelmoija")
            return False
        
    return True
        
def drop_programmers():
    global Ernesti, Kernesti
    Ernesti["position"] = (random.randint(0, VIIDAKKO_SIZE - 1), random.randint(0, VIIDAKKO_SIZE - 1))
    Kernesti["position"] = (random.randint(0, VIIDAKKO_SIZE - 1), random.randint(0, VIIDAKKO_SIZE - 1))
    
    Ernesti["id"] = create_symbol(ERNESTI_SYMBOL, Ernesti["position"])
    Kernesti["id"] = create_symbol(KERNESTI_SYMBOL, Kernesti["position"])
    
    simulate_movement()

def simulate_once():
    # Pudotetaan ohjelmoijat ja leijona satunnaisiin sijainteihin
    Ernesti["position"] = (random.randint(0, VIIDAKKO_SIZE - 1), random.randint(0, VIIDAKKO_SIZE - 1))
    Kernesti["position"] = (random.randint(0, VIIDAKKO_SIZE - 1), random.randint(0, VIIDAKKO_SIZE - 1))
    lion = {
        "position": (random.randint(0, VIIDAKKO_SIZE - 1), random.randint(0, VIIDAKKO_SIZE - 1)),
        "id": None
    }

    while True:
        # Liikuta Ernestia ja Kernestiä
        move_character(Ernesti)
        move_character(Kernesti)
        
        # Tarkista, näkevätkö he toisensa
        if distance(Ernesti["position"], Kernesti["position"]) <= 5:
            return "encounter"
        
        # Liikuta leijonaa kohti lähintä kohdetta
        lx, ly = lion["position"]
        ex, ey = Ernesti["position"]
        kx, ky = Kernesti["position"]
        
        # Lasketaan etäisyydet seikkailijoihin
        distance_to_ernesti = distance((lx, ly), (ex, ey))
        distance_to_kernesti = distance((lx, ly), (kx, ky))
        
        # Valitaan lähin seikkailija
        if distance_to_ernesti <= distance_to_kernesti:
            target = Ernesti
        else:
            target = Kernesti
        
        tx, ty = target["position"]
        
        # Siirrä leijonaa kohti valittua seikkailijaa
        if lx < tx:
            lx += 1
        elif lx > tx:
            lx -= 1
        
        if ly < ty:
            ly += 1
        elif ly > ty:
            ly -= 1
        
        lion["position"] = (lx, ly)
        
        if lion["position"] == target["position"]:
            return "lion"
        
control_frame = tk.Frame(root)
control_frame.pack(side=tk.RIGHT, padx=20)

tk.Button(control_frame, text="Aloita peli", command=drop_programmers).pack(pady=10)
tk.Button(control_frame, text="Lisää leijona", command=add_lion).pack(pady=10)

root.mainloop()



