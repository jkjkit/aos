param(
    [ValidateSet("core", "ai", "design", "full")]
    [string]$Profile = "core",

    [ValidateSet("isolate", "keep", "restore")]
    [string]$ThirdParty = "isolate",

    [string]$Target = "",

    [switch]$InstallRuntime,

    # Backward-compatible no-op. Runtime entry files are no longer installed by default.
    [switch]$SkipRuntime
)

# AOS 一键部署脚本 (Windows PowerShell)
# 示例: .\deploy.ps1 -Profile core -ThirdParty isolate

$ErrorActionPreference = "Stop"

$AOS_SOURCE = Split-Path -Parent $MyInvocation.MyCommand.Path
if ([string]::IsNullOrWhiteSpace($Target)) {
    $Target = Join-Path $env:USERPROFILE ".agents"
}
$AOS_TARGET = [System.IO.Path]::GetFullPath($Target).TrimEnd('\', '/')
$targetRoot = [System.IO.Path]::GetPathRoot($AOS_TARGET).TrimEnd('\', '/')
if ($AOS_TARGET -eq $targetRoot) {
    throw "Refusing to deploy to a filesystem root: $AOS_TARGET"
}

function Assert-ManagedPath {
    param([string]$Path, [string]$Root)
    $fullPath = [System.IO.Path]::GetFullPath($Path)
    $fullRoot = [System.IO.Path]::GetFullPath($Root).TrimEnd('\', '/')
    $prefix = $fullRoot + [System.IO.Path]::DirectorySeparatorChar
    if (!$fullPath.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Unsafe path outside managed root: $fullPath (root: $fullRoot)"
    }
}

function Remove-ManagedDirectory {
    param([string]$Path, [string]$Root)
    Assert-ManagedPath -Path $Path -Root $Root
    if (Test-Path -LiteralPath $Path) {
        Remove-Item -LiteralPath $Path -Recurse -Force
    }
}

function Invoke-ProfileTool {
    param([string[]]$Arguments)
    $output = & python (Join-Path $AOS_SOURCE "scripts\skill_profiles.py") @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "skill_profiles.py failed with exit code $LASTEXITCODE"
    }
    return @($output | Where-Object { ![string]::IsNullOrWhiteSpace($_) })
}

Write-Host ""
Write-Host "  AOS - Agent Operating System"
Write-Host "  Profile: $Profile"
Write-Host "  Third-party policy: $ThirdParty"
Write-Host "  Deploy to: $AOS_TARGET"
if ($InstallRuntime -and !$SkipRuntime) {
    Write-Host "  Runtime entry files: install on request"
} else {
    Write-Host "  Runtime entry files: not modified by default"
}
if ($SkipRuntime) {
    Write-Warning "-SkipRuntime is retained for compatibility; Runtime entry files are not installed unless -InstallRuntime is supplied."
}
Write-Host ""

# 确保生成物与源数据同步。
& python (Join-Path $AOS_SOURCE "scripts\build-manifest.py")
if ($LASTEXITCODE -ne 0) { throw "build-manifest.py failed" }

$profileSkills = Invoke-ProfileTool -Arguments @("--profile", $Profile, "--format", "lines")
$allAosSkills = Invoke-ProfileTool -Arguments @("--all", "--format", "lines")
$selected = @{}
foreach ($name in $profileSkills) { $selected[$name] = $true }
$managed = @{}
foreach ($name in $allAosSkills) { $managed[$name] = $true }

if (!(Test-Path -LiteralPath $AOS_TARGET)) {
    New-Item -ItemType Directory -Path $AOS_TARGET -Force | Out-Null
}

$feedbackTarget = Join-Path $AOS_TARGET "feedback"
New-Item -ItemType Directory -Path $feedbackTarget -Force | Out-Null

# 1. 部署核心目录。
foreach ($dir in @("protocols", "workflows", "templates", "knowledge")) {
    Write-Host "  [$dir] deploying..."
    $targetPath = Join-Path $AOS_TARGET $dir
    Remove-ManagedDirectory -Path $targetPath -Root $AOS_TARGET
    Copy-Item -Recurse -LiteralPath (Join-Path $AOS_SOURCE $dir) -Destination $targetPath
}

# 2. 按 Profile 部署 Skills，并隔离第三方 Skill。
Write-Host "  [skills] deploying profile '$Profile'..."
$skillsTarget = Join-Path $AOS_TARGET "skills"
$packSkillsTarget = Join-Path $AOS_TARGET "packs\third-party\skills"
New-Item -ItemType Directory -Path $skillsTarget -Force | Out-Null
New-Item -ItemType Directory -Path $packSkillsTarget -Force | Out-Null

if ($ThirdParty -eq "restore") {
    Get-ChildItem -LiteralPath $packSkillsTarget -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $dest = Join-Path $skillsTarget $_.Name
        Assert-ManagedPath -Path $_.FullName -Root $packSkillsTarget
        Assert-ManagedPath -Path $dest -Root $skillsTarget
        if (Test-Path -LiteralPath $dest) {
            Write-Warning "Cannot restore third-party Skill '$($_.Name)': active destination exists."
        } else {
            Move-Item -LiteralPath $_.FullName -Destination $dest
            Write-Host "    restored third-party: $($_.Name)"
        }
    }
}

if ($ThirdParty -eq "isolate") {
    Get-ChildItem -LiteralPath $skillsTarget -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        if (!$managed.ContainsKey($_.Name)) {
            $dest = Join-Path $packSkillsTarget $_.Name
            Assert-ManagedPath -Path $_.FullName -Root $skillsTarget
            Assert-ManagedPath -Path $dest -Root $packSkillsTarget
            if (Test-Path -LiteralPath $dest) {
                Write-Warning "Cannot isolate third-party Skill '$($_.Name)': pack destination exists; leaving it active."
            } else {
                Move-Item -LiteralPath $_.FullName -Destination $dest
                Write-Host "    isolated third-party: $($_.Name)"
            }
        }
    }
}

