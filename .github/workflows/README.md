# CI/CD Deploy

## Set up

### Create Secrets on Github

1. **AWS**

   - AWS_ACCESS_KEY_ID: access token
   - AWS_SECRET_ACCESS_KEY: secret access
   - SSH_PRIVATE_KEY: ssh key pair

2. **Dockerhub**

   - DOCKERHUB_USERNAME: username
   - DOCKERHUB_PASSWORD: password

3. **Chat Service**

   - OPENAI_API_KEY: your openai api key

4. **Frontend**

   - GOOGLE_CLIENT_ID: google client id
   - GOOGLE_CLIENT_SECRET: google client password
   - NEXTAUTH_SECRET: nextauth secret

5. **Backend**
   _Config env email_

   - MAIL_HOST
   - MAIL_PORT
   - MAIL_USER
   - MAIL_PASS
   - MAIL_SENDER

   _Config env JWT_

   - AT_SECRET
   - RT_SECRET

   _Database url_

   - DATABASE_URL

6. **Database**
   - POSTGRES_USER: user name
   - POSTGRES_PASSWORD: password
   - POSTGRES_DB: database name

### Create Variables on Github

1. **AWS**

   - TAGS: Tag for resources

   Example:

   ```sh
   [{ "Key": "ApplicationName", "Value": "Omni Assistant" },
   { "Key": "Purpose", "Value": "Learning" },
   { "Key": "Project", "Value": "Omni Assistant" },
   { "Key": "ProjectID", "Value": "Omni Assistant" },
   { "Key": "Creator", "Value": "VectorNguyen" },
   { "Key": "OwnerService", "Value": "VectorNguyen" }
   ]
   ```

2. **Backend**
   _Config env Rate Limitting_

   - RL_TTL
   - RL_LIMIT

   _Config refresh token, token time_

   - EXP_AT
   - EXP_RT

   _Config env API for AI_

   - ENDPOINT_AI

   _Config CORS Socket_

   - FRONTEND_URL

   _Redis_

   - REDIS_HOST
   - REDIST_PORT

   _Config port backend_

   - PORT

## Workflows

### Development - Build and Unittest

#### File: [development_pipeline.yml](development_pipeline.yml)

**Event:** On Commit or Pull Request → any branch into develop

**Jobs:**

- Install dependencies (caches)
- Run isort
- Run black
- Run flake8

**Description:**
This workflow is triggered on Pull Requests into the develop branch. It ensures a clean and standardized codebase by installing dependencies, checking code formatting with isort, black, and flake8, and finally building and pushing Docker images to Docker Hub.

### Staging - CI/CD Pipeline

#### File: [staging_pipeline.yml](staging_pipeline.yml)

**Event:** On Pull Request → any branch into staging

**Jobs:**

- Install dependencies (caches)
- Run isort
- Run black
- Run flake8
- Build images (caches)
- Push images to Docker Hub
- Create infrastructure
- Configure infrastructure
- Deploy application using Docker Compose
- Clean up following the concept of A/B deploy

**Description:**
This pipeline is designed for the staging environment and is triggered on Pull Requests into the staging branch. It includes steps to ensure code quality, build and push Docker images, create and configure necessary infrastructure, and deploy the application using Docker Compose. The cleanup process follows the A/B deployment concept.

### Production - CI/CD Pipeline

#### File: [production_pipeline.yml](production_pipeline.yml)

**Event:** On Pull Request → any branch into master

**Jobs:**

- Install dependencies (caches)
- Run isort
- Run black
- Run flake8
- Build images (caches)
- Push images to Docker Hub
- Create infrastructure
- Configure infrastructure
- Deploy application using Docker Compose
- Clean up following the concept of A/B deploy

**Description:**
The production pipeline is triggered on Pull Requests into the master branch, indicating changes are ready for deployment to the production environment. It follows a similar process to the staging pipeline but is specifically tailored for the production environment. The cleanup process adheres to the A/B deployment concept, ensuring a smooth transition between versions.

## References

- [Reusing workflows](https://docs.github.com/en/actions/sharing-automations/reusing-workflows)
