"""
Universal Project Detection Engine - CCO

Detects languages, frameworks, tools, and project patterns.
100% generic - zero hardcoded project assumptions.
Works with 23 languages, 32+ frameworks, 20+ project types, 34+ tools.

Supports:
- Languages (23): Python, JS, TS, Rust, Go, Java, Kotlin, C#, Ruby, PHP, Swift, Dart,
                  Elixir, Scala, R, Lua, Shell, C, C++, HTML, CSS, Groovy, Haskell
- Frameworks (32+): FastAPI, Django, Flask, React, Vue, Angular, Express, Next.js, Actix,
                    Gin, Spring, Rails, Laravel, Flutter, Phoenix, ASP.NET, Svelte, Astro
- Project Types (20): API, Web, CLI, Library, Mobile, Microservice, Desktop, Data Science,
                      Machine Learning, DevOps, Blockchain, Game, Embedded, Scraper, Bot,
                      Plugin, Monorepo, Serverless, Documentation, Testing
- Tools (34+): Docker, K8s, pytest, jest, black, ruff, mypy, eslint, prettier, GitHub Actions
"""

import json
import logging
import os
import re
import sys
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field

# Standalone detection module - no external dependencies required
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Constants (inlined to maintain standalone module independence)
SEPARATOR_WIDTH = 80
TOP_ITEMS_DISPLAY = {
    "languages": 10,
    "frameworks": 10,
    "tools": 15,
    "project_types": 3,
    "principles": 15,
    "commands": 10,
}

# Detection Confidence Thresholds (U_DRY - DRY Enforcement)
DETECTION_CONFIDENCE_LOW = 0.3
DETECTION_CONFIDENCE_MEDIUM = 0.4
DETECTION_CONFIDENCE_STANDARD = 0.5
DETECTION_CONFIDENCE_HIGH = 0.6
DETECTION_CONFIDENCE_VERY_HIGH = 0.8

# Detection Sampling Limits
CONTENT_SAMPLE_LIMIT = 20  # Maximum files to sample for content detection
PATTERN_MATCH_LIMIT = 10  # Maximum pattern matches to collect

# CLI Arguments
MIN_CLI_ARGS = 2  # Minimum CLI arguments required


@dataclass
class DetectionResult:
    """Result from project analysis"""

    category: str
    detected_value: str
    confidence: float
    evidence: List[str] = field(default_factory=list)

    def dict(self) -> dict:
        """Convert to dict for JSON serialization"""
        return asdict(self)


@dataclass
class ProjectAnalysisReport:
    """Complete project analysis output"""

    languages: List[DetectionResult] = field(default_factory=list)
    frameworks: List[DetectionResult] = field(default_factory=list)
    project_types: List[DetectionResult] = field(default_factory=list)
    tools: List[DetectionResult] = field(default_factory=list)
    codebase_patterns: dict = field(default_factory=dict)
    project_root: str = ""
    analyzed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    analysis_duration_ms: int = 0

    def dict(self) -> dict:
        """Convert to dict for JSON serialization"""
        return {
            "languages": [asdict(x) for x in self.languages],
            "frameworks": [asdict(x) for x in self.frameworks],
            "project_types": [asdict(x) for x in self.project_types],
            "tools": [asdict(x) for x in self.tools],
            "codebase_patterns": self.codebase_patterns,
            "project_root": self.project_root,
            "analyzed_at": self.analyzed_at,
            "analysis_duration_ms": self.analysis_duration_ms,
        }


