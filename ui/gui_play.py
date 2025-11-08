import tkinter as tk
from tkinter import ttk
import random
import math
import json
import os

from game.board import Board
from players.ai_bot import AIPlayer
# HumanPlayer не используется в GUI; оставляем импорт только при необходимости


def _softmax(xs):
    # защитная softmax для численного порядка
    exps = [math.exp(x - max(xs)) for x in xs]
    s = sum(exps)
    if s == 0:
        return [0 for _ in xs]
    return [e / s for e in exps]


class GUIPlay:
    """GUI для игры против ИИ.

    Показаны прогресс-бары с относительными предпочтениями ИИ для каждой клетки.
    """

    def __init__(self, ai_player=None, load_best_if_exists=True):
        self.root = None
        self.board = Board()
        self.human_symbol = 'X'
        self.ai_symbol = 'O'
        self.ai = ai_player or AIPlayer()
        self.load_best_if_exists = load_best_if_exists
        self.cell_buttons = []
        self.progress_bars = []
        self.percent_labels = []
        self.current_turn = None
        self.after_id = None

    def start(self):
        # Попытка подгрузить best.json
        try:
            if self.load_best_if_exists and os.path.exists('best.json'):
                with open('best.json', 'r') as f:
                    data = json.load(f)
                # берем первый набор весов
                item = data[0]
                self.ai = AIPlayer(w1=item['w1'], w2=item['w2'])
        except Exception:
            pass

        self.root = tk.Tk()
        self.root.title('Игра против ИИ')

        # Простая тёмная тема
        style = ttk.Style(self.root)
        style.theme_use('clam')
        bg = '#2e2e2e'
        fg = '#ffffff'
        accent = '#51e24a'
        self.root.configure(bg=bg)
        style.configure('TFrame', background=bg)
        style.configure('TLabel', background=bg, foreground=fg)
        style.configure('TButton', background=bg, foreground=fg)
        style.configure('TProgressbar', troughcolor='#3a3a3a', background=accent)

        main_frame = ttk.Frame(self.root, padding=8)
        main_frame.grid(row=0, column=0)

        board_frame = ttk.Frame(main_frame)
        board_frame.grid(row=0, column=0, padx=(0, 12))

        # 3x3 buttons
        for i in range(9):
            btn = ttk.Button(board_frame, text=' ', width=6, command=lambda i=i: self._on_cell_click(i))
            r, c = divmod(i, 3)
            btn.grid(row=r, column=c, ipadx=8, ipady=12)
            self.cell_buttons.append(btn)

        # Правый фрейм — предпочтения ИИ (один раз)
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky='n')

        ttk.Label(right_frame, text='Предпочтения ИИ:').grid(row=0, column=0, pady=(0, 6))

        for j in range(9):
            pf = ttk.Progressbar(right_frame, orient='horizontal', length=140, mode='determinate')
            pf.grid(row=j+1, column=0, sticky='w')
            lbl = ttk.Label(right_frame, text='0%')
            lbl.grid(row=j+1, column=1, sticky='w', padx=(6,0))
            self.progress_bars.append(pf)
            self.percent_labels.append(lbl)
        
        bottom = ttk.Frame(self.root, padding=6)
        bottom.grid(row=1, column=0, sticky='ew')
        self.status_label = ttk.Label(bottom, text='')
        self.status_label.grid(row=0, column=0, sticky='w')

        self.reset_button = ttk.Button(bottom, text='Сыграть ещё', command=self._reset)
        self.reset_button.grid(row=0, column=1)
        self.close_button = ttk.Button(bottom, text='Закрыть', command=self._close)
        self.close_button.grid(row=0, column=2, padx=(6,0))

        # Результат игры без всплывающего окна
        self.result_label = ttk.Label(bottom, text='')
        self.result_label.grid(row=1, column=0, columnspan=3, sticky='w', pady=(6,0))

        self._reset(initialize=True)
        self.root.protocol('WM_DELETE_WINDOW', self._close)
        self.root.mainloop()

    def _reset(self, initialize=False):
        # Сброс доски и интерфейса
        self.board = Board()
        self.result_label.config(text='')
        for i, btn in enumerate(self.cell_buttons):
            btn.config(text=' ', state='normal')
        for pb in self.progress_bars:
            pb['value'] = 0
        for lbl in self.percent_labels:
            lbl.config(text='0%')

        # случайно выбираем кто первый
        self.current_turn = random.choice(['human','ai'])
        self._set_symbols()
        self._update_status()

        if self.current_turn == 'ai':
            if self.root:
                self.root.after(0, self._ai_think_and_move)

    def _set_symbols(self):
        # человек всегда X для простоты
        self.human_symbol = 'X'
        self.ai_symbol = 'O'
        # устанавливаем символ ИИ в объекте AI
        self.ai.set_symbol(self.ai_symbol)

    def _update_status(self):
        if self.current_turn == 'human':
            self.status_label.config(text='Сейчас: Вы (X)')
        else:
            self.status_label.config(text='Сейчас: ИИ (O)')

    def _on_cell_click(self, i):
        if self.current_turn != 'human':
            return
        if not self.board.is_valid_move(i):
            return
        self.board.make_move(self.human_symbol, i)
        self.cell_buttons[i].config(text=self.human_symbol)

        if self.board.check_winner(self.human_symbol):
            self._show_result(f'Победа {self.human_symbol}!')
            return
        elif self.board.is_full():
            self._show_result('Ничья!')
            return

        self.current_turn = 'ai'
        self._update_status()
        self.root.after(150, self._ai_think_and_move)

    def _ai_think_and_move(self):
        # получить сырой выход сети и выполнить ход

        scores = self.ai.predict_scores(self.board)

        # Преобразуем к вероятностям только для доступных ходов
        avail = [self.board.is_valid_move(i) for i in range(9)]
        masked_scores = [s if a else float('-inf') for s, a in zip(scores, avail)]
        raw_for_softmax = [s if s != float('-inf') else -1e9 for s in masked_scores]
        probs = _softmax(raw_for_softmax)

        # Выбираем ход по тем же сырым оценкам
        available_indices = [i for i, a in enumerate(avail) if a]
        if not available_indices:
            return
        # выбор как argmax по scores
        move = max(available_indices, key=lambda i: scores[i])

        # делаем ход ИИ
        self.board.make_move(self.ai_symbol, move)
        self.cell_buttons[move].config(text=self.ai_symbol)

        # Обновляем прогресс-бары и метки (показываем, с какой вероятностью он сделал ход)
        percs = []
        for idx, (pb, lbl) in enumerate(zip(self.progress_bars, self.percent_labels)):
            perc = int(probs[idx] * 100)
            percs.append(perc)
            pb['value'] = perc
            lbl.config(text=f'{perc}%')

        # Проверка завершения
        if self.board.check_winner(self.ai_symbol):
            self._show_result(f'Победа {self.ai_symbol}!')
            return
        elif self.board.is_full():
            self._show_result('Ничья!')
            return

        # переключаем ход на человека
        self.current_turn = 'human'
        self._update_status()

    def _show_result(self, text):
        # заблокировать кнопки
        for btn in self.cell_buttons:
            btn.config(state='disabled')
        # Показываем результат в окне (без всплывающего окна)
        self.result_label.config(text=text)

    def _close(self):
        # убрать отложенный after
        if self.after_id and self.root:
            self.root.after_cancel(self.after_id)
        if self.root:
            self.root.destroy()
            self.root = None
