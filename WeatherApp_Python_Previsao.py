import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests

widgets = {}  # Dicionário para armazenar os widgets

def get_long_term_forecast(city, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city.strip(),
        'appid': api_key.strip(),
        'units': 'metric',
        'lang': 'pt'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    elif response.status_code == 404:
        return None  # Retornar None se a cidade não for encontrada
    elif response.status_code == 401:
        return None  # Retornar None se houver erro de autenticação
    else:
        return None  # Retornar None para outros erros

def format_forecast_data(data):
    formatted_text = ""
    if data:
        city = data['city']['name']
        formatted_text += f"Previsão do tempo de longo prazo para {city}:\n\n"
        for forecast in data['list']:
            date = forecast['dt_txt']
            weather_description = forecast['weather'][0]['description']
            temperature = forecast['main']['temp']
            formatted_text += f"Data: {date}\nCondição: {weather_description}\nTemperatura: {temperature}°C\n\n"
    else:
        formatted_text = "Não foi possível obter a previsão do tempo de longo prazo."
    return formatted_text

def fetch_weather():
    city = widgets['city_entry'].get()
    if not city:
        messagebox.showerror("Erro", "Por favor, digite o nome da cidade.")
        return
    
    weather_data = get_long_term_forecast(city, api_key)
    if weather_data:
        formatted_result = format_forecast_data(weather_data)
        widgets['result_text'].config(state='normal')
        widgets['result_text'].delete('1.0', tk.END)  # Limpa o texto anterior
        widgets['result_text'].insert(tk.END, formatted_result)
        widgets['result_text'].config(state='disabled')
    else:
        messagebox.showerror("Erro", "Cidade não encontrada. Verifique o nome e tente novamente.")

def create_app():
    # Configuração da janela principal
    root = tk.Tk()
    root.title('Previsão do Tempo de Longo Prazo')

    # Configurações de estilo
    bg_color = "#f0f0f0"  # Cor de fundo
    font_family = "Helvetica"  # Fonte
    font_size = 12  # Tamanho da fonte

    root.configure(bg=bg_color)

    # Widgets
    title_label = tk.Label(root, text='Previsão do Tempo', bg=bg_color, fg='#333', font=(font_family, 20, 'bold'))
    title_label.pack(pady=10)

    city_frame = tk.Frame(root, bg=bg_color)
    city_frame.pack(pady=20)

    city_label = tk.Label(city_frame, text='Digite o nome da cidade:', bg=bg_color, font=(font_family, font_size))
    city_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

    widgets['city_entry'] = tk.Entry(city_frame, width=30, font=(font_family, font_size))
    widgets['city_entry'].grid(row=0, column=1, padx=10, pady=10)

    widgets['get_weather_button'] = tk.Button(root, text='Obter Previsão', command=fetch_weather, bg='#4CAF50', fg='white', font=(font_family, font_size, 'bold'))
    widgets['get_weather_button'].pack(pady=10)

    # Texto para exibir os resultados com barra de rolagem
    widgets['result_text'] = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, font=(font_family, font_size), bg=bg_color)
    widgets['result_text'].pack(pady=20)

    return root

# Chave da API (substitua pela sua própria chave)
api_key = "262e8bc162b7b6cbb593c0edd59d6be4"

if __name__ == '__main__':
    app = create_app()
    app.mainloop()
