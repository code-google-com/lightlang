#xgettext --language=Python --keyword=_ --output=slog.pot --from-code=utf-8 slog/MainWindow.py
#msginit --input=slog.pot --locale=ru_RU.UTF-8
#msgfmt --output-file=slog.mo ru.po

SOURCES=../src/*.py
PLUGINS=../plugins/LightLang/__init__.py

default: ru.po
	msgfmt --output-file=slog.mo ru.po

update: $(SOURCES)
	xgettext --language=Python --keyword=_ --keyword=N_ --output=slog.po $(SOURCES) $(PLUGINS) slog.glade.h
	msgmerge -U ru.po slog.po
    
clean:
	rm -f slog.po *.*~
