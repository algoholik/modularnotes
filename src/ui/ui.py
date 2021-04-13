import tkinter as tk
from services.monoa_service import m_service
from entities.snippet import Snippet

class UI:
    def __init__(self, root):
        self._root = root
        self.snippets = [snippet for snippet in m_service.get_snippets()]
        #for snip in self.snippets:
        #    print(snip)
        #self._current_view = None

    def start(self):

        editor_active_snippet_id = tk.IntVar()

        def _get_snippets():
            self.snippets = [snippet for snippet in m_service.get_snippets()]

        def _update_snippet():
            m_service.update_snippet(1, "derp")

        def _save_snippet():
            m_service.create_snippet(entry.get())
            
        def _update_snippet_list():
            ui_snippet_list.delete(0, "end")
            for snippet in self.snippets:
                ui_snippet_list.insert(snippet.get_id(), snippet.get_snippet())

        def _snippet_list_select(event):
            selection = event.widget.curselection()
            if selection:
                snippet_id = selection[0] + 1
                snippet_content = [snippet.get_snippet() for snippet in self.snippets if snippet.get_id() == snippet_id]
                ui_editor_txt.delete(1.0, "end")
                ui_editor_txt.insert(1.0, snippet_content)
                editor_active_snippet_id.set(snippet_id)

        sidebar = tk.Frame(master=self._root, width=240, bg="grey")
        sidebar.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        content_area = tk.Frame(master=self._root, width=400, bg="white")
        content_area.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        tag_area = tk.Frame(master=self._root, width=100, bg="white")
        tag_area.pack(fill=tk.BOTH, side=tk.RIGHT, expand=False)

        entry = tk.Entry(master=self._root)
        entry.pack()
        #entry.focus_set()

        ui_editor_txt = tk.Text(master=content_area, height=5, width=20, exportselection=True) 
        ui_editor_txt.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        ui_editor_txt_scrollbar = tk.Scrollbar(master=content_area)
        ui_editor_txt_scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        ui_editor_txt_scrollbar.config(command=ui_editor_txt.yview)
        ui_editor_txt.config(yscrollcommand=ui_editor_txt_scrollbar.set)
        ui_editor_txt.focus_set()


        button1 = tk.Button(master=self._root, text="Load all", command=_get_snippets)
        button2 = tk.Button(master=self._root, text="Update list", command=_update_snippet_list)
        button3 = tk.Button(master=self._root, text="Save", command=_save_snippet)
        button1.pack()
        button2.pack()
        button3.pack()

        ui_snippet_list = tk.Listbox(master=sidebar)
        ui_snippet_list.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)
        ui_snippet_list.bind("<<ListboxSelect>>", _snippet_list_select)

        _get_snippets()
        _update_snippet_list()


        '''
        entry = tk.Entry(master=self._root)
        entry.pack()
        entry.focus_set()

        button1 = tk.Button(master=self._root, text="Load all", command=_get_snippets)
        button2 = tk.Button(master=self._root, text="Update", command=_update_snippet)
        button3 = tk.Button(master=self._root, text="Save", command=_save_snippet)
        button1.pack()
        button2.pack()
        button3.pack()

        listbox = tk.Listbox(master=sidebar, width=240)
        listbox.pack()
        '''

