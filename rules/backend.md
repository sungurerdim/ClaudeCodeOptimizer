# Backend Frameworks
*Framework-specific rules for backend development*

**Trigger:** Backend framework detected

## Express (Backend:Express)
**Trigger:** {express_deps}

- **Middleware-Order**: Middleware order matters, error handlers last
- **Router-Modular**: Use express.Router for modular routes
- **Request-Validation**: Validate request body with middleware
- **Error-Handler**: Centralized error handling middleware
- **Security-Headers**: Use helmet for security headers
- **CORS-Config**: Explicit CORS configuration

## Fastify (Backend:Fastify)
**Trigger:** {fastify_deps}

- **Plugin-System**: Leverage plugin system for modularity
- **Schema-Validation**: JSON schema for request/response validation
- **Hooks-Lifecycle**: Use lifecycle hooks for cross-cutting concerns
- **Reply-Type**: Set reply type for automatic serialization
- **Decorator-Register**: Register reusable decorators

## Hapi (Backend:Hapi)
**Trigger:** {hapi_deps}

- **Plugin-Structure**: Plugins for feature organization
- **Validation-Joi**: Joi schemas for request validation
- **Auth-Strategies**: Multiple auth strategies support
- **Lifecycle-Ext**: Lifecycle extensions for middleware-like behavior
- **Pre-Handlers**: Pre-handlers for request preprocessing

## Koa (Backend:Koa)
**Trigger:** {koa_deps}

- **Middleware-Cascade**: Composition over configuration via middleware
- **Context-Object**: Pass context through middleware chain
- **Error-Handling-Koa**: Centralized error handling middleware
- **Body-Parsing**: Body parsing middleware configuration

## NestJS (Backend:NestJS)
**Trigger:** {nestjs_deps}

- **Module-Dependency**: Dependency injection via modules
- **Controller-Service**: Clear separation of controllers and services
- **Guard-Interceptor**: Guards for authorization, interceptors for transformation
- **Exception-Filter**: Custom exception filters
- **Decorator-Custom**: Custom decorators for validation/transformation

## Django (Backend:Django)
**Trigger:** {django_markers}

- **MTV-Pattern**: Model-Template-View pattern
- **ORM-Queries**: Optimize QuerySets, avoid N+1
- **Middleware-Order**: Middleware order matters
- **Settings-Split**: Split settings by environment
- **Management-Commands**: Custom management commands
- **Signals-Sparingly**: Use signals sparingly, prefer explicit

## Flask (Backend:Flask)
**Trigger:** {flask_markers}

- **Blueprint-Modular**: Blueprints for modular routes
- **Factory-Pattern**: Application factory pattern
- **Extension-Config**: Configure extensions properly
- **Context-Locals**: Understand application and request context
- **Error-Handler**: Centralized error handlers

## FastAPI (Backend:FastAPI)
**Trigger:** {fastapi_markers}

- **Pydantic-Models**: Pydantic for request/response validation
- **Dependency-Injection**: Use Depends for DI
- **Async-Endpoints**: async def for I/O-bound endpoints
- **OpenAPI-Auto**: Automatic OpenAPI documentation
- **Background-Tasks**: Background tasks for non-blocking ops

## Spring Boot (Backend:Spring)
**Trigger:** {spring_boot_deps}

- **Starter-Deps**: Use spring-boot-starter-* for curated dependencies
- **Properties-Config**: application.properties or application.yml
- **Component-Scan**: Component scanning for automatic bean discovery
- **AOP-Aspects**: Aspect-oriented programming for cross-cutting concerns
- **Actuator-Monitoring**: Spring Boot Actuator for monitoring endpoints

## Quarkus (Backend:Quarkus)
**Trigger:** {quarkus_deps}

- **Native-First**: Build native image for fast startup
- **Config-Externalize**: Externalized configuration via properties
- **Extension-Model**: Leverage Quarkus extensions for integration
- **GraalVM-Compatible**: Ensure GraalVM compatibility
- **Dev-Mode**: Fast iterative development mode

## Micronaut (Backend:Micronaut)
**Trigger:** {micronaut_deps}

