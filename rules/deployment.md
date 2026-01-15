# Deployment Platforms
*Platform-specific deployment rules*

**Trigger:** Deployment platform detected

## Fly.io (Deploy:Fly)
**Trigger:** {fly_config}

- **App-Configuration**: fly.toml configuration and secrets
- **Regions-Selection**: Multi-region deployment strategy
- **Volumes-Storage**: Persistent volume management
- **Health-Checks**: Health check configuration
- **Auto-Scaling**: Autoscaling rules per region
- **Custom-Domain**: Custom domain and SSL setup

## Railway (Deploy:Railway)
**Trigger:** {railway_config}

- **Services-Connect**: Multi-service deployments and connections
- **Environment-Variables**: Environment variable management across environments
- **Database-Integration**: Built-in database provisioning
- **Custom-Domain**: Custom domain and auto-SSL configuration
- **Deployment-Triggers**: Git-based auto-deployment
- **Plugin-Ecosystem**: Railway plugins for third-party services

## Render (Deploy:Render)
**Trigger:** {render_config}

- **Service-Discovery**: Service-to-service communication
- **Environment-Specific**: Different configurations per environment
- **Build-Command**: Custom build and start commands
- **Cron-Jobs**: Scheduled background jobs
- **Static-Site**: Static site deployment with redirects
- **Custom-Domain**: Custom domains with auto-renewal SSL

## Heroku (Deploy:Heroku)
**Trigger:** {heroku_config}

- **Procfile-Types**: Process types and scaling
- **Buildpack-Selection**: Buildpack for language runtime
- **Add-on-Management**: Add-ons for databases and services
- **Config-Vars**: Config variables for secrets and configuration
- **Dyno-Types**: Dyno type selection and cost optimization
- **Release-Phase**: Release phase scripts for migrations

## Vercel (Deploy:Vercel)
**Trigger:** {vercel_config}

- **Framework-Detection**: Automatic framework detection and optimization
- **Serverless-Functions**: Serverless functions in api/ directory
- **Edge-Functions**: Edge functions for global low-latency
- **Environment-Variables**: Environment variables per deployment
- **Preview-Deployments**: Preview deployments for PRs
- **Build-Cache**: Build caching for faster deploys
- **Rewrites-Redirects**: Rewrites and redirects configuration
- **Analytics-Integration**: Web analytics integration

## Netlify (Deploy:Netlify)
**Trigger:** {netlify_config}

- **Build-Configuration**: Build command and publish directory
- **Serverless-Functions**: Functions in netlify/functions
- **Edge-Functions**: Deno-based edge functions
- **Deploy-Contexts**: Deploy contexts (production, deploy-preview, branch-deploy)
- **Redirects-Headers**: _redirects and _headers files
- **Forms-Handling**: Built-in form handling
- **Identity-Auth**: Netlify Identity for authentication
- **Split-Testing**: A/B testing with branch deploys

## Google Cloud Run (Deploy:CloudRun)
**Trigger:** {gcp_cloudrun}

- **Container-Based**: Container-based deployment
- **Concurrency-Settings**: Concurrency and scaling settings
- **CPU-Allocation**: CPU allocation (always-on vs request-based)
- **Secrets-Manager**: Secret Manager integration
- **VPC-Connector**: VPC connector for private resources
- **Traffic-Splitting**: Traffic splitting for gradual rollouts
- **Min-Instances**: Minimum instances for cold start mitigation
- **Domain-Mapping**: Custom domain mapping

## Azure Web Apps (Deploy:AzureWebApp)
**Trigger:** {azure_webapp}

- **App-Service-Plan**: App Service plan selection
- **Deployment-Slots**: Deployment slots for staging
- **Configuration-Settings**: Application settings and connection strings
- **Managed-Identity**: Managed identity for Azure resources
- **Continuous-Deployment**: GitHub/Azure DevOps integration
- **Health-Probes**: Health check probes configuration
- **Auto-Scale**: Autoscale rules configuration
- **VNet-Integration**: VNet integration for private access

## AWS App Runner (Deploy:AppRunner)
**Trigger:** {aws_apprunner}

- **Source-Connection**: Source connection (ECR or code repo)
- **Auto-Deployment**: Automatic deployments on push
- **Instance-Configuration**: CPU and memory configuration
- **Auto-Scaling**: Auto scaling configuration
- **VPC-Connector**: VPC connector for private resources
- **Secrets-Environment**: Secrets Manager integration
- **Custom-Domain**: Custom domain configuration
- **Observability-Config**: X-Ray tracing and CloudWatch logs
