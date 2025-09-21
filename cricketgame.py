import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk   
import random
import winsound
import pyttsx3

player_runs = 0
player_wickets = 0
comp_runs = 0
comp_wickets = 0
balls = 0
total_balls = 12   
max_wickets = 2
inning = 1        

team_player = "India"
team_comp = "Pakistan"

commentary_list = [
    "What a shot!", "Excellent run!", "Oops, missed!",
    "Great delivery!", "Amazing strike!", "OUT!"
]

engine = pyttsx3.init()
voices = engine.getProperty("voices")
if len(voices) > 1:
    engine.setProperty("voice", voices[1].id)
else:
    engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 175)   
engine.setProperty("volume", 1)   

def speak(msg):
    engine.say(msg)
    engine.runAndWait()

def play_sound(effect):
    try:
        if effect == "cheer":
            winsound.PlaySound("sounds/crowd_cheer.wav", winsound.SND_ASYNC)
        elif effect == "wicket":
            winsound.PlaySound("sounds/wicket.wav", winsound.SND_ASYNC)
        elif effect == "bat":
            winsound.PlaySound("sounds/bat_hit.wav", winsound.SND_ASYNC)
    except:
        winsound.Beep(800, 200)

def balls_to_overs(balls):
    return f"{balls//6}.{balls%6}"

def update_score():
    scoreboard_label.config(
        text=f"{team_player}: {player_runs}/{player_wickets} | "
             f"{team_comp}: {comp_runs}/{comp_wickets} | "
             f"Overs: {balls_to_overs(balls)}/{total_balls//6}"
    )

def add_commentary(msg, speak_flag=True):
    commentary_box.config(state='normal')
    commentary_box.insert(tk.END, msg + "\n")
    commentary_box.yview(tk.END)
    commentary_box.config(state='disabled')
    if speak_flag:
        speak(msg)

def play_ball(run):
    global player_runs, player_wickets, comp_runs, comp_wickets, balls, inning
    comp_run = random.randint(1, 6)
    balls += 1
    if inning == 1:
        if run == comp_run:
            player_wickets += 1
            msg = f"WICKET! Pakistan bowled {comp_run}. {random.choice(commentary_list)}"
            add_commentary(msg)
            play_sound("wicket")
        else:
            player_runs += run
            msg = f"{team_player} scored {run}. Pakistan bowled {comp_run}. {random.choice(commentary_list)}"
            add_commentary(msg)
            play_sound("bat")
            if run == 6:
                play_sound("cheer")
        update_score()
        if balls == total_balls or player_wickets == max_wickets:
            messagebox.showinfo("End of Inning", f"{team_player} scored {player_runs}/{player_wickets}")
            speak(f"End of the first innings. {team_player} scored {player_runs} runs for {player_wickets} wickets.")
            start_second_inning()
    elif inning == 2:
        if run == comp_run:
            comp_wickets += 1
            msg = f"WICKET! You bowled {run}, {team_comp} scored {comp_run}. {random.choice(commentary_list)}"
            add_commentary(msg)
            play_sound("wicket")
        else:
            comp_runs += comp_run
            msg = f"{team_comp} scored {comp_run}. You bowled {run}. {random.choice(commentary_list)}"
            add_commentary(msg)
            play_sound("bat")
            if comp_run == 6:
                play_sound("cheer")
        update_score()
        if comp_runs > player_runs:
            end_game()
            return
        if balls == total_balls or comp_wickets == max_wickets:
            end_game()

def start_second_inning():
    global balls, inning
    balls = 0
    inning = 2
    target = player_runs + 1
    msg = f"----- Second Inning: You bowl, {team_comp} bats! Target is {target} -----"
    add_commentary(msg)

def end_game():
    if player_runs > comp_runs:
        msg = f"Game Over. {team_player} wins! {player_runs} vs {comp_runs}"
        play_sound("cheer")
    elif player_runs < comp_runs:
        msg = f"Game Over. {team_comp} wins! {comp_runs} vs {player_runs}"
        play_sound("cheer")
    else:
        msg = f"Game Over. It's a Tie! {player_runs} vs {comp_runs}"
    messagebox.showinfo("Game Over", msg)
    speak(msg)

def reset_game():
    global player_runs, player_wickets, comp_runs, comp_wickets, balls, inning
    player_runs = player_wickets = comp_runs = comp_wickets = balls = 0
    inning = 1
    commentary_box.config(state='normal')
    commentary_box.delete(1.0, tk.END)
    commentary_box.config(state='disabled')
    msg = f"----- First Inning: {team_player} bats! -----"
    add_commentary(msg, speak_flag=False)
    update_score()

root = tk.Tk()
root.title("India vs Pakistan - Ultimate Cricket Game")
root.geometry("700x550")
root.configure(bg="#3CB371")  

try:
    img = Image.open("sounds/cricket_logo.png")
    img = img.resize((200, 200))   
    logo_img = ImageTk.PhotoImage(img)

    logo_label = tk.Label(root, image=logo_img, bg="#3CB371")
    logo_label.image = logo_img   
    logo_label.pack(pady=5)
except:
    tk.Label(root, text="🏏 India vs Pakistan 🏏", font=("Helvetica", 20, "bold"),
             bg="#3CB371", fg="#006400").pack(pady=5)

scoreboard_label = tk.Label(root, text="", font=("Helvetica", 14),
                            bg="#FFFACD", fg="black", bd=3, relief="ridge")
scoreboard_label.pack(pady=10)
update_score()

commentary_box = scrolledtext.ScrolledText(root, width=75, height=15, state='disabled',
                                           font=("Helvetica", 10), bg="#F0FFF0", bd=3, relief="sunken")
commentary_box.pack(pady=10)
add_commentary(f"----- First Inning: {team_player} bats! -----", speak_flag=False)

button_frame = tk.Frame(root, bg="#3CB371")
button_frame.pack(pady=10)

for i in range(1, 7):
    btn = tk.Button(button_frame, text=str(i), width=5, height=2, font=("Helvetica", 12, "bold"),
                    bg="#FF8C00", fg="white", command=lambda i=i: play_ball(i))
    btn.grid(row=0, column=i - 1, padx=5)

reset_btn = tk.Button(root, text="Reset Game", width=15, bg="#FF4500", fg="white", font=("Helvetica", 12, "bold"),
                      command=reset_game)
reset_btn.pack(pady=10)

root.mainloop()
