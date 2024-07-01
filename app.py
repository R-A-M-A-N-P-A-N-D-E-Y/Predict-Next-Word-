import tkinter as tk
from tkinter import ttk, messagebox
from main import get_all_predictions
import ttkbootstrap as ttk


class PredictionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Prediction with Transformers")
        self.root.geometry("700x780")

        self.label = ttk.Label(root, text="Enter your text:")
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.text_entry = tk.Text(root, height=10, width=80)
        self.text_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.top_k_label = ttk.Label(root, text="Top K:")
        self.top_k_label.grid(row=2, column=0, sticky='w', padx=10)

        self.top_k_entry = ttk.Entry(root)
        self.top_k_entry.grid(row=2, column=1, padx=10, pady=10, sticky='e')

        self.predict_button = ttk.Button(root, text="Get Predictions", command=self.get_predictions)
        self.predict_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Creating a frame for the results with a scrollbar
        self.result_frame = ttk.Frame(root)
        self.result_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.canvas = tk.Canvas(self.result_frame)
        self.scrollbar = ttk.Scrollbar(self.result_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)

        # Creating separate text boxes for each model's predictions
        self.bert_label = ttk.Label(self.scrollable_frame, text="BERT Predictions:")
        self.bert_label.grid(row=0, column=0, sticky='w', padx=10)
        self.bert_text = tk.Text(self.scrollable_frame, height=5, width=40)
        self.bert_text.grid(row=1, column=0, padx=10, pady=10)

        self.xlnet_label = ttk.Label(self.scrollable_frame, text="XLNet Predictions:")
        self.xlnet_label.grid(row=0, column=1, sticky='w', padx=10)
        self.xlnet_text = tk.Text(self.scrollable_frame, height=5, width=40)
        self.xlnet_text.grid(row=1, column=1, padx=10, pady=10)

        self.xlm_label = ttk.Label(self.scrollable_frame, text="XLM-Roberta Predictions:")
        self.xlm_label.grid(row=2, column=0, sticky='w', padx=10)
        self.xlm_text = tk.Text(self.scrollable_frame, height=5, width=40)
        self.xlm_text.grid(row=3, column=0, padx=10, pady=10)

        self.bart_label = ttk.Label(self.scrollable_frame, text="BART Predictions:")
        self.bart_label.grid(row=2, column=1, sticky='w', padx=10)
        self.bart_text = tk.Text(self.scrollable_frame, height=5, width=40)
        self.bart_text.grid(row=3, column=1, padx=10, pady=10)

        self.electra_label = ttk.Label(self.scrollable_frame, text="Electra Predictions:")
        self.electra_label.grid(row=4, column=0, sticky='w', padx=10)
        self.electra_text = tk.Text(self.scrollable_frame, height=5, width=40)
        self.electra_text.grid(row=5, column=0, padx=10, pady=10)

        self.roberta_label = ttk.Label(self.scrollable_frame, text="Roberta Predictions:")
        self.roberta_label.grid(row=4, column=1, sticky='w', padx=10)
        self.roberta_text = tk.Text(self.scrollable_frame, height=5, width=40)
        self.roberta_text.grid(row=5, column=1, padx=10, pady=10)

    def get_predictions(self):
        input_text = self.text_entry.get("1.0", tk.END).strip()
        top_k = self.top_k_entry.get().strip()

        if not input_text or not top_k.isdigit():
            messagebox.showerror("Error", "Please enter valid text and top_k value.")
            return

        top_k = int(top_k)
        input_text += ' <mask>'

        try:
            predictions = get_all_predictions(input_text, top_clean=top_k)
            self.bert_text.delete("1.0", tk.END)
            self.xlnet_text.delete("1.0", tk.END)
            self.xlm_text.delete("1.0", tk.END)
            self.bart_text.delete("1.0", tk.END)
            self.electra_text.delete("1.0", tk.END)
            self.roberta_text.delete("1.0", tk.END)

            self.bert_text.insert(tk.END, predictions['bert'])
            self.xlnet_text.insert(tk.END, predictions['xlnet'])
            self.xlm_text.insert(tk.END, predictions['xlm'])
            self.bart_text.insert(tk.END, predictions['bart'])
            self.electra_text.insert(tk.END, predictions['electra'])
            self.roberta_text.insert(tk.END, predictions['roberta'])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


if __name__ == "__main__":
    root = ttk.Window(themename='journal')
    app = PredictionApp(root)
    root.mainloop()
