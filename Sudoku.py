from random import shuffle, randint, seed, choice
from datetime import date
import tkinter as tk
from time import sleep


class Sudoku:
    def __init__(self):
        """Делает судоку и хранит её в классе"""
        
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

        # поворот на 90° (1 - 3 раза)
        for _ in range(randint(1, 2) * 2 - 1):
            sudoku = [list(row) for row in zip(*sudoku[::-1])]

        # опять перемешивания
        sudoku = self.rows_in_thirds_shuffle(sudoku)
        sudoku = self.thirds_rows_shuffle(sudoku)

       # поворот на 90° (1 - 4 раза)
        for _ in range(randint(1, 4)):
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
        """Выводит судоку в оболочку. Это для разработчиков."""
        
        res = ""
        for i in range(len(self.sudoku)):
            res += str(self.sudoku[i])+"  "
            if (i + 1) % 9 == 0:
                res += "\n\n"
        return res

class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="", color='#FF0000', **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg = self["fg"]

        self.focus_on = False

        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)

        self._add_placeholder()

    def _clear_placeholder(self, event=None):
        self.focus_on = True
        if self["fg"] == self.placeholder_color:
            self.delete(0, tk.END)
            self["fg"] = self.default_fg

    def _add_placeholder(self, event=None):
        self.focus_on = False
        if not self.get():
            self.insert(0, self.placeholder)
            self["fg"] = self.placeholder_color

def difficulty_setup():
    d = date.today()
    d2 = d.strftime("%d.%m")
    d3 = d.strftime("%A")

    # 29 февраля
    if d2 == '29.02':
        level = 10
        
    # конец года
    elif d2 == '31.12':
        level = 9
        
    # конец месяца
    elif d2 in (
        '31.01', '28.02', '31.03', '30.04',
        '31.05', '30.06', '31.07', '31.08',
        '30.09', '31.10', '30.11'
    ):
        level = 8
        
    # дни недели
    elif d3 == 'Sunday':
        level = 7
    elif d3 == 'Saturday':
        level = 6
    elif d3 == 'Friday':
        level = 5
    elif d3 == 'Thursday':
        level = 4
    elif d3 == 'Wednesday':
        level = 3
    elif d3 == 'Tuesday':
        level = 2
    elif d3 == 'Monday':
        level = 1
        
    return level

