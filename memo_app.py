import tkinter as tk
from tkinter import filedialog, messagebox

class MemoApp:
    def __init__(self, root):
        self.root = root
        self.root.title('메모장 - [새 파일]')
        self.root.geometry('800x600')
        self.file_path = None
        self.text = tk.Text(root, undo=True, wrap='none')
        self.text.pack(fill=tk.BOTH, expand=1)
        self.create_menu()
        self.root.protocol('WM_DELETE_WINDOW', self.on_exit)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label='새 파일', command=self.new_file)
        filemenu.add_command(label='열기...', command=self.open_file)
        filemenu.add_command(label='저장', command=self.save_file)
        filemenu.add_command(label='다른 이름으로 저장...', command=self.save_file_as)
        filemenu.add_separator()
        filemenu.add_command(label='종료', command=self.on_exit)
        menubar.add_cascade(label='파일(F)', menu=filemenu)
        self.root.config(menu=menubar)

    def new_file(self):
        if self.confirm_save():
            self.text.delete('1.0', tk.END)
            self.file_path = None
            self.root.title('메모장 - [새 파일]')

    def open_file(self):
        if not self.confirm_save():
            return
        path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.text.delete('1.0', tk.END)
            self.text.insert(tk.END, content)
            self.file_path = path
            self.root.title(f'메모장 - [{self.file_path}]')
        except Exception as e:
            messagebox.showerror('오류', f'파일을 열 수 없습니다:\n{e}')

    def save_file(self):
        if self.file_path:
            try:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text.get('1.0', tk.END))
                self.root.title(f'메모장 - [{self.file_path}]')
            except Exception as e:
                messagebox.showerror('오류', f'파일을 저장할 수 없습니다:\n{e}')
        else:
            self.save_file_as()

    def save_file_as(self):
        path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.text.get('1.0', tk.END))
            self.file_path = path
            self.root.title(f'메모장 - [{self.file_path}]')
        except Exception as e:
            messagebox.showerror('오류', f'파일을 저장할 수 없습니다:\n{e}')

    def confirm_save(self):
        if self.text.edit_modified():
            result = messagebox.askyesnocancel('저장', '변경 내용을 저장하시겠습니까?')
            if result:  # Yes
                self.save_file()
                return True
            elif result is None:  # Cancel
                return False
        return True

    def on_exit(self):
        if self.confirm_save():
            self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = MemoApp(root)
    root.mainloop()
