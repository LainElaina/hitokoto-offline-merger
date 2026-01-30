@echo off
chcp 65001 >nul
title github一键部署工具
color 0A

echo ========================================================
echo  一键部署脚本 (带错误检测版)
echo ========================================================
echo.

:: 1. 获取提交注释
set /p commit_msg=请输入本次更新的内容(注释): 
if "%commit_msg%"=="" set commit_msg=日常维护更新

echo.
echo [1/3] 正在执行 git add ...
git add .
if %errorlevel% neq 0 goto :Error

echo.
echo [2/3] 正在执行 git commit ...
git commit -m "%commit_msg%"
:: 注意：如果没有文件变动，commit 会报错，但我们允许这种情况继续，或者你可以选择报错
:: 这里我设置为：如果 commit 报错（通常是因为没有变动），提示一下但允许尝试 push
if %errorlevel% neq 0 (
    echo [警告] 似乎没有文件需要提交，或者 commit 出错了。
    echo 正在尝试继续...
)

echo.
echo [3/3] 正在推送到 GitHub (源码) ...
git push
if %errorlevel% neq 0 goto :Error

echo.
echo ========================================================
echo                🎉 恭喜！所有步骤均已成功完成！
echo ========================================================
pause
exit

:Error
color 0C
echo.
echo ========================================================
echo                ❌ 错误！脚本已停止运行！
echo ========================================================
echo 请检查上方的错误信息，修复后再试。
pause
exit