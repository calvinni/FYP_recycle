# FYP_recycle
All the code used for the recycle website is in the folder, "Recycle_project"
The Python/Django package requirements to run the program is in the "requirements.txt" file

Instructions on running it on VSCode:
1. Import all the files in the "Recycle_project" folder into your own computer folder

2. Create a virtual enviroment for the recycle website:
Exmaple: In the VSCode console, with the directiory towards the host folder of the "Recycle_project" folder, type " py -m venv *enviromentname* "

3. Activate your virtual enviroment:
Exmaple: In the VSCode console, with the directiory towards the host folder of the "Recycle_project" folder, type " *enviromentname*\Scripts\activate "

4. Add the required packages to your list of packages
Exmaple: In the VSCode console, while in the virtual enviroment, type " pip install -r /path/to/requirements.txt "

5. Once all packages are installed, migrate the database by typing these 2 lines of code in a row:
" py manage.py makemigrations "
" py manage.py migrate "

6. Once all the migration is done, run the server with this line of code:
" py manage.py runserver "

7. Once the server is up, connect to the website through the link that is provided in the VSCode console.

NOTE: All the test are in Recycle_project/recycle_app/test.py, to run them, use this code: " py manage.py test " while in the virtual enviroment.

NOTE: To view the database, you'll have to download "DB Browser (SQLite)" and use it to open the "Recycle_project/db.sqlite3" file
