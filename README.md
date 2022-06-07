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

### Przygotowanie danych

1. Folder zawierający teksty do analizy dla skryptu. Poszczególne pliki powinny mieć formar `<identyfikator>.txt`

2. Plik Json zawierający metadane dla artykułów. Powinien on zawierać następujące pola:
* `id`: Identyfikator, taki sam jak nazwa pliku `.txt` zawierającoego dany tekst.
* `title`: Tytuł tekstu.
* `date`: Data publikacji\\utowrzenia danego tekstu.
* `key`: Lista dodatkowych tagów opisujących dany tekst.
* `source`\\`src`: Źródło\\autor danego tekstu.

Każde z powższych pól jest opcjonalne.

### Uruchumienie aplikcji

1. Przetworzenie danych

```
python3 main.py [options] <path_to_folder_with_articles> <json_describing_loaded_articles>
```

Options are:
* `--no_morph` (`-nm`): Do not use morpheus2 text simplification tool.
* `--fasttext` (`-ft`): Use fasttext text analysis.
* `--tf_idf` (`-ti`): Use tf_idf text analysis.


2. Wyświetlenie wykresów

```
python3 frontend.py <umap_vectors_file>
```
