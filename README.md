# College Admission RAG Assistant

An API-based Retrieval-Augmented Generation (RAG) application that
answers college-admission questions using information retrieved from a
document knowledge base.

> **Project status:** Core RAG, FastAPI, PostgreSQL-backed
> authentication, JWT, refresh-token rotation, and logout workflows have
> been implemented and locally tested. Cloud deployment and the
> remaining production-hardening tasks are not yet documented as
> completed.

## Key Features

### RAG pipeline

-   Load admission-related documents (for example, PDF and text files).
-   Split documents into chunks and attach metadata.
-   Generate embeddings and store vectors in ChromaDB.
-   Rewrite user queries to improve retrieval.
-   Retrieve relevant content using hybrid search.
-   Apply metadata-based filtering.
-   Rerank candidate documents with a Cross-Encoder.
-   Generate grounded answers using the configured Gemini model.
-   Return answer and source information through the API.

### API and application reliability

-   FastAPI REST API.
-   Health-check endpoints.
-   Centralized application logging.
-   Global exception handling and request validation handling.
-   Rate limiting on the chat endpoint.

### Authentication and security

-   User registration and login.
-   Argon2 password hashing.
-   RS256-signed JWT access tokens.
-   PostgreSQL persistence for users and refresh-token records.
-   Refresh tokens stored as SHA-256 hashes.
-   Refresh-token rotation and revocation.
-   Logout endpoint to revoke the submitted refresh token.

## Architecture

``` text
Client
  |
  v
FastAPI
  |
  +--> Authentication / JWT / authorization
  |
  +--> RAG Chat API
         |
         +--> Query rewriting
         |
         +--> Hybrid retrieval
         |      |
         |      +--> ChromaDB vector search
         |      +--> Keyword search
         |
         +--> Metadata filtering
         |
         +--> Cross-Encoder reranking
         |
         +--> Gemini answer generation
         |
         +--> Answer and source response

PostgreSQL: users and refresh-token records
ChromaDB: document embeddings and metadata
```

## Technology Stack

  -----------------------------------------------------------------------
  Area                                Technologies
  ----------------------------------- -----------------------------------
  Language                            Python 3.12

  API                                 FastAPI

  RAG orchestration                   LangChain

  LLM                                 Google Gemini

  Embeddings                          Hugging Face sentence-transformer
                                      model (configured through
                                      environment)

  Vector database                     ChromaDB

  Retrieval                           Hybrid search, metadata filtering

  Reranking                           Cross-Encoder

  Relational database                 PostgreSQL

  ORM and migrations                  SQLAlchemy, Alembic

  Authentication                      JWT (RS256), Argon2

  Testing                             pytest
  -----------------------------------------------------------------------

## Project Structure

The following is a representative structure. Adjust names if your local
repository differs.

``` text
clg_admission_rag/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   └── chat.py
│   │   └── schemas/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── jwt_auth.py
│   │   ├── refresh_tokens.py
│   │   └── security.py
│   ├── models/
│   │   ├── user.py
│   │   └── refresh_token.py
│   └── main.py
├── data_files/
├── migrations/
├── tests/
├── chroma_db/             # generated locally; normally not committed
├── .env.example
├── .gitignore
└── README.md
```

## Prerequisites

-   Python 3.12
-   PostgreSQL
-   A Google Gemini API key
-   Git

Install PostgreSQL and create an application database and a
least-privilege database user before configuring the application.

## Local Setup

### 1. Clone the repository

``` bash
git clone <YOUR_GIT_REPOSITORY_URL>
cd clg_admission_rag
```

### 2. Create and activate a virtual environment

``` bash
python3.12 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

If the project has a `requirements.txt`:

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If dependency management is not yet captured in a requirements file,
export the verified environment before sharing the repository:

``` bash
pip freeze > requirements.txt
```

Review the resulting file and remove unrelated development packages if
necessary.

### 4. Configure environment variables

Create a local `.env` file based on `.env.example`. Example variable
names:

``` env
GOOGLE_API_KEY=replace_with_your_gemini_api_key

DATABASE_URL=postgresql+psycopg://DB_USER:DB_PASSWORD@localhost:5432/college_admission_rag

JWT_ISSUER=college-admission-auth
JWT_AUDIENCE=college-admission-rag
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Keep the embedding model and ChromaDB path consistent
# with the values expected by app/core/config.py.
EMBEDDING_MODEL=your_configured_embedding_model
CHROMA_DB_DIR=chroma_db
```

Use the exact environment variable names and defaults defined by your
`app/core/config.py`. Do not commit the real `.env` file.

### 5. Configure RS256 keys

The application uses an RSA private key to sign access tokens and a
public key to verify them.

-   Keep the private key outside source control and restrict file
    permissions.
-   Provide the public key at the path configured by the application.
-   Never upload or commit either private or public key files unless
    your deployment process explicitly manages public keys safely.
-   For production, prefer a secret manager or mounted secret over
    baking keys into a container image.

Example permission for a locally stored private key:

``` bash
chmod 600 private.pem
```

### 6. Run database migrations

``` bash
python -m alembic upgrade head
```

### 7. Start the API locally

``` bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

-   Swagger UI: `http://127.0.0.1:8000/docs`
-   ReDoc: `http://127.0.0.1:8000/redoc`

