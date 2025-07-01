
@echo off
set CURDIR=%CD%
echo curdir %CURDIR%

pushd %~dp0
    echo jumped to %CD%
    echo running uv run --directory "%CURDIR%" owui_sync %*
    uv run --directory "%CURDIR%" owui_sync %*
popd
echo returned to %CD%
