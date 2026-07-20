# AOS MANIFEST 自动生成脚本 (Windows PowerShell)
# 委托给 build-manifest.py 跨平台实现

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "build-manifest.py"

if ($args.Count -gt 0) {
    & python $PythonScript $args[0]
} else {
    & python $PythonScript
}