param([Parameter(Mandatory=$true)][string]$File)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$schemas = Join-Path $here 'schemas-2.1\schemas'
stix2_validator --version 2.1 -s $schemas $File
