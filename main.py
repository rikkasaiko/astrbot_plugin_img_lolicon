from astrbot.api.all import *
import aiohttp
import time
import json
from astrbot.api.message_components import Node, Plain, Image
from astrbot.api.event.filter import *

@register("setu", "rikka", "一个lolicon api的涩图插件", "2.0.3")
class SetuPlugin(Star):
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context)
        self.config = config or {}
        self.r18 = self.config.get("r18", 0)
        self.num = self.config.get("num", 1)
        self.size = self.config.get("size", "regular")
        self.cooldown_duration = self.config.get("time", 30)  # 默认冷却时间为30秒
        self.cooldowns = {}

    @command_group("st")
    def math(self):
        pass


    @math.command("help")
    async def add(self, event: AstrMessageEvent):
        """获取帮助"""
        yield event.plain_result(

            "   /st help     ⇒ 显示帮助菜单  \n"
            "   /setu          ⇒ 随机推荐涩图  \n"
            "   /setu <标签>   ⇒ 指定标签搜索  \n"
            "─────────────────────────────────\n"
            f"   当前冷却时间：{self.config['time']}秒          \n"
            f"   当前R18设置：{ {0:'关闭',1:'开启',2:'混合'}[self.config['r18']]}\n"
            f"   当前发送数量：{self.config['num']}张         \n"
            "─────────────────────────────────\n"
            "    🔒 需要管理员权限\n"
            "   /st cd <秒数>  ⇒ 调整冷却时间  \n"
            "   /st r18 <0|1|2> ⇒ 切换内容模式  \n"
            "   /st num <1-3>  ⇒ 设置请求数量   \n"
        )

        
    @permission_type(PermissionType.ADMIN)
    @math.command("cd")
    async def cd(self, event: AstrMessageEvent, cd: int):
        """设置涩图冷却时间"""
        if cd <= 0:
            yield event.plain_result("冷却时间必须为正整数")
        else:
            self.config["time"] = int(cd)  # 更新配置
            yield event.plain_result(f"冷却时间设置为: {cd}秒")
            logger.info(f"冷却时间设置为: {self.config}秒")


    @permission_type(PermissionType.ADMIN)
    @math.command("r18")
    
    async def set_r18(self, event: AstrMessageEvent, mode: int):
        """设置R18模式"""
        
        text = {0: "关闭", 1: "开启", 2: "混合"}
        if mode not in (0, 1, 2):   
            yield event.plain_result("参数错误，请输入0(关闭)或1(启用)或者2(混合)")
            return
        if mode == 2:
            yield event.plain_result(f"{f'已开启{text[mode]}模式' if self.config['r18'] != mode else '重复开启混合模式'}")
            self.config["r18"] = mode
            return
        
        yield event.plain_result(f"R18模式{f'已是{text[mode]}状态' if self.config['r18'] == mode else f'已设置为{text[mode]}'}")
        self.config["r18"] = mode



    @permission_type(PermissionType.ADMIN)
    @math.command("num")
    async def set_num(self, event: AstrMessageEvent, num: int):
        """设置单次请求图片数量"""

        if num not in (1, 2, 3):
            yield event.plain_result("参数错误，请输入1-3")
            return

        self.config["num"] = int(num)
        yield event.plain_result(f"请求数量已设置为: {num}")



    @command("setu")
    async def setu(self, event: AstrMessageEvent):
        """发送一张涩图"""
        user_id = str(event.get_sender_id())  # 获取用户ID并转为字符串
        current_time = int(time.time())

        # 检查冷却状态
        user_cooldown = self.cooldowns.get(user_id, 0)  # 获取用户的冷却时间，如果没有则默认为0

        if user_cooldown > current_time:  # 如果用户的冷却时间大于当前时间
            remaining_time = user_cooldown - current_time
            yield event.plain_result(f"涩图冷却中，请等待 {remaining_time} 秒后再试。")
            return

        # 更新用户的冷却时间
        self.cooldowns[user_id] = current_time + self.config["time"]
        print(f"用户{user_id} 剩余冷却时间: {self.cooldowns[user_id] - current_time}, 冷却持续时间: {self.config['time']}")

        # 从用户消息中获取tag（假设用户输入格式为 "setu tag1 tag2"）
        tags = event.get_message_str().split()[1:]  # 获取所有tag
        tag_param = '&tag='.join(tags)  # 将tag合并为字符串



        size = self.config["size"]
        num = self.config["num"]
        r18 = self.config["r18"]
        cd = self.config["time"]


        # 获取图片
        url = f"https://api.lolicon.app/setu/v2?r18={r18}&num={num}&size={size}&tag={tag_param}"
        ssl_context = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=ssl_context) as session:
            try:
                async with session.get(url) as response:
                    data = await response.json()

                    if data["error"]:
                        yield event.plain_result(f"\n获取图片失败：{data['error']}")
                        return

                    if not data["data"]:
                        yield event.plain_result(f"\n未获取到图片{url}")
                        return
                    

                    
                    logger.info(f"收到请求:图片质量为{size}, 数量为{num}, r18为{r18},冷却时间为{cd}")

                    for index, image_data in enumerate(data["data"][:num]):  # 新增循环
                        img_pid = image_data["pid"]
                        img_tag = image_data["tags"]
                        img_title = image_data["title"]
                        image_url = image_data["urls"][size]
                        chain = [
                            At(qq=event.get_sender_id()),
                            Plain(f"tag: {img_tag}\npid: {img_pid}\ntitle: {img_title}"),
                            Image.fromURL(image_url),
                        ]
                        yield event.chain_result(chain)
                        logger.info(f"发送第 {index+1} 张涩图: {image_url}")



            except Exception as e:
                yield event.plain_result(f"\n获取图片失败：{e}")


    @llm_tool(name="search_setu")
    async def search_setu_tool(self, event: AstrMessageEvent, num: int):
        '''根据用户希望发送涩图。当用户要求或者希望你给他1份涩图或者1张涩图,涩图一份,一份涩图时调用此工具
        Args:
            num(number): 请求数量
        '''  
        nums = int(num)
        
        size = self.config["size"]
        r18 = self.config["r18"]

        try:

            
            # 范围验证,避免过多导致卡线程
            if not (1 <= num <= 3):
                yield event.plain_result(f"请求数量 {num} 超出范围 (1-3)")
                return
            user_id = str(event.get_sender_id())  # 获取用户ID并转为字符串
            current_time = int(time.time())

            # 检查冷却状态
            user_cooldown = self.cooldowns.get(user_id, 0)  # 获取用户的冷却时间，如果没有则默认为0

            if user_cooldown > current_time:  # 如果用户的冷却时间大于当前时间
                remaining_time = user_cooldown - current_time
                yield event.plain_result(f"搜索冷却中，请等待 {remaining_time} 秒后再试。")
                return

            # 更新用户的冷却时间
            self.cooldowns[user_id] = current_time + self.config["time"]
            print(f"用户{user_id} 剩余冷却时间: {self.cooldowns[user_id] - current_time}, 冷却持续时间: {self.cooldown_duration}")

            # tag_list = [t.strip() for t in tags.split(',')]

            
            # 复用现有的图片获取逻辑 &tag={'&tag='.join(tag_list)
            url = f"https://api.lolicon.app/setu/v2?r18={r18}&num={nums}&size={size}"
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
                async with session.get(url) as response:
                    data = await response.json()
                    # 发送图片消息链
                    for index, item in enumerate(data["data"][:nums]):
                        image_url = item["urls"][self.size]
                        chain = [
                            Plain(f"标题：{item['title']}\nPID：{item['pid']}\n标签：{', '.join(item['tags'])}"),
                            Image.fromURL(image_url)
                        ]
                        yield event.chain_result(chain)
                        logger.info(f"共{nums}张涩图,正在发送第{index+1}张涩图: {image_url}")
                
                    

        except Exception as e:
            logger.error(f"工具调用失败：{str(e)}")
            yield event.plain_result("涩图搜索服务暂时不可用")
