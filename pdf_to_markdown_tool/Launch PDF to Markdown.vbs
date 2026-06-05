' Launch PDF to Markdown.vbs
' Double-click this file to open the converter with NO terminal window.
'
' Uses the dedicated venv at C:\pmt which has marker-pdf installed.
' windowStyle = 0 hides the Python console; the tkinter GUI still appears.

Dim shell, fso, dir
Set shell = CreateObject("WScript.Shell")
Set fso   = CreateObject("Scripting.FileSystemObject")
dir       = fso.GetParentFolderName(WScript.ScriptFullName)

shell.Run """C:\pmt\Scripts\pythonw.exe"" """ & dir & "\app.py""", 0, False
