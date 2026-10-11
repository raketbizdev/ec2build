#!/usr/bin/env node
// EC2Build CLI — install the ec2build agent skill for Claude Code / Codex, and run its bundled tools.
// No dependencies. Works on Windows, macOS and Linux (Node.js 18+).
'use strict';
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const PKG_ROOT = path.resolve(__dirname, '..');
const SRC = path.join(PKG_ROOT, 'skills', 'ec2build');
const VERSION = require(path.join(PKG_ROOT, 'package.json')).version;

const HELP = `EC2Build ${VERSION} — free agent skill that turns an app idea into build-ready specs.

Usage: npx ec2build <command> [options]

Commands
  install            Install for Claude Code and Codex (default: both)
  update             Same as install (replaces the installed copy with this version)
  uninstall          Remove installed copies
  status             Show where EC2Build is installed and which version
  doctor <project>   Check accounts/tools/env for a stage   (--stage local|staging|production, --app <dir>)
  validate <project> Check a generated project package
  swimlanes <project>  Re-render App Flow swimlane diagrams
  help               Show this help

Install options
  --claude           Claude Code only   (~/.claude/skills/ec2build)
  --codex            Codex only         ($CODEX_HOME or ~/.codex)/skills/ec2build
  --project <dir>    Install into one project folder (<dir>/.claude/skills, <dir>/.agents/skills)

After installing, open any folder in VS Code (Claude Code chat) or a terminal, start a NEW session and type:
  /ec2build help      (Claude Code)
  $ec2build help      (Codex)`;

function parse(argv) {
  const opts = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--claude' || a === '--codex' || a === '--version' || a === '-v' || a === '--help' || a === '-h') opts[a.replace(/^-+/, '')] = true;
    else if (a === '--project') { opts.project = argv[++i]; if (!opts.project) fail('--project needs a directory'); }
    else opts._.push(a);
  }
  return opts;
}

function fail(msg) { console.error(`ec2build: ${msg}`); process.exit(1); }

function targets(opts) {
  if (opts.claude && opts.codex) fail('use --claude or --codex, not both (omit both to install for both)');
  const wantClaude = !opts.codex, wantCodex = !opts.claude;
  const out = [];
  if (opts.project) {
    const base = path.resolve(opts.project);
    if (wantClaude) out.push({ agent: 'Claude Code', dir: path.join(base, '.claude', 'skills', 'ec2build') });
    if (wantCodex) out.push({ agent: 'Codex', dir: path.join(base, '.agents', 'skills', 'ec2build') });
  } else {
    const home = os.homedir();
    const codexHome = process.env.CODEX_HOME || path.join(home, '.codex');
    if (wantClaude) out.push({ agent: 'Claude Code', dir: path.join(home, '.claude', 'skills', 'ec2build') });
    if (wantCodex) out.push({ agent: 'Codex', dir: path.join(codexHome, 'skills', 'ec2build') });
  }
  for (const t of out) {
    if (path.basename(t.dir) !== 'ec2build' || path.basename(path.dirname(t.dir)) !== 'skills') fail(`refusing unexpected target ${t.dir}`);
  }
  return out;
}

function install(opts) {
  if (!fs.existsSync(path.join(SRC, 'SKILL.md'))) fail(`skill files missing in package (${SRC})`);
  for (const t of targets(opts)) {
    fs.rmSync(t.dir, { recursive: true, force: true });
    fs.mkdirSync(path.dirname(t.dir), { recursive: true });
    fs.cpSync(SRC, t.dir, { recursive: true, filter: (p) => !/__pycache__|\.pyc$/.test(p) });
    fs.writeFileSync(path.join(t.dir, '.ec2build-version'), VERSION + '\n');
    console.log(`Installed EC2Build ${VERSION} for ${t.agent}: ${t.dir}`);
  }
  if (!findPython()) console.warn('\nNote: Python 3 was not found. EC2Build works, but its diagram/doctor/validate tools need Python 3 (https://www.python.org/downloads/).');
  console.log('\nNext: open any folder in VS Code (Claude Code chat) or a terminal, start a NEW session and type /ec2build help  (Codex: $ec2build help)');
}

function uninstall(opts) {
  for (const t of targets(opts)) {
    const existed = fs.existsSync(t.dir);
    fs.rmSync(t.dir, { recursive: true, force: true });
    console.log(`${existed ? 'Removed' : 'Not installed'} (${t.agent}): ${t.dir}`);
  }
}

function status(opts) {
  console.log(`Package version: ${VERSION}`);
  for (const t of targets(opts)) {
    const vf = path.join(t.dir, '.ec2build-version');
    const v = fs.existsSync(vf) ? fs.readFileSync(vf, 'utf8').trim() : fs.existsSync(path.join(t.dir, 'SKILL.md')) ? 'unknown version' : null;
    console.log(`${t.agent}: ${v ? `installed (${v}) at ${t.dir}` : 'not installed'}`);
  }
}

function findPython() {
  const candidates = process.platform === 'win32' ? [['py', ['-3']], ['python', []], ['python3', []]] : [['python3', []], ['python', []]];
  for (const [cmd, pre] of candidates) {
    const r = spawnSync(cmd, [...pre, '-c', 'import sys; sys.exit(0 if sys.version_info[0] == 3 else 1)'], { stdio: 'ignore' });
    if (r.status === 0) return [cmd, pre];
  }
  return null;
}

function runTool(tool, args) {
  const py = findPython();
  if (!py) fail('Python 3 is required for this command: https://www.python.org/downloads/');
  if (!args.length) fail(`usage: npx ec2build ${tool} <project-dir> [options]`);
  const r = spawnSync(py[0], [...py[1], path.join(SRC, 'scripts', `${tool}.py`), ...args], { stdio: 'inherit' });
  process.exit(r.status === null ? 1 : r.status);
}

function main() {
  const argv = process.argv.slice(2);
  const cmd = argv[0] && !argv[0].startsWith('-') ? argv[0] : (argv.includes('--version') || argv.includes('-v') ? 'version' : 'help');
  const rest = argv[0] === cmd ? argv.slice(1) : argv;
  switch (cmd) {
    case 'install': case 'update': return install(parse(rest));
    case 'uninstall': case 'remove': return uninstall(parse(rest));
    case 'status': return status(parse(rest));
    case 'doctor': case 'validate': case 'swimlanes': return runTool(cmd, rest);
    case 'version': return console.log(VERSION);
    case 'help': return console.log(HELP);
    default: console.error(`Unknown command: ${cmd}\n`); console.log(HELP); process.exit(2);
  }
}

main();
