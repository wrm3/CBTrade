# Fix for PowerShell Output Formatting Issues in Cursor

## Quick Start
1. Open PowerShell as Administrator
2. Navigate to: `%LOCALAPPDATA%\Programs\cursor\resources\app\out\vs\workbench\contrib\terminal\common\scripts`
3. Backup `shellIntegration.ps1`
4. Apply the minimal fix from Part 2
5. Restart Cursor

## Prerequisites
- Windows 10/11
- PowerShell 5.1 or higher
- Cursor IDE installed
- Administrative access to modify Cursor files

## Version Compatibility
- Cursor: v0.1.0 or higher
- PowerShell: 5.1 or higher
- PSReadLine: 2.0.0 or higher

## Problem
When running Python commands directly in PowerShell terminals within Cursor, you may experience:
- Cursor position errors
- Output formatting issues
- Buffer size exceptions
- PSReadLine integration problems

## Solution
There are three parts to this fix:

### Part 1: Enable Debug Output
Add this line at the top of your `shellIntegration.ps1` file:
```powershell
# Enable debug output
$DebugPreference = "Continue"
```
Location: `c:\Users\{USER}\AppData\Local\Programs\cursor\resources\app\out\vs\workbench\contrib\terminal\common\scripts\shellIntegration.ps1`

### Part 2: Minimal Fix
For a production-ready fix, modify the `Set-MappedKeyHandler` function in `shellIntegration.ps1`:

```powershell
function Set-MappedKeyHandler {
    param ([string[]] $Chord, [string[]]$Sequence)
    
    try {
        # ... existing handler setup code ...
        
        if ($Handler) {
            $wrappedFunction = $Handler.Function
            if ($wrappedFunction -is [ScriptBlock]) {
                Set-PSReadLineKeyHandler -Chord $Sequence -ScriptBlock {
                    try {
                        & $wrappedFunction
                    }
                    catch [System.ArgumentOutOfRangeException] {
                        try {
                            $Host.UI.RawUI.CursorPosition = New-Object System.Management.Automation.Host.Coordinates 0, ($Host.UI.RawUI.CursorPosition.Y)
                        }
                        catch {
                            Write-Debug "Failed to reset cursor: $_"
                        }
                    }
                }
            }
        }
    }
    catch {
        Write-Debug "Error in Set-MappedKeyHandler: $_"
    }
}
```

### Part 3: Detailed Debug Version
For troubleshooting or environments where you need more visibility, use this enhanced version:

```powershell
function Set-MappedKeyHandler {
    param ([string[]] $Chord, [string[]]$Sequence)
    
    Write-Debug "=== Set-MappedKeyHandler Debug ==="
    Write-Debug "Input Chord: $($Chord -join ',')"
    Write-Debug "Input Sequence: $($Sequence -join ',')"
    Write-Debug "Current Output Encoding: $($OutputEncoding.EncodingName)"
    Write-Debug "Console Encoding: $([Console]::OutputEncoding.EncodingName)"
    Write-Debug "Buffer Width: $($Host.UI.RawUI.BufferSize.Width)"
    Write-Debug "Buffer Height: $($Host.UI.RawUI.BufferSize.Height)"
    
    # Safely get PSReadLine version
    $psrlVersion = (Get-Module PSReadLine).Version
    Write-Debug "PSReadLine Version: $psrlVersion"
    
    try {
        # For PSReadLine 2.1+ use newer API
        if ($psrlVersion -ge [Version]"2.1") {
            Write-Debug "Using PSReadLine 2.1+ API"
            $Handler = Get-PSReadLineKeyHandler -Chord $Chord -ErrorAction SilentlyContinue | Select-Object -First 1
            Write-Debug "Handler found: $($Handler -ne $null)"
            if ($Handler) {
                Write-Debug "Handler Function: $($Handler.Function)"
                Write-Debug "Handler Description: $($Handler.Description)"
            }
        }
        else {
            Write-Debug "Using legacy PSReadLine API"
            $Handler = Get-PSReadLineKeyHandler -Bound -ErrorAction SilentlyContinue | 
                Where-Object -FilterScript { $_.Key -eq $Chord } | 
                Select-Object -First 1
            Write-Debug "Handler found: $($Handler -ne $null)"
        }
        
        if ($Handler) {
            $wrappedFunction = $Handler.Function
            Write-Debug "Function type: $($wrappedFunction.GetType().Name)"
            
            if ($wrappedFunction -is [ScriptBlock]) {
                Write-Debug "Wrapping ScriptBlock handler"
                Set-PSReadLineKeyHandler -Chord $Sequence -ScriptBlock {
                    try {
                        Write-Debug "Executing wrapped handler"
                        Write-Debug "Current cursor position: $($Host.UI.RawUI.CursorPosition | ConvertTo-Json)"
                        & $wrappedFunction
                    }
                    catch [System.ArgumentOutOfRangeException] {
                        Write-Debug "Cursor position error caught:"
                        Write-Debug "Exception: $($_.Exception.Message)"
                        Write-Debug "Stack trace: $($_.Exception.StackTrace)"
                        try {
                            $Host.UI.RawUI.CursorPosition = New-Object System.Management.Automation.Host.Coordinates 0, ($Host.UI.RawUI.CursorPosition.Y)
                            Write-Debug "Cursor position reset to: $($Host.UI.RawUI.CursorPosition | ConvertTo-Json)"
                        }
                        catch {
                            Write-Debug "Failed to reset cursor: $_"
                        }
                    }
                    catch {
                        Write-Debug "Unexpected error in handler: $_"
                    }
                }
            }
        }
    }
    catch {
        Write-Debug "Error in Set-MappedKeyHandler:"
        Write-Debug "Exception type: $($_.Exception.GetType().Name)"
        Write-Debug "Message: $($_.Exception.Message)"
        Write-Debug "Stack trace: $($_.Exception.StackTrace)"
    }
    finally {
        Write-Debug "=== End Set-MappedKeyHandler Debug ==="
    }
}
```

### Part 4: PowerShell Wrapper Script
Create a wrapper script to handle command output properly:

```powershell
# run_command.ps1
# Set output encoding to UTF8
$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8

# Function to run Python commands with proper output handling
function Run-PythonCommand {
    param (
        [string]$Command
    )
    
    # Capture and format output
    $output = python -c $Command
    Write-Host $output
}
```

## When to Use Each Version
1. **Minimal Fix**: Use this in production environments where you just need the fix without debugging overhead
2. **Detailed Debug Version**: Use this when:
   - Troubleshooting specific PSReadLine issues
   - Debugging cursor position problems
   - Investigating encoding or buffer size issues
3. **Wrapper Script**: Use for running Python commands that need proper output formatting

## Implementation Steps
1. Choose either the minimal or detailed version for `shellIntegration.ps1`
2. Add the debug preference line at the top of the file
3. Implement the wrapper script for Python commands
4. Restart Cursor to apply changes

## Usage Examples

### 1. Checking Environment Variables
```powershell
# test_env.ps1
$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8
# I fixing an OPENAI_API_KEY issue, changed it from that so that others won't accidentally reveal private info
$output = python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('THINGAMAJIG_API_KEY =', os.getenv('THINGAMAJIG_API_KEY', 'Not set'))"
Write-Host $output
```

### 2. Running Python Scripts
```powershell
# run_script.ps1
$OutputEncoding = [Console]::OutputEncoding = [Text.Encoding]::UTF8

$output = python your_script.py
Write-Host $output
```

## Additional Tips
1. The minimal fix is sufficient for most users
2. Use the detailed version if you encounter specific issues that need debugging
3. The wrapper script is still recommended for running Python commands
4. You can switch between versions as needed for troubleshooting

## Notes
- Both versions of the fix address the same core issues
- The detailed version provides more visibility but adds overhead
- The wrapper script complements both versions
- May need to restart Cursor after making changes

## Troubleshooting
If you still experience issues:
1. Check if debug output is enabled: `$DebugPreference`
2. Verify encoding: `[Console]::OutputEncoding`
3. Test buffer size: `$Host.UI.RawUI.BufferSize`
4. Check PSReadLine version: `(Get-Module PSReadLine).Version`
