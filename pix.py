from astrbot.api.all import *
import aiohttp
from astrbot.api.event.filter import *
from astrbot.api.event import AstrMessageEvent
from astrbot.api.message_components import Node, Plain, Image
import asyncio
from astrbot.api.event import MessageChain

async def pix_plugin(self, config: json, event: AstrMessageEvent, tags: str, num: int):
    """发送一张pix涩图"""
    config = config
    url = "http://pix.zhenxun.org/pix/get_pix"
    headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config['pix_token']}",
            "Referer": "https://www.pixiv.net"
        }
    payload = {
            "tags": [tags],
            "num": num,
            "size": config["pix_size"],
            "nsfw_tag": [0, 1, 2],
            "ai": config["pix_ai"],
            "r18": config["pix_r18"],
        }
        
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, json=payload) as response:
                data = await response.json()
                code = data.get("code")
                data = data.get("data")
                if code == 200:
                    if not data:
                       return event.plain_result("没有找到符合条件的图片")
                ns = Nodes([])
                for index, pix in enumerate(data[:num]):
                    pix_url = pix["url"]
                    url = pix_url.replace("i.pximg.net", "i.pixiv.re")
                    chain = [
                        Plain(f"标题：{pix['title']}\nPID：{pix['pid']}\n标签：{pix['tags']}"),
                        Image.fromURL(url)
                    ]
                    plain = f"标题：{pix['title']}\nPID：{pix['pid']}\n标签：{pix['tags']}"
                    image = url
                    platform = event.get_platform_name()
                    num = num if num else config['pix_num']
                    
                    
                    if platform == "qq_official_webhook":
                        logger.info(f"收到qq_of请求,正在发送图片: {url}")
                        return event.chain_result(chain)
                    elif platform == "gewechat":
                        # 微信平台发送完整消息链
                        logger.info(f"共{num}张图,正在发送第{index+1}张图: {url}")
                        
                        if index < num - 1:  # 如果不是最后一个图片
                            umo = event.unified_msg_origin
                            message_chain = MessageChain().message(plain).url_image(image)
                            await self.context.send_message(event.unified_msg_origin, message_chain)
                            await asyncio.sleep(0.5)  # 添加发送间隔
                            continue
                        return event.chain_result(chain)  # 最后一个消息使用return返回
                    else:
                        node = Node(
                            uin=event.get_sender_id(),
                            name=event.get_sender_name(),
                            content=chain
                        )
                        ns.nodes.append(node)
                        logger.info(f"共{num}张图,正在发送第{index+1}张图: {url}")
                
                if platform not in ["qq_official_webhook", "gewechat"] and ns.nodes:
                    return event.chain_result([ns])

    except aiohttp.ClientError as e:
        return event.plain_result(f"😢 网络请求失败: {str(e)}")
    except ValueError as e:
        return event.plain_result(f"😢 JSON 解析失败: {str(e)}")
    except Exception as e:
        return event.plain_result(f"😢 未知错误: {str(e)}")
            
         
            
async def setu_plugin(self, event: AstrMessageEvent, tags: str, config: json):
    """发送lolicon涩图"""
    config = config
    size = config["size"]
    num = config["num"]
    r18 = config["r18"]
    cd = config["time"]
        # 获取图片
    url = f"https://api.lolicon.app/setu/v2?r18={r18}&num={num}&size={size}&tag={tags}"
    ssl_context = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=ssl_context) as session:
        try:
            async with session.get(url) as response:
                data = await response.json()

                if data["error"]:
                    return event.plain_result(f"\n获取图片失败：{data['error']}")
                    
                if not data["data"]:
                    return event.plain_result(f"\n未获取到图片{url}")
                                       
                logger.info(f"收到请求:图片质量为{size}, 数量为{num}, r18为{r18},冷却时间为{cd}")
                    
                ns = Nodes([])
                for index, image_data in enumerate(data["data"][:num]):  # 新增循环
                    img_pid = image_data["pid"]
                    img_tag = image_data["tags"]
                    img_title = image_data["title"]
                    image_url = image_data["urls"][size]
                    
                    chain = [
                        Plain(f"标题：{img_title}\nPID：{img_pid}\n标签：{', '.join(img_tag)}"),
                        Image.fromURL(image_url)
                    ]
                    plain = f"标题：{img_title}\nPID：{img_pid}\n标签：{', '.join(img_tag)}"
                    image = image_url
                    if event.get_platform_name() == "qq_official_webhook":
                        logger.info(f"收到qq_of请求,正在发送涩图: {image_url}")
                        return event.chain_result(chain)
                    
                    elif event.get_platform_name() == "gewechat":
                        logger.info(f"共{num}张涩图,正在发送第 {index+1} 张涩图: {image_url}")
                        if index < num - 1:  # 如果不是最后一个图片
                            umo = event.unified_msg_origin
                            message_chain = MessageChain().message(plain).url_image(image) #储存消息链
                            await self.context.send_message(event.unified_msg_origin, message_chain)
                            await asyncio.sleep(0.5)  # 添加发送间隔
                            continue
                        return event.chain_result(chain) 
                    else:     
                        node = Node(
                            uin=event.get_sender_id(),
                            name=event.get_sender_name(),
                            content=chain
                        )
                        ns.nodes.append(node)
                        logger.info(f"共{num}张涩图,正在发送第 {index+1} 张涩图: {image_url}")  
                if event.get_platform_name not in ["qq_official_webhook", "gewechat"] and ns.nodes:
                    return event.chain_result([ns])
                
        except Exception as e:
            return event.plain_result(f"\n获取图片失败：{e}")
