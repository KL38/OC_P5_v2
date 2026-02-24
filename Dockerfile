# On utilise l'image officielle Python 3.13.5
FROM python:3.13.5-slim

# On définit le répertoire de travail dans le container
WORKDIR /app

# On copie d'abord le fichier requirements pour profiter du cache Docker
COPY requirements.txt .

# Installation des dépendances
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# On copie le contenu du dossier local app dans le dossier du container
COPY ./app

# Port par défaut pour Hugging Face Spaces
EXPOSE 7860

# Commande pour lancer l'API
# On utilise 0.0.0.0 pour que l'API soit accessible de l'extérieur du container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]