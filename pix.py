from astrbot.api.all import *
import aiohttp
from astrbot.api.event.filter import *
from astrbot.api.event import AstrMessageEvent
from astrbot.api.message_components import Node, Plain, Image
import asyncio

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
            "tags": [标签],
            "num": num,
            "size": config["pix_size"],
            "nsfw_tag": [0, 1, 2],
            "ai": config["pix_ai"],
            "r18": config["pix_r18"],
        }
    ns = Nodes([])
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, json=payload) as response:
                data = await response.json()
                code = data.get("code")
                data = data.get("data")
                if code == 200:
                    if not data:
                        return event.plain_result("没有找到符合条件的图片")
                        
                for index, pix in enumerate(data[:num]):
                    pix_url = pix["url"]
                    url = pix_url.replace("i.pximg.net", "i.pixiv.re")
                        
                    chain = [
                            Plain(f"标题：{pix['title']}\nPID：{pix['pid']}\n标签：{pix['tags']}"),
                            Image.fromURL(url)
                            ]
                    node = Node(
                            uin=event.get_sender_id(),
                            name=event.get_sender_name(),
                            content=chain
                        )
                    ns.nodes.append(node)
                    logger.info(f"共{config['pix_num']}张涩图,正在发送第{index+1}张涩图: {url}")
                                
                return event.chain_result([ns])
            
    except aiohttp.ClientError as e:
        return event.plain_result(f"😢 网络请求失败: {str(e)}")
    except ValueError as e:
        return event.plain_result(f"😢 JSON 解析失败: {str(e)}")
    except Exception as e:
        return event.plain_result(f"😢 未知错误: {str(e)}")
