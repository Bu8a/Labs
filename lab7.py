import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from itertools import combinations

def count_skill(skill_map, group):
    return sum(skill_map[x] for x in group)

def on_run():
    output.delete('1.0', tk.END)
    try:
        num_cand = int(entry_num.get())
        budget = int(entry_budget.get())
    except ValueError:
        output.insert(tk.END, "Ошибка: введите целые числа для количества кандидатов и бюджета\n")
        return

    candidates = list(range(1, num_cand + 1))
    salary = {c: 50 + (c - 1) * 5 for c in candidates}
    skill  = {c: 70 + (c - 1) * 5 for c in candidates}

    def generate_python(cands):
        return [
            (mid[0], seni, juni)
            for mid in combinations(cands, 1)
            for seni in combinations([c for c in cands if c not in mid], 3)
            for juni in combinations([c for c in cands if c not in mid and c not in seni], 2)
        ]

    py_list = generate_python(candidates)

    valid = []
    for mid, seni, juni in py_list:
        total_sal = salary[mid] + sum(salary[x] for x in seni + juni)
        if total_sal <= budget:
            valid.append((mid, seni, juni))

    best = []
    max_sk = -1
    for mid, seni, juni in valid:
        ssum = count_skill(skill, (mid,) + seni + juni)
        if ssum > max_sk:
            max_sk = ssum
            best = [(mid, seni, juni)]
        elif ssum == max_sk:
            best.append((mid, seni, juni))

    output.insert(tk.END, f"Ограничение: суммарная зарплата ≤ {budget}\n")
    output.insert(tk.END, "Целевая функция: максимизация суммарного навыка\n\n")
    output.insert(tk.END, f"Всего допустимых вариантов: {len(valid)}\n")
    output.insert(tk.END, f"Оптимальных вариантов: {len(best)} (макс. навык = {max_sk})\n")
    if best:
        mid, seni, juni = best[0]
        output.insert(tk.END, f"Лучший вариант: Mid={mid}, Seniors={seni}, Juniors={juni}\n")

root = tk.Tk()
root.title("ЛР5 Вариант 32 (GUI)")

frm = ttk.Frame(root, padding=10)
frm.pack(fill='x')

ttk.Label(frm, text="Количество кандидатов:").grid(row=0, column=0, sticky="w")
entry_num = ttk.Entry(frm, width=10)
entry_num.grid(row=0, column=1, padx=5)
entry_num.insert(0, "7")

ttk.Label(frm, text="Бюджет:").grid(row=1, column=0, sticky="w")
entry_budget = ttk.Entry(frm, width=10)
entry_budget.grid(row=1, column=1, padx=5, pady=5)
entry_budget.insert(0, "3000")

btn = ttk.Button(frm, text="Запустить", command=on_run)
btn.grid(row=2, column=0, columnspan=2, pady=5)

output = ScrolledText(root, width=60, height=20, wrap=tk.WORD)
output.pack(padx=10, pady=(0,10))

root.mainloop()
