
---install nodejs
curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
sudo apt-get install -y nodejs

---check whether npm and nodejs have been installed successfully
npm -v
node -v

---install nginx
sudo apt-get install nginx

---install couchDB driver nano
npm install nano

---run the web server
nohup node index.js &