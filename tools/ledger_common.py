#!/usr/bin/env python3
# Общий учёт токенов: хранит сырые строки в docs/.ledger.tsv (по одной на агента, upsert),
# регенерит человекочитаемый docs/ledger.md (RU-шапки, дата дд.мм.гггг, разряды пробелами).
import os

def _sp(n):
    return f"{int(n):,}".replace(",", " ")

def upsert(root, key, ts, role, model, task, i, cr, o):
    tsv = os.path.join(root, "docs", ".ledger.tsv")
    rows = {}
    order = []
    if os.path.exists(tsv):
        for line in open(tsv, encoding="utf-8"):
            p = line.rstrip("\n").split("\t")
            if len(p) == 8:
                k = p[0]
                if k not in rows: order.append(k)
                rows[k] = p
    if key not in rows: order.append(key)
    # для локальных субагентов усиление накопительное — берём максимум total
    prev = rows.get(key)
    if prev and (int(prev[6]) + int(prev[7])) >= (i + o):
        return  # старое значение полнее — не трогаем
    rows[key] = [key, ts, role, model, task, str(i), str(cr), str(o)]
    with open(tsv, "w", encoding="utf-8") as f:
        for k in order:
            f.write("\t".join(rows[k]) + "\n")
    render(root, order, rows)

def render(root, order, rows):
    md = os.path.join(root, "docs", "ledger.md")
    h  = "# Ledger токенов\n\n"
    h += "> Столбцы: **Ввод** — новые входные токены; **Кэш-чтение** — прочитано из кэша (дёшево); "
    h += "**Вывод** — сгенерировано моделью; **Итого** = Ввод + Вывод (без кэша).\n\n"
    h += "| Дата (UTC) | Роль | Модель | Задача | Ввод | Кэш-чтение | Вывод | Итого |\n"
    h += "|---|---|---|---|---:|---:|---:|---:|\n"
    ti = tcr = to = 0
    body = []
    for k in order:
        _, ts, role, model, task, i, cr, o = rows[k]
        i, cr, o = int(i), int(cr), int(o)
        ti += i; tcr += cr; to += o
        body.append(f"| {ts} | {role} | {model} | {task} | {_sp(i)} | {_sp(cr)} | {_sp(o)} | {_sp(i+o)} |")
    tot = f"| **ИТОГО** |  |  |  | **{_sp(ti)}** | **{_sp(tcr)}** | **{_sp(to)}** | **{_sp(ti+to)}** |"
    with open(md, "w", encoding="utf-8") as f:
        f.write(h + "\n".join(body) + "\n" + tot + "\n")
