## Opis projektu

Niniejszy projekt stanowi kompletny system służący do:

- **Symulacji pracy czterech typów sensorów** (temperatury, wilgotności, ciśnienia, oświetlenia, jakości powietrza oraz innych, możliwych do dodania),  
- **Logowania odczytów** do plików CSV z automatyczną rotacją i retencją,  
- **Komunikacji sieciowej** (TCP) umożliwiającej udostępnianie danych z sensorów do zdalnych klientów,  
- **Wizualizacji w czasie rzeczywistym** poprzez prosty interfejs graficzny (Tkinter),  
- **Analizy i wizualizacji historycznych danych** z użyciem Jupyter Notebook (Pandas, Matplotlib),  
- **Obsługi testów jednostkowych** w celu weryfikacji poprawności implementacji każdego modułu.

Projekt ma charakter edukacyjno-praktyczny – demonstruje, jak w sposób modułowy i skalowalny stworzyć system monitoringu czujników, który można łatwo rozszerzać o nowe typy urządzeń, protokoły czy interfejsy.

---

## Funkcjonalności

1. **Symulacja Sensorów**  
   - Generowanie odczytów z czujników temperatury, wilgotności, ciśnienia, oświetlenia, jakości powietrza i innych w oparciu o losowe wartości lub funkcje matematyczne (sinusoidalne, gaussowskie, skokowe fluktuacje).  
   - Metody pozwalające na start/stop symulacji oraz opcjonalną kalibrację.

2. **Logowanie Danych**  
   - Zapis odczytów w postaci wierszy CSV: `timestamp, sensor_id, value, unit`.  
   - Automatyczna rotacja plików: kiedy plik przekroczy zdefiniowany rozmiar (w MB) lub pewną liczbę kopii zapasowych, tworzony jest nowy plik, a stare archiwizowane.

3. **Komunikacja Sieciowa (TCP)**  
   - Prosty **serwer TCP** (klasa `NetworkServer`), który co wywołanie przesyła JSON-em najnowsze odczyty wszystkich czujników do każdego połączonego klienta, wysyłając kolejne wiersze w strumieniu.  
   - Prosty **klient TCP** (klasa `NetworkClient`), który łączy się z serwerem, odbiera JSON-wiadomości i (opcjonalnie) przekazuje je dalej (np. do GUI lub innej aplikacji).

4. **GUI (Tkinter)**  
   - Aplikacja desktopowa z tabelą prezentującą aktualne odczyty wszystkich aktywnych czujników.  
   - Możliwość włączenia / wyłączenia symulacji (uruchomienie wbudowanego serwera TCP w tle).  
   - Obliczanie średnich ruchomych (1h, 12h) w locie i wyświetlanie ich w tabeli.  
   - Pasek statusu informujący o stanie (nasłuchiwanie na porcie, zatrzymany, błąd).

5. **Analiza Danych (Jupyter Notebook)**  
   - Wczytanie wszystkich plików CSV z katalogu `logs/`, automatyczne sklejanie w jeden DataFrame.  
   - Konwersja kolumn (`timestamp`, `value`), usuwanie wadliwych / pustych wierszy.  
   - Podstawowe statystyki opisowe dla każdej grupy `sensor_id`.  
   - Wizualizacja odczytów jako wykresy w czasie, obliczenie i narysowanie średnich ruchomych (rolling window).  
   - Eksport oczyszczonych danych do nowego pliku CSV.

6. **Testy Jednostkowe**  
   - Moduł `tests/` zawiera testy dla każdego typu sensora (`test_sensors.py`), testy dla klienta/serwera sieciowego (`test_network.py`), testy modułu loggera (`test_logger.py`) oraz (opcjonalnie) testy GUI (`test_gui.py`).  
   - Uruchamianie z użyciem `pytest` po instalacji zależności.

---

## Wymagania wstępne

