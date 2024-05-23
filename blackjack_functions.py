# file: blackjack_functions.py
import random

def deal_card():
    """隨機發一張牌"""
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    return random.choice(cards)

def calculate_score(cards):
    """計算牌面總點數"""
    score = sum(cards)
    if score == 21 and len(cards) == 2:
        return 0  # 21點為勝利，但不是Blackjack
    if 11 in cards and score > 21:
        cards.remove(11)
        cards.append(1)
    return score

first_cards_msg = ['來給你看看我的第一張', '吾的第一張', '看好了，我的第一張']
get_cards_msg = ['來拿下一張', '領下一張', '給你下一張', '我發下一張']
forgive_cards_msg = ['pass', '結束惹，要想好餒', '不繼續，要確欸', '要決勝負惹']

async def play_blackjack(bot, message):
    print("play_blackjack function called")
    player_cards = []
    dealer_cards = []

    # 初始化發兩張牌給玩家和莊家
    for _ in range(2):
        player_cards.append(deal_card())
        dealer_cards.append(deal_card())

    player_score = calculate_score(player_cards)
    dealer_score = calculate_score(dealer_cards)
    first_message = random.choice(first_cards_msg)

    print(f"Your cards: {player_cards}, current score: {player_score}")
    await message.channel.send(f"你的牌: {player_cards}, 總共點數: {player_score}")
    await message.channel.send(f"{first_message}: {dealer_cards[0]}")

    # 玩家回合
    while player_score != 0 and player_score < 21:
        # 提示玩家輸入是否要牌
        for_continue_message = random.choice(get_cards_msg)
        for_forgive_message = random.choice(forgive_cards_msg)
    
        prompt_message = f"輸入 '繼續' {for_continue_message}, 輸入 '放棄' 就 {for_forgive_message}: "
        await message.channel.send(prompt_message)

        # 等待玩家的輸入
        def check(m):
            return m.author == message.author and m.channel == message.channel
        msg = await bot.wait_for("message", check=check)

        # 解析玩家的輸入，並根據輸入決定是否要牌
        if msg.content.lower() == "繼續":
            # 玩家要牌，發一張牌給玩家
            player_cards.append(deal_card())
            player_score = calculate_score(player_cards)
            await message.channel.send(f"你的牌: {player_cards}, 現在點數: {player_score}")
        elif msg.content.lower() == "放棄":
            # 玩家不要牌，結束玩家回合
            break
        else:
            # 如果玩家輸入了無效的指令，提示玩家重新輸入
            await message.channel.send("聽不懂人話嗎？ 輸入 '繼續' 或 '放棄'")

    # 玩家回合結束後，檢查玩家是否選擇繼續要牌
    if player_score > 21:
        await message.channel.send("笑死，你爆了")
        return
    elif player_score == 21:
        await message.channel.send("握草，居然是你 21")
    else:
        await message.channel.send("到我了，看好了")

    # 莊家回合
    while dealer_score != 0 and dealer_score < 17:
        dealer_cards.append(deal_card())
        dealer_score = calculate_score(dealer_cards)

    # 判斷莊家是否爆牌
    if dealer_score > 21:
        await message.channel.send("喔好吧")
        return

    # 判断胜负
    if player_score > dealer_score:
        await message.channel.send("好啦好啦給你贏")
    elif player_score < dealer_score:
        await message.channel.send("笑死我贏了")
    else:
        await message.channel.send("平手算你運氣好啦")

    await message.channel.send(f"回顧一下你的手牌: {player_cards}, 你的總分: {player_score}")
    await message.channel.send(f"我的全部手牌: {dealer_cards}, 我的總分: {dealer_score}")

