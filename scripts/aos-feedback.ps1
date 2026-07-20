# AOS Feedback CLI (PowerShell)
# 用法: .\scripts\aos-feedback.ps1 <skill> [options]

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Skill,

    [Parameter(Mandatory=$false)]
    [ValidateSet("useful", "needs-improvement", "outdated", "mislabeled")]
    [string]$Rating,

    [Parameter(Mandatory=$false)]
    [string]$Note = "",

    [Parameter(Mandatory=$false)]
    [string]$Context = "",

    [Parameter(Mandatory=$false)]
    [switch]$FirstMatch,

    [Parameter(Mandatory=$false)]
    [switch]$Rework,

    [Parameter(Mandatory=$false)]
    [switch]$Init,

    [Parameter(Mandatory=$false)]
    [switch]$Show
)

$ErrorActionPreference = "Stop"
$SchemaVersion = "0.1"

$FeedbackDir = if ($env:AOS_FEEDBACK_DIR) { $env:AOS_FEEDBACK_DIR } else { Join-Path $env:USERPROFILE ".agents\feedback" }

if (-not (Test-Path $FeedbackDir)) {
    New-Item -ItemType Directory -Path $FeedbackDir -Force | Out-Null
}

$File = Join-Path $FeedbackDir "$Skill.json"

# 校验 skill 名
if ($Skill -notmatch '^[a-z][a-z0-9-]*$') {
    Write-Host "❌ Skill 名必须是 kebab-case: $Skill" -ForegroundColor Red
    exit 1
}

function Initialize-File {
    param([string]$Path, [string]$SkillName)
    $today = Get-Date -Format "yyyy-MM-dd"
    $template = @{
        skill = $SkillName
        schema_version = $SchemaVersion
        created_at = $today
        updated_at = $today
        stats = @{ total_calls = 0; first_match_count = 0; rework_count = 0 }
        ratings = @{ useful = 0; "needs-improvement" = 0; outdated = 0; mislabeled = 0 }
        feedback = @()
    }
    $template | ConvertTo-Json -Depth 10 | Set-Content -Path $Path -Encoding UTF8
}

function Show-Feedback {
    param([string]$Path, [string]$SkillName)
    if (-not (Test-Path $Path)) {
        Write-Host "📭 无反馈数据: $SkillName"
        Write-Host "   提示: 用 -Rating 或 -FirstMatch 开始记录"
        return
    }

    $data = Get-Content $Path -Raw | ConvertFrom-Json
    $total = $data.stats.total_calls
    $useful = $data.ratings.useful
    $fm = $data.stats.first_match_count
    $rework = $data.stats.rework_count

    $usefulRate = if ($total -gt 0) { [math]::Round($useful * 100 / $total) } else { 0 }
    $fmRate = if ($total -gt 0) { [math]::Round($fm * 100 / $total) } else { 0 }
    $reworkRate = if ($total -gt 0) { [math]::Round($rework * 100 / $total) } else { 0 }

    Write-Host "📊 反馈数据: $SkillName"
    Write-Host "---"
    Write-Host "总调用：$total"
    Write-Host "有用率：${usefulRate}%"
    Write-Host "首次匹配率：${fmRate}%"
    Write-Host "返工率：${reworkRate}%"
    Write-Host ""
    Write-Host "评分分布："
    $data.ratings.PSObject.Properties | ForEach-Object {
        Write-Host "  $($_.Name): $($_.Value)"
    }
    Write-Host ""
    Write-Host "最近反馈（最多 5 条）："
    $recent = $data.feedback | Select-Object -Last 5
    $recent | ForEach-Object {
        $noteText = if ($_.note) { $_.note } else { "" }
        Write-Host "  [$($_.date)] $($_.rating): $noteText"
    }
}

function Record-Rating {
    param([string]$Path, [string]$SkillName, [string]$Rating, [string]$Note, [string]$Context)

    if (-not (Test-Path $Path)) {
        Initialize-File -Path $Path -SkillName $SkillName
    }

    $today = Get-Date -Format "yyyy-MM-dd"
    $data = Get-Content $Path -Raw | ConvertFrom-Json

    # 更新统计
    $data.stats.total_calls += 1
    $data.ratings.$Rating += 1
    $data.updated_at = $today

    # 添加反馈
    $entry = @{
        date = $today
        rating = $Rating
    }
    if ($Note) { $entry.note = $Note }
    if ($Context) { $entry.context = $Context }
    $data.feedback += [PSCustomObject]$entry

    # 限制最多 50 条
    if ($data.feedback.Count -gt 50) {
        $data.feedback = $data.feedback | Select-Object -Last 50
    }

    $data | ConvertTo-Json -Depth 10 | Set-Content -Path $Path -Encoding UTF8
    Write-Host "✅ 已记录 [$Rating]: $SkillName$(if ($Note) { " — $Note" })" -ForegroundColor Green
}

function Record-FirstMatch {
    param([string]$Path, [string]$SkillName)

    if (-not (Test-Path $Path)) {
        Initialize-File -Path $Path -SkillName $SkillName
    }

    $today = Get-Date -Format "yyyy-MM-dd"
    $data = Get-Content $Path -Raw | ConvertFrom-Json
    $data.stats.total_calls += 1
    $data.stats.first_match_count += 1
    $data.updated_at = $today

    $data | ConvertTo-Json -Depth 10 | Set-Content -Path $Path -Encoding UTF8
    Write-Host "✅ 已记录首次匹配: $SkillName" -ForegroundColor Green
}

function Record-Rework {
    param([string]$Path, [string]$SkillName)

    if (-not (Test-Path $Path)) {
        Initialize-File -Path $Path -SkillName $SkillName
    }

    $today = Get-Date -Format "yyyy-MM-dd"
    $data = Get-Content $Path -Raw | ConvertFrom-Json
    $data.stats.total_calls += 1
    $data.stats.rework_count += 1
    $data.updated_at = $today

    $data | ConvertTo-Json -Depth 10 | Set-Content -Path $Path -Encoding UTF8
    Write-Host "✅ 已记录返工: $SkillName" -ForegroundColor Green
}

# 执行
if ($Init) {
    Initialize-File -Path $File -SkillName $Skill
    Write-Host "✅ 已初始化: $File" -ForegroundColor Green
} elseif ($Show) {
    Show-Feedback -Path $File -SkillName $Skill
} elseif ($FirstMatch) {
    Record-FirstMatch -Path $File -SkillName $Skill
} elseif ($Rework) {
    Record-Rework -Path $File -SkillName $Skill
} elseif ($Rating) {
    Record-Rating -Path $File -SkillName $Skill -Rating $Rating -Note $Note -Context $Context
} else {
    Write-Host "❌ 缺少操作: -Rating / -FirstMatch / -Rework / -Init / -Show" -ForegroundColor Red
    Write-Host ""
    Write-Host "用法示例："
    Write-Host "  .\scripts\aos-feedback.ps1 coding -Rating useful -Note '清晰'"
    Write-Host "  .\scripts\aos-feedback.ps1 design -FirstMatch"
    Write-Host "  .\scripts\aos-feedback.ps1 review -Show"
    exit 1
}