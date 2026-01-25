# Requirements Document: Opti-Scholar Fixes

## Introduction

The Opti-Scholar platform is an "Intelligent Academic Assessment & Student Success Platform" that is currently non-functional due to multiple compatibility and configuration issues. This specification addresses the critical fixes needed to make the core platform operational, focusing on Python version compatibility, dependency management, database configuration, and basic API functionality.

The fixes prioritize getting the core functionality working (document upload, grading, basic API endpoints) before addressing advanced features. The platform uses FastAPI with SQLAlchemy for the backend, Gemini AI for grading intelligence, and includes a Streamlit dashboard for analytics.

## Glossary

- **System**: The Opti-Scholar platform backend API and database
- **Database_Engine**: SQLAlchemy async engine managing database connections
- **Model_Layer**: SQLAlchemy ORM models defining database schema
- **API_Layer**: FastAPI routes and endpoints
- **Dependency_Manager**: pip/requirements.txt package management system
- **Environment_Config**: .env file and pydantic-settings configuration
- **Migration_Tool**: Alembic database migration system
- **AI_Service**: Gemini AI integration for grading functionality
- **Seed_Data**: Initial test data for database tables

## Requirements

### Requirement 1: Python Version Compatibility

**User Story:** As a developer, I want the system to work with Python 3.9, so that I can run the application on the current environment without upgrading Python.

#### Acceptance Criteria

1. THE System SHALL be compatible with Python 3.9.10 or higher
2. WHEN using SQLAlchemy models, THE Model_Layer SHALL use type hints compatible with Python 3.9
3. WHEN importing metadata utilities, THE System SHALL use importlib.metadata syntax compatible with Python 3.9
4. THE System SHALL avoid using Python 3.10+ exclusive features like match statements or union type operators (|)
5. WHEN defining typed attributes, THE Model_Layer SHALL use Optional[Type] instead of Type | None syntax

### Requirement 2: Database Configuration and Compatibility

**User Story:** As a developer, I want the database configuration to work correctly with SQLite, so that I can run and test the application locally without PostgreSQL.

#### Acceptance Criteria

1. WHEN using SQLite as the database, THE Model_Layer SHALL use generic UUID types instead of PostgreSQL-specific UUID types
2. WHEN the application starts, THE Database_Engine SHALL successfully connect to the SQLite database
3. THE System SHALL create all database tables on first run without errors
4. WHEN using async database operations, THE Database_Engine SHALL use aiosqlite driver for SQLite connections
5. THE Environment_Config SHALL default to SQLite connection string for local development

### Requirement 3: Dependency Management

**User Story:** As a developer, I want all required dependencies to be correctly specified and compatible, so that pip install works without errors.

#### Acceptance Criteria

1. THE Dependency_Manager SHALL include aiosqlite package for async SQLite support
2. THE Dependency_Manager SHALL remove or make optional the asyncpg package when using SQLite
3. WHEN installing dependencies, THE System SHALL use package versions compatible with Python 3.9
4. THE Dependency_Manager SHALL specify google-generativeai version compatible with Python 3.9
5. WHEN dependencies are installed, THE System SHALL have all packages needed for core functionality

### Requirement 4: Environment Configuration

**User Story:** As a developer, I want proper environment configuration with sensible defaults, so that I can run the application with minimal setup.

#### Acceptance Criteria

1. THE System SHALL provide a .env file with working default values for local development
2. WHEN no Gemini API key is provided, THE AI_Service SHALL fail gracefully with clear error messages
3. THE Environment_Config SHALL use SQLite database URL by default
4. WHEN the upload directory does not exist, THE System SHALL create it automatically
5. THE Environment_Config SHALL document all required and optional configuration variables

### Requirement 5: Database Model Fixes

**User Story:** As a developer, I want database models to work correctly with SQLite, so that I can create tables and perform database operations.

#### Acceptance Criteria

1. WHEN defining UUID primary keys, THE Model_Layer SHALL use String type for SQLite compatibility
2. WHEN using relationships, THE Model_Layer SHALL properly configure foreign key constraints
3. THE Model_Layer SHALL use nullable=True explicitly for all Optional fields
4. WHEN models are imported, THE System SHALL not raise import errors
5. THE Model_Layer SHALL define all relationships with proper back_populates configuration

### Requirement 6: API Functionality

**User Story:** As a developer, I want the API endpoints to be functional and testable, so that I can verify the system works correctly.

#### Acceptance Criteria

1. WHEN the API server starts, THE API_Layer SHALL successfully initialize all routes without errors
2. WHEN accessing the /health endpoint, THE System SHALL return a valid health status response
3. WHEN accessing the /docs endpoint, THE System SHALL display the OpenAPI documentation
4. WHEN authentication is required, THE API_Layer SHALL properly validate JWT tokens
5. WHEN file uploads are attempted, THE API_Layer SHALL validate file size and type correctly

### Requirement 7: Database Seeding

**User Story:** As a developer, I want test data in the database, so that I can test API endpoints and verify functionality.

#### Acceptance Criteria

1. THE Seed_Data SHALL create at least one teacher user with valid credentials
2. THE Seed_Data SHALL create at least one student user with valid credentials
3. THE Seed_Data SHALL create at least one course with associated exam
4. THE Seed_Data SHALL create sample rubric data for grading tests
5. WHEN seed script runs, THE System SHALL handle existing data gracefully without duplicates

### Requirement 8: Service Layer Implementation

**User Story:** As a developer, I want core service methods to have basic implementations, so that API endpoints return meaningful responses instead of NotImplementedError.

#### Acceptance Criteria

1. WHEN document upload is requested, THE System SHALL save files to the upload directory
2. WHEN student ID extraction is requested, THE System SHALL attempt OCR or return mock data with clear indication
3. WHEN grading is requested, THE System SHALL call Gemini API if configured or return mock grades with warnings
4. WHEN verification is requested, THE System SHALL perform basic statistical checks on grade data
5. THE System SHALL log clearly when returning mock data versus real AI responses

### Requirement 9: Error Handling and Logging

**User Story:** As a developer, I want clear error messages and logging, so that I can diagnose issues quickly.

#### Acceptance Criteria

1. WHEN database connection fails, THE System SHALL log the specific error with connection details
2. WHEN API key is missing, THE System SHALL return HTTP 503 with clear message about configuration
3. WHEN file upload fails, THE System SHALL return specific error about file size, type, or permission issues
4. THE System SHALL log all database queries when debug mode is enabled
5. WHEN exceptions occur, THE System SHALL return structured error responses with request IDs

### Requirement 10: Documentation Updates

**User Story:** As a developer, I want accurate documentation, so that I can set up and run the system correctly.

#### Acceptance Criteria

1. THE System SHALL update README.md to reflect actual Python version requirements
2. THE System SHALL document the difference between SQLite (development) and PostgreSQL (production) setup
3. THE System SHALL provide clear instructions for obtaining and configuring Gemini API key
4. THE System SHALL document all environment variables with examples
5. THE System SHALL include troubleshooting section for common setup issues
