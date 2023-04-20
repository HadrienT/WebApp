#!/bin/bash
export DEBIAN_FRONTEND=noninteractive

# Update system packages
sudo apt update
sudo apt upgrade -y

# Install necessary packages
sudo apt install -y nginx git python3-pip python3-venv tmux

# Install Certbot
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

# Setup firewall
echo "y" | sudo ufw enable
sudo ufw allow ssh 
sudo ufw allow http 
sudo ufw allow https

# Replace this with the path to your Nginx configuration file
nginx_config_file="/etc/nginx/sites-available/imageinsight.xyz"

# Create Nginx configuration file
sudo tee "$nginx_config_file" <<EOL
server {
    listen 80;
    server_name imageinsight.xyz www.imageinsight.xyz;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}

EOL

# Create symlink for Nginx configuration
sudo ln -s "$nginx_config_file" /etc/nginx/sites-enabled/

# Restart Nginx
sudo systemctl restart nginx

# Replace 'yourdomain.com' and 'www.yourdomain.com' with your actual domain names
domain="imageinsight.xyz"
www_domain="www.imageinsight.xyz"

# Obtain SSL certificate
echo " " | sudo certbot --nginx -d "$domain" -d "$www_domain" --email tramonihadrien@gmail.com --agree-tos --no-eff-email

# Clone the Git repository
git clone https://github.com/HadrienT/WebApp.git
mv .env WebApp/.env
# Change to the cloned repository directory
cd WebApp

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Start the Uvicorn server using tmux
tmux new-session -d -s uvicorn_server 'python3 src/app/run.py'
