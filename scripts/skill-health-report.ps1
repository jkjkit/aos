# AOS Skill 健康度报告 (PowerShell)
# 用法: .\scripts\skill-health-report.ps1
# 输出: ~/.agents\health-report.md

$ErrorActionPreference = "Stop"

$FeedbackDir = if ($env:AOS_FEEDBACK_DIR) { $env:AOS_FEEDBACK_DIR } else { Join-Path $env:USERPROFILE ".agents\feedback" }
$ReportPath = if ($env:AOS_HEALTH_REPORT) { $env:AOS_HEALTH_REPORT } else { Join-Path $env:USERPROFILE ".agents\health-report.md" }

if (-not (Test-Path $FeedbackDir)) {
    Write-Host "📭 反馈目录不存在: $FeedbackDir"
    Write-Host "   提示: 用 'aos feedback <skill> -Rating ...' 开始记录"
    exit 0
}

$files = Get-ChildItem $FeedbackDir -Filter "*.json" | Sort-Object Name

$totalCalls = 0
$totalUseful = 0
$totalFm = 0
$totalRework = 0
$skillCount = 0
$rows = @()

foreach ($file in $files) {
    $data = Get-Content $file.FullName -Raw | ConvertFrom-Json
    $skill = $file.BaseName
    $calls = $data.stats.total_calls
    $useful = $data.ratings.useful
    $fm = $data.stats.first_match_count
    $rework = $data.stats.rework_count

    if ($calls -eq 0) { continue }

    $usefulRate = [math]::Round($useful * 100 / $calls)
    $fmRate = [math]::Round($fm * 100 / $calls)
    $reworkRate = [math]::Round($rework * 100 / $calls)

    if ($usefulRate -ge 80 -and $fmRate -ge 70) {
        $status = "✅ 健康"
    } elseif ($usefulRate -lt 60 -or $fmRate -lt 50) {
        $status = "⚠️ 关注"
    } else {
        $status = "🟡 一般"
    }

    $totalCalls += $calls
    $totalUseful += $useful
    $totalFm += $fm
    $totalRework += $rework
    $skillCount++

    $rows += [PSCustomObject]@{
        Skill = $skill
        Calls = $calls
        UsefulRate = $usefulRate
        FmRate = $fmRate
        ReworkRate = $reworkRate
        Status = $status
        File = $file.FullName
    }
}

$overallUseful = if ($totalCalls -gt 0) { [math]::Round($totalUseful * 100 / $totalCalls) } else { 0 }
$overallFm = if ($totalCalls -gt 0) { [math]::Round($totalFm * 100 / $totalCalls) } else { 0 }
$overallRework = if ($totalCalls -gt 0) { [math]::Round($totalRework * 100 / $totalCalls) } else { 0 }

$dateNow = Get-Date -Format "yyyy-MM-dd"

# 生成报告
$report = @()
$report += "# AOS Skill 健康度报告"
$report += ""
$report += "生成时间：$dateNow"
$report += ""
$report += "## 总览"
$report += ""
$report += "| 指标 | 数值 |"
$report += "|------|------|"
$report += "| 已记录 Skill 数 | $skillCount |"
$report += "| 总调用次数 | $totalCalls |"
$report += "| 整体有用率 | ${overallUseful}% |"
$report += "| 整体首次匹配率 | ${overallFm}% |"
$report += "| 整体返工率 | ${overallRework}% |"
$report += ""

if ($skillCount -eq 0) {
    $report += "## 暂无数据"
    $report += ""
    $report += "使用 `aos feedback <skill> -Rating ...` 开始记录。"
    $report -join "`n" | Set-Content -Path $ReportPath -Encoding UTF8
    Write-Host "✅ 健康度报告已生成: $ReportPath"
    exit 0
}

$report += "## Skill 健康度（按调用次数排序）"
$report += ""
$report += "| Skill | 调用 | 有用率 | 首次匹配 | 返工率 | 状态 |"
$report += "|-------|------|--------|----------|--------|------|"

$sortedRows = $rows | Sort-Object Calls -Descending
foreach ($row in $sortedRows) {
    $report += "| $($row.Skill) | $($row.Calls) | $($row.UsefulRate)% | $($row.FmRate)% | $($row.ReworkRate)% | $($row.Status) |"
}

$report += ""

# 需要关注的 Skill
$report += "## 需要关注的 Skill"
$report += ""

$hasWarn = $false
foreach ($row in $rows) {
    if ($row.Calls -lt 3) { continue }
    if ($row.UsefulRate -ge 80 -and $row.FmRate -ge 70) { continue }

    $hasWarn = $true
    $data = Get-Content $row.File -Raw | ConvertFrom-Json
    $mislabeled = $data.ratings.mislabeled
    $outdated = $data.ratings.outdated

    $report += "### $($row.Skill)"
    $report += ""
    $report += "- 有用率：$($row.UsefulRate)%（调用 $($row.Calls) 次）"
    $report += "- 首次匹配率：$($row.FmRate)%"

    if ($row.FmRate -lt 50) {
        $report += "- ⚠️ 首次匹配率过低：description 可能不够精准或与其他 Skill 边界不清"
    }
    if ($row.ReworkRate -gt 25) {
        $report += "- ⚠️ 返工率较高：Skill 输出常需用户二次修改"
    }

    $report += ""
    $report += "**最近反馈：**"
    $report += ""

    $recent = $data.feedback | Select-Object -Last 5
    foreach ($entry in $recent) {
        $noteText = if ($entry.note) { ": $($entry.note)" } else { "" }
        $report += "  - [$($entry.date)] $($entry.rating)$noteText"
    }

    $report += ""
    $report += "**改进建议：**"
    $report += ""

    if ($row.FmRate -lt 50) {
        $report += "- 收窄 description 的触发场景"
        $report += "- 加更具体的触发示例"
    }
    if ($row.ReworkRate -gt 25) {
        $report += "- 检查 Skill 流程是否覆盖了常见边界场景"
        $report += "- 补充示例与反例"
    }
    if ($mislabeled -gt 0) {
        $report += "- $mislabeled 次「描述不准确」标记：description 需要重新审视"
    }
    if ($outdated -gt 0) {
        $report += "- $outdated 次「过时」标记：检查 Skill 内容是否需要更新"
    }

    $report += ""
}

if (-not $hasWarn) {
    $report += "_无。_"
    $report += ""
}

$report += "## 长期建议"
$report += ""
$report += "- 每季度 review 一次本报告"
$report += "- 优先改写：高频调用但低有用率的 Skill"
$report += "- 收集 30+ 反馈后再下结论（避免小样本噪声）"
$report += "- 持续观察改写后的指标变化"
$report += ""
$report += "---"
$report += ""
$report += "_本报告由 `scripts\skill-health-report.ps1` 自动生成。_"

$report -join "`n" | Set-Content -Path $ReportPath -Encoding UTF8

Write-Host "✅ 健康度报告已生成: $ReportPath"
Write-Host ""
Write-Host "快速预览："
Write-Host "---"
Get-Content $ReportPath -TotalCount 20