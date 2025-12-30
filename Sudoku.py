from random import shuffle, randint, seed, choice
from datetime import date
import tkinter as tk
from time import sleep


class Sudoku:
    def __init__(self):
        self.sudoku = self.create_sudoku()
        self.task = []
        self.pattern = []

    def create_sudoku(self):
        """Генерирует случайную судоку и перемешивает строки/блоки."""

        # базовая строка 1–9
        base_row = [i + 1 for i in range(9)]
        shuffle(base_row)

        sudoku = []
        for _ in range(3):
            for _ in range(3):
                sudoku.append(base_row.copy())
                for _ in range(3):
                    base_row.append(base_row.pop(0))
            base_row.append(base_row.pop(0))

        # перемешивания
        sudoku = self.rows_in_thirds_shuffle(sudoku)
        sudoku = self.thirds_rows_shuffle(sudoku)

        # поворот на 90° (1 или 3 раза)
        for _ in range(randint(1, 2) * 2 - 1):
            sudoku = [list(row) for row in zip(*sudoku[::-1])]

        # превращаем в одномерный список
        flat = [n for row in sudoku for n in row]
        return flat

    def rows_in_thirds_shuffle(self, sudoku):
        """Перемешивает строки внутри каждой тройки."""
        for i in range(0, 9, 3):
            part = sudoku[i:i + 3]
            shuffle(part)
            sudoku[i:i + 3] = part.copy()
        return sudoku

    def thirds_rows_shuffle(self, sudoku):
        """Перемешивает блоки строк по три."""
        blocks = [sudoku[i:i + 3] for i in range(0, 9, 3)]
        shuffle(blocks)
        return [row for block in blocks for row in block]

    def compli(self, level):
        """Прячет клетки в зависимости от уровня сложности."""
        self.pattern = ["-" for _ in range(81)]

        for _ in range(level * 5 + 7):
            idx = randint(0, 80)
            while self.pattern[idx] == "?":
                idx = randint(0, 80)
            self.pattern[idx] = "?"

        self.task = [
            " " if self.pattern[i] == "?" else self.sudoku[i]
            for i in range(81)
        ]

    def __str__(self):
        res = ""
        for i in range(len(self.sudoku)):
            res += str(self.sudoku[i])+"  "
            if (i + 1) % 9 == 0:
                res += "\n\n"
        return res

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", color='#A99CCD', **kwargs): # '#ABABFF' is COLOR_ACCENT, lol
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg = self["fg"]

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _clear_placeholder(self, event=None):
        if self["fg"] == self.placeholder_color:
            self.delete(0, tk.END)
            self["fg"] = self.default_fg

    def _add_placeholder(self, event=None):
        if not self.get():
            self.insert(0, self.placeholder)
            self["fg"] = self.placeholder_color

def difficulty_setup():
    d = date.today()
    d2 = d.strftime("%d.%m")

    # 29 февраля
    if d2 == '29.02':
        level = 10
        
    # конец года
    elif d2 == '31.12':
        level = 9
        
    # конец месяца
    elif d2 in ('31.01', '28.02', '31.03', '30.04', '31.05', '30.06', '31.07', '31.08', '30.09', '31.10', '30.11'):
        level = 8
        
    # дни недели
    elif d.strftime("%A") == 'Sunday':
        level = 7
    elif d.strftime("%A") == 'Saturday':
        level = 6
    elif d.strftime("%A") == 'Friday':
        level = 5
    elif d.strftime("%A") == 'Thursday':
        level = 4
    elif d.strftime("%A") == 'Wednesday':
        level = 3
    elif d.strftime("%A") == 'Tuesday':
        level = 2
    elif d.strftime("%A") == 'Monday':
        level = 1

    return level

def varriables_and_tk_setup(manual):
    global COLOR_BG
    global COLOR_FG
    global COLOR_ACCENT
    global COLOR_BG2
    
    COLOR_BG = '#E6D1F2'
    COLOR_FG = '#9489B1'
    COLOR_ACCENT = '#A99CCD'
    COLOR_BG2 = '#C3B1E1'

    global root
    
    root = tk.Tk()
    root.title("Daily Sudoku")
    root.geometry("3000x3000")
    root.configure(bg=COLOR_BG)

    if manual == 0:
        title = tk.Label(root, text="Daily Sudoku:", font=("Noita Blackletter", 130))
    else:
        title = tk.Label(root, text="Manual Sudoku:", font=("Noita Blackletter", 130))
    title.configure(bg=COLOR_BG, fg=COLOR_FG)
    title.place(relx=0.5, rely=0, anchor="n")

