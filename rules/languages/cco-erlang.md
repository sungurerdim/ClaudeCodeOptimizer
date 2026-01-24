# Erlang Rules
*Stack-specific rules for Erlang projects*

**Trigger:** {erlang_manifest}, {erlang_ext}

- **OTP-Patterns**: Use OTP behaviors (gen_server, gen_statem, supervisor)
- **Let-It-Crash**: Fail fast, let supervisors handle recovery
- **Message-Passing**: Message passing for process communication
- **Pattern-Match**: Pattern matching in function heads
- **Tail-Recursion**: Tail-recursive functions for loops
- **Hot-Code**: Design for hot code reloading
- **ETS-Mnesia**: ETS for fast lookups, Mnesia for distributed state
- **Dialyzer-Types**: Type specs for Dialyzer analysis
- **Rebar3-Build**: Use rebar3 for build management
- **PropEr-Test**: Property-based testing with PropEr or EQC
