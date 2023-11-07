from flask import Flask, jsonify
from clickhouse_driver import Client
from collections import Counter
import re
import json

app = Flask(__name__)

# Подключение к ClickHouse
client = Client('localhost')

@app.route('/getWords', methods=['GET'])
def get_top_words():
    # Выполнить SQL-запрос, чтобы получить тексты новостей
    query = "SELECT text FROM my_database.news"
    result = client.execute(query)

    # Инициализация счетчика слов
    word_counts = Counter()

    # Обработка текстов новостей по частям
    for row in result:
        text = row[0]
        # Извлечение слов с использованием регулярных выражений
        words = re.findall(r'\w+', text)
        # Обновление счетчика слов
        word_counts.update(words)

    # Получение топ-100 слов
    top_words = word_counts.most_common(100)
    print(top_words)

    response_data = json.dumps(top_words, ensure_ascii=False)
    return response_data, 200, {'Content-Type': 'application/json; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='localhost', port=9090)