- **Python 3.9+** (zalecane 3.9 lub 3.10; działa również na 3.11)  
- System operacyjny: Windows / Linux / macOS  
- Przynajmniej **100 MB wolnego miejsca** (na instalację pakietów i pliki CSV w folderze `logs/`)  

### Biblioteki Python

Projekt wymaga następujących bibliotek (zawartych w `requirements.txt`):

- **pandas** – do analizy danych (w notebooku), operacji na CSV, resamplingu i rollingu.  
- **numpy** – wewnętrznie używane przez niektóre generatory (choć wiele bazuje także na `random` z Pythona).  
- **matplotlib** – wykresy i wizualizacja w notebooku.  
- **scipy** – (opcjonalnie) do rozszerzonej analizy statystycznej i rozkładów (np. gaussian noise).  
- **pyyaml** – do wczytywania konfiguracji sieciowej (plik `network/config.yaml`).  
- **pytest** – do uruchamiania testów jednostkowych.  

---

## Instalacja i uruchomienie

Poniżej krok po kroku opisano, jak sklonować repozytorium, utworzyć wirtualne środowisko, zainstalować wymagania i uruchomić poszczególne moduły projektu.

### 1. Klonowanie repozytorium

Otwórz terminal (PowerShell / Bash / CMD) i przejdź do katalogu, w którym chcesz umieścić projekt, np.:

### 2. Utworzenie i aktywacja wirtualnego środowiska
python -m venv .venv
.\.venv\Scripts\Activate.ps1

### 3. Instalacja zależności
Gdy środowisko jest aktywne, zainstaluj pakiety z requirements.txt:
pip install --upgrade pip
pip install -r requirements.txt

### 4. Uruchomienie poszczególnych modułów
a) Uruchomienie serwera TCP
Sprawdź zawartość network/config.yaml – domyślnie może wyglądać tak:
Uruchom serwer:
python -m network.server
b) Uruchomienie klienta TCP (opcjonalne)
Jeżeli chcesz samodzielnie przetestować, co serwer wysyła,
w drugiej konsoli (również z aktywnym .venv) uruchom prostego skryptu-klienta. Na przykład możesz utworzyć plik network/test_client.py z zawartością:
# network/test_client.py
import socket
import yaml
import json

# Wczytanie konfiguracji
with open("network/config.yaml") as f:
    cfg = yaml.safe_load(f)
host = cfg['server']['host']
port = cfg['server']['port']

# Nawiązywanie połączenia
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((host, port))
    # Odbieramy kilkanaście wierszy JSON (jeden JSON + \n = jeden odczyt)
    for _ in range(5):
        data = sock.recv(1024)
        if not data:
            break
        print(json.loads(data.decode().strip()))
c) Uruchomienie GUI
Aby zobaczyć interfejs graficzny z tabelą w czasie rzeczywistym, w nowej konsoli przejdź do głównego katalogu projektu i:
python gui/app.py
d) Analiza danych w Jupyter Notebooku
Upewnij się, że w folderze logs/ znajdują się pliki sensors_YYYYMMDD.csv (np. sensors_20250531.csv).
Uruchom środowisko Jupyter:
W przeglądarce otworzy się panel Jupyter; kliknij na analysis/analysis.ipynb.

W pierwszych komórkach Notebooka wykonaj polecenia (Shift+Enter), aby:

Zmienić bieżący katalog na katalog główny projektu,

Wczytać wszystkie pliki CSV z logs/,

Połączyć je w jeden DataFrame,

Dokonać konwersji kolumn (timestamp, value),

Usunąć wiersze zawierające puste/nieprawidłowe wartości,

Wyświetlić podstawowe statystyki opisowe,

Narysować wykresy oryginalnych odczytów i średnich ruchomych.

Całość kodu w Notebooku przygotowana jest tak, by krok po kroku pokazać cały proces analizy i wizualizacji.

e) Uruchamianie testów jednostkowych
Aby przetestować poprawność modułów, uruchom w głównym katalogu:
pytest