class UniversalDetector:
    """Detects languages, frameworks, and tools in any project"""

    # Language detection patterns (file extensions + content)
    LANGUAGE_PATTERNS = {
        "python": {
            "extensions": [".py"],
            "config_files": [
                "setup.py",
                "setup.cfg",
                "pyproject.toml",
                "requirements.txt",
                "Pipfile",
                "poetry.lock",
            ],
            "content_patterns": [
                r"^import\s+\w+",
                r"^from\s+\w+\s+import",
                r"^def\s+\w+\s*\(",
                r"^class\s+\w+",
            ],
            "confidence_boost": ["pyproject.toml", "requirements.txt", "setup.py"],
        },
        "javascript": {
            "extensions": [".js", ".mjs"],
            "config_files": ["package.json", "webpack.config.js", ".babelrc"],
            "content_patterns": [
                r"const\s+\w+\s*=",
                r"function\s+\w+\s*\(",
                r"import\s+",
                r"require\(\)",
            ],
            "confidence_boost": ["package.json"],
        },
        "typescript": {
            "extensions": [".ts", ".tsx"],
            "config_files": ["tsconfig.json", "package.json"],
            "content_patterns": [
                r":\s*(string|number|boolean|any|interface|type|class)",
                r"interface\s+\w+",
                r"type\s+\w+\s*=",
            ],
            "confidence_boost": ["tsconfig.json"],
        },
        "rust": {
            "extensions": [".rs"],
            "config_files": ["Cargo.toml", "Cargo.lock"],
            "content_patterns": [r"fn\s+\w+\s*\(", r"impl\s+\w+", r"struct\s+\w+", r"use\s+"],
            "confidence_boost": ["Cargo.toml"],
        },
        "go": {
            "extensions": [".go"],
            "config_files": ["go.mod", "go.sum"],
            "content_patterns": [r"package\s+\w+", r"func\s+\w+\s*\(", r"import\s+\("],
            "confidence_boost": ["go.mod"],
        },
        "java": {
            "extensions": [".java"],
            "config_files": ["pom.xml", "build.gradle", "build.gradle.kts"],
            "content_patterns": [
                r"package\s+\w+",
                r"class\s+\w+",
                r"public\s+(class|interface|void|static)",
            ],
            "confidence_boost": ["pom.xml", "build.gradle"],
        },
        "kotlin": {
            "extensions": [".kt", ".kts"],
            "config_files": ["build.gradle.kts"],
            "content_patterns": [r"fun\s+\w+\s*\(", r"class\s+\w+", r"data\s+class"],
            "confidence_boost": ["build.gradle.kts"],
        },
        "csharp": {
            "extensions": [".cs"],
            "config_files": ["*.csproj", "*.sln"],
            "content_patterns": [r"namespace\s+", r"class\s+\w+", r"public\s+", r"async\s+"],
            "confidence_boost": [".csproj"],
        },
        "ruby": {
            "extensions": [".rb"],
            "config_files": ["Gemfile", "Rakefile", ".ruby-version"],
            "content_patterns": [r"def\s+\w+", r"class\s+\w+", r"^require", r"^\s*#"],
            "confidence_boost": ["Gemfile"],
        },
        "php": {
            "extensions": [".php"],
            "config_files": ["composer.json", "composer.lock"],
            "content_patterns": [r"<\?php", r"function\s+\w+", r"class\s+\w+", r"\$\w+\s*="],
            "confidence_boost": ["composer.json"],
        },
        "swift": {
            "extensions": [".swift"],
            "config_files": ["Package.swift"],
            "content_patterns": [r"func\s+\w+\s*\(", r"class\s+\w+", r"struct\s+\w+", r"import\s+"],
            "confidence_boost": ["Package.swift"],
        },
        "dart": {
            "extensions": [".dart"],
            "config_files": ["pubspec.yaml"],
            "content_patterns": [r"void\s+\w+\s*\(", r"class\s+\w+", r"import\s+"],
            "confidence_boost": ["pubspec.yaml"],
        },
        "elixir": {
            "extensions": [".ex", ".exs"],
            "config_files": ["mix.exs"],
            "content_patterns": [r"def\s+\w+", r"defmodule\s+", r"require\s+"],
            "confidence_boost": ["mix.exs"],
        },
        "scala": {
            "extensions": [".scala"],
            "config_files": ["build.sbt"],
            "content_patterns": [r"def\s+\w+", r"class\s+\w+", r"object\s+\w+"],
            "confidence_boost": ["build.sbt"],
        },
        "r": {
            "extensions": [".r", ".R"],
            "config_files": ["DESCRIPTION"],
            "content_patterns": [r"<-", r"function\s*\(", r"library\("],
            "confidence_boost": ["DESCRIPTION"],
        },
        "lua": {
            "extensions": [".lua"],
            "config_files": ["init.lua"],
            "content_patterns": [r"function\s+\w+", r"local\s+\w+", r"require\("],
            "confidence_boost": ["init.lua"],
        },
        "shell": {
            "extensions": [".sh", ".bash"],
            "config_files": [".bashrc", ".zshrc"],
            "content_patterns": [r"^#!/bin/(ba)?sh", r"function\s+\w+\s*\{", r"if\s+\["],
            "confidence_boost": ["Makefile"],
        },
        "c": {
            "extensions": [".c"],
            "config_files": ["CMakeLists.txt"],
            "content_patterns": [r"#include\s*<", r"int\s+main\s*\(", r"void\s+\w+\s*\("],
            "confidence_boost": ["CMakeLists.txt"],
        },
        "cpp": {
            "extensions": [".cpp", ".cc", ".cxx", ".h", ".hpp"],
            "config_files": ["CMakeLists.txt"],
            "content_patterns": [r"#include\s*<", r"class\s+\w+", r"namespace\s+"],
            "confidence_boost": ["CMakeLists.txt"],
        },
        "html": {
            "extensions": [".html", ".htm"],
            "config_files": [],
            "content_patterns": [r"<!DOCTYPE\s+html", r"<html", r"<body>"],
            "confidence_boost": ["index.html"],
        },
        "css": {
            "extensions": [".css"],
            "config_files": [".prettierrc", ".stylelintrc"],
            "content_patterns": [r"^[.\#]?\w+\s*\{", r"selector\s*\{"],
            "confidence_boost": [],
        },
        "groovy": {
            "extensions": [".groovy"],
            "config_files": [],
            "content_patterns": [r"def\s+\w+", r"class\s+\w+"],
            "confidence_boost": [],
        },
        "haskell": {
            "extensions": [".hs"],
            "config_files": ["stack.yaml", "*.cabal"],
            "content_patterns": [r"^module\s+", r"::\s+", r"->\s+"],
            "confidence_boost": ["stack.yaml"],
        },
    }

    # Framework detection patterns
    FRAMEWORK_PATTERNS = {
        # Python frameworks
        "fastapi": {
            "languages": ["python"],
            "files": ["requirements.txt", "pyproject.toml", "setup.py"],
            "patterns": [r"fastapi", r"FastAPI\s*\("],
            "confidence_boost": ["main.py", "app.py"],
        },
        "django": {
            "languages": ["python"],
            "files": ["requirements.txt", "manage.py"],
            "patterns": [r"django", r"Django\s+version", r"django\."],
            "confidence_boost": ["manage.py", "settings.py"],
        },
        "flask": {
            "languages": ["python"],
            "files": ["requirements.txt"],
            "patterns": [r"flask", r"from\s+flask\s+import"],
            "confidence_boost": ["app.py"],
        },
        "starlette": {
            "languages": ["python"],
            "files": ["requirements.txt", "pyproject.toml"],
            "patterns": [r"starlette"],
            "confidence_boost": [],
        },
        # JavaScript/TypeScript frameworks
        "react": {
            "languages": ["javascript", "typescript"],
            "files": ["package.json", "package-lock.json"],
            "patterns": [r"react", r"\"react\"\s*:", r"import.*React"],
            "confidence_boost": ["App.jsx", "App.tsx"],
        },
        "vue": {
            "languages": ["javascript", "typescript"],
            "files": ["package.json"],
            "patterns": [r"vue", r"\"vue\"\s*:", r"\.vue\s+files"],
            "confidence_boost": ["App.vue"],
        },
        "angular": {
            "languages": ["typescript"],
            "files": ["package.json", "angular.json"],
            "patterns": [r"@angular", r"\"@angular"],
            "confidence_boost": ["angular.json"],
        },
        "express": {
            "languages": ["javascript", "typescript"],
            "files": ["package.json"],
            "patterns": [r"express", r"\"express\"\s*:"],
            "confidence_boost": ["server.js", "index.js"],
        },
        "nextjs": {
            "languages": ["javascript", "typescript"],
            "files": ["package.json", "next.config.js"],
            "patterns": [r"next", r"\"next\"\s*:"],
            "confidence_boost": ["next.config.js"],
        },
        "nuxt": {
            "languages": ["javascript"],
            "files": ["package.json", "nuxt.config.js"],
            "patterns": [r"nuxt", r"\"nuxt\"\s*:"],
            "confidence_boost": ["nuxt.config.js"],
        },
        "svelte": {
            "languages": ["javascript", "typescript"],
            "files": ["package.json"],
            "patterns": [r"svelte", r"\.svelte\s+files"],
            "confidence_boost": ["App.svelte"],
        },
        "astro": {
            "languages": ["javascript", "typescript"],
            "files": ["package.json", "astro.config.mjs"],
            "patterns": [r"astro"],
            "confidence_boost": ["astro.config.mjs"],
        },
        "remix": {
            "languages": ["javascript", "typescript"],
            "files": ["package.json"],
            "patterns": [r"remix"],
            "confidence_boost": [],
        },
        # Rust frameworks
        "actix": {
            "languages": ["rust"],
            "files": ["Cargo.toml"],
            "patterns": [r"actix-web", r"actix-rt"],
            "confidence_boost": ["main.rs"],
        },
        "axum": {
            "languages": ["rust"],
            "files": ["Cargo.toml"],
            "patterns": [r"axum"],
            "confidence_boost": [],
        },
        "rocket": {
            "languages": ["rust"],
            "files": ["Cargo.toml"],
            "patterns": [r"rocket"],
            "confidence_boost": [],
        },
        # Go frameworks
        "gin": {
            "languages": ["go"],
            "files": ["go.mod"],
            "patterns": [r"github\.com/gin-gonic/gin"],
            "confidence_boost": ["main.go"],
        },
        "gorilla": {
            "languages": ["go"],
            "files": ["go.mod"],
            "patterns": [r"github\.com/gorilla"],
            "confidence_boost": [],
        },
        "echo": {
            "languages": ["go"],
            "files": ["go.mod"],
            "patterns": [r"github\.com/labstack/echo"],
            "confidence_boost": [],
        },
        # Java frameworks
        "spring": {
            "languages": ["java"],
            "files": ["pom.xml", "build.gradle"],
            "patterns": [r"spring-boot", r"org\.springframework"],
            "confidence_boost": ["pom.xml"],
        },
        "quarkus": {
            "languages": ["java"],
            "files": ["pom.xml"],
            "patterns": [r"quarkus"],
            "confidence_boost": [],
        },
        "micronaut": {
            "languages": ["java"],
            "files": ["pom.xml"],
            "patterns": [r"micronaut"],
            "confidence_boost": [],
        },
        # Ruby frameworks
        "rails": {
            "languages": ["ruby"],
            "files": ["Gemfile", "config/application.rb"],
            "patterns": [r"rails", r"Rails"],
            "confidence_boost": ["config/application.rb"],
        },
        "sinatra": {
            "languages": ["ruby"],
            "files": ["Gemfile"],
            "patterns": [r"sinatra"],
            "confidence_boost": [],
        },
        # PHP frameworks
        "laravel": {
            "languages": ["php"],
            "files": ["composer.json", "artisan"],
            "patterns": [r"laravel"],
            "confidence_boost": ["artisan"],
        },
        "symfony": {
            "languages": ["php"],
            "files": ["composer.json"],
            "patterns": [r"symfony"],
            "confidence_boost": [],
        },
        "yii": {
            "languages": ["php"],
            "files": ["composer.json"],
            "patterns": [r"yiisoft"],
            "confidence_boost": [],
        },
        # Mobile frameworks
        "flutter": {
            "languages": ["dart"],
            "files": ["pubspec.yaml"],
            "patterns": [r"flutter"],
            "confidence_boost": ["pubspec.yaml"],
        },
        "react-native": {
            "languages": ["javascript", "typescript"],
            "files": ["package.json"],
            "patterns": [r"react-native"],
            "confidence_boost": [],
        },
        # Elixir frameworks
        "phoenix": {
            "languages": ["elixir"],
            "files": ["mix.exs"],
            "patterns": [r":phoenix"],
            "confidence_boost": ["mix.exs"],
        },
        # C# frameworks
        "aspnet": {
            "languages": ["csharp"],
            "files": ["*.csproj"],
            "patterns": [r"Microsoft\.AspNetCore"],
            "confidence_boost": [".csproj"],
        },
        "entity-framework": {
            "languages": ["csharp"],
            "files": ["*.csproj"],
            "patterns": [r"EntityFramework"],
            "confidence_boost": [],
        },
    }

    # Tool detection patterns
    TOOL_PATTERNS = {
        # Container orchestration
        "docker": {
            "files": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml", ".dockerignore"],
            "patterns": [r"FROM\s+", r"docker"],
            "confidence_boost": ["Dockerfile"],
        },
        "kubernetes": {
            "files": ["*.yaml", "*.yml"],
            "patterns": [r"kind:\s+(Pod|Service|Deployment)", r"apiVersion:\s+v1"],
            "confidence_boost": ["deployment.yaml", "service.yaml"],
        },
        # Testing frameworks
        "pytest": {
            "files": ["pyproject.toml", "pytest.ini", "setup.cfg"],
            "patterns": [r"pytest", r"\[tool\.pytest"],
            "confidence_boost": ["pytest.ini"],
        },
        "jest": {
            "files": ["package.json", "jest.config.js"],
            "patterns": [r"jest", r"\"jest\""],
            "confidence_boost": ["jest.config.js"],
        },
        "mocha": {
            "files": ["package.json"],
            "patterns": [r"mocha"],
            "confidence_boost": [],
        },
        "unittest": {
            "files": ["test_*.py", "*_test.py"],
            "patterns": [r"import\s+unittest", r"from\s+unittest"],
            "confidence_boost": [],
        },
        "rspec": {
            "files": ["spec_helper.rb"],
            "patterns": [r"rspec"],
            "confidence_boost": [],
        },
        # Code formatting/linting
        "black": {
            "files": ["pyproject.toml", ".black"],
            "patterns": [r"black", r"\[tool\.black\]"],
            "confidence_boost": ["pyproject.toml"],
        },
        "ruff": {
            "files": ["pyproject.toml", ".ruff.toml"],
            "patterns": [r"ruff", r"\[tool\.ruff\]"],
            "confidence_boost": ["pyproject.toml"],
        },
        "mypy": {
            "files": ["pyproject.toml"],
            "patterns": [r"mypy", r"\[tool\.mypy\]"],
            "confidence_boost": ["pyproject.toml"],
        },
        "eslint": {
            "files": [".eslintrc", ".eslintrc.js", ".eslintrc.json", "package.json"],
            "patterns": [r"eslint", r"\"eslint\""],
            "confidence_boost": [".eslintrc"],
        },
        "prettier": {
            "files": [".prettierrc", "prettier.config.js", "package.json"],
            "patterns": [r"prettier"],
            "confidence_boost": [".prettierrc"],
        },
        "stylelint": {
            "files": [".stylelintrc"],
            "patterns": [r"stylelint"],
            "confidence_boost": [],
        },
        "rustfmt": {
            "files": ["rustfmt.toml"],
            "patterns": [r"rustfmt"],
            "confidence_boost": [],
        },
        # CI/CD
        "github-actions": {
            "files": [".github/workflows/*.yml", ".github/workflows/*.yaml"],
            "patterns": [r"name:\s+", r"on:\s+"],
            "confidence_boost": [".github/workflows"],
        },
        "gitlab-ci": {
            "files": [".gitlab-ci.yml"],
            "patterns": [r"stages:\s+", r"script:"],
            "confidence_boost": [".gitlab-ci.yml"],
        },
        "jenkins": {
            "files": ["Jenkinsfile"],
            "patterns": [r"pipeline\s*\{", r"stage\("],
            "confidence_boost": ["Jenkinsfile"],
        },
        "circleci": {
            "files": [".circleci/config.yml"],
            "patterns": [r"version:", r"jobs:"],
            "confidence_boost": [".circleci/config.yml"],
        },
        "travis": {
            "files": [".travis.yml"],
            "patterns": [r"language:", r"script:"],
            "confidence_boost": [".travis.yml"],
        },
        # Package management
        "npm": {
            "files": ["package.json", "package-lock.json"],
            "patterns": [r"\"dependencies\"", r"\"devDependencies\""],
            "confidence_boost": ["package.json"],
        },
        "yarn": {
            "files": ["yarn.lock"],
            "patterns": [r"yarn"],
            "confidence_boost": ["yarn.lock"],
        },
        "pip": {
            "files": ["requirements.txt", "pyproject.toml"],
            "patterns": [r"pip", r"dependencies"],
            "confidence_boost": ["requirements.txt"],
        },
        "poetry": {
            "files": ["poetry.lock", "pyproject.toml"],
            "patterns": [r"poetry"],
            "confidence_boost": ["poetry.lock"],
        },
        "cargo": {
            "files": ["Cargo.toml", "Cargo.lock"],
            "patterns": [r"cargo"],
            "confidence_boost": ["Cargo.toml"],
        },
        "maven": {
            "files": ["pom.xml"],
            "patterns": [r"<project", r"<dependencies>"],
            "confidence_boost": ["pom.xml"],
        },
        "gradle": {
            "files": ["build.gradle", "build.gradle.kts"],
            "patterns": [r"gradle"],
            "confidence_boost": ["build.gradle"],
        },
        "bundler": {
            "files": ["Gemfile", "Gemfile.lock"],
            "patterns": [r"bundler"],
            "confidence_boost": ["Gemfile"],
        },
        "composer": {
            "files": ["composer.json", "composer.lock"],
            "patterns": [r"composer"],
            "confidence_boost": ["composer.json"],
        },
    }

    # Project type patterns (20+ popular types)
    PROJECT_TYPE_PATTERNS = {
        "api": {
            "frameworks": ["fastapi", "django", "flask", "express", "actix", "gin", "spring"],
            "files": ["requirements.txt", "openapi.json", "swagger.json"],
            "patterns": [r"api", r"endpoint", r"route"],
        },
        "web": {
            "frameworks": ["react", "vue", "angular", "nextjs", "nuxt"],
            "files": ["index.html", "public/index.html"],
            "patterns": [],
        },
        "cli": {
            "frameworks": [],
            "files": ["setup.py", "Cargo.toml", "go.mod"],
            "patterns": [r"cli", r"command", r"argument"],
        },
        "library": {
            "frameworks": [],
            "files": ["setup.py", "pyproject.toml", "package.json", "Cargo.toml"],
            "patterns": [r"library", r"module", r"package"],
        },
        "mobile": {
            "frameworks": ["flutter", "react-native"],
            "files": ["pubspec.yaml", "package.json", "AndroidManifest.xml", "Info.plist"],
            "patterns": [r"mobile", r"android", r"ios"],
        },
        "microservice": {
            "frameworks": [],
            "files": ["docker-compose.yml", "Dockerfile"],
            "patterns": [r"microservice", r"service"],
        },
        "desktop": {
            "frameworks": [],
            "files": ["package.json", "tauri.conf.json", "electron-builder.json"],
            "patterns": [r"electron", r"tauri", r"desktop", r"gui"],
        },
        "data-science": {
            "frameworks": [],
            "files": ["requirements.txt", "environment.yml", "*.ipynb"],
            "patterns": [r"jupyter", r"pandas", r"numpy", r"analysis", r"data"],
        },
        "machine-learning": {
            "frameworks": [],
            "files": ["requirements.txt", "model.py", "train.py"],
            "patterns": [r"tensorflow", r"pytorch", r"keras", r"scikit-learn", r"model"],
        },
        "devops": {
            "frameworks": [],
            "files": ["terraform.tf", "ansible.yml", "Vagrantfile"],
            "patterns": [r"infrastructure", r"terraform", r"ansible", r"provisioning"],
        },
        "blockchain": {
            "frameworks": [],
            "files": ["truffle-config.js", "hardhat.config.js", "foundry.toml"],
            "patterns": [r"solidity", r"smart.?contract", r"web3", r"ethereum"],
        },
        "game": {
            "frameworks": [],
            "files": ["*.unity", "*.uproject", "godot.project"],
            "patterns": [r"unity", r"unreal", r"godot", r"game"],
        },
        "embedded": {
            "frameworks": [],
            "files": ["platformio.ini", "*.ino", "CMakeLists.txt"],
            "patterns": [r"embedded", r"iot", r"firmware", r"arduino", r"esp32"],
        },
        "scraper": {
            "frameworks": [],
            "files": ["requirements.txt", "package.json"],
            "patterns": [r"scrapy", r"beautifulsoup", r"selenium", r"puppeteer", r"scraper"],
        },
        "bot": {
            "frameworks": [],
            "files": ["requirements.txt", "package.json"],
            "patterns": [r"discord", r"telegram", r"slack.?bot", r"chatbot"],
        },
        "plugin": {
            "frameworks": [],
            "files": ["plugin.json", "manifest.json", "*.vsix"],
            "patterns": [r"plugin", r"extension", r"addon"],
        },
        "monorepo": {
            "frameworks": [],
            "files": ["lerna.json", "pnpm-workspace.yaml", "nx.json", "turbo.json"],
            "patterns": [r"monorepo", r"workspace", r"packages/"],
        },
        "serverless": {
            "frameworks": [],
            "files": ["serverless.yml", "template.yaml", "netlify.toml", "vercel.json"],
            "patterns": [r"lambda", r"function", r"serverless"],
        },
        "documentation": {
            "frameworks": [],
            "files": ["mkdocs.yml", "docusaurus.config.js", "sphinx.conf"],
            "patterns": [r"documentation", r"docs", r"sphinx", r"mkdocs"],
        },
        "testing": {
            "frameworks": [],
            "files": ["pytest.ini", "jest.config.js", "karma.conf.js"],
            "patterns": [r"test.?framework", r"testing.?suite"],
        },
    }

    def __init__(self, project_root: str) -> None:
        """Initialize detector with project root"""
        self.project_root = Path(project_root)
        self.file_cache: Dict[str, str] = {}
        self.extension_count: Dict[str, int] = defaultdict(int)

    def analyze(self) -> ProjectAnalysisReport:
        """Run complete project analysis"""
        start_time = time.time()

        # Scan project structure
        self._scan_files()

        # Detect components
        languages = self._detect_languages()
        frameworks = self._detect_frameworks()
        project_types = self._detect_project_types()
        tools = self._detect_tools()
        patterns = self._analyze_codebase_patterns()

        duration_ms = int((time.time() - start_time) * 1000)

        return ProjectAnalysisReport(
            languages=languages,
            frameworks=frameworks,
            project_types=project_types,
            tools=tools,
            codebase_patterns=patterns,
            project_root=str(self.project_root),
            analysis_duration_ms=duration_ms,
        )

    def _scan_files(self) -> None:
        """Scan project files for caching"""
        for ext, count in self._count_file_extensions().items():
            self.extension_count[ext] = count

        # Sample config files for content analysis
        for root, dirs, files in os.walk(self.project_root):
            # Skip common non-project directories
            dirs[:] = [
                d
                for d in dirs
                if d
                not in [".git", ".cco", ".claude", "node_modules", "__pycache__", ".venv", "venv"]
            ]

            for file in files:
                if any(
                    file.endswith(ext)
                    for ext in [".toml", ".json", ".yaml", ".yml", ".ini", ".cfg"]
                ):
                    try:
                        with open(os.path.join(root, file), encoding="utf-8", errors="ignore") as f:
                            self.file_cache[file] = f.read(2000)  # Cache first 2KB
                    except (OSError, PermissionError) as e:
                        logging.debug(f"Skipping file {file}: {e}")
                        continue

    def _count_file_extensions(self) -> Dict[str, int]:
        """Count file extensions in project"""
        counts: Dict[str, int] = defaultdict(int)
        try:
            for _root, dirs, files in os.walk(self.project_root):
                dirs[:] = [
                    d
                    for d in dirs
                    if d not in [".git", ".cco", ".claude", "node_modules", "__pycache__"]
                ]
                for file in files:
                    ext = Path(file).suffix.lower()
                    if ext:
                        counts[ext] += 1
        except (OSError, PermissionError) as e:
            logging.warning(f"Error walking directory tree: {e}. Returning partial results.")
        return dict(counts)

    def _detect_languages(self) -> List[DetectionResult]:
        """Detect programming languages used"""
        results: Dict[str, Tuple[float, List[str]]] = {}

        for lang, patterns in self.LANGUAGE_PATTERNS.items():
            confidence = 0.0
            evidence = []

            # Check file extensions
            ext_count = sum(self.extension_count.get(ext, 0) for ext in patterns["extensions"])
            if ext_count > 0:
                confidence = min(0.9, 0.1 + (ext_count * 0.05))
                evidence.append(f"{ext_count} {lang} files")

            # Check config files
            for config in patterns["config_files"]:
                if config in self.file_cache or self._file_exists(config):
                    confidence = max(confidence, 0.9)
                    evidence.append(f"{config} present")

            # Check content patterns in sampled files
            if ext_count > 0 and confidence > DETECTION_CONFIDENCE_STANDARD:
                matching_content = self._check_content_patterns(
                    patterns["extensions"],
                    patterns["content_patterns"],
                )
                if matching_content > 0:
                    confidence = min(1.0, confidence + 0.05)
                    evidence.append(f"Detected {lang} syntax patterns")

            if confidence > DETECTION_CONFIDENCE_LOW:
                results[lang] = (confidence, evidence)

        # Convert to sorted list
        detected = [
            DetectionResult(
                category="language",
                detected_value=lang,
                confidence=conf,
                evidence=evidence,
            )
            for lang, (conf, evidence) in sorted(
                results.items(),
                key=lambda x: x[1][0],
                reverse=True,
            )
        ]

        return detected[: TOP_ITEMS_DISPLAY["languages"]]  # Return top languages

    def _detect_frameworks(self) -> List[DetectionResult]:
        """Detect frameworks used"""
        results: Dict[str, Tuple[float, List[str]]] = {}

        for framework, patterns in self.FRAMEWORK_PATTERNS.items():
            confidence = 0.0
            evidence = []

            # Check config files
            for config_pattern in patterns["files"]:
                matching_files = self._find_files_matching(config_pattern)
                if matching_files:
                    confidence = max(confidence, 0.7)
                    evidence.append(f"Found {len(matching_files)} matching file(s)")

            # Check patterns in config content
            for filename, content in self.file_cache.items():
                for pattern in patterns["patterns"]:
                    if re.search(pattern, content, re.IGNORECASE):
                        confidence = min(1.0, confidence + 0.2)
                        evidence.append(f"'{pattern}' found in {filename}")

            # Confidence boost from specific files
            for boost_file in patterns["confidence_boost"]:
                if self._file_exists(boost_file):
                    confidence = min(1.0, confidence + 0.1)

            if confidence > DETECTION_CONFIDENCE_MEDIUM:
                results[framework] = (confidence, evidence)

        # Convert to sorted list
        detected = [
            DetectionResult(
                category="framework",
                detected_value=fw,
                confidence=conf,
                evidence=evidence[:3],  # Limit evidence
            )
            for fw, (conf, evidence) in sorted(results.items(), key=lambda x: x[1][0], reverse=True)
        ]

        return detected[: TOP_ITEMS_DISPLAY["frameworks"]]  # Return top frameworks

    def _detect_tools(self) -> List[DetectionResult]:
        """Detect development tools and CI/CD systems"""
        results: Dict[str, Tuple[float, List[str]]] = {}

        for tool, patterns in self.TOOL_PATTERNS.items():
            confidence = 0.0
            evidence = []

            # Check for tool files
            for file_pattern in patterns["files"]:
                matching_files = self._find_files_matching(file_pattern)
                if matching_files:
                    confidence = max(confidence, 0.8)
                    evidence.append(f"{len(matching_files)} file(s) found")

            # Check patterns in cached files
            for _filename, content in self.file_cache.items():
                for pattern in patterns["patterns"]:
                    if re.search(pattern, content, re.IGNORECASE | re.MULTILINE):
                        confidence = min(1.0, confidence + 0.15)

            # Confidence boost
            for boost_file in patterns["confidence_boost"]:
                if self._file_exists(boost_file):
                    confidence = min(1.0, confidence + 0.1)

            if confidence > DETECTION_CONFIDENCE_LOW:
                results[tool] = (confidence, evidence)

        # Convert to sorted list
        detected = [
            DetectionResult(
                category="tool",
                detected_value=tool,
                confidence=conf,
                evidence=evidence[:2],
            )
            for tool, (conf, evidence) in sorted(
                results.items(),
                key=lambda x: x[1][0],
                reverse=True,
            )
        ]

        return detected[: TOP_ITEMS_DISPLAY["tools"]]  # Return top tools

    def _detect_project_types(self) -> List[DetectionResult]:
        """Detect project type (API, web, library, etc.)"""
        results: Dict[str, Tuple[float, List[str]]] = {}

        for project_type, patterns in self.PROJECT_TYPE_PATTERNS.items():
            confidence = 0.0
            evidence = []

            # Check for type-specific files
            for file_pattern in patterns["files"]:
                if self._file_exists(file_pattern) or self._find_files_matching(file_pattern):
                    confidence = max(confidence, 0.5)
                    evidence.append(f"Found {file_pattern}")

            # Check frameworks match
            detected_frameworks = {fw.detected_value for fw in self._detect_frameworks()}
            matching_frameworks = set(patterns["frameworks"]) & detected_frameworks
            if matching_frameworks:
                confidence = min(1.0, confidence + 0.3)
                evidence.append(f"Matches frameworks: {', '.join(matching_frameworks)}")

            if confidence > DETECTION_CONFIDENCE_MEDIUM:
                results[project_type] = (confidence, evidence)

        # Convert to sorted list
        detected = [
            DetectionResult(
                category="project_type",
                detected_value=ptype,
                confidence=conf,
                evidence=evidence,
            )
            for ptype, (conf, evidence) in sorted(
                results.items(),
                key=lambda x: x[1][0],
                reverse=True,
            )
        ]

        return detected[:5]

    def _analyze_codebase_patterns(self) -> Dict[str, Any]:
        """Analyze codebase patterns (metrics that are language-agnostic)"""
        patterns: Dict[str, Any] = {
            "total_files": sum(self.extension_count.values()),
            "extension_distribution": dict(self.extension_count),
            "has_tests": self._file_exists("test*.py") or self._file_exists("*.test.js"),
            "has_ci_cd": any(
                self._file_exists(f) for f in [".github/workflows", ".gitlab-ci.yml", "Jenkinsfile"]
            ),
            "has_docker": self._file_exists("Dockerfile")
            or self._file_exists("docker-compose.yml"),
            "has_config": any(
                self._file_exists(f) for f in ["pyproject.toml", "package.json", ".env.example"]
            ),
        }

        # Count key file types
        patterns["config_files_count"] = len(
            [f for f in self.file_cache.keys() if f.endswith((".toml", ".json", ".yaml", ".yml"))],
        )
        patterns["source_files_count"] = sum(self.extension_count.values())

        return patterns

    def _check_content_patterns(self, extensions: List[str], patterns: List[str]) -> int:
        """Check how many files match content patterns"""
        matches = 0
        scanned = 0
        try:
            for root, dirs, files in os.walk(self.project_root):
                dirs[:] = [d for d in dirs if d not in [".git", ".cco", ".claude", "node_modules"]]
                for file in files:
                    if any(file.endswith(ext) for ext in extensions):
                        scanned += 1
                        if scanned > CONTENT_SAMPLE_LIMIT:  # Sample limit
                            break
                        try:
                            path = os.path.join(root, file)
                            with open(path, encoding="utf-8", errors="ignore") as f:
                                content = f.read(500)
                                for pattern in patterns:
                                    if re.search(pattern, content):
                                        matches += 1
                                        break
                        except (OSError, PermissionError, UnicodeDecodeError) as e:
                            logging.debug(f"Skipping file {file}: {e}")
                            continue
        except (OSError, PermissionError) as e:
            logging.warning(f"Error scanning content patterns: {e}. Returning partial results.")
        return matches

    def _find_files_matching(self, pattern: str) -> List[str]:
        """Find files matching a glob pattern"""
        matches = []
        try:
            if "*" in pattern:
                # Handle glob patterns
                pattern_obj = re.compile(
                    pattern.replace(".", r"\.").replace("*", ".*"),
                    re.IGNORECASE,
                )
                for root, dirs, files in os.walk(self.project_root):
                    dirs[:] = [
                        d for d in dirs if d not in [".git", ".cco", ".claude", "node_modules"]
                    ]
                    for file in files:
                        if pattern_obj.match(file):
                            matches.append(os.path.join(root, file))
                            if len(matches) > PATTERN_MATCH_LIMIT:
                                break
            else:
                # Direct file check
                if self._file_exists(pattern):
                    matches.append(pattern)
        except (OSError, PermissionError, re.error) as e:
            logging.warning(
                f"Error finding files matching '{pattern}': {e}. Returning partial results."
            )
        return matches

    def _file_exists(self, filename: str) -> bool:
        """Check if file exists in project"""
        try:
            if "*" in filename:
                return len(self._find_files_matching(filename)) > 0
            path = self.project_root / filename
            return path.exists()
        except Exception:
            return False


