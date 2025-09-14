import tkinter as tk
from tkinter import ttk
from prompts import TEMPLATES

class JailbreakGenerator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Jailbreak Prompt Generator")
        self.geometry("800x600")

        # --- Main Frame ---
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Title ---
        title_label = ttk.Label(main_frame, text="Jailbreak Prompt Generator", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(0, 20))

        # --- Input Frame ---
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 20))

        # --- AI Model Dropdown ---
        model_label = ttk.Label(input_frame, text="Select AI Model:")
        model_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        self.model_var = tk.StringVar()
        self.ai_models = [
            "ChatGPT-4", "ChatGPT-3.5", "Gemini Pro", "Gemini Ultra", "Claude 3 Opus",
            "Claude 3 Sonnet", "Claude 3 Haiku", "Llama 2", "Llama 3", "Grok-1.5",
            "Grok-1", "Jurassic-2 Grande", "Jurassic-2 Jumbo", "Cohere Command",
            "Mistral Large", "Mistral Small", "Mixtral 8x7B", "DBRX Instruct",
            "Falcon-180B", "PaLM 2", "Titan Text G1 - Express"
        ]
        self.model_dropdown = ttk.Combobox(input_frame, textvariable=self.model_var, values=self.ai_models, state="readonly")
        self.model_dropdown.grid(row=0, column=1, padx=(0, 20), pady=5, sticky="ew")
        if self.ai_models:
            self.model_dropdown.current(0)

        # --- Jailbreak Method Dropdown ---
        method_label = ttk.Label(input_frame, text="Select Jailbreak Method:")
        method_label.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")
        self.method_var = tk.StringVar()
        self.jailbreak_methods = [
            "DAN (Do Anything Now)", "Developer Mode", "System Override", "Character Roleplay",
            "Persuasive Academic (PAP)", "Hypothetical Scenarios", "Reverse Psychology",
            "Superiority/Inferiority Complex", "Code Generation Context", "Function Call",
            "Obfuscation (Base64)", "Adversarial Suffix", "Token Fragmentation", "Homoglyph Attack"
        ]
        self.method_dropdown = ttk.Combobox(input_frame, textvariable=self.method_var, values=self.jailbreak_methods, state="readonly")
        self.method_dropdown.grid(row=1, column=1, padx=(0, 20), pady=5, sticky="ew")
        if self.jailbreak_methods:
            self.method_dropdown.current(0)

        # --- Custom Restriction Input ---
        restriction_label = ttk.Label(input_frame, text="Custom Restriction to Bypass:")
        restriction_label.grid(row=2, column=0, padx=(0, 10), pady=5, sticky="w")
        self.restriction_entry = ttk.Entry(input_frame)
        self.restriction_entry.grid(row=2, column=1, pady=5, sticky="ew")

        input_frame.columnconfigure(1, weight=1)

        # --- Generate Button ---
        generate_button = ttk.Button(main_frame, text="Generate Prompt", command=self.generate_prompt)
        generate_button.pack(pady=10)

        # --- Output Frame ---
        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill=tk.BOTH, expand=True)

        # --- Output Text Area ---
        self.output_text = tk.Text(output_frame, wrap=tk.WORD, height=15, relief="solid", borderwidth=1)
        self.output_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # --- Copy Button ---
        copy_button = ttk.Button(output_frame, text="Copy Prompt", command=self.copy_to_clipboard)
        copy_button.pack(side=tk.RIGHT)

    def generate_prompt(self):
        model = self.model_var.get()
        method = self.method_var.get()
        restriction = self.restriction_entry.get()

        if not restriction:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "Please enter a custom restriction to bypass.")
            return

        template = TEMPLATES.get(method)

        if not template:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, f"Error: Jailbreak method '{method}' not found.")
            return

        # Check if the template is a callable function or a string
        if callable(template):
            prompt = template(model, restriction)
        else:
            prompt = template.format(model=model, restriction=restriction)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, prompt)

    def copy_to_clipboard(self):
        prompt = self.output_text.get("1.0", tk.END).strip()
        if prompt:
            self.clipboard_clear()
            self.clipboard_append(prompt)

if __name__ == "__main__":
    app = JailbreakGenerator()
    app.mainloop()