def highlight(number):
    # перевод в интеджер
    try:
        number = int(number)
    except ValueError:
        pass

    # проверка на количество цифр (если 9)
    numbers = [0] * 9
    for i in sudoku:
        if isinstance(i, tk.Entry):
            try:
                if 0 < int(i.var.get()) and int(i.var.get()) < 10:
                    numbers[int(i.var.get())-1] += 1
                else:
                    int('a')
            except ValueError:
                pass
        else:
            numbers[i.number-1] += 1

    for i in range(len(numbers)):
        if numbers[i] == 9:
            buttons[i].configure(bg=COLOR_BG2, fg=COLOR_FG)
        else:
            buttons[i].configure(bg=COLOR_BG, fg=COLOR_FG)

    # подсветка номеров
    for i in range(len(sudoku)):
        val = None
        if isinstance(sudoku[i], tk.Entry):
            try:
                val = int(sudoku[i].var.get())
            except ValueError:
                pass

        if getattr(sudoku[i], "number", None) == number or val == number:
            sudoku[i].configure(bg=COLOR_ACCENT)
        else:
            if i in (3, 4, 5, 12, 13, 14, 21, 22, 23, 27, 28, 29, 33, 34, 35, 36, 37, 38, 42, 43, 44, 45, 46, 47, 51, 52, 53, 57, 58, 59, 66, 67, 68, 75, 76, 77):
                sudoku[i].configure(bg=COLOR_BG)
            else:
                sudoku[i].configure(bg=COLOR_BG2)

def buttons_setup():
    # цифры
    global buttons
    buttons = []
    for i in range(9):
        button = tk.Button(
            root, text=i+1, font=("Noita Blackletter", 40),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=lambda n=i+1: highlight(number=n)
        )
        button.number = i+1
        button.place(relx=0.8, rely=i/10+0.1, anchor='w', relwidth=0.1, relheight=0.08)
        buttons.append(button)

    # управление
    global check_button
    check_button = tk.Button(
            root, text='Ready', font=("Noita Blackletter", 40),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=check
    )
    check_button.place(relx=0.2, rely=0.1, anchor='e', relwidth=0.1, relheight=0.08)
    
    tk.Button(
            root, text='Clear all', font=("Noita Blackletter", 40),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=clear
    ).place(relx=0.2, rely=0.2, anchor='e', relwidth=0.1, relheight=0.08)
    
    global num_size
    num_size = True
    tk.Button(
            root, text='Number size', font=("Noita Blackletter", 35),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=swich
    ).place(relx=0.2, rely=0.3, anchor='e', relwidth=0.1, relheight=0.08)

def check():
    global win
    
    for i in range(len(sudoku)):
        if isinstance(sudoku[i], tk.Entry):
            if sudoku[i].var.get() != str(s.sudoku[i]):
                return
                
    global check_button
    if not win:
        check_button.place_forget()

    check_button = tk.Label(
            root, text='You Won', font=("Noita Blackletter", 40),
            bg=COLOR_FG, fg=COLOR_BG
    ).place(relx=0.2, rely=0.1, anchor='e', relwidth=0.1, relheight=0.08)
    win = True

def clear():
    for i in sudoku:
        if isinstance(i, tk.Entry):
            i.delete(0, tk.END)

def swich():
    global num_size
    num_size = not num_size

    for i in sudoku:
        if isinstance(i, tk.Entry):
            if num_size:
                i.configure(font=("Noita Blackletter", 40))
            else:
                i.configure(font=("Noita Blackletter", 25))

def make_sudoku(level):
    global s
    s = Sudoku()
    s.compli(level)

def build():
    # квадраты 3 на 3
    l1 = tk.Label(root)
    l1.configure(bg=COLOR_BG2)
    l1.place(relx=0.345, rely=0.25, relwidth=0.105, relheight=0.204)
    
    l2 = tk.Label(root)
    l2.configure(bg=COLOR_BG2)
    l2.place(relx=0.548, rely=0.25, relwidth=0.105, relheight=0.204)
    
    l3 = tk.Label(root)
    l3.configure(bg=COLOR_BG2)
    l3.place(relx=0.345, rely=0.65, relwidth=0.105, relheight=0.204)
    
    l4 = tk.Label(root)
    l4.configure(bg=COLOR_BG2)
    l4.place(relx=0.548, rely=0.65, relwidth=0.105, relheight=0.204)
    
    l5 = tk.Label(root)
    l5.configure(bg=COLOR_BG2)
    l5.place(relx=0.448, rely=0.45, relwidth=0.102, relheight=0.204)

    # само судоку
    global sudoku
    sudoku = []
    for i in range(len(s.sudoku)):
        if s.task[i] == s.sudoku[i]:
            label = tk.Label(root, text=s.sudoku[i], font=("Noita Blackletter", 40))
            label.number = s.sudoku[i]
        else:
            label_var = tk.StringVar()
            label = tk.Entry(root, textvariable=label_var, font=("Noita Blackletter", 40), justify='center')
            label.var = label_var
            label.number = None
            # Привязываем trace для подсветки
            label_var.trace_add("write", lambda *args, l=label: highlight(l.var.get()))
        label.configure(bg=COLOR_BG, fg=COLOR_FG)
        sudoku.append(label)

    for i in range(len(sudoku)):
        sudoku[i].place(relx=(i % 9) / 30 + 0.35, rely=int(i / 9) / 15 + 0.26, relwidth=0.03, relheight=0.05)