Use the actual host and port configured for your environment.

## API Overview

Confirm the exact route prefix in your FastAPI router configuration.

  -------------------------------------------------------------------------
  Method                  Endpoint                  Purpose
  ----------------------- ------------------------- -----------------------
  GET                     `/health`                 Basic health check

  GET                     `/health/details`         Detailed health
                                                    information

  POST                    `/api/v1/auth/register`   Register a user

  POST                    `/api/v1/auth/login`      Authenticate and
                                                    receive tokens

  POST                    `/api/v1/auth/refresh`    Rotate refresh token
                                                    and issue new tokens

  POST                    `/api/v1/auth/logout`     Revoke the submitted
                                                    refresh token

  GET                     `/api/v1/auth/me`         Get the authenticated
                                                    user's identity

  POST                    `/api/v1/chat`            Submit a question to
                                                    the RAG pipeline
  -------------------------------------------------------------------------

### Authentication flow

1.  Register a user.
2.  Log in with the registered credentials.
3.  Use the access token as a Bearer token for protected endpoints.
4.  When the access token expires, submit the current refresh token to
    the refresh endpoint.
5.  Store the newly returned refresh token and stop using the previous
    one.
6.  On logout, submit the current refresh token so the server can revoke
    it.

**Token handling:** Never share access tokens, refresh tokens,
passwords, API keys, database credentials, or private keys in
screenshots, issue trackers, or source control.

## Running Tests

Run the complete test suite from the project root:

``` bash
python -m pytest -v
```

Run a specific test module:

``` bash
python -m pytest -v tests/test_rate_limiting.py
```

Add and maintain tests for registration, login, invalid credentials, JWT
validation, refresh-token rotation, token reuse rejection, logout, role
permissions, and RAG retrieval behavior.

## Production Deployment Checklist

The project has been developed and tested locally. Before describing it
as production-deployed, complete and verify the deployment work.

-   [ ] Confirm all automated tests pass in a clean environment.
-   [ ] Add a reviewed and reproducible dependency lock or requirements
    file.
-   [ ] Use production environment variables and a managed secret store.
-   [ ] Keep RSA private keys out of the repository and container image.
-   [ ] Configure PostgreSQL with least-privilege credentials, backups,
    and network restrictions.
-   [ ] Configure Alembic migrations as a controlled deployment step.
-   [ ] Configure persistent storage and backups for ChromaDB, or select
    a managed vector database.
-   [ ] Build and test a Docker image.
-   [ ] Run the API behind a production ASGI server and reverse
    proxy/load balancer.
-   [ ] Configure HTTPS/TLS.
-   [ ] Configure CORS for trusted origins only.
-   [ ] Review authentication, authorization, token revocation, rate
    limits, and request-size limits.
-   [ ] Add monitoring, centralized logs, error reporting, and health
    probes.
-   [ ] Configure CI/CD and a rollback strategy.
-   [ ] Verify deployment with smoke tests.

Do not expose `/docs`, detailed health diagnostics, database ports, or
internal exception details publicly unless there is a deliberate
access-control decision.

## Screenshots for the README

Create a `screenshots/` directory and add genuine screenshots from your
running application. Suggested captures:

  -----------------------------------------------------------------------
  Suggested filename                  What to capture
  ----------------------------------- -----------------------------------
  `01-swagger-overview.png`           Swagger UI showing the API groups

  `02-register-user.png`              Successful user registration
                                      response; hide email if it is
                                      personal

  `03-login-response.png`             Login response with all token
                                      values fully masked

  `04-rag-chat-response.png`          A representative RAG question,
                                      answer, and source references

  `05-health-check.png`               Successful health-check response

  `06-logout-response.png`            Successful logout response

  `07-database-schema.png`            Database tables/schema; hide
                                      usernames and sensitive data
  -----------------------------------------------------------------------

Add screenshots to this repository only after checking that no tokens,
passwords, API keys, private keys, personal data, or sensitive database
values are visible.

Example Markdown for adding screenshots after capturing them:

``` markdown
## Application Screenshots

### Swagger API Documentation
![Swagger API overview](screenshots/01-swagger-overview.png)

### RAG Chat Response
![RAG chat response](screenshots/04-rag-chat-response.png)

### Health Check
![Health check](screenshots/05-health-check.png)
```

## Security Notes

-   `.env`, private keys, database credentials, generated tokens, and
    local database files must not be committed.
-   Store only password hashes, never plaintext passwords.
-   Store only refresh-token hashes in the database.
-   Validate JWT signature, issuer, audience, and expiration.
-   Enforce authorization on the server for every protected operation.
-   Use HTTPS in deployed environments.
-   Rotate credentials immediately if they are accidentally exposed.

## Current Development Status

Implemented and locally tested: core RAG workflow, FastAPI integration,
logging and exception handling, health checks, rate limiting, PostgreSQL
integration, registration, login, Argon2 password hashing, RS256 JWT
authentication, refresh-token persistence/rotation, and logout.

Next planned work includes RBAC, additional authentication and
authorization tests, remaining security hardening, Docker, deployment,
and monitoring. Update this section as each item is implemented and
verified.

## License

Add the license that applies to this repository before publishing it
publicly.