foreach ($name in $allAosSkills) {
    if (!$selected.ContainsKey($name)) {
        Remove-ManagedDirectory -Path (Join-Path $skillsTarget $name) -Root $skillsTarget
    }
}

foreach ($name in $profileSkills) {
    $source = Join-Path $AOS_SOURCE "skills\$name"
    $dest = Join-Path $skillsTarget $name
    Remove-ManagedDirectory -Path $dest -Root $skillsTarget
    Copy-Item -Recurse -LiteralPath $source -Destination $dest
    Write-Host "    + $name"
}

# 3. 部署轻量 Router、完整 Manifest 和托管状态。
Copy-Item -LiteralPath (Join-Path $AOS_SOURCE "routers\$Profile.md") -Destination (Join-Path $AOS_TARGET "ROUTER.md") -Force
Copy-Item -LiteralPath (Join-Path $AOS_SOURCE "MANIFEST.md") -Destination (Join-Path $AOS_TARGET "MANIFEST.md") -Force
& python (Join-Path $AOS_SOURCE "scripts\skill_profiles.py") --profile $Profile --write-state (Join-Path $AOS_TARGET ".aos-managed-skills.json") --third-party-policy $ThirdParty | Out-Null
if ($LASTEXITCODE -ne 0) { throw "failed to write managed Skill state" }

# 4. 安装 Runtime 入口文件。
# Default behavior preserves user-owned Runtime files.
if ($InstallRuntime -and !$SkipRuntime) {
    Write-Host ""
    Write-Host "  [runtime] installing entry files..."

    $claudeDir = Join-Path $env:USERPROFILE ".claude"
    New-Item -ItemType Directory -Path $claudeDir -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $AOS_SOURCE "runtimes\claude.md") -Destination (Join-Path $claudeDir "CLAUDE.md") -Force
    Write-Host "    + ~/.claude/CLAUDE.md"

    $codexDir = Join-Path $env:USERPROFILE ".codex"
    New-Item -ItemType Directory -Path $codexDir -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $AOS_SOURCE "runtimes\codex.md") -Destination (Join-Path $codexDir "AGENT.md") -Force
    Write-Host "    + ~/.codex/AGENT.md"

    $cursorDir = Join-Path $env:USERPROFILE ".cursor\rules"
    New-Item -ItemType Directory -Path $cursorDir -Force | Out-Null
    Copy-Item -LiteralPath (Join-Path $AOS_SOURCE "runtimes\cursor.md") -Destination (Join-Path $cursorDir "aos.md") -Force
    Write-Host "    + ~/.cursor/rules/aos.md"
}

# 5. 部署观察层脚本。
Write-Host ""
Write-Host "  [scripts] installing observation tools..."
$scriptsTarget = Join-Path $AOS_TARGET "scripts"
New-Item -ItemType Directory -Path $scriptsTarget -Force | Out-Null
foreach ($file in @(
    "aos-feedback.ps1", "skill-health-report.ps1",
    "aos-feedback.py", "skill-health-report.py",
    "aos-feedback.sh", "skill-health-report.sh"
)) {
    Copy-Item -LiteralPath (Join-Path $AOS_SOURCE "scripts\$file") -Destination (Join-Path $scriptsTarget $file) -Force
}

Write-Host ""
Write-Host "  Done! Active AOS Skills: $($profileSkills.Count); profile: $Profile."
Write-Host ""