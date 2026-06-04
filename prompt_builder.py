"""Prompt Builder

A small Tkinter UI that turns a rough prompt into a more complete,
chain-of-thought style prompt suitable for use with an LLM.

Standard library only - no pip installs required.
"""

import tkinter as tk
from tkinter import ttk, messagebox


def build_prompt(rough_prompt: str, role: str = "", example: str = "") -> str:
    """Expand a rough prompt into a structured chain-of-thought prompt.

    Args:
        rough_prompt: The user's raw idea/request.
        role: Optional persona the LLM should adopt.
        example: Optional example or expected output to guide the response.

    Returns:
        A formatted prompt string.
    """
    rough_prompt = rough_prompt.strip()
    role = role.strip()
    example = example.strip()

    sections = []

    if role:
        sections.append(f"You are {role}.")
    else:
        sections.append(
            "You are an expert assistant with deep, relevant domain knowledge."
        )

    sections.append(
        "## Task\n"
        f"{rough_prompt}"
    )

    sections.append(
        "## Context & Assumptions\n"
        "- Identify any information you need but were not given, and state the "
        "reasonable assumptions you will make.\n"
        "- Note any constraints, edge cases, or ambiguities relevant to the task."
    )

    sections.append(
        "## Chain of Thought\n"
        "Reason through the problem step by step before giving the final answer:\n"
        "1. Restate the goal in your own words.\n"
        "2. Break the problem into smaller sub-problems.\n"
        "3. Work through each sub-problem in order, explaining your reasoning.\n"
        "4. Check your reasoning for errors or missed cases.\n"
        "5. Synthesize the results into a coherent solution."
    )

    sections.append(
        "## Output Requirements\n"
        "- Provide a clear, well-structured final answer.\n"
        "- Keep the reasoning concise but complete.\n"
        "- If code is involved, make it correct, runnable, and commented where useful.\n"
        "- Call out any remaining uncertainties or follow-up questions."
    )

    if example:
        sections.append(
            "## Example / Expected Output\n"
            "Use the following as a guide for the format and style of your answer:\n"
            f"{example}"
        )

    return "\n\n".join(sections)


class PromptBuilderApp:
    """Tkinter application window for the prompt builder."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Prompt Builder")
        root.geometry("800x650")
        root.minsize(600, 500)

        main = ttk.Frame(root, padding=10)
        main.pack(fill=tk.BOTH, expand=True)
        main.columnconfigure(0, weight=1)
        # rows: inputs fixed, output expands
        main.rowconfigure(9, weight=2)

        # Rough prompt input
        ttk.Label(main, text="Rough prompt:").grid(
            row=0, column=0, sticky="w"
        )
        self.input_text = tk.Text(main, height=8, wrap="word")
        self.input_text.grid(row=1, column=0, sticky="nsew", pady=(2, 8))

        # Optional role
        ttk.Label(main, text="Role (optional):").grid(
            row=2, column=0, sticky="w"
        )
        self.role_var = tk.StringVar()
        self.role_entry = ttk.Entry(main, textvariable=self.role_var, font=("TkDefaultFont", 12))
        self.role_entry.grid(row=3, column=0, sticky="new", pady=(2, 8), ipady=6)

        # Optional example / expected output
        ttk.Label(main, text="Example / expected output (optional):").grid(
            row=4, column=0, sticky="w"
        )
        self.example_text = tk.Text(main, height=5, wrap="word")
        self.example_text.grid(row=5, column=0, sticky="nsew", pady=(2, 8))

        # Buttons
        button_bar = ttk.Frame(main)
        button_bar.grid(row=6, column=0, sticky="w", pady=(0, 8))
        ttk.Button(
            button_bar, text="Generate", command=self.generate
        ).pack(side=tk.LEFT)
        ttk.Button(
            button_bar, text="Copy to Clipboard", command=self.copy_output
        ).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(
            button_bar, text="Clear", command=self.clear_all
        ).pack(side=tk.LEFT, padx=(6, 0))

        # Output (editable)
        ttk.Label(main, text="Generated prompt (editable):").grid(
            row=8, column=0, sticky="w"
        )
        output_frame = ttk.Frame(main)
        output_frame.grid(row=9, column=0, sticky="nsew", pady=(2, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)

        self.output_text = tk.Text(output_frame, wrap="word")
        self.output_text.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            output_frame, orient="vertical", command=self.output_text.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.output_text.configure(yscrollcommand=scrollbar.set)

    def generate(self) -> None:
        rough = self.input_text.get("1.0", tk.END).strip()
        if not rough:
            messagebox.showwarning(
                "Missing input", "Please enter a rough prompt first."
            )
            return
        result = build_prompt(rough, self.role_var.get(), self.example_text.get("1.0", tk.END))
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert("1.0", result)

    def copy_output(self) -> None:
        content = self.output_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showinfo(
                "Nothing to copy", "Generate a prompt before copying."
            )
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        messagebox.showinfo("Copied", "Prompt copied to clipboard.")

    def clear_all(self) -> None:
        self.input_text.delete("1.0", tk.END)
        self.role_var.set("")
        self.example_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)


def main() -> None:
    root = tk.Tk()
    PromptBuilderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
