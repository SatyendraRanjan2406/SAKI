#!/bin/bash

# Update system packages
sudo yum update -y

# Install required packages
sudo yum install -y python3 python3-devel nginx git gcc

# Install virtualenv
sudo pip3 install virtualenv

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install project dependencies
pip install -r requirements.txt

# Install gunicorn
pip install gunicorn

# Configure Nginx
sudo tee /etc/nginx/conf.d/saki.conf << EOF
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ec2-user/SAKI;
    }

    location / {
        proxy_set_header Host \$http_host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

# Remove default Nginx configuration
sudo rm -f /etc/nginx/conf.d/default.conf

# Configure Gunicorn
sudo tee /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=ec2-user
Group=nginx
WorkingDirectory=/home/ec2-user/SAKI
ExecStart=/home/ec2-user/SAKI/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          SakiProject.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Create Gunicorn socket
sudo tee /etc/systemd/system/gunicorn.socket << EOF
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

# Create directory for Gunicorn socket
sudo mkdir -p /run/gunicorn
sudo chown ec2-user:nginx /run/gunicorn

# Start and enable Gunicorn
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate

# Create superuser (optional, uncomment if needed)
# python manage.py createsuperuser

# Set proper permissions
sudo chown -R ec2-user:nginx /home/ec2-user/SAKI
sudo chmod -R 775 /home/ec2-user/SAKI

# Configure SELinux
sudo setsebool -P httpd_can_network_connect 1

# Restart services
sudo systemctl restart gunicorn
sudo systemctl restart nginx 