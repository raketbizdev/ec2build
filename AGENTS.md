# EC2Build repository policy (Codex and other agents)

You are operating in an EC2Build workspace. For requests invoking `ec2build`, read `skills/ec2build/SKILL.md` and its `references/EC2BUILD_AGENT.md`, `references/WORKFLOW.md` and `references/TEMPLATES.md` completely and follow the six-document workflow. Treat `/ec2build` as a project-specific workflow, not a built-in Codex CLI command. For Codex, use the `$ec2build` skill or natural language "Use the ec2build skill: ...".

- Source of truth: `projects/<slug>/docs/` and `projects/<slug>/manifest.json`.
- Before modifying documents, inspect existing files and git status. Do not overwrite approved content without cause.
- Changes must be scoped, diff-reviewed, dependency-propagated, and validated.
- Maintain ID traceability from requirement to flow, UI, API, schema, implementation task, and test.
- No claims that a test, deployment, or command succeeded unless run and verified.
- Do not execute production deployment, destructive database migrations, payments, or infrastructure provisioning without explicit approval.
- Never commit secrets, .env files, credentials or personal data.
- Keep generated artifacts deterministic, readable and suitable for Git review.
