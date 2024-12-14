import tkinter as tk
from tkinter import messagebox
import csv


def info_save(student_name, student_attempts, scores):
    try:
        with open('student_info.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([student_name, student_attempts, *scores])
            print('Data saved')
    except Exception as e:
        print(f'Error saving data: {e}')
        messagebox.showerror("Error", f"Failed to save data: {e}")


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Info")
        self.geometry("400x400")
        self.resizable(True, True)

        self.inputs_generated = False

        self.name_label = tk.Label(self, text="Student name:", font=("Times New Roman", 15))
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.name_input = tk.Entry(self, font=("Times New Roman", 15))
        self.name_input.grid(row=0, column=1, padx=10, pady=10)

        self.attempt_label = tk.Label(self, text="# of attempts:", font=("Times New Roman", 15))
        self.attempt_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.attempt_input = tk.Entry(self, font=("Times New Roman", 15))
        self.attempt_input.grid(row=1, column=1, padx=10, pady=10)

        self.submit_button = tk.Button(self, text="SUBMIT", font=("Times New Roman", 15), command=self.user_submit)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.score_inputs_frame = tk.Frame(self)
        self.score_inputs_frame.grid(row=2, column=0, columnspan=2)

        self.score_inputs = []

    def user_submit(self):
        student_name = self.name_input.get().strip()
        if not student_name:
            messagebox.showwarning("Input Error", "Student name cannot be empty.")
            return

        try:
            student_attempts = int(self.attempt_input.get())
            if student_attempts <= 0:
                raise ValueError("Number of attempts must be greater than zero.")
        except ValueError:
            messagebox.showwarning("Input Error", "Enter a valid number of attempts (positive integer).")
            return

        if not self.inputs_generated:
            self.generate_score(student_attempts)
            self.inputs_generated = True
        else:
            scores = self.collect_scores()
            if scores is None:
                messagebox.showwarning("Input Error", "Please enter valid numbers for all scores.")
                return

            try:
                info_save(student_name, student_attempts, scores)
                messagebox.showinfo("Success", "Student data saved successfully.")
                self.clear_inputs()
                self.inputs_generated = False
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save data: {e}")

    def generate_score(self, student_attempts):
        self.clear_inputs()
        self.score_inputs = []

        for i in range(student_attempts):
            score_label = tk.Label(self.score_inputs_frame, text=f"Score {i + 1}:", font=("Times New Roman", 15))
            score_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            score_input = tk.Entry(self.score_inputs_frame, font=("Times New Roman", 15))
            score_input.grid(row=i, column=1, padx=10, pady=5)
            self.score_inputs.append(score_input)

    def clear_inputs(self):
        for widget in self.score_inputs_frame.winfo_children():
            widget.destroy()
        self.score_inputs = []

    def collect_scores(self):
        scores = []
        for score_input in self.score_inputs:
            score = score_input.get().strip()
            if not score:
                scores.append(0)
            else:
                try:
                    scores.append(int(score))
                except ValueError:
                    return None
        return scores


if __name__ == "__main__":
    app = Application()
    app.mainloop()
