import tkinter as tk
from tkinter.constants import ACTIVE
from services.monoa_service import m_service
from entities.snippet import Snippet

class UI:
    def __init__(self, root):
        self._root = root
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

        self.active_snippet_id = tk.IntVar()
        self.active_snippet_txt = tk.StringVar()
        #self._current_view = None


    def start(self):
        def _update_snippet():
            print(self.active_snippet_id.get(), self.active_snippet_txt.get())
            m_service.update_snippet(self.active_snippet_id.get(), self.active_snippet_txt.get())
            _update_snippet_list()

        def _new_snippet():
            m_service.create_snippet("")
            _update_snippet_list()
            ui_snippet_list.select_set(0) 
            ui_snippet_list.event_generate("<<ListboxSelect>>")

        def _save_snippet():
            m_service.create_snippet(ui_editor_txt.get(1.0, "end-1c"))
            _update_snippet_list()
            
        def _update_snippet_list():
            ui_snippet_list.delete(0, "end")
            for snippet in m_service.get_snippets():
                list_item_str = f"({snippet.get_id()}) {snippet.get_snippet()}"
                ui_snippet_list.insert(0, list_item_str)

        def _snippet_list_select(event):
            for item in event.widget.curselection():
                snippet_str = ui_snippet_list.get(item)
                snippet_id = int(snippet_str[snippet_str.find("(")+1:snippet_str.find(")")])
                snippet = m_service.get_snippet(snippet_id)
                self.active_snippet_id.set(snippet.get_id())
                self.active_snippet_txt.set(snippet.get_snippet())
            ui_editor_txt.delete(1.0, "end")
            ui_editor_txt.insert(1.0, self.active_snippet_txt.get())

        menubar = tk.Frame(master=self._root, width=100, height=50, bg="grey")
        menubar.pack(fill=tk.X, side=tk.TOP, expand=False)
        sidebar = tk.Frame(master=self._root, width=320, bg="grey")
        sidebar.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        content_area = tk.Frame(master=self._root, width=640, bg="white")
        content_area.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        ui_editor_txt = tk.Text(master=content_area, height=5, width=20, exportselection=True) 
        ui_editor_txt.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        ui_editor_txt_scrollbar = tk.Scrollbar(master=content_area)
        ui_editor_txt_scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        ui_editor_txt_scrollbar.config(command=ui_editor_txt.yview)
        ui_editor_txt.config(yscrollcommand=ui_editor_txt_scrollbar.set)
        ui_editor_txt.focus_set()
        ui_editor_txt.bind("<KeyPress>", _update_snippet)


        button1 = tk.Button(master=menubar, text="New Snippet", command=_new_snippet)
        button2 = tk.Button(master=menubar, text="Save Snippet", command=_save_snippet)
        button1.grid(row=0, column=0)
        button2.grid(row=0, column=1)

        ui_snippet_list = tk.Listbox(master=sidebar)
        ui_snippet_list.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        ui_snippet_list.bind("<<ListboxSelect>>", _snippet_list_select)

        # Select most recent snippet in the list and update editor contents
        _update_snippet_list()
        ui_snippet_list.select_set(0) 
        ui_snippet_list.event_generate("<<ListboxSelect>>")


