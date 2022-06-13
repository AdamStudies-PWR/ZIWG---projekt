# ZIWG - projekt
Projekt na przedmiot Zastosowania informatyki w gospodasrce na politechnike wrocławską

Grupa E

Temat projektu: Relacje podobieństwa treści dla dużego zbioru

## Instrukcje

Poniższe instrukcje zostały przygotowane i przetestowane pod system z rodziny Linux.

### Przygotowanie środowiska

```
python3 -m venv venv/
```

```
. venv/bin/activate
```

```
pip3 install -r requirements.txt
```
Dodatkowo dla metody FastText konieczne jest pobranie modelu bin dla języka polskiego ze strony [projektu fasttext](https://fasttext.cc/docs/en/crawl-vectors.html)

### Przygotowanie danych

1. Folder zawierający teksty do analizy dla skryptu. Poszczególne pliki powinny mieć formar `<identyfikator>.txt`

2. Plik Json zawierający metadane dla artykułów. Powinien on zawierać następujące pola:
* `id`: Identyfikator, taki sam jak nazwa pliku `.txt` zawierającoego dany tekst.
* `title`: Tytuł tekstu.
* `date`: Data publikacji\\utworzenia danego tekstu.
* `key`: Lista dodatkowych tagów opisujących dany tekst.
* `source`\\`src`: Źródło\\autor danego tekstu.

Każde z powższych pól jest opcjonalne.

### Uruchomienie aplikcji

1. Przetworzenie danych

```
python3 main.py [options] <path_to_folder_with_articles> <json_describing_loaded_articles>
```

Dostępne opcje:
* `--no_morph` (`-nm`): Nie używaj narzędzia morpheus2 do uproszczenia tekstu wejściowego.
* `--fasttext` (`-ft`): Użyj metody TastText.
* `--tf_idf` (`-ti`): Użyj metody Tf_Idf.


2. Wyświetlenie wykresów

```
python3 frontend.py <umap_vectors_file>
```

### Docker

Podwyższy projekt umożliwia uruchomienie go w kontenerze, aby to zrobić należy użyć następującej komendy z poziomu folderu, w którym znajduje się aplikacja:

```
docker-compose up -d
```

W celu "wejścia" do kontenera i uruchamiania komend z jego poziomu można użyć komendy:

```
docker exec -it ziwg bash
```

Pliki znajdujące się w lokalizacji projektu zostaną przeniesione do kontenera i będą dostępne pod ścieżką /app
