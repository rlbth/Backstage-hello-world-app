[![LintAndTest](https://github.com/rlbth/Backstage-hello-world-app/actions/workflows/linting-testing.yaml/badge.svg)](https://github.com/rlbth/Backstage-hello-world-app/actions/workflows/linting-testing.yaml)
[![Docker Build and Deploy with CloudFormation](https://github.com/rlbth/Backstage-hello-world-app/actions/workflows/docker-deploy.yaml/badge.svg?branch=main)](https://github.com/rlbth/Backstage-hello-world-app/actions/workflows/docker-deploy.yaml)
# Application Integration with Backstage

This document contains the paper solution (concept) and blue print for priliminary implimentation involved in the automated build, test, and deployment of our "hello-world" app through backstage.
The application is managed through Backstage and integrates with various services such as AWS, Docker, and GitHub.

## Contents of the documentation:

- Overall Flow 
- Tech Stack
- Priliminary implementation
- Steps to reproduce
- Challenges
- Common problems and troubleshooting

### Overall Flow
There are 3 main pieces of the solution:
- Infrastructure for backstage
- Backstage service 
- Hello-world application

These are located in three repositories, i.e, 
- rlbth/backstage-infrastucture
- rlbth/backstage
- rlbth/backstage-hello-world

### Hello Application Archectecture
Hello world or Hello truck application is a simple python API application using Flask which a simple python framework for API programming. 
Branching Strategy:  A long living main branch exists for the length of the application lifecycle with feature branches taken from the main branch from time to time for development, testing, sandboxes, etc. A rule of thumb with 14 day (one sprint) principle is followed to avoid merge conflicts from stale branches. 
Docker and Docker Compose: Docker and docker-compose files are included for a manual, yet packaged deployment . They are located in the root of the directory and can be easily utilised with 'docker-compose up' or 'docker build . -t hello-world-app' like commands 
Github Actions: GitHub actions are divided into two workflow files located in .github/workflow directory. The first, which is linting and testing is run on merging commits with main branch and the build/ deployment workflow is triggered upon successful completion of linting workflow. Build and deployment workflow are  fully automated with IaC written in CloudFormation templates, dockerized and deployed serverless with Fargate using Elastic Container Service. The workflow consideres existing VPC and security groups as parameters in infrastructure/cft.yml files. 
Deployment on AWS: Cloud formation templates are written for deploying infrastructure as code, secretive information such as AWS access key id and secret access key are stored on gihub secrets. Secret exposure scanning and vulnerability scans are also enabled on every commit from which I get notified over the email. Cloudwatch was used for observability of the application. Some thought on security was also given for this application with WAF patterns to avoid cross site scripting and SQL Injection attacks, principle of least privilage was followed for security groups and IAM policies , roles for instance. It was an intension to have multiple lines of defence for the application. Cloudformation is used for observability but there are plenty of things that can be done to improvise the application stock ofcourse. 
app-config.yml : this file is included in the root of the repository and describes the metadata of the application to configure with Backstage as a component. It includes dependencies, API documentation, etc. An Open AI specification was also included in the sample application.  


## Conceptual plan to trigger CI/CD and AWS deployments from Backstage
The idea is to create a template and register it in the Software catalog along with GitHub CDK files to easily bootstrap a new application with all the pipelines and secrity princoples baked in. The template can then be used to trigger building an application and deploying that application later to AWS.  CI/CD pinelines can also be monitored and triggred from the backstage application as needed.   

### Tech stack
The overall techstack is as follows: 
- Docker 
- AWS 
- GitHub 
- Kubernetes 
- JavaScript 
- Python 
- Postgres
- Backstage

For backstage deployment, I used: 
- AWS CDK v2 in Python for Infrastructure as Code 
- GitHub Actions
- GitHub for source code management 
- Docker for containerising the application 
- Kubernetes for deploying and scaling the application

AWS services used for backstage deployment are as follows:
- AWS Elastic Kubernetes Service for managed Kubernetes cluster 
- AWS WAF - Web Application Firewall for securing against DDOS attacks etc 
- AWS Fargate - For serveless deployment in the EKS cluster (Fargate Profile). 
- AWS Application Load Balancer - for managing traffic to backstage 
- AWS EC2 Security Groups - for controlling INGRESS and EGRESS for RDS DB, EKS cluster, ALB etc. 
- AWS Identity and Access Management - For EKS role, Fargate role to create and manage AWS resources
- AWS VPC - we assume that a default VPC exists 
- AWS VPC subnets - we assume existance on one public subnet and two private subnets
- AWS Internet gatway - we assume that an internet gateway exists and traffic for the public subnet is routed through internt gateway
- AWS NAT gateway - we assume that NAT gateway is created on the public subnet and associated with the private subnets.
- AWS Cloudwatch - For observability and monitoring for resources and logs. 

For hello world application, I used: 
- AWS CDK v2 in Python for Infrastructure as Code 
- GitHub Actions
- GitHub for source code management 
- Docker for containerising the application 

AWS services used for hello-world deployment are as follows:
- AWS CFT is used for deployment
- AWS ElasticBeanStalk which is a managed service for running docker applications was used.


Deployment strategy used for hello-world-application - Blue Green Deployment 



### Priliminary implementation

- Install necessary commandline tools such as 
yarn, npm, tox (python library), docker, git, python or pip, etc

- Setup backstage
	- Fork the main branch of backstage that has "tag" on version release
	- Add Dockerfile if not already available in packages/backend 
	- Make sure you have an app-config.yml file and use it to integrate and authenticate with Github, provide metadata, and other necessary integrations such as AWS etc
	- Setup Github Actions which will check, build and uploads to dockerHub the latest docker image (when there's changes to the main branch of backstage)
	- Build steps include: yarn install, yarn tsc, yarn build, docker build -t .

- Backstage-infra setup
	- Write a CDK in python to seup the kubernetes cluster
	- Kubernetes manifestation includes 
		- installing kubectl for command line communication with the kubernetes cluster
		- setting up a namespace
		- adding postgresDB service, backstage service and secrets to enable communication with each other
	- Deploying it to AWS EKS (Fargate)
		nodes, security groups
		
- Hello-world-app
	- Write up and push to Github, a simple application with a catalog-info.yml file with annotations, component metadata such as owner/ team name, links to dashboards, tech docs, etc
	- Register this application as a component in backstage by linking the catalog-info.yml file from Github
	- Dockerfile that runs the application
	- Setup CI/CD with GitHub Actions that contains a basic workflow of checking out code; Building the Docker image; push the image to a container registry (Docker Hub); deploy the image to localhost or a AWS EKS.
	- Bash script (for deploying the image to localhost) that pulls the altest image and restarts it.


i. Building the Application
Yarn Install: Command-line is used to install dependencies
Yarn tsc: Will  create type definitions that will be consumed by the build
Yarn build: Will build the application.
Docker build : will build a image from the app  

ii. Containerization with Docker
Docker Build: npx is used to create backstage app, yarn dependencies are installed from lock file and then the docker image is built with Dockerfile provided
Docker Hub: Docker username and password are stored in github secrets and gihub actions trigger push the image to docker hub

iii. From code commit to release
The idea is to write backstage template with github actions baked into it and add it to the software catalog to trigger initialisation to deployment as well as have minimal documentation included in readme.md of that template.


### Challenges
Some challenges with the current setup and work to be done.
- Deploying to EKS - cluster creation fails with CDKs
- Origin 'http://localhost' is not allowed for GitHub OAuth.
- Basic monitoring is setup, extensive monitoring work can be carried out 

### Common problems and troubleshooting
Common issues and their resolutions.
- Backstage app doesn't get created with yarn@3, but only does with yarn@1 
	can be found in backstage documentation :https://backstage.io/docs/getting-started/#:~:text=You%20will%20need%20to%20use%20Yarn%20classic%20to%20create%20a%20new%20project%2C%20but%20it%20can%20then%20be%20migrated%20to%20Yarn%203
- ImagePullBackOff Error - Make sure the right docker image is mentioned in backstage.yaml
- CrashLoopBackOff Error - Kubernetes service needs to be mentioned in app-config.yaml instead of localhost
