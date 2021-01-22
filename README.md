### Overview

With UMIAC retiring, the T&L Service Management team needs a new way to look up a large number of emplids based on a list of uniqnames. For example, in UMIAC, we can enter 500 student uniqnames, and it returns a list of emplids that match to the uniqnames, which we can then download to a .csv file and use to upload that list to Canvas to add everyone on the list to a course.

The find_user_id_from_canvas.py script uses Canvas API to retrieve UM IDs ("sis_user_id" in Canvas) for given user uniqnames ("login_id" in Canvas)

#### set up environment

- Duplicate the env_sample.json file as env.json
- Add values to setting variables in env.json

#### Run the script with a Virtual Environment

You can also set up the application using `virtualenv` by doing the following:

1. Setup

   ```sh
   pip install virtualenv
   ```

2. Create a virtual environment using `virtualenv`.

   ```sh
   virtualenv -p python3 venv
   source venv/bin/activate  # for Mac OS
   ```

3. Install the dependencies specified in `requirements.txt`.

   ```sh
   pip install -r requirements.txt
   ```

4. Initialize the database using `create_db.py`.

   ```sh
   python ./find_user_id_from_canvas.py
   ```

5. Deactivate virtual environment and exit

   ```sh
   deactivate
   ```
