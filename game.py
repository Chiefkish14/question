import tkinter as tk
import random
import time
import math

GIRL_NAME = "Damini"
QUESTION = f"Will you be my Valentine, {GIRL_NAME}?"
YES_TEXT = "Yes"
NO_TEXT = "No"

WIN_LINE_1 = "💘"
WIN_LINE_2 = "Yay. She said yes."
WIN_LINE_3 = f"Happy Valentine’s, {GIRL_NAME}."

W, H = 900, 540

YES_W, YES_H = 180, 54
NO_W, NO_H = 150, 50

ROUND_SECONDS = 25
TICK_MS = 35

YES_START_SPEED = 7.0
YES_END_SPEED = 2.8
NO_SPEED = 9.5

NO_DODGE_RADIUS = 200
NO_DODGE_STRENGTH = 3.2
YES_DODGE_RADIUS = 90
YES_DODGE_STRENGTH = 0.7

BG = "#fff6f8"
TEXT_DARK = "#111111"
TEXT_MID = "#555555"
TEXT_LIGHT = "#7a7a7a"

class Particle:
def __init__(self, canvas, x, y):
self.canvas = canvas
self.life = random.randint(18, 36)
self.id = canvas.create_text(
x, y,
text="♥",
font=("Helvetica", random.randint(10, 14)),
fill=random.choice(["#ff5a7a", "#ff8fa3", "#ffb3c1"]),
)
ang = random.random() * math.tau
spd = random.uniform(0.6, 2.2)
self.vx = math.cos(ang) * spd
self.vy = math.sin(ang) * spd - random.uniform(0.8, 1.8)

def step(self):
self.life -= 1
self.canvas.move(self.id, self.vx, self.vy)
self.vy += 0.06
if self.life <= 0:
self.canvas.delete(self.id)
return False
return True

class AestheticValentine:
def __init__(self, root):
self.root = root
root.title("question")
root.resizable(False, False)

self.canvas = tk.Canvas(root, width=W, height=H, bg=BG, highlightthickness=0)
self.canvas.pack()

self.scene = "intro"
self.particles = []
self.widgets = []

self.mouse_x, self.mouse_y = W//2, H//2
self.canvas.bind("<Motion>", self.on_mouse_move)
self.root.bind("<KeyPress-r>", lambda e: self.restart())

self.build_intro()
self.loop()

def clear(self):
self.canvas.delete("all")
for w in self.widgets:
try:
w.destroy()
except:
pass
self.widgets = []

def build_intro(self):
self.clear()
self.scene = "intro"

self.canvas.create_text(W//2, H//2 - 22,
text="Start the game",
font=("Helvetica", 30, "bold"),
fill=TEXT_DARK)

self.canvas.create_text(W//2, H//2 + 16,
text="(a tiny question for you)",
font=("Helvetica", 14),
fill=TEXT_LIGHT)

start_btn = tk.Button(
self.root,
text="Start",
font=("Helvetica", 14, "bold"),
command=self.start_game,
relief="solid", bd=1)

