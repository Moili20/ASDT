import tkinter as tk
import random
import time
import threading
import winsound

# Sanakirja maailmanennätysajoille ja leijonille
maailmanennatykset = {
    1920: {'aika': 10.6, 'nimi': 'Charlie Paddock'},
    1930: {'aika': 10.3, 'nimi': 'Percy Williams'},
    1988: {'aika': 9.79, 'nimi': 'Ben Johnson'},
    2009: {'aika': 9.58, 'nimi': 'Usain Bolt'},
}

leijonat = {
    "Simba": 8.2,
    "Nala": 8.5,
    "Mufasa": 7.9,
    "Scar": 8.7,
    "Kiara": 8.4,
}

# Juoksijoiden ominaisuudet
ernesti_speed = random.uniform(10.0, 15.0)  # Satunnainen aika Ernestin juoksulle
kernesti_speed = random.uniform(10.0, 15.0)  # Satunnainen aika Kernestin juoksulle

# Tkinter käyttöliittymä
root = tk.Tk()
root.title("Ernestin ja Kernestin Juoksu")

# Canvas-komponentti juoksijoiden piirtämiseksi
canvas = tk.Canvas(root, width=600, height=200, bg="white")
canvas.pack(pady=20)

# Piirretään lähtö- ja maaliviivat
canvas.create_line(50, 50, 50, 150, fill="black", width=5)  # Lähtöviiva
canvas.create_line(550, 50, 550, 150, fill="black", width=5)  # Maaliviiva

# Piirretään juoksijat
ernesti_shape = canvas.create_oval(30, 90, 70, 130, fill="blue")  # Ernesti
kernesti_shape = canvas.create_oval(30, 140, 70, 180, fill="red")  # Kernesti

# Juoksuanimaatiofunktiot
def juokse_ernesti():
    return run_simulation("Ernesti", ernesti_speed, ernesti_shape, 100, 100)

def juokse_kernesti():
    return run_simulation("Kernesti", kernesti_speed, kernesti_shape, 1100, 50)

def run_simulation(name, speed, shape, frequency, duration):
    progress = 0
    step = 500 / speed  # Mitä nopeampi, sitä suurempi askel (500 on viivan pituus)
    
    start_time = time.time()  # Start time for the runner
    
    while progress < 500:
        progress += step
        canvas.move(shape, step, 0)  # Liikutetaan juoksijaa x-akselilla
        root.update()
        
        # Soitetaan ääni jokaisella askeleella
        winsound.Beep(frequency, duration)
        
        time.sleep(1)  # Animaatio päivittyy sekunnin välein

    end_time = time.time()  # End time for the runner
    total_time = end_time - start_time  # Calculate total time taken
    show_result(name, total_time)
    return total_time

def show_result(name, time_taken):
    result_label.config(text=f"{name} juoksi 100m aikaan {time_taken:.2f} sekuntia!")
    # Show the winner
    result_label.config(text=winner_text)

# Yhteislähtö-funktio
def yhteis_laukaisu():
    ernesti_thread = threading.Thread(target=lambda: juokse_ernesti())
    kernesti_thread = threading.Thread(target=lambda: juokse_kernesti())
    ernesti_thread.start()
    kernesti_thread.start()
    
    ernesti_thread.join()  # Wait for Ernesti to finish
    ernesti_time = juokse_ernesti()
    
    kernesti_thread.join()  # Wait for Kernesti to finish
    kernesti_time = juokse_kernesti()

    # Determine the winner
    if ernesti_time < kernesti_time:
        winner_text = "Ernesti voitti!"
    elif kernesti_time < ernesti_time:
        winner_text = "Kernesti voitti!"
    else:
        winner_text = "Tasapeli!"
        
    result_label.config(text=winner_text)

# Käyttöliittymän komponentit
ernesti_button = tk.Button(root, text="Juokse Ernesti!", command=lambda: threading.Thread(target=juokse_ernesti).start())
ernesti_button.pack(pady=10)

kernesti_button = tk.Button(root, text="Juokse Kernesti!", command=lambda: threading.Thread(target=juokse_kernesti).start())
kernesti_button.pack(pady=10)

# Yhteislähtöpainike
yhteis_laukaisu_button = tk.Button(root, text="Yhteis Laukaisu!", command=lambda: threading.Thread(target=yhteis_laukaisu).start())
yhteis_laukaisu_button.pack(pady=10)

result_label = tk.Label(root, text="")
result_label.pack(pady=10)

root.mainloop()