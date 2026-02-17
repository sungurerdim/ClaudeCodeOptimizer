# Changelog

## [5.0.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.2.2...v5.0.0) (2026-02-17)


### ⚠ BREAKING CHANGES

* commands/ directory replaced by skills/ with SKILL.md files. Install scripts (install.sh, install.ps1) replaced by Go binary installer. Run ./cco install to migrate.
* rule structure reorganized into 5 categories
* CCO is no longer distributed as a Claude Code plugin. Install via `curl -fsSL .../install.sh | bash` (Unix) or `irm .../install.ps1 | iex` (Windows). Commands renamed from `/cco:*` to `/cco-*` format.
* **core:** Installation now via `/plugin marketplace add` instead of `pip install`
* **release:** Command renames from v1.0.0:
    - /cco-tune → /cco-config
    - /cco-health → /cco-status
    - /cco-audit → /cco-optimize
    - /cco-refactor → /cco-review
    - /cco-generate → /cco-research

### refactor

* **core:** migrate to plugin architecture ([5145f4b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/5145f4b28af3b0fdda65dbc93587b94509f2cad9))


### chore

* **release:** bump version to 2.0.0 ([f299f3d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/f299f3d93106cff1df5aaa4003df69389b756a07))


### Features

* add blueprint, pr commands and feature branch workflow ([#11](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/11)) ([6243c7b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6243c7b65ec09d8dcdc56853f3404c36780aa298))
* add stable/dev channel support to install scripts ([e735f83](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/e735f83360ea80f04426ef506539cae05cc404dd))
* **agents:** embed artifact handling and strategy evolution ([1446faf](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1446fafe844c70b404975071073ca0ca060f9703))
* **agents:** expand analyze scopes, add research ([c651bff](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/c651bffbe3a3feb2851db385d0fb8d890571f383))
* **analyze:** add projectCritical extraction ([d3f97a3](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d3f97a37a3c4c094ea1df9922c687ee2c3178f02))
* **audit:** add AI-patterns detection ([f861253](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/f86125336e021430e01530a51d57401beb01db95))
* **benchmark:** add --deps flag to ccbox commands ([5078bc5](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/5078bc593741abd73c2e7090f2519470e5fd5d38))
* **benchmark:** add -s auto flag to ccbox ([375eeb4](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/375eeb45c13a58f8a278e62fdc750d29c7292ce7))
* **benchmark:** add AI-powered comparison via ccbox ([1943f1f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1943f1fb440382e490bffeb45da1ef932b9cfb8b))
* **benchmark:** add blind 10-dimension AI comparison ([07a5bfb](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/07a5bfb3de7c354d34e3f2f5209b3b5030a52f9b))
* **benchmark:** add comprehensive benchmark suite for CCO evaluation ([897bcbe](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/897bcbefcc9a992a8cb8c1dde4d0f9b6638f7900))
* **benchmark:** add comprehensive multi-dimensional analyzer ([8407cd7](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/8407cd7eee2553629c97ab1cff2b453c0831f781))
* **benchmark:** add date column to results table ([b7aae41](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/b7aae41b99cf3453c53328647e9eafc81d0f6895))
* **benchmark:** add Docker dependency validation ([f29e444](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/f29e44401f6ff65cf77d1ca72fe81f304c78fe9c))
* **benchmark:** add executive summary to AI comparison ([4fc6c41](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/4fc6c41b3d95a3eb6598d291ee21da2e7ad808f9))
* **benchmark:** add gosu error handling and docs ([f55f6cb](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/f55f6cbf1404f82d6f79cc8b3d9ae51838dbf830))
* **benchmark:** add refresh and Docker start ([1ec4403](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1ec4403565e5cd1dfadbe2d154657205467674ff))
* **benchmark:** add Reports tab with executive summary ([d0b4b47](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d0b4b47cfff72d6c1fde2a941a2883f53bde2feb))
* **benchmark:** add streaming output ([456db0a](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/456db0ae83c5ede59beada5a4b5be71e834ee269))
* **benchmark:** add unattended CCO config and two-phase setup ([5c977ea](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/5c977ea42ee89c5d48727a2e3f4b1e8277574a20))
* **benchmark:** add weighted scoring system ([4d1bccd](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/4d1bccdce29f8a20a05ca9ed0417c3feee8e1a20))
* **benchmark:** apply Claude 4 best practices to prompts ([9bc974a](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/9bc974a2e79ef5e24a57340a7f4aeaa16943bf91))
* **benchmark:** enhance UI with additional features ([6f55fdf](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6f55fdf733c131902103f60e97c72c7002a56cda))
* **benchmark:** percentage-based impact analysis ([70dcf09](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/70dcf09f9ff22c2e30b24106732cc91678774942))
* **benchmark:** phase timings + visual separators ([7141662](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/71416623319030c0088eb8e620da87093fa5cd2b))
* **benchmark:** update UI to use comprehensive 6-dimension comparison ([1b63c14](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1b63c14511dbb184ee42b18694234cca793b5462))
* **calibrate:** add strategic context fields ([39fe61f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/39fe61fdda238cafdfa7872778ee79e68f0bcb13))
* **calibrate:** update context with maturity/breaking/priority ([257a96f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/257a96f60d177018c7d92b34d5cf04dee631781f))
* **cco-config:** add --target-dir argument ([154dd94](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/154dd9476f418dcdfa0e8fee45c6d2f673406b54))
* **cco-tune:** add dynamic complexity profile detection ([ea9290f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/ea9290fa81692e7ae392dc8a10ef09d1b0dd14ea))
* **cco-tune:** add statusline verification and configure=update ([8b72d74](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/8b72d74fc51e0e444d49ffb120123e4a71dd4ed0))
* **cco-tune:** improve with dynamic parsing and full report ([c6cc527](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/c6cc527cc3c4e23b4fdcc9fabb4b5e99c265f818))
* **cco:** add confirmation clarity and output format ([3180d19](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/3180d19938343d8b143485d2b2744817af07e3ab))
* **cli:** add --help flag and signal handling ([b6dce5f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/b6dce5f8ae40e1a010cc898e2df18fbdcb5df556))
* **commands:** add All option to multiSelect lists ([d4b37e8](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d4b37e86a426a37b67a5c304ca805b917c3868b2))
* **commands:** add dynamic context and strategy evolution ([5784f76](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/5784f765cb5bd4e29009c8e36282739a5959c493))
* **commands:** add meta commands, restructure ([73d4902](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/73d490274a37a7863f8edf0a1bbbcf5283c5d160))
* **commands:** add project context system for calibrated recommendations ([9ffb1ad](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/9ffb1ad0f7796e8d4d09a6d9b95aa3ec47aa5684))
* **commands:** add step progress UX and improve test coverage ([f973c36](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/f973c36b14ac9941cb2e2e18d66b5d7d92834248))
* **commands:** apply official Claude Code best practices ([ec6f15c](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/ec6f15c90713dd6fddc610d4dfc67231fc33341a))
* **commands:** merge config and calibrate into cco-tune ([1ce5d94](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1ce5d94da9859ffcfec7c56cb65f98dd4f5c9a08))
* **commands:** require context guard for all CCO commands ([6c46abb](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6c46abb71b6496dea963f73aebed5305c2608544))
* **commit:** add secrets detection, breaking change, staging handling ([1daa9b4](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1daa9b4e8cc4af218ed67fac8226177403448047))
* **config:** add detection priority with documentation fallback ([9a5bcc0](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/9a5bcc08c2b82a8b919860e3a733854332fba8e8))
* **config:** add write modes for safe file ops ([f1b8288](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/f1b828804ce1117abb0ac4504db92653e1b5722c))
* **config:** add write modes for safe file ops ([80d7da7](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/80d7da797edf983a6994402040520e84c2d28423))
* **context:** add scoped detection and context-aware commands ([ea798b4](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/ea798b4d742adafaaa011c9e3978b95fad6ee535))
* **context:** add strategic guidelines generation ([21d7424](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/21d74242f4bb79dca1d727e5c1b47fe6df7a31fe))
* **context:** complete context system redesign ([c2ff08b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/c2ff08b4063624f26c788e32b6bce6c273305e34))
* **context:** require context-justified recommendations ([8eefc05](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/8eefc05d972848598a8a0303745d60a3afa44db2))
* **detect:** enhance detection system ([198e6d5](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/198e6d5c6d766ca0ebc81aacf326df5b4b6a9530))
* **detection:** add game engine support and trigger SSOT ([69412f2](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/69412f20f44695d98aa3b51d248f06ce2a7d4cac))
* **detection:** add orphan frameworks and modern technology triggers ([5cc1a04](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/5cc1a04355ce52454376e3b10f786628b45a565a))
* **detection:** complete terzi-dikim coverage ([0a6d770](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0a6d770883dde1ce059e54fb06dfb30b133ecadb))
* **detection:** expand framework detection with 2025 tooling ([0766635](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0766635a710b389993d3fe1afd31876ccc342cdd))
* **docs:** add documentation gap analysis command ([2ba481d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/2ba481d6624d4680705c29e299eb400b88202de2))
* **extras:** add statusline for Claude Code ([6a7afa9](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6a7afa940da6978e18479571e90eb64e2bfdd45e))
* **hooks:** add context check with auto-setup trigger ([2014651](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/201465178ae130b5b771242c345beaa5906f9dc0))
* **install:** add --dry-run flag for installation preview ([cf9e14a](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/cf9e14af5cac5dedb97d251021abca6f738e56f5))
* **install:** add --local mode for project statusline and permissions ([effb079](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/effb07984d77d25df74e9553917f0ce081bcb793))
* **installer:** install binary to ~/.local/bin with PATH setup ([#31](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/31)) ([fbfbd40](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/fbfbd403f07299a3a23266a6f214803f5758b6b7))
* migrate to skills and Go installer ([#24](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/24)) ([5c8a055](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/5c8a0553eed7ec9582a61be311f68916993e28e5))
* optimize all files for Opus 4.6 ([d6b2dbc](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d6b2dbc1c99ddddba0acfe2c2fe35d22e7848ce6))
* **optimize:** add dependency freshness check ([2f67a5b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/2f67a5befe31f8d7b6f318afd862937aea319c3d))
* **permissions:** derive all levels from full.json template ([590fafb](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/590fafbe817c51ccba27b8fe3008e7219b979528))
* **profile:** comprehensive project profile with full detection ([f7b4acf](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/f7b4acfb867d217aa18267acb2817142ce083c87))
* **release:** add 5 pre-flight checks ([89dc611](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/89dc611859e5dce69c27339f0cf6cbfcc6634781))
* **review:** add production readiness mode ([c3f4763](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/c3f4763f3a995aae1d9922cbc07a464031a25256))
* **rules:** add adaptive learning, best practices scope, and mandatory AskUserQuestion ([a0970a2](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/a0970a2ab68fe4a5b57cda3bd6a81955e2258fc3))
* **rules:** add agent delegation rules ([2c6bcab](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/2c6bcab86ea9cddc2103d3a9ca4884c55fae5f7c))
* **rules:** add context awareness and Claude 4.5 rules ([72fe29d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/72fe29dbe996d4ec3b7532b1619031a4227c0f16))
* **rules:** add dependency-based detection for 40+ project types ([ffc6dbb](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/ffc6dbb038283756e9affe0280327a23b2dfe335))
* **rules:** add DIP, OWASP, ISP principles ([1841099](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/184109988f9e4c07233f3f0ba195379d2d18037b))
* **rules:** add framework detections and rules ([210ec9e](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/210ec9e985b4f76de9b4bbef0aa68f9b9b2dc8ce))
* **rules:** add Option Batching for questions exceeding 4 options ([fa07262](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/fa07262db78263119bd7ea1c71901a19da154073))
* **rules:** add project-local CCO rules to .claude/ ([37e67e4](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/37e67e4b4fe5646a447c71586dcad49ff5e58e5e))
* **security:** add path traversal and ReDoS protection ([42c56b5](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/42c56b529828cfb1b68e5561920316e4f821e201))
* **skills:** add --auto unattended mode ([6f2ed0f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6f2ed0f710c94e87756e87211acd62972c72cd4d))
* **skills:** expand scopes and improve agent integration ([#28](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/28)) ([c03964f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/c03964f31e88c47780d2d0a4c9fbd769cd493c4f))
* standards exemplars, research command, and v1.1.0 updates ([98384e0](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/98384e0a4d5792c5a4a311ca55bdf02619bb4954))
* **standards:** add AI Context to Universal Standards ([4cef07e](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/4cef07e00e8afdf889c1d434990f08dcfa63d70b))
* **standards:** add impact preview to fix workflow ([b2810d6](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/b2810d63789d3a927c62dc0c3702e71be1037534))
* **standards:** add Output Formatting with DRY schema ([52506ca](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/52506ca6f7f2144654e78ee24f36d77de1486f8d))
* **statusline:** add context usage display ([54e6db5](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/54e6db5037ae40eb346d2fdd54f613d4b8b5684c))
* **statusline:** add progressive context warning and todo indicator ([1bf3bf0](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1bf3bf0301ab4d03914638e1df76792bfc06b076))
* **statusline:** reorder rows for UX ([2b73d04](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/2b73d043cd59b434d9246f974f1ef1c328b8047f))
* **statusline:** restore original 5-column grid format ([ac924b7](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/ac924b758b2e57f28e417d57935f17a9f91009d8))
* switch from plugin to install script distribution model ([33cffe6](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/33cffe63556a1bc84b4cd1ada0f809536dd7398a))
* **templates:** add dependency audit and quality improvements ([efa8927](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/efa8927b64117746fdf4cd0fc4b332b41b45393e))
* **templates:** enforce fix-all mode rules ([6db4611](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6db46119371c3e4ea6effd05df776e1df900eb5a))
* **templates:** implement Claude 4 best practices compliance ([f7430fc](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/f7430fc3981101683ebbaadb8da7ee6f5ff044b0))
* **tools:** add User Input standard requiring AskUserQuestion ([7cd9cd4](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/7cd9cd490414c25dfea317cfe36b1baef5a02246))
* **tools:** enforce AskUserQuestion with semicolon separator ([928dda8](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/928dda89f1e7c2003ffe16bcc0a43716076ccf70))
* **tune:** add comprehensive trigger elements and standards ([7cf88a8](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/7cf88a8f73dad1cceb798141a903d3cb38b37a44))
* **tune:** add Remove and Export integration ([648db8b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/648db8b777082360492440bfb130dd2960f89817))
* **tune:** add statusline and permissions content with install support ([0610e7d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0610e7dcc2d9deaf1934baf4c24d6b6f3195b645))
* **tune:** auto-detect AI Performance based on project complexity ([00dfa40](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/00dfa4047c56ff017f00e44a5c689e975b35654b))
* **tune:** enforce local-only settings, add AI Performance config ([47051e7](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/47051e7dfb999e17682843d2deb04673cf4df342))
* **tune:** expand to 8 questions for comprehensive config ([8d43be7](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/8d43be7451833442040655db943ca50bf7ddbf46))
* **tune:** full detection for all 8 questions ([2175701](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/21757014eade9fe1e83a6fed662a563afcc20dcd))
* **tune:** update statusline and permissions configuration ([dccf75d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/dccf75dc984ecfed7524367b6ca43c4ab61e934b))
* **v2:** zero-global-pollution architecture with context injection ([985b147](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/985b147df45c4c96170dfa03a34f78c134d6cafb))


### Bug Fixes

* agent invocation gates and false positive prevention ([#34](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/34)) ([7eed4c8](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/7eed4c8daabcaa35f44f63d4091865883aacb11b))
* **agent-analyze:** correct team/scale values, add data/compliance ([0f64689](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0f646893d3169b3df1ae3e9aa0eadd7c0e269d03))
* **agents:** remove legacy core.md/ai.md references ([f23a9f9](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/f23a9f9f5108913ba45d264866fb9f4044a4dc88))
* **agents:** require fresh coverage run, remove stale file reads ([0376df9](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0376df9540ee2168c34d4ef0e2ddb5c850dfedf5))
* **benchmark:** dynamic UI polling and config persistence ([6a1769f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6a1769fa5b9cb896e850d30ce20efd0df5fe4999))
* **benchmark:** handle timeout output decode ([9661a45](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/9661a451f904e5b5dd3db65376822c181111b4f5))
* **benchmark:** improve AI evaluator error handling ([8fd1e0f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/8fd1e0f1950908e68f3c4275b3befae5ddf81d3d))
* **benchmark:** improve UI and scoring ([a76f08e](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/a76f08ec10ef7d9b27b98b7b567a6cf5846f7846))
* **benchmark:** inactivity-based timeout ([abcd80b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/abcd80b727cc6d54ab937a7b5539083900a0666b))
* **benchmark:** prioritize SUCCESS/FAILED colors ([d8d5929](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d8d59296d497db0033dd008d774e17e7a9395702))
* **benchmark:** run CCO tests first ([9d550d2](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/9d550d230476f1bfe1c9feaf97dc8109070bf4e7))
* **benchmark:** sync dimension wins with AI evaluator ([18c2d20](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/18c2d20d42ddf1e2df98616ddd33772447b49150))
* **benchmark:** update log message for 3-phase CCO flow ([d779356](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d7793567b0f751d97a0898f4a1b2561d7e4cc451))
* **benchmark:** use file for prompt to avoid CLI limits ([e0a255d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/e0a255da1aeb0ed1347c6382b0e8b71fb9f0062f))
* **build:** SPDX license, exclude benchmark ([2f00eb3](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/2f00eb390cd9fed80b7bea25b015881fec034c54))
* **build:** use static description in pyproject.toml ([2147329](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/2147329f254b882e26977305353f531a7152ef9b))
* **calibrate:** show existing context before asking for confirmation ([8ca2b07](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/8ca2b07705760bbe324fcd02b5e732044a6b5d24))
* **cco-commit:** enforce 50-char title limit ([b11cbe1](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/b11cbe15096dfa7ff18cc67b4e988a8d54b42be3))
* **cco-commit:** enforce full project checks ([4ade113](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/4ade11330da5ef4adea39cec685aed8e069fec5b))
* **cco-config:** use package templates for statusline instead of generating ([0947383](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/094738328c38ee3c1931d301ab29711df491b091))
* **ci:** add pyyaml dependency for tests ([31dd96d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/31dd96d1f7e593bc9cb2f6eef8d0985fc3361dd2))
* **ci:** add version consistency validation across all release-please managed files ([0f85b90](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0f85b90218158c3ea041268f42314f4e670dea85))
* **ci:** bypass release-please release creation with gh CLI fallback ([#38](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/38)) ([49a48fe](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/49a48fe17418b389fa8c3832ff27bd253cb1b22d))
* **ci:** revert to simple release-please workflow ([#39](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/39)) ([08860ab](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/08860ab10a76c82192b8a99438641945ec12bbaa))
* **ci:** scope manifest-sync regex to var blocks and fix test errcheck ([#35](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/35)) ([04c748e](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/04c748e78dd1a0498a0c34713aba35dbe36db5f9))
* **ci:** update rules validation for new structure ([c8e14c4](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/c8e14c4ea76c678fb99130e6a7ec39ae1723e90c))
* **ci:** update workflow for new hooks-based structure ([95687bd](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/95687bd2eaf8bdaf50670612177198a8d69f60eb))
* clean AI performance settings from permission files ([e713b5a](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/e713b5ad6cc57ac45eb2e63a817c46a173f81f60))
* **commands:** add channel support to cco-update and fix cco-commit parsing ([daa8e39](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/daa8e39e707d7eee7e4a1ea9c1278fd47df84ca6))
* **commands:** clarify CCO_CONTEXT path as project root ([9b2ccd3](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/9b2ccd3280e16792c2296eb4c5aef5a52654ff1f))
* **commands:** count consistency and tab philosophy ([fd1dead](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/fd1dead63540cc28533fc457defbec1ab0da0326))
* **commit:** detect tested content for quality gates ([66631ff](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/66631ff18b06810a9e83530dcc417a436bdc5c66))
* **commit:** use placeholders in examples ([3789562](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/378956271e31d0cea803f8bdfd729cf264844a35))
* **compat:** add Python 3.10 support for StrEnum ([12fd518](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/12fd518b2d8f90b6aaac755119ccf7cdd78fe548))
* **compat:** fix Python 3.10 StrEnum string conversion for path operations ([a124f04](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/a124f04f4a87e0a211b892cffe71aa6692b3d35b))
* **config:** enforce agent usage, prevent duplication ([58354f7](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/58354f7a9f8ab8008dc416f09f40c271194efdda))
* **config:** enforce recommendations and writes ([19e95ca](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/19e95cab233011c385984f0098c27f7c24b63d9e))
* **config:** make statusline question mandatory in cco-config ([7d70bcf](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/7d70bcfd670cecd07eaa15f8c66994605b765778))
* **config:** translate Turkish content to English ([52cd193](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/52cd1938df889546f6d3878ad6781d856bb45ee4))
* **config:** use dynamic path for statusline command ([0cba203](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0cba20365fd2c177207f24769792c4587ab4eae0))
* **content:** rename dirs to prevent Claude Code command scanning ([e02773a](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/e02773a36118900be6368651e8b8e7c410d8e8af))
* **docs:** align docs with implementation ([6de019f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6de019fe6f5a375d4c5bf3c04b7f89f5705aa217))
* **docs:** correct AI rules count (61→60) ([5182103](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/5182103e8f47143ca5f28f8e7f756d5f79e16d09))
* **docs:** update CLI refs and add missing documentation ([118ca05](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/118ca05d782f967ddfe8548b25f35d1a95486f2b))
* **docs:** update install instructions for GitHub ([564c3d5](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/564c3d5c1784648b9270d85712d221a68bc6959d))
* **hooks:** cross-platform SessionStart hook ([2516d19](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/2516d1986d3baea57114d7a46d83ac90425ba099))
* **hooks:** fix structure and add Windows compatibility ([68ccd5a](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/68ccd5af759070d90e4e06d482f1b7c9b721654a))
* **hooks:** flush stdout to prevent buffering issues ([475bff1](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/475bff19184d5e542b85703c1717f0337b88bd91))
* **hooks:** restore required nested hooks array structure ([38d42ce](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/38d42ce88390c051e8fbb7ce51607cb22054e08c))
* **hooks:** simplify to Python script, add Windows encoding fix ([cfbdc0c](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/cfbdc0ce1c92b561f4a20ff31d1b2e92e828a64b))
* **hooks:** use agent hook for context check ([48c9b05](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/48c9b05b8324336b5ae64f0e37839878d02a95af))
* **hooks:** use correct Claude Code hook schema ([368ce0b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/368ce0b76126944db65a3b6fb0636f05f174d77c))
* **install:** add full v1+v2 legacy cleanup ([5010517](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/50105177911f397e1f2a785ac8b00e076f011e12))
* **install:** add preflight validation, content checks, and legacy cleanup ([1f3c6fb](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1f3c6fb958bc979027262545ab1dc64474f9361d))
* **install:** update v1 pip package name and present all findings ([#18](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/18)) ([aa52c65](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/aa52c65bb0865ba7115317d6e647c947fe13db2e))
* **install:** use dev branch URL for dev channel installer ([a77fdb4](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/a77fdb468ed36248f52960d28c6207cc22e26b65))
* **install:** use glob for cleanup, verify deletion ([49b846c](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/49b846c65a9d58194ee1ee6e4eea22da285abdab))
* **markers:** update cco-tune to use correct CCO marker patterns ([36d982f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/36d982f6b795b694f84b84cdeaad4d48844c7109))
* **migration:** complete v1.0.0 cleanup for seamless upgrade ([63f6ce1](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/63f6ce197df31995e1c5c8e25d4c10cc2b3473ba))
* normalize line endings and update legacy comment ([d2934d5](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d2934d5ff7a2d4f7b435d6ec54087f0e86fa97df))
* **permissions:** remove duplicate allow rules from full.json ([1cb1d3c](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1cb1d3cb7c4c862cea6f4400274bd14a75083a7b))
* **plugin:** correct source path for marketplace resolution ([78f4715](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/78f47153b202bf5bcb5f94000f72cb495f9f2d65))
* **plugin:** remove duplicate hooks reference ([333e030](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/333e0308f28e17ef278d7cff9cb707d9fc210d47))
* **plugin:** update schema to match Claude Code marketplace format ([0785eb4](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0785eb4a431fb248b5d4f98cade388b9f942267c))
* **plugin:** use inline hooks config for compatibility ([6fd637b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6fd637b8527149615263e8362c07ec172c543214))
* **plugin:** use URL format for marketplace source field ([0d4d681](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0d4d68191062a2a2d13f2408bbf7e0002db8d4b1))
* **quick-install:** correct Python version and add timeouts ([1527bf5](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1527bf5f3694bebfa104c76e9bf01a374911b164))
* **release:** configure manifest mode for release-please ([d983aec](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d983aeccce8272592014a08f2b0cee7f3e804f54))
* **release:** configure manifest mode for release-please ([0669e47](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0669e47b96dfc3a60cde2cbd8390e57a7038b752))
* **release:** switch to simple release type ([dc55817](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/dc5581784c637951cde2fa297f44f527a17d870e))
* **release:** use config file instead of hardcoded node type ([33e022d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/33e022dae6d21e317540c8491ac91bedbe273375))
* **release:** use config file instead of hardcoded node type ([a47ff8d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/a47ff8d4406c01601c67d92fba55364e66daa613))
* **release:** use simple release type instead of node ([3e93f93](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/3e93f933897eb3b6305881a7a9bfae6d55e97973))
* **review:** sync rule counts and add AskUserQuestion ([92bef2d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/92bef2d914f096798d97ed771dd6b3678702b36b))
* **rules:** use SSOT trigger placeholders ([1f70437](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1f70437ab40bd001f56f98641b1a4a4b61e25609))
* **security:** bind benchmark server to localhost only ([39b8a56](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/39b8a56db2c80ae0f893935ae021dfa6c153d44e))
* **skills:** use pipe pattern for reliable skill context evaluation ([#47](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/47)) ([bf6c977](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/bf6c9777ba0168302e875216f0b198afcf4ad381))
* **standards:** remove speculative AI settings, use verified docs ([e17ee66](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/e17ee66fa49baaf03d822eef8d2da3262518f6b1))
* **statusline,tune:** path only root dir, dynamic permission recommendation ([eda96e7](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/eda96e7ef2e5bd44a1a90ef2b826d2ad89c32b87))
* **statusline:** correct emoji width calculation for alignment ([a89616c](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/a89616c9384c11c1b02b0103b5e4615268825231))
* **statusline:** display project name when not in git repo ([dcdb9b7](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/dcdb9b76b70a0d5566f6146b906b088ae050b3e6))
* **statusline:** improve untracked file counting ([6d8a9ff](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6d8a9ff12865355d44e03ed184435a1fade1a752))
* **statusline:** remove Unix-only stderr redirect ([dc68e15](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/dc68e155b4ce7ef082ae1627275fd83023b683a4))
* switch Task to sync for reliable results ([6efc005](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6efc00546fc36decf7cf885d56b89d9e29675e19))
* **templates:** align frontmatter with official CC format ([8691361](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/8691361c1bb50ce591d26af42cff8bcb33f7ab64))
* **templates:** align with best practices ([b047f60](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/b047f601f3b3d1c60a2a89ab81ac4581684daf49))
* **templates:** ignore metadata in fix-all mode ([26066ae](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/26066ae3e9b8dd625b71552c318ddd94e250b6c2))
* **templates:** replace /dev/null with cross-platform alternatives ([60d83db](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/60d83dbd7463cf67c7caedd4e71eff7c6228ed48))
* **templates:** resolve cco-full-review findings ([f0e1737](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/f0e173721a08860bb533a2b986cbb4c33609d264))
* **test:** add --no-statusline flag to install hook test ([9427171](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/94271719ef3f8ad74973a7db6da2bb56f061a5f3))
* **test:** add missing RULES_DIR patch ([4d9ee83](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/4d9ee830710997cfff14848f6cd3637239c40a62))
* **tests:** add missing imports, extract paths ([08a09f2](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/08a09f21881c24f555a70619d2a26fa2c1a7f9eb))
* **tune:** add detection exclusions for test/example dirs ([0c88c73](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0c88c732dab6e6e7a0ce9301d85e4764b311c5ba))
* **tune:** ask update mode when profile exists ([2517686](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/25176867d1b708c9b175e363bb7f90d71e6f9611))
* **tune:** correct element count to 21 ([3619fa3](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/3619fa3a75616ca5ee6931485912e4638c6add8f))
* **tune:** make standard counts dynamic and exact ([31ef171](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/31ef1719c13825959d15a286160b7776226241b7))
* **tune:** sequential execution to prevent race condition ([23d2c34](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/23d2c343f95d64fa6dd5f64d386a93d60e8fe571))
* **tune:** use CCO-recommended values, not fictional tiers ([b2804e6](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/b2804e6c898670ddd3c1ca97f2752552deae2a9a))
* **types:** improve Callable and encoding types ([15e915f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/15e915fc77ccbe8085dcbd1dbad4011c9bdf78d1))


### Performance

* **agents:** add Parallel Execution sections ([38a84bb](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/38a84bb379753e55226d7b364e35a590296fdb9d))
* **cco-commit:** optimize speed, add message format ([85c020c](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/85c020c2095c9983e638938c5e9d905c79d67424))
* **config:** add lru_cache for rules loading ([4ad434a](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/4ad434a35424524ac48b0ee89e2ce2337a02ce0d))
* **core:** pre-compile regex and add TypedDict ([0305e72](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0305e7294aa2565204614b8ce7a7457e6cb30262))
* **statusline:** optimize process and disk usage ([1e59aa3](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1e59aa3a64f94c2019710c8e4c80d9abda14d4a3))
* **templates:** optimize config token usage ([2077fb5](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/2077fb5e6ad29ebfec2cb54e6200428b23402f93))
* **templates:** remove TodoWrite from short commands ([2d2b331](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/2d2b3319992f1f000dba0d65499968b0de184712))

## [4.2.2](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.2.1...v4.2.2) (2026-02-17)


### Bug Fixes

* **skills:** use pipe pattern for reliable skill context evaluation ([#47](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/47)) ([bf6c977](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/bf6c9777ba0168302e875216f0b198afcf4ad381))

## [4.2.1](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.2.0...v4.2.1) (2026-02-17)


### Bug Fixes

* agent invocation gates and false positive prevention ([#34](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/34)) ([7eed4c8](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/7eed4c8daabcaa35f44f63d4091865883aacb11b))
* **ci:** bypass release-please release creation with gh CLI fallback ([#38](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/38)) ([49a48fe](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/49a48fe17418b389fa8c3832ff27bd253cb1b22d))
* **ci:** revert to simple release-please workflow ([#39](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/39)) ([08860ab](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/08860ab10a76c82192b8a99438641945ec12bbaa))
* **ci:** scope manifest-sync regex to var blocks and fix test errcheck ([#35](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/35)) ([04c748e](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/04c748e78dd1a0498a0c34713aba35dbe36db5f9))

## [4.2.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.1.0...v4.2.0) (2026-02-16)


### Features

* **installer:** install binary to ~/.local/bin with PATH setup ([#31](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/31)) ([fbfbd40](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/fbfbd403f07299a3a23266a6f214803f5758b6b7))

## [4.1.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v4.0.0...v4.1.0) (2026-02-16)


### Features

* **skills:** expand scopes and improve agent integration ([#28](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/28)) ([c03964f](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/c03964f31e88c47780d2d0a4c9fbd769cd493c4f))

## [4.0.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v3.2.1...v4.0.0) (2026-02-11)


### ⚠ BREAKING CHANGES

* commands/ directory replaced by skills/ with SKILL.md files. Install scripts (install.sh, install.ps1) replaced by Go binary installer. Run ./cco install to migrate.

### Features

* migrate to skills and Go installer ([#24](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/24)) ([5c8a055](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/5c8a0553eed7ec9582a61be311f68916993e28e5))

## [3.2.1](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v3.2.0...v3.2.1) (2026-02-08)


### Bug Fixes

* **install:** update v1 pip package name and present all findings ([#18](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/18)) ([aa52c65](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/aa52c65bb0865ba7115317d6e647c947fe13db2e))

## [3.2.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v3.1.0...v3.2.0) (2026-02-08)


### Features

* add blueprint, pr commands and feature branch workflow ([#11](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues/11)) ([6243c7b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6243c7b65ec09d8dcdc56853f3404c36780aa298))

## [3.1.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v3.0.0...v3.1.0) (2026-02-07)


### Features

* **extras:** add statusline for Claude Code ([6a7afa9](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/6a7afa940da6978e18479571e90eb64e2bfdd45e))


### Bug Fixes

* **install:** add full v1+v2 legacy cleanup ([5010517](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/50105177911f397e1f2a785ac8b00e076f011e12))

## [3.0.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v2.0.1...v3.0.0) (2026-02-06)


### ⚠ BREAKING CHANGES

* rule structure reorganized into 5 categories
* CCO is no longer distributed as a Claude Code plugin. Install via `curl -fsSL .../install.sh | bash` (Unix) or `irm .../install.ps1 | iex` (Windows). Commands renamed from `/cco:*` to `/cco-*` format.

### Features

* add stable/dev channel support to install scripts ([e735f83](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/e735f83360ea80f04426ef506539cae05cc404dd))
* optimize all files for Opus 4.6 ([d6b2dbc](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d6b2dbc1c99ddddba0acfe2c2fe35d22e7848ce6))
* switch from plugin to install script distribution model ([33cffe6](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/33cffe63556a1bc84b4cd1ada0f809536dd7398a))


### Bug Fixes

* **ci:** add version consistency validation across all release-please managed files ([0f85b90](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0f85b90218158c3ea041268f42314f4e670dea85))
* **commands:** add channel support to cco-update and fix cco-commit parsing ([daa8e39](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/daa8e39e707d7eee7e4a1ea9c1278fd47df84ca6))
* **hooks:** flush stdout to prevent buffering issues ([475bff1](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/475bff19184d5e542b85703c1717f0337b88bd91))
* **install:** add preflight validation, content checks, and legacy cleanup ([1f3c6fb](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/1f3c6fb958bc979027262545ab1dc64474f9361d))
* **install:** use dev branch URL for dev channel installer ([a77fdb4](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/a77fdb468ed36248f52960d28c6207cc22e26b65))

## [2.0.1](https://github.com/sungurerdim/ClaudeCodeOptimizer/compare/v2.0.0...v2.0.1) (2026-02-04)


### Bug Fixes

* **ci:** update workflow for new hooks-based structure ([95687bd](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/95687bd2eaf8bdaf50670612177198a8d69f60eb))
* **hooks:** simplify to Python script, add Windows encoding fix ([cfbdc0c](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/cfbdc0ce1c92b561f4a20ff31d1b2e92e828a64b))
* **release:** configure manifest mode for release-please ([d983aec](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/d983aeccce8272592014a08f2b0cee7f3e804f54))
* **release:** configure manifest mode for release-please ([0669e47](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/0669e47b96dfc3a60cde2cbd8390e57a7038b752))
* **release:** switch to simple release type ([dc55817](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/dc5581784c637951cde2fa297f44f527a17d870e))
* **release:** use config file instead of hardcoded node type ([33e022d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/33e022dae6d21e317540c8491ac91bedbe273375))
* **release:** use config file instead of hardcoded node type ([a47ff8d](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/a47ff8d4406c01601c67d92fba55364e66daa613))
* **release:** use simple release type instead of node ([3e93f93](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/3e93f933897eb3b6305881a7a9bfae6d55e97973))


### Reverts

* **release:** restore original working config ([e45da1b](https://github.com/sungurerdim/ClaudeCodeOptimizer/commit/e45da1b64691c97bd97f6ab52df48bf5203c122b))

## [2.0.0](https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/tag/v2.0.0) (2025-01-24)

### ⚠ BREAKING CHANGES

* **Command Changes** (v1 → v2):
  * `/cco-tune` → `/cco:tune`
  * `/cco-health` → removed (use `/cco:tune --preview` instead)
  * `/cco-generate` → removed (generation now handled inline by agents)
  * `/cco-audit` + `/cco-optimize` → `/cco:optimize` (merged)
  * `/cco-review` + `/cco-refactor` → `/cco:align` (merged)
* **Agent Restructure**:
  * `cco-agent-detect` + `cco-agent-scan` → `cco-agent-analyze`
  * `cco-agent-action` → `cco-agent-apply`
  * NEW: `cco-agent-research`

### Features

* **Zero Global Pollution** — CCO never writes to `~/.claude/` or any global directory
* **Context Injection** — Core rules injected via SessionStart hook, not file copying
* **Safe Updates** — All rules use `cco-` prefix; your own rules are never touched
* **Modular Rules** — 85 standards in 2 files → 45 focused rule files
* **SessionStart hook** — Injects core rules directly into context via `additionalContext`
* **`/cco:preflight`** — Pre-release workflow with quality gates
* **`/cco:research`** — Multi-source research with CRAAP+ reliability scoring
* **`/cco:docs`** — Documentation gap analysis
* **`cco-agent-research`** — External source research with reliability scoring (T1-T6)
* **Confidence scoring** — 0-100 scale for findings with ≥80 threshold for auto-fix
* **Phase gates** — Explicit checkpoints (GATE-1, GATE-2, etc.) in command workflows
* **Parallel scope execution** — Multiple scope groups analyzed concurrently
* **Test suite** — 69 tests covering commands, hooks, edge cases, and plugin structure
* **Permissions system** — Four levels (safe/balanced/permissive/full)

### Bug Fixes

* **Path traversal security** — Resolve paths before validation to prevent symlink bypasses
* **YAML frontmatter** — Quoted argument-hint values to prevent parsing errors
* **CI dependencies** — Added pyyaml for test execution
* **Task execution** — Switched to sync calls for reliable result handling

## 1.0.0 (2025-12-02)

### Features

* **8 slash commands** — `/cco-tune`, `/cco-health`, `/cco-audit`, `/cco-optimize`, `/cco-review`, `/cco-generate`, `/cco-refactor`, `/cco-commit`
* **3 specialized agents** — `cco-agent-detect`, `cco-agent-scan`, `cco-agent-action`
* **85 standards** — 51 universal + 34 Claude-specific
* **Risk-based approval flow** — AskUserQuestion integration
* **Project-aware tuning** — Stack detection via `/cco-tune`
* **Doc-code mismatch detection** — SSOT resolution