## Struktura katalogów:
Poniżej prezentowana jest hierarchia plików i katalogów oraz krótka charakterystyka zawartości:
py2025-project-v1-131439/
├── .gitignore
├── README.md                  ← Ten plik
├── requirements.txt           ← Lista wszystkich bibliotek (pandas, numpy, matplotlib, scipy, pyyaml, pytest)
├── sensors/                   ← Moduł odpowiedzialny za symulację sensorów
│   ├── __init__.py
│   ├── sensor.py              ← Klasa bazowa Sensor
│   ├── temperature_sensor.py  ← Symulacja czujnika temperatury (-20°C–50°C, sinusoidalnie)
│   ├── humidity_sensor.py     ← Symulacja czujnika wilgotności (0–100%, szum gaussowski)
│   ├── pressure_sensor.py     ← Symulacja czujnika ciśnienia (950–1050 hPa, lekka fluktuacja)
│   ├── light_sensor.py        ← Symulacja czujnika oświetlenia (0–10000 lx, cykl dobowy)
│   ├── air_quality_sensor.py  ← Symulacja czujnika jakości powietrza (0–500 AQI, skoki co 5% szansy)
│   
│
├── logger/                    ← Moduł odpowiedzialny za zapisywanie odczytów do CSV
│   ├── __init__.py
│   ├── config.json            ← Konfiguracja loggera (katalog logów, wzorzec nazwy pliku, rozmiar, retencja, bufor)
│   └── logger.py              ← Klasa Logger:
│                                • log_reading(sensor_id, timestamp, value, unit)  
│                                • rotacja plików po przekroczeniu rozmiaru  
│                                • tworzenie nowego pliku CSV z nagłówkiem
│
├── network/                   ← Moduł komunikacji sieciowej (TCP)
│   ├── __init__.py
│   ├── config.yaml            ← Konfiguracja serwera (host, port, timeout, retries)
│   ├── server.py              ← Klasa NetworkServer (nasłuchiwanie, obsługa klientów, wysyłanie JSON)
│   └── client.py              ← Klasa NetworkClient (connect, send, close)
│
├── gui/                       ← Graficzny interfejs użytkownika (Tkinter)
│   ├── __init__.py
│   └── app.py                 ← Klasa App(tk.Tk):
│                                • przyciski Start/Stop, pole portu  
│                                • tabela z kolumnami: Sensor | Wartość | Jednostka | Timestamp | Śr. 1h | Śr. 12h  
│                                • w tle wątek zbierający odczyty, liczący średnie i logujący do CSV  
│                                • pasek statusu (Stopped / Listening on port …)
│
├── analysis/                  ← Notebook Jupyter do analizy historycznych danych
│   └── analysis.ipynb         ← Krok po kroku:
│                                1. Ustawienie bieżącego katalogu  
│                                2. Import bibliotek (pandas, matplotlib, glob)  
│                                3. Odszukanie wszystkich plików „logs/sensors_*.csv”  
│                                4. Połączenie w jeden DataFrame (pandas.concat)  
│                                5. Konwersja i czyszczenie danych (to_datetime, to_numeric, dropna)  
│                                6. Statystyki opisowe (groupby + describe)  
│                                7. Rysowanie odczytów w czasie  
│                                8. Obliczanie średnich ruchomych (rolling(60), rolling(720))  
│                                9. Rysowanie wykresów oryginalnych odczytów + średnich ruchomych  
│                               10. Eksport oczyszczonych danych do CSV  
│
├── logs/                      ← Katalog, w którym logger zapisuje pliki CSV
│   └── sensors_YYYYMMDD.csv   ← Przykładowy plik wygenerowany przez Logger, np.  
│                                sensors_20250531.csv  
│
├── tests/                     ← Testy jednostkowe (pytest)
│   ├── __init__.py
│   ├── test_sensors.py        ← Testy dla poszczególnych sensorów (Temperature, Humidity, Pressure, Light, AirQuality)
│   ├── test_logger.py         ← Testy modułu logger (zapis do pliku, rotacja, bufor)
│   ├── test_network.py        ← Testy dla NetworkClient i NetworkServer (poprawność serializacji JSON, reconnect)
│   └── test_gui.py            ← Testy GUI (inicjalizacja okna, tytuł, podstawowe widgety)
│
└── …                          ← Dodatkowe pliki pomocnicze (np. README.md)

