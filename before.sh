# run on host system
sudo apt update
sudo apt install -y git-lfs
sudo git lfs install

git clone "https://github.com/mozilla/firefox-translations-models"
gzip -d firefox-translations-models/models/dev/*/*


