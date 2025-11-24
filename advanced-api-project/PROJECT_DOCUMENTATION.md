# Advanced Django REST Framework Project with Custom Serializers

## Project Overview
This project demonstrates advanced API development with Django REST Framework, focusing on custom serializers, nested relationships, and data validation.

## Project Structure

## Models Implemented

### Author Model
- **Fields**: `name` (CharField, max_length=100)
- **Purpose**: Represents book authors
- **Relationships**: One-to-Many with Book model

### Book Model
- **Fields**: 
  - `title` (CharField, max_length=200)
  - `publication_year` (IntegerField)
  - `author` (ForeignKey to Author)
- **Purpose**: Represents published books
- **Constraints**: Unique constraint on (title, author) combination

## Custom Serializers

### BookSerializer
- **Type**: ModelSerializer
- **Fields**: All Book model fields (id, title, publication_year, author)
- **Custom Validation**: Ensures `publication_year` is not in the future
- **Read-only**: id field

### AuthorSerializer
- **Type**: ModelSerializer with nested serialization
- **Fields**: id, name, books (nested BookSerializer)
- **Features**: Includes all related books for each author
- **Read-only**: books field

## API Endpoints
- `GET /api/authors/` - List all authors with their books
- `GET /api/books/` - List all books
- `POST /api/books/create/` - Create new books (with validation)

## Key Features

### 1. Nested Serialization
- AuthorSerializer includes nested BookSerializer
- Automatic handling of related objects
- Clean JSON output with complete relationship data

### 2. Custom Validation
- Publication year cannot be in the future
- Custom error messages for validation failures
- Integration with DRF validation system

### 3. Database Relationships
- Proper ForeignKey relationships
- Efficient querying with select_related and prefetch_related
- Unique constraints to prevent duplicate entries

## Testing
The project includes comprehensive testing for:
- Model creation and relationships
- Serializer functionality
- Custom validation rules
- Nested serialization

## Admin Interface
- Custom admin configurations for both models
- Search and filter capabilities
- Autocomplete fields for better UX

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run migrations: `python manage.py migrate`
3. Create superuser: `python manage.py createsuperuser`
4. Run tests: `python test_setup.py`
5. Start server: `python manage.py runserver`

## Access Points
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **API Endpoints**: http://127.0.0.1:8000/api/
- **Admin Credentials**: admin / adminpassword

This project provides a solid foundation for building advanced APIs with complex data relationships and custom business logic.
