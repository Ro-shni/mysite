# Student Project Management System

A web-based platform that allows students to upload their projects, categorize them based on branch, section, and domain, and view/filter projects easily.

## Features
- **User Authentication**: Secure login system for students and admins.
- **Project Upload**: Students can upload their projects with details such as name, description, link, branch, section, and domain.
- **Filtering System**: View and filter projects based on branch, section, and domain using checkboxes.
- **Dashboard**: Displays statistics like total projects, students, and updates.
- **Admin Panel**: Manage users, projects, and monitor progress.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Django
- PostgreSQL or SQLite
- Git

### Clone the Repository
```sh
$ git clone https://github.com/Ro-shni/mysite.git
$ cd mysite
```


### Setup Virtual Environment
```sh
$ python -m venv venv
$ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies
```sh
$ pip install -r requirements.txt
```

### Apply Migrations
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

### Create Superuser
```sh
$ python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Run the Server
```sh
$ python manage.py runserver
```
Access the project at http://127.0.0.1:8000/

## Usage
- Log in as a student to upload projects.
- Use the filter sidebar to filter projects by domain, branch, or section.
- Admins can manage users and projects from the admin panel (/admin).

## Deployment
To deploy the project:
1. Set up a production database.
2. Configure settings.py for production.
3. Use *Gunicorn* and *Nginx* for hosting.

## Contributing
1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Commit changes (git commit -m 'Add new feature').
4. Push to the branch (git push origin feature-branch).
5. Open a pull request.

## License
This project is licensed under the *MIT License*.

## Contact
For any queries, reach out via GitHub Issues or roshninekkanti@gmail.com.

---
**GitHub Repository:** [Ro-shni/mysite](https://github.com/Ro-shni/mysite)