- **Compile-Time-DI**: Compile-time dependency injection (no reflection)
- **Http-Client**: Declarative HTTP client
- **Config-Management**: Configuration management and environment properties
- **Bean-Introspection**: Compile-time bean introspection
- **Build-Time-Optimization**: Optimized for serverless/microservices

## Rails (Backend:Rails)
**Trigger:** {rails_markers}

- **Convention-Config**: Convention over configuration
- **Active-Record**: Active Record patterns and queries
- **Concerns-Extract**: Extract shared behavior to concerns
- **Strong-Params**: Strong parameters for mass assignment protection
- **Background-Jobs**: Active Job for background processing
- **Turbo-Hotwire**: Modern frontend with Turbo/Hotwire

## Laravel (Backend:Laravel)
**Trigger:** {laravel_markers}

- **Eloquent-ORM**: Eloquent patterns and relationships
- **Service-Container**: Leverage service container for DI
- **Middleware-Auth**: Middleware for authentication/authorization
- **Queue-Jobs**: Queued jobs for background processing
- **Artisan-Commands**: Custom artisan commands
- **Blade-Templates**: Blade templating best practices

## Phoenix (Backend:Phoenix)
**Trigger:** {phoenix_deps}

- **Context-Module**: Contexts for business logic organization
- **LiveView-First**: LiveView for real-time UI
- **Channels-Realtime**: Channels for WebSocket communication
- **Ecto-Queries**: Ecto for database operations
- **Pub-Sub**: PubSub for event broadcasting

## Sinatra (Backend:Sinatra)
**Trigger:** {sinatra_deps}

- **Route-Definition**: Simple route DSL
- **Middleware-Stack**: Middleware stack for request handling
- **Template-Engine**: Template engine selection and configuration
- **Error-Handling-Sinatra**: Error handlers and error templates
- **Helper-Methods**: Helper methods for view/route logic

## Symfony (Backend:Symfony)
**Trigger:** {symfony_deps}

- **Bundle-Organization**: Bundles for code organization
- **Console-Commands**: Symfony Console for CLI commands
- **Service-Container**: Service container for dependency injection
- **Event-System**: Event system for loose coupling
- **Doctrine-ORM**: Doctrine ORM integration

## Gin (Backend:Gin)
**Trigger:** {gin_deps}

- **Middleware-Chain**: Middleware for logging, auth, recovery
- **Group-Routes**: Route groups for API versioning
- **Binding-Validation**: ShouldBind for request validation
- **Context-Values**: Use c.Set/c.Get for request-scoped values
- **Graceful-Shutdown-Gin**: os.Signal for graceful shutdown
- **Recovery-Middleware**: Use gin.Recovery for panic handling

## Echo (Backend:Echo)
**Trigger:** {echo_deps}

- **Middleware-Stack**: Built-in middleware for common needs
- **Validator-Integration**: Use echo.Validator for validation
- **Binder-Custom**: Custom binders for complex requests
- **Context-Extension**: Extend context for custom data
- **Static-Files**: Static file serving with cache headers

## Fiber (Backend:Fiber)
**Trigger:** {fiber_deps}

- **Fasthttp-Based**: Leverage fasthttp performance
- **Middleware-Use**: Use built-in middleware stack
- **Prefork-Mode**: Prefork for multi-core utilization
- **Storage-Drivers**: Session storage with multiple drivers
- **Rate-Limiter**: Built-in rate limiting middleware

## Chi (Backend:Chi)
**Trigger:** {chi_deps}

- **Context-Native**: Use chi.URLParam with stdlib context
- **Middleware-Chain**: Compose middleware with Use/With
- **Route-Groups**: Group routes with common middleware
- **Pattern-Routing**: URL parameters with {param} syntax
- **Graceful-Shutdown-Chi**: Built-in graceful shutdown support
- **Lightweight**: Minimal dependencies, stdlib compatible

## Gorilla Mux (Backend:Gorilla)
**Trigger:** {gorilla_deps}

- **Route-Matching**: Path variables with {name} or {name:pattern}
- **Method-Matching**: Methods().Handler() for HTTP method routing
- **Subrouters**: PathPrefix() for route grouping
- **Middleware-Wrapper**: Use() for middleware registration
- **Host-Matching**: Host() for virtual host routing
- **Query-Matching**: Queries() for query parameter matching

