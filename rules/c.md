# C Rules
*Stack-specific rules for C projects*

**Trigger:** {c_manifest}, {c_ext}

- **Memory-Manual**: Explicit malloc/free, check null returns
- **Buffer-Safe**: Use safe string functions (strncpy, snprintf)
- **Const-Correct**: const for read-only parameters and returns
- **Header-Guards**: Include guards or #pragma once
- **Static-Analysis**: Include clang-tidy, cppcheck in CI workflows
- **Valgrind-Test**: Include memory leak detection (valgrind) in test targets
- **Compiler-Warnings**: Use -Wall -Wextra -Werror flags
