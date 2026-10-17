param([string]$Engine = 'xelatex')
$ErrorActionPreference = 'Stop'
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location -LiteralPath $projectRoot
try {
    New-Item -ItemType Directory -Force build | Out-Null
    $env:TEXINPUTS = '.;./vendor/texmf/tex//;'
    $env:OPENTYPEFONTS = '.;./vendor/texmf/fonts/opentype//;'
    $env:TFMFONTS = '.;./vendor/texmf/fonts/tfm//;'
    $engineVersion = (& $Engine --version | Out-String)
    if ($LASTEXITCODE -ne 0) { throw 'Could not identify the LaTeX engine.' }
    $latexArguments = @('-no-shell-escape', '-interaction=nonstopmode',
        '-halt-on-error', '-file-line-error', '-synctex=1', '-output-directory=build')
    if ($engineVersion -match 'MiKTeX') { $latexArguments += '-disable-installer' }
    $latexArguments += 'main.tex'
    & $Engine @latexArguments
    if ($LASTEXITCODE -ne 0) { throw 'LaTeX first pass failed.' }
    & biber --input-directory=build --output-directory=build main
    if ($LASTEXITCODE -ne 0) { throw 'Bibliography compilation failed.' }
    & $Engine @latexArguments
    if ($LASTEXITCODE -ne 0) { throw 'LaTeX second pass failed.' }
    & $Engine @latexArguments
    if ($LASTEXITCODE -ne 0) { throw 'LaTeX final pass failed.' }
    Copy-Item -LiteralPath build/main.pdf -Destination '扩散模型：从分布直觉到多模态生成.pdf' -Force
} finally {
    Pop-Location
}
