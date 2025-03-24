# GrooveFlaskAPI

GrooveFlaskAPI is a RESTful API built with Flask that manages data about artists and albums. The project was developed with a focus on best practices in testing, data validation, and pagination. The API supports various endpoints for CRUD operations and includes authentication via JWT tokens.

## Features

* Full CRUD operations for Artists and Albums
* JWT-based authentication
* Pagination support
* Data filtering, sorting, and field selection
* Detailed error handling and data validation
* Comprehensive test coverage using pytest

## Requirements

* Python 3.12
* Flask 3.0
* SQLAlchemy 2.x
* Pytest 8.x
* Flask-SQLAlchemy

## Instalation

#### 1. Clone the repository:
~~~
git clone https://github.com/Kali2114/GrooveFlaskAPI.git
cd GrooveFlaskAPI
~~~

### 2. Create a virtual environment and activate it:
~~~
python -m venv groovenv
source groovenv/bin/activate  # On Windows use 'groovenv\Scripts\activate'
~~~

### 3. Install dependencies:
~~~
pip install -r requirements.txt
~~~

### 4. Set environment variables in a .env file:
~~~
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
~~~

### 5. Initialize the database:
~~~
flask db upgrade
flask db_manage add_data
~~~

### 6. Run the application:
~~~
flask run
~~~

## Usage

### Authentication

* Register: POST /api/auth/register
* Login: POST /api/auth/login
* Get Current User: GET /api/auth/me

### Artists Endpoints

* Get All Artists: GET /api/artists
* Get Artist by ID: GET /api/artists/<int:artist_id>
* Create Artist: POST /api/artists
* Update Artist: PUT /api/artists/<int:artist_id>
* Delete Artist: DELETE /api/artists/<int:artist_id>

### Albums Endpoints

* Get All Albums: GET /api/albums
* Get Album by ID: GET /api/albums/<int:album_id>
* Create Album: POST /api/artist/<int:artist_id>/albums
* Update Album: PUT /api/albums/<int:album_id>
* Delete Album: DELETE /api/albums/<int:album_id>

### Example Requests

Example GET request to fetch all albums with pagination and sorted by name:

~~~
GET /api/albums?fields=name&sort=-id&page=2&limit=2
~~~

Response Example

~~~
{
    "success": true,
    "data": [
        {
            "name": "PeeRZet"
        },
        {
            "name": "Oxon"
        }
    ],
    "number_of_records": 2,
    "pagination": {
        "total_pages": 4,
        "total_records": 7,
        "current_page": "/api/albums?page=2&fields=name&sort=-id&limit=2",
        "next_page": "/api/albums?page=3&fields=name&sort=-id&limit=2",
        "previous_page": "/api/albums?page=1&fields=name&sort=-id&limit=2"
    }
}
~~~

## Code Style

This project follows PEP 8 guidelines using:

- **Flake8** for linting to ensure code quality and consistency.
- **Black** for code formatting to maintain uniform styling.

To run Flake8:
~~~
flake8 .
~~~

To format code with black:
~~~
black .
~~~

## Testing

To run the tests with Pytest, use following command:

~~~
python -m pytest -vv
~~~

## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007.

## Contact

For inquiries or collaboration, please reach out via [GitHub: Kali2114](https://github.com/Kali2114).