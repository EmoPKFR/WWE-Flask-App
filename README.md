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
Home page
![Home_page](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/17d759d3-2e77-4dca-9fd9-a501ddc62beb)
Logged in as admin
![logged_in_as_admin](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/5cd66822-bfb2-442e-a49f-e0711c2bc6de)
Database (Logged in as admin)
![Database_admin](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/eeab171d-b420-4b6b-87d4-3ce8f486956e)
When a user successfully registers
![When_a_user_successfully_registers](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/8a6986e6-801a-486e-91bf-e072431dc033)
Shop
![Shop](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/021d1488-0694-45b2-bd41-b516cbfb996f)
T-Shirts
![T-shirts](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/07bd8b04-d5b4-4323-a75e-28433ecd0450)
Toys
![Toys](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/3690282e-3d63-4a62-ac61-6b7f9182c7a7)
Clicking on product
![Clicking on product](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/f12c71aa-8a88-4ce6-825c-b7784ca345a6)
Clicking on Basket/Cart
![basket](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/f5d2aa5e-db4f-46c8-8229-bcee5fc44a2f)
Clicking on Profile page
![click_on_the_profile_page](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/b0361fcf-8849-400f-a88e-4eb16d84acb0)
Change password form
![change_password_form](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/46e13d21-a396-467e-8525-ed9cb143c1a4)
Orders history
![Orders_history](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/916cf367-a9b4-4fce-beb7-ff9234b4dd0d)
Shows image 1
![Shows_1](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/1c6cab02-8416-4feb-9f43-e8d04fe79c9e)
Shows image 2
![Shows_2](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/977a92b8-c389-4d41-a776-749935c3c193)
Shows image 3
![Shows_3](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/ca2d964f-3fd6-4463-8731-e5776e3f8c5d)
All Superstars
![Superstars](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/79b465bb-3bef-493e-83b6-1857fd24d536)
Only the Champions
![Only_champions](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/4cfc8b8a-cfed-43ce-9f06-70609ac3749a)
Clicking on a Champion
![Clicking_on_champion](https://github.com/EmoPKFR/WWE-Flask-App/assets/85705360/cd987697-aa73-42bf-a9ed-1c3f0d7587cf)









