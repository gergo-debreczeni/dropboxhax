
param([string]$mac)

function  WaitForVMToStop ([string] $vmName ,[string]  $hvServer, [int] $timeout)
{
       $tmo = $timeout
    while ($tmo -gt 0)
    {
        Start-Sleep -s 1
        $tmo -= 5

        $vm = Get-VM -Name $vmName -ComputerName $hvServer
        if (-not $vm)
        {
            return $False
        }

        if ($vm.State -eq [Microsoft.HyperV.PowerShell.VMState]::off)
        {
            return $True
        }
    }

    Write-Error -Message "StopVM: VM did not stop within timeout period" -Category OperationTimeout -ErrorAction SilentlyContinue
    return $False
}

$hvServer = 'localhost'
$vmName = 'ubuntu-dropbox'
$snapshotname = "ICABase"
if ((Get-VM -ComputerName $hvServer -Name $vmName).State -ne "Off") {
    Stop-VM -ComputerName $hvServer -Name $vmName -Force -Confirm:$false
}

if (-not (WaitForVmToStop $vmName $hvServer 300))
{
    Write-Output "Error: Unable to stop VM"
    return $False
}

Restore-VMSnapshot -VMName $vmName -Name $snapshotname -ComputerName $hvServer -Confirm:$false

$na = Get-VMNetworkAdapter -VMName $vmName
Set-VMNetworkAdapter $na -StaticMacAddress $mac
Start-VM $vmName -ComputerName $hvServer
