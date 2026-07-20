$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $scriptDir "context-budget-report.py") @args
exit $LASTEXITCODE