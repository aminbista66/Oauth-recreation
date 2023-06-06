# OAuth Token Authentication Flow Project

This project aims to recreate the OAuth token authentication flow from scratch. It provides an implementation of the authentication flow using Django, Django REST Framework, and various other libraries and frameworks.

## Features

- Custom login view that handles authentication and redirects based on client parameters.
- OTP (One-Time Password) authentication view for additional security.
- Grant confirmation view to display the confirmation page before granting access.
- Grant view to generate and return the appropriate token or code based on the response type and scope.
- Token refresh endpoint for refreshing access tokens.
- Client registration form for registering new clients.
- Scope addition form for adding scopes to existing clients.

## Prerequisites

- Python 3.x
- Django
- Django REST Framework
- Other dependencies mentioned in the requirements.txt file

## Installation

1. Clone the repository:

```bash
git clone https://github.com/aminbista6666/Oauth-recreation.git
```

2. Create and activate a virtual environment:

```bash
python3 -m venv myenv
source myenv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Run database migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

## Usage

1. Access the application by visiting [http://localhost:8000/](http://localhost:8000/) in your web browser.

2. Follow the provided URLs and views to navigate through the authentication flow.

3. Explore the code files in the project to understand the implementation details and customize as per your requirements.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

[MIT License](https://opensource.org/licenses/MIT)
