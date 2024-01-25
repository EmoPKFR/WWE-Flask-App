Key Features:
1. User profiles: Registration and Login; Password management
2. E-commerce: Product catalog; Discount after a certain amount; Order confirmation emails
3. Role-based access: Admin and User roles; Admin dashboard
4. Security measures: Data protection; Data security


Requirements to run the Flask App:

1. Install requirements.txt (pip install -r requirements.txt)

2. In the __init__.py you have to replace MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS, MAIL_USERNAME AND MAIL_PASSWORD with valid ones.
This is example:
app.config['MAIL_SERVER'] =  "your_secret_key"
app.config['MAIL_PORT'] =  "your port, only digits"
app.config['MAIL_USE_TLS'] = "this is True/False"
app.config['MAIL_USERNAME'] =  "your email"
app.config['MAIL_PASSWORD'] =  "you can check about this on the web"

3. In emails.py replace MAIL_USERNAME with your email

4. You can go to /database route
The Admin password is: aaa

Screenshots:

Register form
![Register form](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/e443076b-0c28-4db3-a698-4c2f4092ddc1)
Login form
![Login form](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/5ee185e7-b61e-41cb-825f-c110930e14c4)


