// This workspace preserves the local customized kit. Never run the upstream lifecycle here.
process.stderr.write("Disabled in this project-local customized installation. Read docs/maintenance.md at the workspace root; use tools/workspace.py verify. No files changed.\n");
process.exit(2);
