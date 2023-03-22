FROM python:3.11.2
# Alpine Fehlermeldung: Cargo, the Rust package manager, is not installed

# Workdir innerhalb des Containers festlegen
WORKDIR /home/ic20b050/app
# Kopiert das aktuelle Verzeichnis vom Host in das Image Verzeichnis
ADD . /home/ic20b050/app

# installiert die Libraries
RUN pip install --no-cache-dir -r requirements.txt

# gibt den Port 9000 frei
EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