def varriables_and_tk_setup(manual, color):
    global COLOR_BG
    global COLOR_FG
    global COLOR_ACCENT
    global COLOR_BG2
    
    COLOR_BG = [
        '#F0F5E1', '#E6D1F2',  # Надин и Анин
        "#1A1A1A", "#FFFFFF", "#0D0221", "#283618", "#0F172A", 
        "#ECEFF4", "#2D1B33", "#0B120B", "#1B1212", "#212529",
        "#121212", "#FDF6E3", "#002B36", "#2D3436", "#202020", # 13-17
        "#F8F0E3", "#141414", "#FFFFFF", "#1E1E2E", "#2B2B2B", # 18-22
        "#000000", "#FAF9F6", "#121212", "#F5F5DC", "#2C3E50", # 23-27
        "#16161D", "#FFFFFF", "#3C3633", "#0F0F0F", "#1A1B26",  # 28-32
        '#FFFFFF', '#000000', '#BBBBBB', '#555555', '#000000', # Мои
        '#CCCCFF'
    ]

    COLOR_FG = [
        '#5E7052', '#9489B1',  # Надин и Анин
        "#F8F9FA", "#212529", "#00FFC8", "#FEFAE0", "#F1F5F9", 
        "#2E3440", "#F1E9DA", "#E8F5E9", "#D4A373", "#F8F9FA",
        "#BB86FC", "#657B83", "#839496", "#DFE6E9", "#E0E0E0", # 13-17
        "#5D4037", "#FFFFFF", "#000000", "#CDD6F4", "#A9B7C6", # 18-22
        "#E0E0E0", "#2C3E50", "#03DAC6", "#4B3621", "#ECF0F1", # 23-27
        "#C5C8C6", "#333333", "#EEEDEB", "#00FF00", "#A9B1D6",  # 28-32
        '#000000', '#FFFFFF', '#555555', '#BBBBBB', '#FF0000', # Мои
        '#4444FF'
    ]

    COLOR_ACCENT = [
        '#8DA37E', '#A99CCD',  # Надин и Анин
        "#FA0754", "#007BFF", "#FF007F", "#BC6C25", "#38BDF8", 
        "#88C0D0", "#FF79C6", "#6A994E", "#A44A3F", "#ADB5BD",
        "#03DAC6", "#B58900", "#268BD2", "#FAB1A0", "#FFD700", # 13-17
        "#8D6E63", "#FF4500", "#6200EE", "#F5E0DC", "#CC7832", # 18-22
        "#CF6679", "#E74C3C", "#BB86FC", "#8B4513", "#E67E22", # 23-27
        "#CC6666", "#FF0000", "#E0CCBE", "#008000", "#7AA2F7",  # 28-32
        '#777777', '#BBBBBB', '#888888', '#AAAAAA', '#AA0000', # Мои
        '#7777FF'
    ]

    COLOR_BG2 = [
        '#CEDBB0', '#C3B1E1',  # Надин и Анин
        "#2D2D2D", "#F1F3F5", "#240B36", "#606C38", "#1E293B", 
        "#D8DEE9", "#402A47", "#1B2E1B", "#2D2424", "#343A40",
        "#1E1E1E", "#EEE8D5", "#073642", "#636E72", "#333333", # 13-17
        "#EFEBE9", "#2C2C2C", "#F0F0F0", "#313244", "#3B3B3B", # 18-22
        "#1F1F1F", "#F2F2F2", "#292929", "#E5D3B3", "#34495E", # 23-27
        "#1D1F21", "#E5E5E5", "#747264", "#1A1A1A", "#24283B", # 28-32
        '#BBBBBB', '#777777', '#AAAAAA', '#888888', '#550000', # Мои
        '#AAAAFF'
    ]

    chosen = color

    COLOR_BG = str(COLOR_BG[chosen])
    COLOR_FG = str(COLOR_FG[chosen])
    COLOR_ACCENT = str(COLOR_ACCENT[chosen])
    COLOR_BG2 = str(COLOR_BG2[chosen])

    global root
    
    root = tk.Tk()
    
    root.attributes('-fullscreen', True)
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))
    root.bind("<F11>", lambda event: root.attributes("-fullscreen", True))
    
    root.title("Sudoku App")
    root.geometry("3000x3000")
    root.configure(bg=COLOR_BG)

    if manual == 0:
        title = tk.Label(root, text="Daily Sudoku:", font=("Noita Blackletter", 100))
    else:
        title = tk.Label(root, text="Manual Sudoku:", font=("Noita Blackletter", 100))
        
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
        i.configure(fg=COLOR_FG)
        if isinstance(i, PlaceholderEntry):
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
        if isinstance(sudoku[i], PlaceholderEntry):
            try:
                val = int(sudoku[i].var.get())
            except ValueError:
                val = sudoku[i].var.get()

        if ((str(number) in str(getattr(sudoku[i], "number", None))) or (str(number) in str(val))) and not str(number) == '':
            sudoku[i].configure(bg=COLOR_ACCENT)
        else:
            if i in (
                3, 4, 5, 12, 13, 14, 21, 22, 23, 27,
                28, 29, 33, 34, 35, 36, 37, 38, 42,
                43, 44, 45, 46, 47, 51, 52, 53, 57,
                58, 59, 66, 67, 68, 75, 76, 77
            ):
                sudoku[i].configure(bg=COLOR_BG)
            else:
                sudoku[i].configure(bg=COLOR_BG2)

def buttons_setup():
    # цифры
    global buttons
    buttons = []
    for i in range(9):
        button = tk.Button(
            root, text=i+1, font=("Noita Blackletter", 30),
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
            root, text='Ready', font=("Noita Blackletter", 30),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=check
    )
    check_button.place(relx=0.2, rely=0.1, anchor='e', relwidth=0.1, relheight=0.08)
    
    tk.Button(
            root, text='Clear all', font=("Noita Blackletter", 30),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=clear
    ).place(relx=0.2, rely=0.2, anchor='e', relwidth=0.1, relheight=0.08)
    
    global num_size
    num_size = True
    tk.Button(
            root, text='Number size', font=("Noita Blackletter", 25),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=swich
    ).place(relx=0.2, rely=0.3, anchor='e', relwidth=0.1, relheight=0.08)

def check():
    global win
    
    for i in range(len(sudoku)):
        if isinstance(sudoku[i], PlaceholderEntry):
            if sudoku[i].var.get() != str(s.sudoku[i]):
                return
                
    global check_button
    if not win:
        check_button.place_forget()

    check_button = tk.Label(
            root, text='You Won', font=("Noita Blackletter", 30),
            bg=COLOR_FG, fg=COLOR_BG
    ).place(relx=0.2, rely=0.1, anchor='e', relwidth=0.1, relheight=0.08)
    win = True

def clear():
    global timer
    global hints
    
    if not win:
        timer = 0
        hints = 0
        hint_counter.config(text=str(f'Hints used: {hints}'))
        
        for i in sudoku:
            if isinstance(i, PlaceholderEntry):
                i.delete(0, tk.END)