## Opis modułów
a) Moduł sensors
Ten moduł to serce symulacji – definiuje klasy abstrakcyjne i konkretne implementacje różnych czujników. Bieżąca zawartość:

sensor.py
Klasa bazowa Sensor, zapewniająca wspólny interfejs do symulacji odczytów. Metody:

__init__(sensor_id, name, unit, min_value, max_value, frequency) – inicjalizacja czujnika.

read_value() – zwraca syntetyczny odczyt w zadanym zakresie (w bazowej implementacji: losowa wartość z przedziału [min_value, max_value]).

calibrate(factor) – mnoży ostatni odczyt przez współczynnik kalibracji.

get_last_value() – zwraca ostatnio wygenerowaną wartość, jeśli jest, w przeciwnym razie wywołuje read_value().

start(), stop() – włączanie/wyłączanie symulacji (flaga active).

__str__() – ładne wyświetlanie id i nazwy czujnika.

temperature_sensor.py
class TemperatureSensor(Sensor)

Symuluje cykl dobowy temperatury (funkcja sinusoidalna).

Parametry domyślne:

min_value=-20.0, max_value=50.0, frequency=1 (sekunda).

humidity_sensor.py
class HumiditySensor(Sensor)

Losowo generuje wilgotność od 0% do 100% z niewielkim szumem gaussowskim (noise = random.gauss(0, 2)).

Wartość jest obcinana do zakresu [min_value, max_value].

Parametry domyślne: min_value=0.0, max_value=100.0, frequency=1.

pressure_sensor.py
class PressureSensor(Sensor)

Parametry domyślne: min_value=950.0, max_value=1050.0, frequency=1.

Generuje ciśnienie w podanym przedziale, z niewielkimi fluktuacjami (np. noise = random.gauss(0, 0.5)), symulując zjawiska meteorologiczne.

light_sensor.py
class LightSensor(Sensor)

Symuluje natężenie oświetlenia (0 lx – noc; 10 000 lx – słoneczny dzień).

Przyjmuje, że pełny cykl dobowy (od 0 lx do max i z powrotem) trwa 24 h (86 400 s).


AQI w zakresie [0, 500].

Domyślnie rozpoczynamy od losowej wartości z przedziału [20, 80].

Każde wywołanie read_value() generuje:

z prawdopodobieństwem 5% nagły wzrost do zakresu [200, max],

w przeciwnym razie dodaje mały losowy szum gaussowski ±10, obcinając wynik do przedziału [min, max], aby symulować łagodne wahania jakości powietrza.

b) Moduł logger
Moduł odpowiedzialny za zapisywanie odczytów do plików CSV z automatycznym rotowaniem:

config.json
Konfiguracja loggera w formacie JSON:
{
  "log_dir": "./logs",
  "filename_pattern": "sensors_%Y%m%d.csv",
  "max_size_mb": 5,
  "backup_count": 5,
  "buffer_size": 100
}
log_dir: katalog, w którym przechowywane są pliki logów (domyślnie ./logs).

filename_pattern: wzorzec nazwy pliku, np. sensors_20250531.csv.

max_size_mb: maksymalny rozmiar pliku (w MB) przed rotacją.

backup_count: ile kopii zapasowych (z sufiksami .1, .2, …) ma być przechowywane.

buffer_size: ile rekordów trzymamy w pamięci, zanim wymusimy flush() do pliku.

logger.py
Klasa Logger:

__init__(self, config_path="logger/config.json")

Wczytuje plik konfiguracyjny JSON, tworzy katalog log_dir (jeśli nie istnieje) i wywołuje _open_file().

_open_file(self)

