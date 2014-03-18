__author__ = 'jankiel'
from tkinter import *
from tkinter import ttk


class LetsDoThis:

    def __init__(self):
        self.points = []
        root = Tk()
        root.title("Kalkulator trasy")

        mainframe = ttk.Frame(root, padding="3 4 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        self.generations = StringVar()
        self.pop_size = StringVar()
        self.m_chance = StringVar()
        self.x_chance = StringVar()
        self.generations.set('600')
        self.pop_size.set('300')
        self.x_chance.set('0.3')
        self.m_chance.set('0.1')
        e1 = ttk.Entry(mainframe, width=7, textvariable=self.generations)
        e2 = ttk.Entry(mainframe, width=7, textvariable=self.pop_size)
        e3 = ttk.Entry(mainframe, width=7, textvariable=self.x_chance)
        e4 = ttk.Entry(mainframe, width=7, textvariable=self.m_chance)
        e1.grid(column=2, row=1, sticky=(W, E))
        e2.grid(column=2, row=2, sticky=(W, E))
        e3.grid(column=2, row=3, sticky=(W, E))
        e4.grid(column=2, row=4, sticky=(W, E))

        ttk.Button(mainframe, text="Wczytaj plik", command=self.read_file).grid(column=1, row=6, sticky=W)
        ttk.Button(mainframe, text="Wyznacz trasę", command=self.calculate).grid(column=2, row=6, sticky=W)
        self.state = BooleanVar()
        self.state.set(True)
        self.checkbox = ttk.Checkbutton(mainframe, text="wykres", command=self.toggle_label, variable=self.state)
        self.checkbox.grid(column=1, row=5, sticky=W)
        ttk.Label(mainframe, text="liczba pokoleń").grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="liczebność populacji").grid(column=1, row=2, sticky=W)
        ttk.Label(mainframe, text="prawd. krzyżowania").grid(column=1, row=3, sticky=W)
        ttk.Label(mainframe, text="prawd. mutacji").grid(column=1, row=4, sticky=W)
        self.file_loaded = ttk.Label(mainframe, text='wybierz plik')
        self.file_loaded.grid(column=1, row=7, sticky=W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        e1.focus()
        root.bind('<Return>', self.calculate)

        root.mainloop()

    def read_file(self):
            import tkinter.filedialog
            path = tkinter.filedialog.askopenfilename()
            import re
            with open(path, 'r') as f:
                lines = f.read()
                result = re.findall(r'\d+\.\d+ \d+\.\d+', lines)
                if not result:
                    print('not found')
                    return

                result = [elem.split(' ') for elem in result] # elem: 'x y' -> ['x', 'y']
                result = [(float(elem[0]), float(elem[1])) for elem in result] # elem: ['x','y'] -> (x, y)
                self.points = result
            self.file_loaded['text'] = 'plik załadowany'

    def toggle_label(self):
        if self.state.get():
            self.checkbox['text'] = 'wykres'
        else:
            self.checkbox['text'] = 'średnia'

    def calculate(self):
        import tsp

        if not self.points:
            return
        t = tsp.TSP(self.points)
        t.evaluate(int(self.pop_size.get()), float(self.x_chance.get()),
                   float(self.m_chance.get()), int(self.generations.get()),show=self.state.get())


if __name__ == '__main__':
    LetsDoThis()