def tick():
    global timer
    global clock
    timer += 1
    minn = round(timer/60-0.5)
    secc = timer-minn*60

    if secc == 60:
        minn += 1
        secc = 0

    if len(str(minn)) == 1:
        minn = '0' + str(minn)
    if len(str(secc)) == 1:
        secc = '0' + str(secc)
    
    clock.config(text=str(f'Your time:\n{minn} : {secc}'))
    if not win:
        root.after(1000, tick)  # вызываем снова через секунду

def add_hint():
    global hints
    hints += 1

    global hint_counter
    hint_counter.config(text=str(f'Hints used: {hints}'))

def main(manual_level=0):
    global timer
    timer = 0
    global win
    win = False

    global hints
    hints = -1

    if manual_level == 0:
        seed(str(date.today()))
        level = difficulty_setup()
    else:
        seed()
        level = manual_level

    varriables_and_tk_setup(manual_level)
    global COLOR_BG
    global COLOR_FG
    global COLOR_ACCENT
    global COLOR_BG2
    
    make_sudoku(level)

    build()
    
    buttons_setup()

    highlight(1)

    global clock
    clock = tk.Label(
            root, text=timer, font=("Noita Blackletter", 35),
            bg=COLOR_BG2, fg=COLOR_FG
        )
    clock.place(relx=0.5, rely=0.92, anchor='center', relwidth=0.1, relheight=0.1)

    global hint_counter
    hint_counter = tk.Label(
            root, text='', font=("Noita Blackletter", 35),
            bg=COLOR_BG2, fg=COLOR_FG
        )
    hint_counter.place(relx=0.5, rely=0.2, anchor='center', relwidth=0.12, relheight=0.06)
    add_hint()

    tk.Button(
            root, text='Activate\nmanual sudoku', font=("Noita Blackletter", 28),
            bg=COLOR_BG2, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=restart
        ).place(relx=0.2, rely=0.4, anchor='e', relwidth=0.1, relheight=0.08)

    global manual_entry
    manual_entry = PlaceholderEntry(
            root, justify='center', font=("Noita Blackletter", 30),
            bg=COLOR_BG2, fg=COLOR_FG,
            placeholder='Level (1 - 10)'
        )
    manual_entry.place(relx=0.2, rely=0.5, anchor='e', relwidth=0.1, relheight=0.08)

    if manual_level != 0:
        tk.Button(
                root, text='Back to\ndaily sudoku', font=("Noita Blackletter", 28),
                bg=COLOR_BG, fg=COLOR_FG,
                activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
                command=back_to_daily
            ).place(relx=0.2, rely=0.6, anchor='e', relwidth=0.1, relheight=0.08)

    tk.Button(
            root, text='Hint', font=("Noita Blackletter", 35),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=give_hint
        ).place(relx=0.2, rely=0.7, anchor='e', relwidth=0.1, relheight=0.08)

    tk.Button(
            root, text='Quit the game', font=("Noita Blackletter", 32),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=root.destroy
        ).place(relx=0.2, rely=0.8, anchor='e', relwidth=0.1, relheight=0.08)

    tk.Label(
            root, text=f'Current level:\n{level}', font=("Noita Blackletter", 32),
            bg=COLOR_BG, fg=COLOR_FG
        ).place(relx=0.2, rely=0.9, anchor='e', relwidth=0.1, relheight=0.1)
    
    tick()

def restart():
    try:
        ml = int(manual_entry.get())
        if ml < 1 or ml > 10:
            return
    except ValueError:
        return

    root.destroy()
    main(manual_level=ml)

def back_to_daily():
    root.destroy()
    main()

def give_hint():
    for i in range(len(sudoku)):
        if isinstance(sudoku[i], tk.Entry):
            try:
                a = int(sudoku[i].get())
            except ValueError:
                a = 'a'
            if a != s.sudoku[i]:
                break
    else:
        return
    
    i = randint(0, 80)
    while True:
        if isinstance(sudoku[i], tk.Entry):
            try:
                a = int(sudoku[i].get())
            except ValueError:
                a = 'a'
            if a != s.sudoku[i]:
                break
            else:
                i = randint(0, 80)
        else:
            i = randint(0, 80)
            
    sudoku[i].delete(0, tk.END)
    sudoku[i].insert(0, s.sudoku[i])
    add_hint()

# print(date.today().strftime("%A"))
if __name__ == "__main__":
    main()
