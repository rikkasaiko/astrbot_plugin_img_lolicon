</div>

<div align="center">

![:name](https://count.getloli.com/@img_lolicon?name=img_lolicon&theme=booru-jaypee&padding=7&offset=-5&align=top&scale=1&pixelated=1&darkmode=auto)

</div>

# 使用lolicon api获取涩图

- api文档 <https://api.lolicon.app/>

## 指令
 `/st help` 查看帮助信息
 ```
  /st help
  ```
 `/setu` 获取随机图片
```
  /setu
```
 `/setu <tag>`  **or** `/setu <tag> <tag>` 获取对应tags图片
 ```
  /setu 萝莉
  /setu 少女 白丝
```
 `/st cd <num>`, 通过指令修改cd限制, 单位秒, 默认为`30`秒
 ```
  /st cd 10
```
 `/st r18 <num>`, 通过指令修改r18开关, 默认为`0`,  `1`为开启, `0`为关闭, `2`为混合
 ```
  /st r18 2
```

## LLM函数调用

  支持通过自然语言，比如: `给我一份涩图` 或者 `想要两张涩图`

  需要模型支持函数调用，推荐 `gpt-4o-mini`

  关闭这个功能 `/tool off search_setu`

## 使用帮助

- 输入`/st help`查看帮助信息
- 或者通过**webui**面板配置

## 更新日志
  - 新增以合并转发形式发送
  - 新增`llm调用`
  - 新增帮助信息,输入`/st help`查看帮助信息
  - 新增对应tags获取图片
  - 新增通过指令修改cd限制, 单位秒, 默认为`30`秒
  - 新增 通过指令修改r18开关
  
## Astrbot文档

[帮助文档](https://astrbot.soulter.top/center/docs/%E5%BC%80%E5%8F%91/%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91/)