## Actix-web (Backend:Actix)
**Trigger:** {actix_deps}

- **Actor-System**: Use actors for concurrent state
- **Extractors-Type**: Type-safe extractors for requests
- **Middleware-Wrap**: Wrap services with middleware
- **State-Shared**: Web::Data for shared application state
- **Error-Handling-Actix**: Implement ResponseError for custom errors
- **Async-Handlers**: async fn for all request handlers

## Axum (Backend:Axum)
**Trigger:** {axum_deps}

- **Tower-Based**: Leverage tower middleware ecosystem
- **Extractors-Order**: Extractor order matters (body last)
- **State-Extension**: Extension for request-local state
- **Router-Nest**: Nest routers for modularity
- **Error-Into-Response**: Implement IntoResponse for errors
- **Layer-Stack**: Layer stack for cross-cutting concerns

## Rocket (Backend:Rocket)
**Trigger:** {rocket_deps}

- **Fairings-Lifecycle**: Fairings for lifecycle hooks
- **Guards-Request**: Request guards for validation
- **Responders-Custom**: Custom responders for responses
- **Managed-State**: Managed state for application data
- **Config-Environment**: Environment-based configuration
- **Catchers-Error**: Error catchers for custom error pages

## Warp (Backend:Warp)
**Trigger:** {warp_deps}

- **Filter-Composition**: Compose filters with and/or/map
- **Rejection-Handling**: Custom rejection handlers for errors
- **Path-Extraction**: Type-safe path parameter extraction
- **Body-Parsing**: JSON/form body parsing with filters
- **TLS-Support**: Built-in TLS with rustls
- **Streaming**: Stream responses with hyper integration

## ASP.NET Core (Backend:AspNetCore)
**Trigger:** {aspnet_markers}

- **Dependency-Injection**: Built-in DI container
- **Middleware-Pipeline**: Request pipeline configuration
- **Minimal-API**: Minimal APIs for simple endpoints
- **Options-Pattern**: IOptions for configuration
- **Health-Checks**: Built-in health check endpoints
- **Logging-Structured**: Structured logging with ILogger
- **EF-Core**: Entity Framework Core for data access
- **Identity-Auth**: ASP.NET Identity for authentication

## Blazor (Frontend:Blazor)
**Trigger:** {blazor_deps}

- **Render-Mode**: Choose Server vs WebAssembly vs Auto based on use case
- **Component-Parameters**: Use [Parameter] for component inputs
- **Cascading-Values**: Use CascadingParameter for deep prop passing
- **JS-Interop**: IJSRuntime for JavaScript calls, minimize usage
- **State-Container**: Scoped services for state management
- **Virtualize**: Use Virtualize component for large lists
- **EditForm-Validation**: EditForm with DataAnnotations validation
- **Auth-State**: AuthenticationStateProvider for auth handling
- **Streaming-Rendering**: Use streaming rendering for slow data

## Ktor (Backend:Ktor)
**Trigger:** {ktor_deps}

- **Plugins-System**: Install plugins for features
- **Routing-DSL**: Type-safe routing DSL
- **Serialization-Content**: Content negotiation for serialization
- **Authentication-Plugins**: Authentication via plugins
- **Client-Same-API**: Same API for client and server
- **Coroutines-Native**: Native coroutines support

## Exposed (ORM:Exposed)
**Trigger:** {exposed_deps}

- **DSL-vs-DAO**: Use DSL for complex queries, DAO for simple CRUD
- **Transaction-Block**: Wrap operations in transaction {} block
- **Lazy-Loading**: Configure lazy loading for relationships
- **Batch-Insert**: Use batchInsert for bulk operations
- **Schema-Generation**: Use SchemaUtils for DDL generation
- **Coroutines-Support**: Use newSuspendedTransaction for coroutines

## Vapor (Backend:Vapor)
**Trigger:** {vapor_deps}

- **Fluent-ORM**: Fluent ORM for database operations
- **Middleware-Chain**: Middleware for request processing
- **Leaf-Templates**: Leaf templating engine
- **Async-Handlers-Vapor**: Swift async/await for handlers
- **Validation-Request**: Request validation with Validatable
- **Environment-Config**: Environment-based configuration
