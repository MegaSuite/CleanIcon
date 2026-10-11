# CleanIcon
## 开发环境
- wsl，安装有android studio cli，用于开发。
- 宿主机安装有android studio，仅用于模拟器和界面微调。

## 注意事项
- 需覆盖的应用列表位于`ref/applist.csv`，仅从完美图标计划中获取这些应用的图标，如果某个应用的图标不存在，则跳过该应用并输出到`ref/missing.csv`。
- 开发过程中的中间产物文件均在当前项目目录下生成。