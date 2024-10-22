FROM nodered/node-red:latest

# Copier le package.json
COPY package.json /data/package.json

# Définir le répertoire de travail
WORKDIR /data

# Installer les dépendances en tant que root et configurer les permissions
USER root
RUN npm install --unsafe-perm --no-update-notifier --no-audit --no-fund && \
    chown -R node-red:root /data && \
    chmod -R 775 /data

# Revenir à l'utilisateur node-red
USER node-red

# Créer un fichier flows.json vide s'il n'existe pas
RUN touch /data/flows.json

# Utiliser directement la commande node-red
ENTRYPOINT ["node-red", "--userDir", "/data"]