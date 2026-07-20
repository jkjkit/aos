# AOS 协议 lint 脚本 (Windows PowerShell)
# 用法: .\scripts\lint-skill.ps1 [路径]

$ErrorActionPreference = "Stop"

$AOS_ROOT = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$TARGET = if ($args.Count -gt 0) { (Resolve-Path $args[0]).Path } else { $AOS_ROOT }

$Script:Errors = 0
$Script:Warnings = 0

function Ok($msg)   { Write-Host "  [OK] $msg" }
function Warn($msg) { Write-Host "  [WARN] $msg"; $Script:Warnings++ }
function Err($msg)  { Write-Host "  [ERROR] $msg"; $Script:Errors++ }

function Check-Skill($dir) {
    $name = Split-Path $dir -Leaf
    Write-Host "[Skill] $name"

    $file = Join-Path $dir "SKILL.md"
    if (-not (Test-Path $file)) {
        Err "缺少 SKILL.md"
        return
    }

    if (Test-Path (Join-Path $dir "README.md")) {
        Warn "存在 README.md（按规范应为单文件 SKILL.md）"
    }
    if (Test-Path (Join-Path $dir "examples")) {
        Warn "存在 examples/ 目录（按规范应为单文件 SKILL.md）"
    }
    if (Test-Path (Join-Path $dir "tests")) {
        Warn "存在 tests/ 目录（按规范应为单文件 SKILL.md）"
    }

    $firstLine = (Get-Content $file -TotalCount 1)
    if ($firstLine -ne "---") {
        Err "第一行不是 ---（缺少 YAML frontmatter）"
        return
    }

    # 提取 frontmatter 内容
    $inFrontmatter = $false
    $hasName = $false
    $hasDesc = $false
    $nameValue = ""
    $descValue = ""
    $extraFields = @()

    Get-Content $file | ForEach-Object {
        $line = $_
        if ($line -eq "---") {
            $inFrontmatter = -not $inFrontmatter
            return
        }
        if ($inFrontmatter) {
            if ($line -match '^name:\s*(.+)$') {
                $hasName = $true
                $nameValue = $Matches[1].Trim()
            } elseif ($line -match '^description:\s*(.+)$') {
                $hasDesc = $true
                $descValue = $Matches[1].Trim()
            } elseif ($line -match '^([a-z_]+):\s') {
                $key = $Matches[1]
                if ($key -ne "name" -and $key -ne "description") {
                    $extraFields += $key
                }
            }
        }
    }

    if (-not $hasName) {
        Err "frontmatter 缺少 name 字段"
    } elseif ($nameValue -ne $name) {
        Err "frontmatter name='$nameValue' 与目录名 '$name' 不一致"
    } else {
        Ok "name 与目录一致"
    }

    if (-not $hasDesc) {
        Err "frontmatter 缺少 description 字段"
    } else {
        $len = $descValue.Length
        if ($descValue -match '\?{3,}') {
            Err "description 疑似包含编码损坏（连续问号）"
        } elseif ($len -lt 10) {
            Err "description 过短（$len 字符，建议 ≥ 10）"
        } elseif ($len -lt 24) {
            Warn "description 较短（$len 字符），可能缺少对象或职责边界"
        } else {
            Ok "description: $len 字符"
        }
    }

    if ($extraFields.Count -gt 0) {
        Warn "frontmatter 包含规范外的字段: $($extraFields -join ', ')"
    }

    $content = Get-Content $file -Raw
    if ($content -match "^# End") {
        Err "包含 # End 标记（应删除）"
    }

    $lineCount = (Get-Content $file).Count
    if ($lineCount -lt 20) {
        Warn "文件仅 $lineCount 行，可能内容不够完整"
    } else {
        Ok "$lineCount 行"
    }

    Write-Host ""
}

function Check-Workflow($dir) {
    $name = Split-Path $dir -Leaf
    Write-Host "[Workflow] $name"

    $file = Join-Path $dir "WORKFLOW.md"
    if (-not (Test-Path $file)) {
        Err "缺少 WORKFLOW.md"
        return
    }

    if (Test-Path (Join-Path $dir "README.md")) {
        Warn "存在 README.md"
    }
    if (Test-Path (Join-Path $dir "examples")) {
        Warn "存在 examples/ 目录"
    }

    $content = Get-Content $file -Raw
    if ($content -match "^# End") {
        Err "包含 # End 标记"
    }

    $firstLine = (Get-Content $file -TotalCount 1)
    if ($firstLine -notmatch "^# ") {
        Err "第一行不是 # 标题"
    }

    Ok "$((Get-Content $file).Count) 行"
    Write-Host ""
}

function Check-Knowledge($dir) {
    $name = Split-Path $dir -Leaf
    Write-Host "[Knowledge] $name"

    $file = Join-Path $dir "KNOWLEDGE.md"
    if (-not (Test-Path $file)) {
        Err "缺少 KNOWLEDGE.md"
        return
    }

    $content = Get-Content $file -Raw
    if ($content -match "^# End") {
        Err "包含 # End 标记"
    }

    Ok "$((Get-Content $file).Count) 行"
    Write-Host ""
}

function Check-Template($dir) {
    $name = Split-Path $dir -Leaf
    Write-Host "[Template] $name"

    $file = Join-Path $dir "TEMPLATE.md"
    if (-not (Test-Path $file)) {
        Err "缺少 TEMPLATE.md"
        return
    }

    $content = Get-Content $file -Raw
    if ($content -match "^# End") {
        Err "包含 # End 标记"
    }

    Ok "$((Get-Content $file).Count) 行"
    Write-Host ""
}

Write-Host "AOS Lint"
Write-Host "Target: $TARGET"
Write-Host ""

if (Test-Path (Join-Path $TARGET "skills")) {
    Write-Host "=== Skills ==="
    Get-ChildItem (Join-Path $TARGET "skills") -Directory | ForEach-Object { Check-Skill $_.FullName }

    Write-Host "=== Workflows ==="
    Get-ChildItem (Join-Path $TARGET "workflows") -Directory | ForEach-Object { Check-Workflow $_.FullName }

    Write-Host "=== Knowledge ==="
    Get-ChildItem (Join-Path $TARGET "knowledge") -Directory | ForEach-Object { Check-Knowledge $_.FullName }

    Write-Host "=== Templates ==="
    Get-ChildItem (Join-Path $TARGET "templates") -Directory | ForEach-Object { Check-Template $_.FullName }
} else {
    $parent = Split-Path $TARGET -Leaf
    $grandParent = Split-Path (Split-Path $TARGET -Parent) -Leaf
    switch ($grandParent) {
        "skills"    { Check-Skill $TARGET }
        "workflows" { Check-Workflow $TARGET }
        "knowledge" { Check-Knowledge $TARGET }
        "templates" { Check-Template $TARGET }
        default     { Write-Host "未知路径：$TARGET"; exit 1 }
    }
}

Write-Host "=============================="
Write-Host "Errors:   $Script:Errors"
Write-Host "Warnings: $Script:Warnings"
Write-Host "=============================="

if ($Script:Errors -gt 0) { exit 1 }