def print_report(report: ProjectAnalysisReport) -> None:
    """Print analysis report in human-readable format"""
    print("\n" + "=" * SEPARATOR_WIDTH)
    print("PROJECT ANALYSIS REPORT")
    print("=" * SEPARATOR_WIDTH)
    print(f"\nProject Root: {report.project_root}")
    print(f"Analysis Time: {report.analyzed_at}")
    print(f"Analysis Duration: {report.analysis_duration_ms}ms")

    if report.languages:
        print("\n[LANGUAGES]")
        for lang in report.languages[: TOP_ITEMS_DISPLAY["languages"]]:
            print(
                f"  {lang.detected_value:15} {lang.confidence:.0%}  {', '.join(lang.evidence[:2])}",
            )

    if report.frameworks:
        print("\n[FRAMEWORKS]")
        for fw in report.frameworks[: TOP_ITEMS_DISPLAY["frameworks"]]:
            print(f"  {fw.detected_value:20} {fw.confidence:.0%}  {', '.join(fw.evidence[:1])}")

    if report.project_types:
        print("\n[PROJECT TYPES]")
        for ptype in report.project_types:
            print(f"  {ptype.detected_value:15} {ptype.confidence:.0%}")

    if report.tools:
        print("\n[TOOLS & CI/CD]")
        for tool in report.tools[: TOP_ITEMS_DISPLAY["tools"]]:
            print(f"  {tool.detected_value:20} {tool.confidence:.0%}")

    if report.codebase_patterns:
        print("\n[CODEBASE PATTERNS]")
        patterns = report.codebase_patterns
        print(f"  Total Files:        {patterns.get('total_files', 0)}")
        print(f"  Has Tests:          {patterns.get('has_tests', False)}")
        print(f"  Has CI/CD:          {patterns.get('has_ci_cd', False)}")
        print(f"  Has Docker:         {patterns.get('has_docker', False)}")
        print(f"  Config Files:       {patterns.get('config_files_count', 0)}")

    print("\n" + "=" * SEPARATOR_WIDTH)


def main() -> int:
    """CLI entry point"""
    if len(sys.argv) < MIN_CLI_ARGS:
        print("Usage: python detection.py <project_root>")
        print("\nExample:")
        print("  python detection.py D:\\GitHub\\backend")
        sys.exit(1)

    project_root = sys.argv[1]

    if not os.path.isdir(project_root):
        print(f"Error: Directory not found: {project_root}")
        sys.exit(1)

    print(f"Analyzing project: {project_root}")
    print("(This may take a moment...)\n")

    detector = UniversalDetector(project_root)
    report = detector.analyze()

    print_report(report)

    # Output JSON if requested
    if "--json" in sys.argv:
        print("\n[JSON OUTPUT]")
        print(json.dumps(report.dict(), indent=2, default=str))

    return 0


if __name__ == "__main__":
    sys.exit(main())
