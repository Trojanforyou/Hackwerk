#!/bin/bash

echo "🚀 Запуск Ondernemersloket Nederland с DigiD интеграцией..."
echo "📍 URL: http://localhost:8501"
echo ""
echo "🔐 Для тестирования DigiD:"
echo "1. Нажмите кнопку 'Inloggen met DigiD'"
echo "2. Автоматический вход как King Arthur"
echo ""
echo "� Demo пользователь:"
echo "- King Arthur (Camelot Enterprises B.V., Government & Leadership, Den Haag)"
echo ""

# Start the Streamlit app
cd /home/trojanforyou/hackwerk
streamlit run app.py --server.port 8501