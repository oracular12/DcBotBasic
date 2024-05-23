import discord
import json
from discord.ext import commands
import random

from blackjack_functions import deal_card, calculate_score, play_blackjack

# 讀取 config.json 中的 token
with open('config.json') as f:
    config = json.load(f)
token = config['token']

# 初始化bot
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# 指定訊息列表
fortune_messages = ['不告訴你' , '不想講' , '哇靠大吉', '哎唷，大吉','吉，夠簡短吧','吉，很不錯欸', '中吉，還行', '中吉，不是錯覺吧', '小吉，只好嘎掉了', '末吉，好喔', '末吉喔喔喔', '乾杯！末小吉！', '末小吉！恭喜恭喜', '怕爛凶','靠笑死凶', '小凶！讓你長長記性！', '小凶，白了','半凶笑死', '沒關係啦，半凶', '末凶！只好ㄒㄧㄠ……安慰你了', '怎麼那麼可憐，末凶', '大凶，你好自為之', '大凶，然後最近超多智障']
mora_messages = ['剪刀', '石頭', '布']

# 定义扑克牌
poker_suits = ['♠️', '♥️', '♦️', '♣️']
poker_ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
# 否定字串
negation_words = ['不', '嗎', '？', '?']


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


async def autosend_stickers(channel, sticker_ids):
    try:
        guild = channel.guild
        stickers = [await guild.fetch_sticker(sticker_id) for sticker_id in sticker_ids]
        await channel.send(stickers=stickers)
    except discord.errors.DiscordServerError as e:
        print(f"Failed to fetch sticker: {e}")

async def send_stickers(message, sticker_ids):
    try:
        guild = message.guild
        stickers = [await guild.fetch_sticker(sticker_id) for sticker_id in sticker_ids]
        await message.channel.send(stickers=stickers)
    except discord.errors.DiscordServerError as e:
        print(f"Failed to fetch sticker: {e}")

@bot.event
async def on_guild_channel_update(before, after):
    # 檢查頻道權限覆蓋是否有變化
    if before.overwrites != after.overwrites:
        # 獲取 Bot 的權限覆蓋對象 (可能是新增或修改)
        overwrite = next((ow for ow in after.overwrites if isinstance(ow, discord.PermissionOverwrite) and ow.is_owner(bot.user)), None)
        
        # 如果 Bot 被新增到該頻道
        if overwrite is None:
            overwrite_before = next((ow for ow in before.overwrites if isinstance(ow, discord.PermissionOverwrite) and ow.is_owner(bot.user)), None)
            if overwrite_before is None and isinstance(after, discord.TextChannel):
                sticker_ids = [1243206026208088165]
                await autosend_stickers(after, sticker_ids)

@bot.event
async def on_member_join(member):
    # 當新成員加入時發送貼圖
    await send_stickers(member, [1243206026208088165])

@bot.event
async def on_message(message):
    # 忽略bot自己的消息，防止自我回复
    if message.author == bot.user:
        return
    # # # 检查消息是否包含贴图
    # if message.stickers:
    #     for sticker in message.stickers:
    #         await message.channel.send(f'Sticker ID: {sticker.id}, Sticker Name: {sticker.name}')
    if (message.content.lower() == 'hi' or message.content.lower() == '嗨') and message.author.id != 1112074895984185375:
        await message.channel.send('嗨老人')
    elif (message.content.lower() == '……' or message.content.lower() == '咕' or message.content.lower() == '腳毛獎') and message.author.id != 1112074895984185375:
        await message.channel.send('笑死')
    elif '他' in message.content.lower() and any(phrase in message.content.lower() for phrase in ['難道不', '能不能', '可不可']) and message.author.id != 1112074895984185375:
        await message.channel.send('他沒辦法')

    elif '早' in message.content.lower() and ('安' in message.content.lower() or '上好' in message.content.lower()):
        await message.channel.send(f'時候不早了')
    elif message.content.lower() == '恭喜恭喜':
        await message.channel.send('恭喜恭喜')

    elif '寫' in message.content.lower() and '完' in message.content.lower() and \
        not any(word in message.content.lower() for word in negation_words):
        await send_stickers(message, [1243207349343223870])
    elif '寫' in message.content.lower() and '完' in message.content.lower() and any(word in message.content.lower() for word in negation_words):
        await message.channel.send(f'寫完了')
    elif '危' in message.content.lower() and ('高雄' in message.content.lower() or '台北' in message.content.lower() or '台南' in message.content.lower() or '基隆' in message.content.lower() or '開車' in message.content.lower() or '路上' in message.content.lower()):
        await message.channel.send('地球太危險了')
    elif '醒了' in message.content.lower():
        await message.channel.send('乖，該睡了')







    elif message.mentions and bot.user in message.mentions and '晚安' in message.content.lower():
        await message.channel.send(f'{message.author.mention} 祝好夢！')
    elif message.mentions and bot.user in message.mentions and '戰否' in message.content.lower():
        await message.channel.send(f'{message.author.mention} 不要')

    elif message.mentions and bot.user in message.mentions and "功能" in message.content.lower():
        await message.channel.send(
            f"```@我後：\n"
            f"運勢輸入：'運勢'\n"
            f"猜拳輸入：'猜拳', '剪刀石頭布'\n"
            f"梭哈輸入：'梭哈', '沙蟹', '曬冷', '話事啤', 'stud'\n"
            f"玩21點輸入：'21點'\n"
            f"抽撲克牌輸入：'抽牌', '比大小'```"
        )


    # 隨機選擇一個訊息
    elif message.mentions and bot.user in message.mentions and '運勢' in message.content.lower():
        selected_message = random.choice(fortune_messages)
        await message.channel.send(f'>>> {message.author.mention} {selected_message}')
    elif message.mentions and bot.user in message.mentions and \
       ('猜拳' in message.content.lower() or '剪刀石頭布' in message.content.lower()):
        selected_message = random.choice(mora_messages)
        await message.channel.send(f'{message.author.mention} ||{selected_message}||')
     # 如果消息内容是 'Stud'
    elif (message.mentions and bot.user in message.mentions) and \
       any(phrase in message.content.lower() for phrase in ['梭哈', '沙蟹', '曬冷', '話事啤', 'stud']):
        hand = random.sample([f'{suit}{rank}' for suit in poker_suits for rank in poker_ranks], 5)
        formatted_hand = ' '.join(hand)
        await message.channel.send(f'```{formatted_hand}```')
    elif (message.mentions and bot.user in message.mentions) and \
       any(phrase in message.content.lower() for phrase in ['抽牌', '比大小']):
        hand = random.sample([f'{suit}{rank}' for suit in poker_suits for rank in poker_ranks], 1)
        formatted_hand = ' '.join(hand)
        await message.channel.send(f'```{formatted_hand}```')


    elif message.mentions and bot.user in message.mentions and '21點' in message.content.lower():
        # 21點
        await play_blackjack(bot, message)




    elif message.mentions and bot.user in message.mentions :
        await send_stickers(message, [1243206026208088165])


    # 确保所有消息都通过 bot.process_commands
    await bot.process_commands(message)


# 使用你的Bot Token
bot.run(token)
