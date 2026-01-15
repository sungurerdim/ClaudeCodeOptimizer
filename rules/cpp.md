# C++ Rules
*Stack-specific rules for C++ projects*

**Trigger:** {cpp_manifest}, {cpp_ext}

- **RAII-Pattern**: Resource acquisition is initialization
- **Smart-Pointers**: unique_ptr/shared_ptr over raw pointers
- **Move-Semantics**: std::move for efficient transfers
- **Const-Ref**: const& for read-only parameters
- **Modern-Features**: Use modern standards features (concepts, ranges, modules)
- **STL-Algorithms**: Prefer STL algorithms over manual loops
- **Exception-Safe**: Strong exception safety guarantee
- **Static-Analysis**: Include clang-tidy, cppcheck in CI workflows