Generuje nazwę pliku wg filename_pattern (np. sensors_20250531.csv) i otwiera go do zapisu w trybie "a".

Jeśli plik jest nowy, zapisuje nagłówek: ["timestamp", "sensor_id", "value", "unit"].

log_reading(self, sensor_id, timestamp, value, unit)

Dodaje nowy wiersz [timestamp.isoformat(), sensor_id, value, unit] do bufora _buffer.

Jeśli rozmiar bufora >= buffer_size, wywołuje _flush().

Następnie sprawdza, czy trzeba dokonać rotacji pliku (_rotate_if_needed()).

_flush(self)

Zapisuje zawartość bufora na dysk (metodą writer.writerow(row)) i wywołuje file.flush().

Czyści bufor.

_rotate_if_needed(self)

Sprawdza rozmiar pliku (MB) i jeśli >= max_size_mb, wywołuje _rotate().

_rotate(self)

Zamknięcie bieżącego pliku, zmiana nazw kopii zapasowych według backup_count (.1 → .2, .2 → .3, …), przeniesienie bieżącego pliku do .1.

Wywołuje ponownie _open_file(), aby utworzyć nowy plik do dalszego logowania.

read_logs(self, start, end, sensor_id=None)

(Opcjonalnie) Iteruje wstecz przez pliki CSV w log_dir/, zwraca tylko wpisy w przedziale [start, end] i (ewentualnie) dla zadanego sensor_id.

W obecnej wersji domyślnie zgłasza NotImplementedError. Można rozbudować według potrzeb.

c) Moduł network
Odpowiada za moduł serwer/klient w oparciu o protokół TCP i format JSON.

config.yaml
server.py
Klasa NetworkServer:

__init__(self, config_path="network/config.yaml")

Wczytuje ustawienia z pliku YAML (host, port).

Inicjuje listę sensorów:

python
Kopiuj
Edytuj
self.sensors = [
    TemperatureSensor('temp1'),
    HumiditySensor('hum1'),
    PressureSensor('pres1')
]
Tworzy gniazdo TCP (socket.socket(...)) z opcją SO_REUSEADDR.

start(self)

bind((host, port)), listen(5), a następnie w pętli głównej:

python
Kopiuj
Edytuj
client, _ = self.sock.accept()
threading.Thread(target=self._handle_client, args=(client,), daemon=True).start()
_handle_client(self, client)

Dla każdego czujnika w self.sensors wywołuje read_value(), tworzy słownik:

python
Kopiuj
Edytuj
data = {
    'sensor': s.sensor_id,
    'value': s.read_value(),
    'unit': s.unit,
    'timestamp': datetime.now().isoformat()
}
Serializuje go do JSON (json.dumps(data) + '\n') i wysyła do client.send(...).

Po wysłaniu wszystkich czujników zamyka połączenie client.close().

W razie błędów (np. wyjątek odczytu), wypisuje Client error: ... i zamyka gniazdo.

client.py
Klasa NetworkClient (prosty klient TCP):

__init__(self, host, port, timeout=5.0, retries=3)

Inicjalizacja parametrów połączenia: self.host, self.port, self.timeout, self.retries.

self.sock = None.

connect(self)

Tworzy socket.socket(), ustawia settimeout(self.timeout), wywołuje sock.connect((host, port)).

Jeśli nie uda się nawiązać, próbuje ponownie (do retries razy).

send(self, data: dict) → bool

Serializuje data do JSON (json.dumps(data).encode()).

Wywołuje sock.send(...).

Oczekuje potwierdzenia od serwera (np. w postaci 'ACK\n').

Zwraca True/False w zależności od powodzenia.

close(self)

Zamknięcie gniazda (self.sock.close()).

d) Moduł gui
Graficzny interfejs użytkownika (Tkinter), w którym:

Tworzymy główne okno (class App(tk.Tk)), w którym znajdują się:

Górny pasek przycisków:

Pole tekstowe Port: (domyślnie 9999).

Przycisk Start → uruchamia symulację + wątek, który co sekundę pobiera odczyty sensorów.