self.canvas.create_window(W//2, H//2 + 85, window=start_btn, width=140, height=46)
self.widgets.append(start_btn)

def start_game(self):
self.clear()
self.scene = "game"
self.running = True
self.start_time = time.time()

self.canvas.create_text(W//2, 70,
text=QUESTION,
font=("Helvetica", 26, "bold"),
fill=TEXT_DARK)

self.hud_id = self.canvas.create_text(W//2, 108,
text="",
font=("Helvetica", 12),
fill=TEXT_LIGHT)

self.msg_id = self.canvas.create_text(W//2, 150,
text="Catch one to answer.",
font=("Helvetica", 15),
fill=TEXT_MID)

self.play_top = 180
self.play_left = 24
self.play_right = W - 24
self.play_bottom = H - 24

self.yes_btn = tk.Button(self.root, text=YES_TEXT,
font=("Helvetica", 14, "bold"),
command=self.on_yes, relief="solid", bd=1)

self.no_btn = tk.Button(self.root, text=NO_TEXT,
font=("Helvetica", 13, "bold"),
command=self.on_no, relief="solid", bd=1)

self.yx, self.yy = 300.0, 350.0
self.nx, self.ny = 600.0, 350.0

self.yes_id = self.canvas.create_window(self.yx, self.yy,
window=self.yes_btn, width=YES_W, height=YES_H)

self.no_id = self.canvas.create_window(self.nx, self.ny,
window=self.no_btn, width=NO_W, height=NO_H)

self.widgets += [self.yes_btn, self.no_btn]

self.yvx, self.yvy = self.rand_vel(YES_START_SPEED)
self.nvx, self.nvy = self.rand_vel(NO_SPEED)

def build_win(self):
self.clear()
self.scene = "win"

self.canvas.create_text(W//2, H//2 - 60,
text=WIN_LINE_1,
font=("Helvetica", 44),
fill=TEXT_DARK)

self.canvas.create_text(W//2, H//2 - 10,
text=WIN_LINE_2,
font=("Helvetica", 22, "bold"),
fill=TEXT_DARK)

self.canvas.create_text(W//2, H//2 + 28,
text=WIN_LINE_3,
font=("Helvetica", 16),
fill=TEXT_MID)

def on_mouse_move(self, event):
self.mouse_x, self.mouse_y = event.x, event.y

def rand_vel(self, base_speed):
ang = random.random() * math.tau
spd = random.uniform(base_speed * 0.8, base_speed * 1.2)
return math.cos(ang) * spd, math.sin(ang) * spd

def clamp(self, x, y, w, h):
half_w = w / 2
half_h = h / 2
x = max(self.play_left + half_w, min(self.play_right - half_w, x))
y = max(self.play_top + half_h, min(self.play_bottom - half_h, y))
return x, y

def bounce(self, x, y, vx, vy, w, h):
half_w = w / 2
half_h = h / 2
nx, ny = x + vx, y + vy

if nx - half_w <= self.play_left or nx + half_w >= self.play_right:
vx = -vx
nx = x + vx
if ny - half_h <= self.play_top or ny + half_h >= self.play_bottom:
vy = -vy
ny = y + vy

nx, ny = self.clamp(nx, ny, w, h)
return nx, ny, vx, vy

def cap_speed(self, vx, vy, max_speed):
spd = math.sqrt(vx*vx + vy*vy)
if spd > max_speed and spd > 1e-6:
s = max_speed / spd
return vx * s, vy * s
return vx, vy

def dodge_force(self, ox, oy, radius, strength):
dx = ox - self.mouse_x
dy = oy - self.mouse_y
dist2 = dx*dx + dy*dy
if dist2 <= radius*radius and dist2 > 1e-6:
dist = math.sqrt(dist2)
push = strength * (1.0 - dist / radius)
return (dx / dist) * push, (dy / dist) * push
return 0.0, 0.0

def yes_speed_now(self):
elapsed = time.time() - self.start_time
t = min(1.0, elapsed / max(1.0, ROUND_SECONDS))
return YES_START_SPEED + (YES_END_SPEED - YES_START_SPEED) * t

def on_yes(self):
if self.scene != "game":
return
self.running = False
self.build_win()

def on_no(self):
if self.scene != "game" or not self.running:
return
self.canvas.itemconfig(self.msg_id, text="Try again.", fill=TEXT_MID)
self.nx = random.randint(int(self.play_left + NO_W/2), int(self.play_right - NO_W/2))
self.ny = random.randint(int(self.play_top + NO_H/2), int(self.play_bottom - NO_H/2))
self.canvas.coords(self.no_id, self.nx, self.ny)

def restart(self):
self.build_intro()

def loop(self):
self.particles = [p for p in self.particles if p.step()]

if self.scene == "game":
elapsed = int(time.time() - self.start_time)
remaining = max(0, ROUND_SECONDS - elapsed)
self.canvas.itemconfig(self.hud_id, text=f"Time left: {remaining}s")

if remaining == 0 and self.running:
self.running = False
self.canvas.itemconfig(self.msg_id, text="Time’s up. Click Yes 🙂", fill="#b00020")
self.yvx = self.yvy = 0.0
self.nvx = self.nvy = 0.0
self.yx, self.yy = self.clamp(W/2, (self.play_top + self.play_bottom)/2, YES_W, YES_H)
self.canvas.coords(self.yes_id, self.yx, self.yy)

if self.running:
yd_x, yd_y = self.dodge_force(self.yx, self.yy, YES_DODGE_RADIUS, YES_DODGE_STRENGTH)
self.yvx += yd_x
self.yvy += yd_y
self.yvx, self.yvy = self.cap_speed(self.yvx, self.yvy, self.yes_speed_now() * 1.6)

nd_x, nd_y = self.dodge_force(self.nx, self.ny, NO_DODGE_RADIUS, NO_DODGE_STRENGTH)
self.nvx += nd_x
self.nvy += nd_y
self.nvx, self.nvy = self.cap_speed(self.nvx, self.nvy, NO_SPEED * 1.9)

self.yx, self.yy, self.yvx, self.yvy = self.bounce(self.yx, self.yy, self.yvx, self.yvy, YES_W, YES_H)
self.nx, self.ny, self.nvx, self.nvy = self.bounce(self.nx, self.ny, self.nvx, self.nvy, NO_W, NO_H)

self.canvas.coords(self.yes_id, self.yx, self.yy)
self.canvas.coords(self.no_id, self.nx, self.ny)

if random.random() < 0.45:
self.particles.append(Particle(self.canvas,
self.yx + random.randint(-6, 6),
self.yy + random.randint(-6, 6)))

self.root.after(TICK_MS, self.loop)

if __name__ == "__main__":
root = tk.Tk()
AestheticValentine(root)
root.mainloop()