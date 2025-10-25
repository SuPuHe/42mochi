# src/App/Services/GameService.py
from typing import Dict, Any
from datetime import datetime
from fastapi import Response

# Импорт set_session_data для обновления сессии после изменения состояния
from App.Utility.session_manager import set_session_data

class GameService:
    def __init__(self, session: Dict[str, Any], response: Response):
        self.session = session
        self.response = response

    def _log_action(self, desc: str, delta: int = 0):
        """Логирует действие в сессию, сохраняя последние 20 записей."""
        self.session.setdefault('logs', [])

        self.session['logs'].append({
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'desc': desc,
            'delta': delta
        })
        # Сохраняем последние 20 логов (array_slice($_SESSION['logs'], -20))
        self.session['logs'] = self.session['logs'][-20:]

    def initialize_state(self):
        """Инициализирует переменные игры в сессии, если они отсутствуют."""
        # Используем .setdefault для имитации PHP-логики инициализации !isset($_SESSION)
        self.session.setdefault('hp', 100)
        self.session.setdefault('days', 0)
        self.session.setdefault('int_food', 0)
        self.session.setdefault('char_food', 0)
        self.session.setdefault('coins', 10)
        self.session.setdefault('logs', [])

        # Переменные из секции 4 (BUTTON ACTIONS)
        self.session.setdefault('mochi_hp', 100) # Предполагаемое начальное значение
        self.session.setdefault('monster_hp', 100) # Предполагаемое начальное значение
        self.session.setdefault('food', 0)
        self.session.setdefault('monster_level', 1)
        self.session.setdefault('hunger', 50) # Предполагаемое начальное значение
        self.session.setdefault('alive', "true") # Для логики 'if ($_SESSION['hp'] == 0) $_SESSION['alive'] = "false";'


    async def handle_action(self, action: str):
        """Обрабатывает игровые действия (action) из POST-запроса."""

        self.initialize_state() # Убеждаемся, что состояние инициализировано

        # --- Обработка действий ---
        if action == 'tick':
            self.session['mochi_hp'] = max(0, self.session.get('mochi_hp', 0) - 5)
            if self.session['mochi_hp'] == 0:
                self.session['monster_hp'] = max(0, self.session.get('monster_hp', 0) - 5)
            self._log_action("Tick passed", 0)

        elif action == 'simulate_day':
            self.session['hp'] = max(0, self.session.get('hp', 0) - 12)
            if self.session['hp'] == 0:
                self.session['alive'] = "false"
            self.session['days'] += 1
            self._log_action("A new day passed (-12 HP, +1 day from birth)", 10) # PHP-код передавал +10

        elif action == 'feed':
            if self.session.get('food', 0) > 0:
                self.session['food'] -= 1
                self.session['hunger'] = min(100, self.session.get('hunger', 0) + 20)
                self.session['monster_hp'] = min(100, self.session.get('monster_hp', 0) + 10)
                self._log_action("Fed monster", 0)

        elif action == 'snack':
            self.session['hunger'] = min(100, self.session.get('hunger', 0) + 10)
            self._log_action("Gave snack", 0)

        elif action == 'work':
            self.session['coins'] += 50
            self._log_action("Worked hard", 50)

        elif action == 'buy_food':
            if self.session.get('coins', 0) >= 30:
                self.session['food'] += 1
                self.session['coins'] -= 30
                self._log_action("Bought food", -30)

        elif action == 'level_up':
            if self.session.get('monster_hp', 0) == 100 and self.session.get('hunger', 0) > 50:
                self.session['monster_level'] = self.session.get('monster_level', 0) + 1
                self.session['monster_hp'] = 50
                self.session['hunger'] = 70
                self._log_action("Monster leveled up!", 0)

        elif action == 'earn_project':
            self.session['coins'] += 50
            self._log_action("Completed project", 50)
        elif action == 'earn_evaluation':
            self.session['coins'] += 20
            self._log_action("Did evaluation", 20)
        elif action == 'earn_streak':
            self.session['coins'] += 50
            self._log_action("Daily streak bonus", 50)
        elif action == 'earn_milestone':
            self.session['coins'] += 200
            self._log_action("Milestone reward", 200)

        # После изменения состояния записываем его обратно в Redis
        await set_session_data(self.response, self.session)


    def get_current_state(self) -> Dict[str, Any]:
        """Возвращает текущие переменные состояния для рендеринга шаблона."""
        self.initialize_state() # Гарантируем наличие всех ключей

        logs = self.session.get('logs', [])
        # array_reverse в PHP -> list(reversed(...)) в Python
        logs_reversed = list(reversed(logs))

        return {
            'hp': self.session['hp'],
            'days': self.session['days'],
            'monster_hp': self.session['monster_hp'],
            'food': self.session['food'],
            'monster_level': self.session['monster_level'],
            'total_coins': self.session['coins'],
            'hunger': self.session['hunger'],
            'logs': logs_reversed
        }
