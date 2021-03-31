from tkinter import Tk
from ui.ui import UI

def main():
    window = Tk()
    window.title('MoNoA - Modular Notes App 0.1.0')

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = screen_width - 200
    window_height = screen_height - 200
    window_x = screen_width//2 - window_width//2
    window_y = screen_height//2 - window_height//2
    window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')
    window.minsize(screen_width//2, screen_height//2)

    ui = UI(window)
    ui.start()
    window.mainloop()

if __name__ == '__main__':
    main()