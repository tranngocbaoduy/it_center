# it-center - INTRODUCE 
- * Im running code in Mac OS 

- Link github: https://github.com/tranngocbaoduy/it_center

- A program about manage technology center: 
    + manage student, teacher
    + mange staff: academic, cashier
    + manage login, logout, create new staff
    + mange course: opening, open soon
    + mange receipt: tuition, payment
    + statistic revenue and expenditure
    

# B1: INSTALL CONDA AND ESSENTIAL LIBRARY
    
    1. install anaconda: https://www.anaconda.com/distribution/
    2. run cmd to create new environment, active it and install essential library

    cmd: conda deactivate 
    cmd: conda create −n [env_name] python=3.6     
    cmd: conda activate [env_name]
    cmd: pip install −r requirements.txt
    

# B2: CHECK MONGO (IF YOU HAVE ALREADY MONGO, PASS THIS STEP)
    
    1. install mongodb at link: https://www.mongodb.com/download-center/community
    If you want to see a interface of mongo, you can install mongo - compass (interface) at link: 
    	https://www.mongodb.com/download-center/compass
    2. check mongo is running 

        cmd: mongod (start server mongo)
    	cmd: mongo  (check server is starting)

    This app is using my database (cloud-mongo on mongo atlas). 

# B3: MODIFY DATABASE AND START SERVER
    MODIFY
        If you want to use your database, you need modify some config in config.py
        - First: you need modify path your db (some config as: name, password db, name db, port mongo in your computer, ...)
        - Second: open blocked row, and run 'python create_data.py' in your cmd -> to create db
            of course this is sample data and not real
        - Third: From cmd type: python run.py (server'll be started at http://127.0.0.1:5000)
    
    NO MODIFY DB
        If you don't modify config.py. It'll use my database in cloud-mongo, and you just need type
        python run.py in your cmd to start server. (server'll be started at http://127.0.0.1:5000)

# B4: ACCOUNT TO LOGIN
    username: admin1
    password: 1
        