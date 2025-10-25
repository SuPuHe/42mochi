# src/App/Services/FortyTwoApiService.py
import httpx
from typing import Dict, Any, Optional

class FortyTwoApiService:
    def __init__(self, session: Dict[str, Any]):
        """Инициализация клиента с токеном из сессии."""
        self.session = session
        self.access_token = self.session.get('access_token')
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        # httpx.AsyncClient используется для выполнения запросов
        self.client = httpx.AsyncClient(headers=self.headers, base_url="https://api.intra.42.fr/v2")

    async def _fetch_api(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Общий метод для безопасного получения данных из 42 API."""
        if not self.access_token:
            return None

        try:
            response = await self.client.get(endpoint)
            response.raise_for_status() # Вызывает исключение для 4xx/5xx ошибок
            return response.json()
        except httpx.HTTPStatusError as e:
            # Обработка ошибки, например, просроченного токена
            print(f"42 API Error on {endpoint}: {e}")
            return None
        except Exception as e:
            print(f"General API Error on {endpoint}: {e}")
            return None

    async def get_user_data(self) -> Dict[str, Any]:
        """Получает и кэширует информацию о пользователе (/me)."""
        if 'user_info' in self.session:
            return self.session['user_info']

        user_data = await self._fetch_api("/me")
        if user_data:
            self.session['user_info'] = user_data

        return user_data if user_data else {}

    async def get_coalition_data(self, user_id: int) -> Dict[str, str]:
        """Получает и кэширует информацию о коалиции."""
        if 'coalition_info' in self.session:
            return self.session['coalition_info']

        coalition_info = {'coalition': 'None', 'color': '#ccc'}

        if user_id:
            coal_data = await self._fetch_api(f"/users/{user_id}/coalitions")

            if coal_data and isinstance(coal_data, list) and len(coal_data) > 0:
                coalition_info['coalition'] = coal_data[0].get('name', 'None')
                coalition_info['color'] = coal_data[0].get('color', '#ccc')

        self.session['coalition_info'] = coalition_info
        return coalition_info

    def parse_user_details(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Разбирает данные пользователя, извлекая необходимые поля (аналог логики PHP)."""

        # Логика извлечения уровня (cursus_id 21)
        level = 0
        for cursus in user_data.get('cursus_users', []):
            if cursus.get('cursus_id') == 21:
                level = cursus.get('level', 0)
                break

        return {
            'login': user_data.get('login', 'Unknown'),
            'first_name': user_data.get('first_name', 'Unknown'),
            'last_name': user_data.get('last_name', ''), # В PHP это было сложнее, упростим
            'campus': user_data.get('campus', [{}])[0].get('name', 'Unknown'),
            'level': level,
        }