def swich():
    global num_size

    for i in sudoku:
        if isinstance(i, PlaceholderEntry) and i.focus_on:
            if int(i['font'][-2:]) == 14:
                i.configure(font=("Noita Blackletter", 30))
            else:
                i.configure(font=("Noita Blackletter", 14))

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
            label = tk.Label(root, text=s.sudoku[i], font=("Noita Blackletter", 30))
            label.number = s.sudoku[i]
        else:
            label_var = tk.StringVar()
            label = PlaceholderEntry(root, textvariable=label_var, font=("Noita Blackletter", 30), justify='center')
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

    if len(str(minn)) == 1 and minn != 0:
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

def main(manual_level=0, color=0):
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

    varriables_and_tk_setup(manual_level, color)
    global COLOR_BG
    global COLOR_FG
    global COLOR_ACCENT
    global COLOR_BG2

    global color_mode
    color_mode = color
    global manual_level_mode
    manual_level_mode = manual_level
    
    make_sudoku(level)

    build()
    
    buttons_setup()

    highlight(1)

    global clock
    clock = tk.Label(
            root, text=timer, font=("Noita Blackletter", 25),
            bg=COLOR_BG2, fg=COLOR_FG
        )
    clock.place(relx=0.5, rely=0.92, anchor='center', relwidth=0.1, relheight=0.1)

    global hint_counter
    hint_counter = tk.Label(
            root, text='', font=("Noita Blackletter", 25),
            bg=COLOR_BG2, fg=COLOR_FG
        )
    hint_counter.place(relx=0.5, rely=0.2, anchor='center', relwidth=0.12, relheight=0.06)
    add_hint()

    tk.Button(
            root, text='Activate\nmanual sudoku', font=("Noita Blackletter", 20),
            bg=COLOR_BG2, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=restart
        ).place(relx=0.2, rely=0.4, anchor='e', relwidth=0.1, relheight=0.08)

    global manual_entry
    manual_entry = PlaceholderEntry(
            root, justify='center', font=("Noita Blackletter", 20),
            bg=COLOR_BG2, fg=COLOR_FG,
            placeholder='Level (1 - 10)',
            color=COLOR_ACCENT
        )
    manual_entry.place(relx=0.2, rely=0.5, anchor='e', relwidth=0.1, relheight=0.08)

    if manual_level != 0:
        tk.Button(
                root, text='Back to\ndaily sudoku', font=("Noita Blackletter", 20),
                bg=COLOR_BG, fg=COLOR_FG,
                activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
                command=back_to_daily
            ).place(relx=0.2, rely=0.6, anchor='e', relwidth=0.1, relheight=0.08)

    tk.Button(
            root, text='Hint', font=("Noita Blackletter", 25),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=give_hint
        ).place(relx=0.2, rely=0.7, anchor='e', relwidth=0.1, relheight=0.08)

    tk.Button(
            root, text='Quit the game', font=("Noita Blackletter", 22),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=root.destroy
        ).place(relx=0.2, rely=0.8, anchor='e', relwidth=0.1, relheight=0.08)

    tk.Label(
            root, text=f'Current level:\n{level}', font=("Noita Blackletter", 22),
            bg=COLOR_BG2, fg=COLOR_FG
        ).place(relx=0.2, rely=0.9, anchor='e', relwidth=0.1, relheight=0.1)

    tk.Button(
            root, text='Apply color\nand restart', font=("Noita Blackletter", 22),
            bg=COLOR_BG, fg=COLOR_FG,
            activebackground=COLOR_ACCENT, activeforeground=COLOR_FG,
            command=lambda: change_color()
        ).place(relx=0.67, rely=0.92, anchor='e', relwidth=0.1, relheight=0.08)

    global color_entry
    color_entry = PlaceholderEntry(
            root, placeholder='Color (0 - 37)', font=("Noita Blackletter", 22),
            bg=COLOR_BG, fg=COLOR_FG, color=COLOR_ACCENT, justify='center'
        )
    color_entry.place(relx=0.33, rely=0.92, anchor='w', relwidth=0.1, relheight=0.08)
    
    tick()

def restart():
    try:
        ml = int(manual_entry.get())
        if ml < 1 or ml > 10:
            return
    except ValueError:
        return

    root.destroy()
    main(manual_level=ml, color=color_mode)

def back_to_daily():
    root.destroy()
    main(color=color_mode)

def give_hint():
    for i in range(len(sudoku)):
        if isinstance(sudoku[i], PlaceholderEntry):
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
        if isinstance(sudoku[i], PlaceholderEntry):
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

def change_color():
    try:
        color = int(color_entry.get())
        if color > 37 or color < 0:
            return
        root.destroy()
        main(manual_level=manual_level_mode, color=color)
    except:
        return

# print(date.today().strftime("%A"))
if __name__ == "__main__":
    main()

root.mainloop()
