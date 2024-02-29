"""Help and usage instruction texts used for the command line parser"""


SRC = "Path(s) to the Python source file(s) to reformat"

REVISION = (
    "Revisions to compare. The default is `HEAD..:WORKTREE:` which compares the latest"
    " commit to the working tree. Tags, branch names, commit hashes, and other"
    " expressions like `HEAD~5` work here. Also a range like `main...HEAD` or `main...`"
    " can be used to compare the best common ancestor. With the magic value"
    " `:PRE-COMMIT:`, {application} works in pre-commit compatible mode. {application}"
    " expects the revision range from the `PRE_COMMIT_FROM_REF` and `PRE_COMMIT_TO_REF`"
    " environment variables. If those are not found, {application} works against"
    " `HEAD`. Also see `--stdin-filename=` for the `:STDIN:` special value."
)

STDIN_FILENAME = (
    "The path to the file when passing it through stdin. Useful so {application} can"
    " find the previous version from Git. Only valid with `--revision=<rev1>..:STDIN:`"
    " (`HEAD..:STDIN:` being the default if `--stdin-filename` is enabled)."
)

VERBOSE = "Show steps taken and summarize modifications"
QUIET = "Reduce amount of output"
COLOR = (
    "Enable syntax highlighting even for non-terminal output. Overrides the environment"
    " variable PY_COLORS=0"
)
NO_COLOR = (
    "Disable syntax highlighting even for terminal output. Overrides the environment"
    " variable PY_COLORS=1"
)

VERSION = "Show the version of {application}"

WORKERS = "How many parallel workers to allow, or `0` for one per core [default: 1]"
