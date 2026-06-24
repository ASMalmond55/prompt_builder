"""Prompt Builder (Autonomous Blueprint)

A small Tkinter UI that turns a rough prompt into a more complete,
autonomous-blueprint style prompt suitable for use with an LLM.

The autonomous blueprint technique asks the model to first draft a
self-contained execution blueprint (objective, deliverables, plan,
quality bar) and then autonomously carry it out and self-verify,
rather than narrating an exploratory chain of thought.

Standard library only - no pip installs required.
"""

import tkinter as tk
from tkinter import ttk, messagebox


def build_prompt(rough_prompt: str, role: str = "", example: str = "") -> str:
    """Expand a rough prompt into a structured autonomous-blueprint prompt.

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
        "## Objective & Constraints\n"
        "- Restate the goal as a single, unambiguous objective.\n"
        "- List the known constraints, requirements, and success criteria.\n"
        "- Identify missing information and the reasonable default assumptions "
        "you will adopt so you can proceed autonomously without stopping to ask."
    )

    sections.append(
        "## Blueprint\n"
        "Before doing the work, produce a concise, self-contained blueprint that "
        "fully specifies the solution. Do not narrate exploratory reasoning; "
        "commit to a plan:\n"
        "1. Deliverables: the concrete artifacts you will produce.\n"
        "2. Architecture/Approach: the structure, components, and how they fit "
        "together.\n"
        "3. Execution steps: an ordered, actionable task list to build each "
        "deliverable.\n"
        "4. Quality bar: the standards, edge cases, and acceptance checks each "
        "deliverable must satisfy."
    )

    sections.append(
        "## Autonomous Execution\n"
        "Execute the blueprint end to end without pausing for confirmation:\n"
        "- Build each deliverable in the order defined above.\n"
        "- Resolve ambiguities using your stated assumptions and keep going.\n"
        "- Self-verify the result against the Quality bar and acceptance checks, "
        "and silently correct any deviations before presenting the final output."
    )

    sections.append(
        "## Output Requirements\n"
        "- Lead with the blueprint, then the completed deliverables.\n"
        "- Provide a clear, well-structured final answer ready to use.\n"
        "- If code is involved, make it correct, runnable, and commented where useful.\n"
        "- End with a brief self-verification note and any assumptions that were "
        "material to the result."
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
        root.title("Prompt Builder (Autonomous Blueprint)")
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
