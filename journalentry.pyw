import tkinter as tk
import tkinter.ttk
import tkinter.font
import tkinter.messagebox

import jf


class Journalentry_tk(tk.Toplevel):
	def __init__(self, parent=None, entry=None, standalone=False):
		tk.Toplevel.__init__(self, parent)
		self.parent = parent

		if entry is None:
			self.entry = jf.Entry()
		else:
			self.entry = entry
			self.transient(parent)
			self.geometry("+{}+{}".format(parent.winfo_rootx() + 0,
			                              parent.winfo_rooty() + 0))

		self.protocol("WM_DELETE_WINDOW", self.on_close)
		self.standalone = standalone
		self.initialize()

	def initialize(self):
		self.var_date_label = tk.StringVar()
		time = "{} {}".format(self.entry.str_date, self.entry.str_time_short)
		self.var_date_label.set(time)
		self.var_title_input = tk.StringVar()
		self.var_title_input.set(self.entry.title)
		self.var_text_input = tk.StringVar()
		self.var_text_input.set(self.entry.text)
		self.var_tags_input = tk.StringVar()
		self.var_tags_input.set(", ".join(self.entry.tags))

		# Frames
		frame_title = tk.Frame(self, height=10, width=256)
		frame_text = tk.Frame(self, height=128, width=256)
		frame_tags = tk.Frame(self, height=10, width=256)

		frame_title.grid(column=0, row=0, sticky="we", padx=2, pady=2)
		frame_text.grid(column=0, row=1, sticky="nswe")
		frame_tags.grid(column=0, row=2, sticky="we", padx=2, pady=2)

		self.columnconfigure(0, weight=1)
		self.rowconfigure(1, weight=1)

		frame_title.columnconfigure(1, weight=1)
		frame_text.columnconfigure(0, weight=1)
		frame_text.rowconfigure(0, weight=1)
		frame_tags.columnconfigure(1, weight=1)

		########
		# Title
		self.date_label = tk.Label(frame_title,
		                           anchor="w",
		                           textvariable=self.var_date_label,
		                           font=jf.config.font_label)
		self.title_input = tk.Entry(frame_title,
		                            textvariable=self.var_title_input,
		                            font=jf.config.font_label)

		self.date_label.grid(column=0, row=0, padx=2)
		self.title_input.grid(column=1, row=0, sticky="we", padx=2)

		#############
		# Text input
		text_scroll = tk.Scrollbar(frame_text)
		self.text_input = tk.Text(frame_text, width=80, height=20,
		                          wrap="word",
		                          yscrollcommand=text_scroll.set,
		                          font=jf.config.font_content)
		self.text_input.insert("end", self.entry.text)
		self.text_input.focus()
		text_scroll.config(command=self.text_input.yview)

		self.text_input.grid(column=0, row=0, sticky="nswe")
		text_scroll.grid(column=1, row=0, sticky="ns")

		#######
		# Tags
		self.tag_label = tk.Label(frame_tags,
		                          anchor="w",
		                          text="Tags:",
		                          font=jf.config.font_label)
		self.tags_input = tk.Entry(frame_tags,
		                           textvariable=self.var_tags_input,
		                           font=jf.config.font_label)
		self.save_button = tk.Button(frame_tags, text="Save and quit",
		                             font=jf.config.font_label)
		self.save_button.bind("<ButtonRelease-1>", self.on_save_click)

		self.tag_label.grid(column=0, row=0, padx=2)
		self.tags_input.grid(column=1, row=0, sticky="we", padx=2)
		self.save_button.grid(column=2, row=0, padx=2)

		self.update()
		self.minsize(self.winfo_width(), self.winfo_height())

	def has_changes(self):
		title = self.entry.title != self.var_title_input.get().strip()
		text = self.entry.text != self.text_input.get("1.0", "end-1c")
		tags = ", ".join(self.entry.tags) != self.var_tags_input.get()

		if title or text or tags:
			return True
		return False

	def on_save_click(self, event):
		try:
			title = self.var_title_input.get().strip()
			text = self.text_input.get("1.0", "end-1c")
			tags = self.var_tags_input.get().split(",")
			# Strips and removes empty tags
			tags = [i.strip() for i in tags if i.strip()]

			if not self.has_changes():
				tk.messagebox.showwarning("Oops", "There is nothing to save.")
			else:
				self.entry.title = title
				self.entry.text = text
				self.entry.tags = tags
				self.entry.save()

				self.on_close(skip_check=True)
		except Exception as e:
			e = str(e) + "\nBackup your entry and fix the error, you lazy bum."
			tk.messagebox.showwarning("Exception", e)

	def on_close(self, skip_check=False):
		should_not_save = True
		if self.has_changes() and not skip_check:
			title = "Unsaved changes"
			message = f"You have unsaved changes.\nAre you sure you want to exit?"
			should_not_save = tk.messagebox.askokcancel(title, message,
			                                            icon="warning")

		if should_not_save or skip_check:
			self.destroy()
			if self.standalone:
				self.parent.destroy()


def open_edit(parent, entry):
	app = Journalentry_tk(parent, entry)
	app.title("Journal - Edit")
	app.iconbitmap("media/icon.ico")
	app.grab_set()
	parent.wait_window(app)


if __name__ == "__main__":
	root = tk.Tk()
	root.withdraw()
	root.iconbitmap("media/icon.ico")
	app = Journalentry_tk(root, standalone=True)
	app.title("Journal - Entry")
	app.iconbitmap("media/icon.ico")
	app.mainloop()
