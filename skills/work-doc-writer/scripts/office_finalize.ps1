param(
    [Parameter(Mandatory = $true)][string]$Docx,
    [string]$Pdf = ""
)
$ErrorActionPreference = "Stop"
$Docx = (Resolve-Path -LiteralPath $Docx).Path

$app = $null
$kind = ""
foreach ($prog in @("Word.Application", "KWps.Application")) {
    try {
        $app = New-Object -ComObject $prog
        $kind = $prog
        break
    } catch { }
}
if (-not $app) {
    Write-Output "FINALIZE_SKIPPED no Word/WPS COM"
    exit 2
}

try {
    $app.Visible = $false
    try { $app.DisplayAlerts = 0 } catch { }
    $doc = $app.Documents.Open($Docx, $false, $false)
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    $doc.Save()
    if ($Pdf) { $doc.ExportAsFixedFormat($Pdf, 17) }
    $doc.Close($false)
    Write-Output "FINALIZE_OK $kind"
} catch {
    Write-Error $_
    exit 1
} finally {
    try { $app.Quit() } catch { }
    try { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null } catch { }
}
