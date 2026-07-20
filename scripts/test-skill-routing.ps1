# Validate AOS Skill routing regression cases (Windows PowerShell)
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "test-skill-routing.py"

& python $PythonScript @args
exit $LASTEXITCODE