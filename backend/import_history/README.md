# Import History / История импортов / Importverlauf

**🇷🇺** Здесь хранятся отдельные скрипты для каждого нового импорта HerzeLied.

**🇬🇧** Separate import scripts for each new HerzeLied import session.
Each session has its own script to keep the import history organized.
New albums, singles and other content are imported independently.

**🇩🇪** Separate Import-Skripte für jede neue HerzeLied-Importsitzung.
Jede Importsitzung hat ihr eigenes Skript, damit die Importgeschichte übersichtlich bleibt.
Neue Alben, Singles und andere Inhalte werden unabhängig voneinander importiert.

Запуск из корня проекта:

```bash
python -m backend.import_history.import_<session>
```

Старые импорты находятся в `import_media.py`, `import_songs.py` и `import_text.py`.
