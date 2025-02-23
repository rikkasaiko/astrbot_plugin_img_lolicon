# 使用lolicon api获取涩图

- api文档 <https://api.lolicon.app/>

## 指令

 `/setu st` 获取随机图片
    ```
  /setu st
    ```
 `/setu st <tag>`  **or** `/setu st <tag> <tag>` 获取对应tags图片
    ```
  /setu st 萝莉
  /setu st 少女 白丝
    ```
 `/setu cd <num>`, 通过指令修改cd限制, 单位秒, 默认为`30`秒
    ```
  /setu cd 10
    ```
 `/setu r18 <num>`, 通过指令修改r18开关, 默认为`0`,  `1`为开启, `0`为关闭, `2`为混合
    ```
  /setu r18 2
    ```

## LLM函数调用

  默认支持通过自然语言搜歌，比如: `给我1份少女涩图` 或者 `给我1份少女,白丝涩图`

  需要模型支持函数调用，推荐 `gpt-4o-mini`

  关闭这个功能 `/tool off search_setu`

## 使用帮助

- 输入`/setu help`查看帮助信息
- 或者通过**webui**面板配置

## 更新日志

- **2025/02/24**
  - 新增`llm调用`
  - 新增帮助信息,输入`/setu help`查看
  - 新增`/setu st` 获取随机图片
  - 新增`/setu st <萝莉>`  **or** `/setu st <萝莉> <白丝>` 获取对应tags图片
  - 新增`/setu cd <10>`, 通过指令修改cd限制, 单位秒, 默认为`30`秒
  - 新增`/setu r18 <1>`, 通过指令修改r18开关
  
## Astrbot文档

[帮助文档](https://astrbot.soulter.top/center/docs/%E5%BC%80%E5%8F%91/%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91/)