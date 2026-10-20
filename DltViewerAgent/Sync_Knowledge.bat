@echo off
rem Converts everything listed in agent\knowledge_sources.txt into the agent's knowledge base.
cd /d "%~dp0agent"
".venv\Scripts\python.exe" sync_knowledge.py
pause
