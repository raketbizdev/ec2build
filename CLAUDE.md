# EC2Build project instructions (Claude Code)

This repository is the EC2Build agent source only. Never write project output here; `/ec2build` writes to `./<slug>/` in the folder where it is run (see `skills/ec2build/SKILL.md`). The agent's canonical files live in `skills/ec2build/` (`SKILL.md`, `references/EC2BUILD_AGENT.md`, `references/WORKFLOW.md`, `references/TEMPLATES.md`, `scripts/`). Read them when asked to use `/ec2build` or to change an EC2Build project. A project's documents in `<project>/docs` are its source of truth, not previous chat context.

Use the `/ec2build` skill for the workflow. Keep changes scoped, perform impact analysis, and reflect approved changes across dependent documents. Report changed files and remaining assumptions. Do not run irreversible changes or deployment without explicit approval.

When changing the agent itself (anything in `skills/ec2build/`), bump `version` in `package.json`, `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` and note it in `CHANGELOG.md`.
