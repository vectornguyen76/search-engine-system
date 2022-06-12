# Search Engine on Shopee
This is a project about Image Retrieval. You can search Men Clothes on Shopee by image. It is the same as google image search

# Website
[https://search.vectornguyen.com/](https://search.vectornguyen.com/)

# How to Deploy on Nginx - Ubuntu Server 18.04
## 1. Update and upgrade
```
sudo apt update
sudo apt upgrade
```
## 2. Install Nginx
```
sudo apt install nginx
```
## 3. Create 1 file on sites-enabled in Nginx
```
sudo nano /etc/nginx/sites-enabled/flask_app
```
## 4. Add context
```
server {
	listen 80;

	server_name your_domain.com; //if you have domain

	location / {
		proxy_pass http://127.0.0.1:8000;
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-For- $proxy_add_x_forwarded_for;
	}
}
```
## 5. Unlink default file on site-enabled
```
sudo unlink /etc/nginx/sites-enabled/default
```
## 6. Edit the conf file of nginx
```
nano /etc/nginx/nginx.conf
```
## 7. Add a line in the http, server or location section
```
client_max_body_size 20M;
```
## 8. Test to make sure that there are no syntax errors in any of your Nginx files
```
sudo nginx -t
```
## 9. Reload Nginx
```
sudo nginx -s reload
```
## 10. Install python 3.8
```
sudo apt install python3-pip

sudo apt install python3.8
```
## 11. Add python3 choice using python3.6
```
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
```
## 12. Add python3 choice using python3.8
```
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 2
```
## 13. Install pip and requirements.txt
```
pip3 install --upgrade pip

pip3 install -r requirements.txt
```
## 14. Install gunicorn3
```
sudo apt install gunicorn3
```
## 15. Finally build and run app on gunicorn3
```
gunicorn3 --bind=0.0.0.0 --timeout 200 app:app --daemon
```
## 15. Kill gunicorn3 if you stop the app
```
sudo pkill -f gunicorn3
```
# Model
![image](https://user-images.githubusercontent.com/80930272/159145415-4fbdb6b4-0f13-4aab-bcff-5cdb4cad2460.png)

# Cosine Similarity
![image](https://user-images.githubusercontent.com/80930272/159145489-549915ca-476c-480d-9cfa-1e54c7725a17.png)

# Result 
![Screenshot 2022-03-24 132528](https://user-images.githubusercontent.com/80930272/159855740-f89c031a-80a2-4aed-a1bb-e403b837772a.png)
![Screenshot 2022-03-24 132554](https://user-images.githubusercontent.com/80930272/159855745-af4bbf92-f871-4b37-9a78-041eb9100ba3.png)
![Screenshot 2022-03-24 132613](https://user-images.githubusercontent.com/80930272/159855755-f257c721-5801-4af3-bf43-c7e2c3e761ea.png)
![Screenshot 2022-03-24 132629](https://user-images.githubusercontent.com/80930272/159855762-98a435bf-5679-40a1-b2bd-f18a602f5c73.png)
![Screenshot 2022-03-24 132703](https://user-images.githubusercontent.com/80930272/159855772-eec805d6-945c-4652-a37c-3fbd703419e9.png)

# Reference
- Datasets: https://shopee.vn/
