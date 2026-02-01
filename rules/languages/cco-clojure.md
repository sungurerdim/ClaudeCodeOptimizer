# Clojure Rules
*Stack-specific rules for Clojure projects*

**Trigger:** {clojure_manifest}, {clojure_ext}

## Immutable-First

Leverage immutable data structures by default

## Pure-Functions

Pure functions over side effects, isolate I/O

## REPL-Driven

REPL-driven development workflow

## Spec-Validate

Use clojure.spec for data validation and documentation

## Namespaces

Namespace per file, clear require/import

## Threading-Macros

Use -> and ->> for readability

## Protocols-Multimethods

Protocols for polymorphism, multimethods for open dispatch

## Atoms-Refs

Atoms for uncoordinated state, refs for coordinated transactions

## Core-Async

core.async for async programming patterns

## Deps-Edn

Prefer deps.edn over Leiningen for new projects
