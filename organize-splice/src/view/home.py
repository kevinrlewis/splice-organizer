import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
import service.organizer as organize

class Home():
    def __init__(self):
        print("HOME!")
        self.organized = None
        self.splice_location_label = None
        self.destination_location_label = None

        self.vars = {
            "splice_location": None,
            "destination_location": None
        }

        self.window = tk.Tk()
        self.window.title('Splice Organizer')

        s = ttk.Style().theme_use('alt')

        self.main_frm = ttk.Frame(self.window)
        self.main_frm.grid(row=0, padx=5, pady=5)

    def display(self):
        self.splice_location_label = ttk.Label(self.main_frm, text='Splice Location')
        self.splice_location_label.grid(row=0)
        self.destination_location_label = ttk.Label(self.main_frm, text='Destination Location')
        self.destination_location_label.grid(row=1)

        splice_location_button = ttk.Button(
            self.main_frm,
            text='...',
            width=25,
            command=lambda: self.browse_files(self.splice_location_label, "splice_location")
        )

        destination_location_button = ttk.Button(
            self.main_frm,
            text='...',
            width=25,
            command=lambda: self.browse_files(self.destination_location_label, "destination_location")
        )

        splice_location_button.grid(row=0, column=1)
        destination_location_button.grid(row=1, column=1)

        move = tk.BooleanVar()
        ttk.Checkbutton(
            self.main_frm,
            text='Move files to processed folder within Splice folder.',
            variable=move
        ).grid(row=2, sticky=tk.W)

        button = ttk.Button(
            self.main_frm,
            text='ORGANIZE',
            width=25,
            command=lambda: self.organize_click(
                self.vars.get("splice_location"),
                self.vars.get("destination_location"),
                move.get()
            )
        )

        button.grid(row=3, column=0)
        self.window.mainloop()

    def organize_click(self, splice_folder, destination, move):
        if not splice_folder or not destination:
            self.organized = False

        o = organize.Organizer(splice_folder, destination, move)
        self.organized = o.organize()

        print("organized: %s" % self.organized)
        if self.organized:
            self.status = ttk.Label(self.main_frm, text='Organized Successfully', foreground='#00b300')
            self.status.grid(row=3, column=1)

    def browse_files(self, label, var):
        filename = fd.askdirectory(
            title="Select a Directory"
        )

        # Change label contents
        label.configure(text="File Opened: " + filename)
        upd = {
            var: filename
        }
        print(upd)
        self.vars.update(upd)
        print(self.vars)