Przycisk Stop → zatrzymuje symulację i zatrzymuje pingowanie.

Tabela (Treeview):

Kolumny: ("Sensor", "Wartość", "Jednostka", "Timestamp", "Śr. 1h", "Śr. 12h").

Po każdym odczycie:

Aktualna wartość (z czujnika) jest logowana do CSV: self.logger.log_reading(sid, now, val, unit).

Doliczane są średnie ruchome z historii (ostatnia godzina, ostatnie 12 godzin).

Tabela jest aktualizowana (jeśli iid istnieje, to update, w przeciwnym razie insert).

Pasek stanu (Status Bar):

Pokazuje aktualny stan serwera:

"Stopped" – gdy symulacja jest zatrzymana.

"Listening on port {port}" – gdy symulacja/serwer jest włączony.

Tryb multi‐thread:

Gdy naciśniesz Start, tworzy się wątek (daemon) wywołujący _update_loop().

W pętli _update_loop() co sekundę pobierane są nowe wartości z czujników i logowane.

Dodatkowo wzbogacamy wektor historycznych odczytów (self.history[sid].append((now, val))), aby liczyć rolling‐average.

Kod implementacji znajduje się w gui/app.py i zawiera detale dotyczące stylizacji ttk.Style, budowy interfejsu, obsługi zdarzeń Start/Stop oraz wątku czytającego dane.

e) Moduł analysis
To Jupyter Notebook (analysis.ipynb) służący do przeprowadzenia analizy historycznych danych. Główne kroki:
Ustawienie bieżącego katalogu
Import bibliotek
Wczytanie listy plików CSV
Połączenie wszystkich plików w jeden DataFrame
Konwersja i czyszczenie danych
Podstawowe statystyki opisowe
Wizualizacja odczytów w czasie (dla wszystkich sensorów)
Obliczenie średnich ruchomych (rolling) dla jednego wybranego czujnika
Rysowanie wykresu
Eksport oczyszczonych danych
f) Moduł tests
Testy jednostkowe realizowane za pomocą pytest.

tests/test_sensors.py

Testuje, czy każdy z czterech typów sensorów (TemperatureSensor, HumiditySensor, PressureSensor, LightSensor, AirQualitySensor) zwraca wartości mieszczące się w swoim zadanym przedziale:

python
Kopiuj
Edytuj
def test_temperature():
    s = TemperatureSensor('t')
    v = s.read_value()
    assert s.min_value <= v <= s.max_value
Dla LightSensor sprawdzamy, że po dwóch wywołaniach read_value() nadal mieści się w min_value–max_value.

Dla AirQualitySensor sprawdzamy, że w 100 próbach pojawi się co najmniej raz wartość ≥ 200 (co jest bardzo prawdopodobne przy p=5% na skok).

tests/test_logger.py

Testuje:

Inicjalizację Logger(config_path) i tworzenie katalogu log_dir.

Metodę log_reading(): czy po np. 1000 wywołaniach plik rotuje poprawnie (zmiana nazw sensors_YYYYMMDD.csv → sensors_YYYYMMDD.csv.1 → …).

Buforowanie: czy po przekroczeniu buffer_size następuje rzeczywisty zapis w pliku.

(Opcjonalnie) Czy read_logs() rzuca NotImplementedError.

tests/test_network.py

Testuje, czy NetworkServer poprawnie odczytuje config.yaml.

Sprawdza, czy NetworkClient nawiązuje połączenie, wysyła dane w formacie JSON i odbiera potwierdzenie ACK.

(Można dokładniej testować symulację błędów timeout/ponowienia).

tests/test_gui.py

Test GUI:

Czy App().title to "Network Server GUI".

Czy po inicjalizacji wszystkie widgety (pole portu, przyciski, tabela, pasek stanu) istnieją i mają odpowiednie domyślne wartości.

(Opcjonalnie) Można zasymulować kliknięcie Start i sprawdzić, czy wątek działa.




