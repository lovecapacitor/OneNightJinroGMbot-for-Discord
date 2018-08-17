import discord
import asyncio
import random
from time import sleep

client = discord.Client()

#start up
@client.event
async def on_ready():
    print('Connected')

@client.event
async def on_message(message):
    if message.content.startswith('/jinro'):
        num = 0 #number of members
        online=[] #online member
        for member in client.get_all_members():        
            print(member.display_name)
            print(member.status)
            if str(member.status)=='online':
                if member.display_name != 'OneNightJinroGM':
                    num = num + 1
                    online.append(member)
        await client.send_message(message.channel,str(num)+'人オンライン')
        #add 2 N/A
        online.append('N/A')
        online.append('N/A')
        if num < 3:
            await client.send_message(message.channel, '人が少なすぎます（３～６人用です）。')
        elif num > 6:
            await client.send_message(message.channel, '人が多すぎます（３～６人用です）')
        else :
        #assignment w:0,1 f:2 t:3 v:others
            await client.send_message(message.channel,'人狼2名、占い師1名、怪盗1名、村人'+str(num-2)+'名です。ランダムに２枚抜けます。')
            await client.send_message(message.channel,'********ゲーム開始********')
            random.shuffle(online)
            for i in range(0,num+2):
                if online[i]!='N/A':
                    if i == 0:
                        await client.send_message(online[0], 'あなたは「人狼」です。')
                        if online[1]!='N/A':
                            await client.send_message(online[0], '人狼仲間は'+online[1].display_name+'です。')
                        else :
                            await client.send_message(online[0], '仲間はいません。')
                        await client.send_message(online[0], '夜があけるのを待ってください。')
                    elif i == 1:
                        await client.send_message(online[1], 'あなたは「人狼」です。')
                        if online[0]!='N/A':
                            await client.send_message(online[1], '人狼仲間は'+online[0].display_name+'です。')

                        else :
                            await client.send_message(online[1], '仲間はいません')
                        await client.send_message(online[1], '夜があけるのを待ってください。')
                    elif i == 2:
                        await client.send_message(online[2], 'あなたは「占い師」です。')
                        await client.send_message(online[2], 'しばらくお待ちください')
                    elif i == 3:
                        await client.send_message(online[3], 'あなたは「怪盗」です。')
                        await client.send_message(online[3], 'しばらくお待ち下さい')
                    else :
                        await client.send_message(online[i], 'あなたは「村人」です。')
                        await client.send_message(online[i], '夜があけるのを待ってください')
          #process of fortune teller and thief
            for i in range(2,4):
                if online[i]!='N/A':
                    if i == 2:
                        for j in client.get_all_members():
                            if str(j.status) == 'online':
                                if j.display_name != 'OneNightJinroGM':
                                    await client.send_message(online[2],j.display_name)
                        flag = True
                        await client.send_message(online[2], '誰を占いますか？（名前を入力してください）')
                        while(flag):
                            telling = await client.wait_for_message(author=online[2])
                            for k in range(0,num+2):
                                if online[k] !='N/A':
                                    if telling.content == online[k].display_name:
                                        if k == 0 or k == 1:
                                            await client.send_message(online[2],online[k].display_name+'は「人狼」です。')
                                        elif k == 2:
                                            await client.send_message(online[2],online[k].display_name+'は「占い師」です。')
                                        elif k == 3:
                                            await client.send_message(online[2],online[k].display_name+'は「怪盗」です。')
                                        else :
                                            await client.send_message(online[2],online[k].display_name+'は「村人」です。')
                                        await client.send_message(online[2],'夜があけるのを待ってください。')
                                        flag = False
                            if flag == True:
                                await client.send_message(online[2],'入力が不正です。')
                                await client.send_message(online[2],'誰を占いますか？（名前を入力してください）')
                    if i == 3:
                        for j in client.get_all_members():
                            if str(j.status) == 'online':
                                if j.display_name != 'OneNightJinroGM':
                                    await client.send_message(online[3],j.display_name)
                        flag = True
                        change = 3
                        await client.send_message(online[3], '誰と入れ替わりますか？（名前を入力してください）')
                        while(flag):
                            telling = await client.wait_for_message(author=online[3])
                            for k in range(0,num+2):
                                if online[k] !='N/A':
                                    if telling.content == online[k].display_name:
                                        if k == 0 or k == 1:
                                            await client.send_message(online[3],online[k].display_name+'は「人狼」でした。')
                                            await client.send_message(online[3],'今はあなたが「人狼」です。')
                                            await client.send_message(online[3],'夜があけるのを待ってください。')
                                            change = k
                                        elif k == 2:
                                            await client.send_message(online[3],online[k].display_name+'は「占い師」でした。')
                                            await client.send_message(online[3],'今はあなたが「占い師」です。')
                                            await client.send_message(online[3],'夜があけるのを待ってください。')
                                            change = k
                                        elif k == 3:
                                            await client.send_message(online[3],'あなたは交換をしませんでした。')
                                            await client.send_message(online[3],'夜があけるのを待ってください。')
                                        else :
                                            await client.send_message(online[3],online[k].display_name+'は「村人」でした。')
                                            await client.send_message(online[3],'今はあなたが「村人」です。')
                                            await client.send_message(online[3],'夜があけるのを待ってください。')
                                            change = k
                                        flag = False
                            if flag == True:
                                await client.send_message(online[3],'入力が不正です。')
                                await client.send_message(online[3],'誰と入れ替わりますか？（名前を入力してください）')
                        online[change],online[3]=online[3],online[change]    
                elif online[i] == 'N/A':
                        await asyncio.sleep(30+30*random.randrange(2))
            #daytime
            await asyncio.sleep(5)
            await client.send_message(message.channel,'夜が明けました。')
            await client.send_message(message.channel,'議論時間は5分です。')
            for tim in range(0,5):
                await client.send_message(message.channel,'残り'+str(5-tim)+'分です。')
                await asyncio.sleep(60)
            await client.send_message(message.channel,'日が暮れました。投票の時間です。')
            #vote
            vote=[0,0,0,0,0,0,0,0,0] #vote[from]=to
            await client.send_message(message.channel,'ランダムな順序でDMにて投票を行います。しばらくお待ち下さい。')
            #randomize
            temp=[]
            for i in range(0,num+2):
                temp.append(i)
            random.shuffle(temp)
            print(temp)
            for i in range(0,num+2):
                if online[temp[i]]!='N/A':
                    for j in client.get_all_members():
                        if str(j.status) == 'online':
                            if j.display_name != 'OneNightJinroGM':
                                await client.send_message(online[temp[i]],j.display_name)
                    flag = True
                    await client.send_message(online[temp[i]], '誰に投票しますか？（名前を入力してください）')
                    while(flag):
                        telling = await client.wait_for_message(author=online[temp[i]])
                        for k in range(0,num+2):
                            if online[k] !='N/A':
                                if telling.content == online[k].display_name:
                                    vote[temp[i]]=k
                                    await client.send_message(online[temp[i]],online[k].display_name+'に投票しました。')    
                                    await client.send_message(online[temp[i]],'しばらくお待ちください。')
                                    flag = False
                        if flag == True:
                            await client.send_message(online[temp[i]],'入力が不正です。')
                            await client.send_message(online[temp[i]],'誰に投票しますか？（名前を入力してください）')
            point=[0,0,0,0,0,0,0,0,0]
            for i in range(0,num+2):
                if online[i]!='N/A':
                    point[vote[i]]=point[vote[i]]+1
            maximum = max(point)
            print(maximum)
            nummax = 0
            loser = 0
            winner = 'none'
            for i in point:
                if i == maximum:
                    nummax = nummax+1
            if nummax == 1:
                for i in range(0,num+2):
                    if point[i] == maximum:
                        loser = i
            else :
                loser = 114514
            await client.send_message(message.channel,'投票が終わりました。')
            if loser != 114514:
                await client.send_message(message.channel,online[loser].display_name+'が処刑されました！！')
            else :
                await client.send_message(message.channel,'誰も処刑されませんでした。')
            if online[0] == 'N/A' and online[1] == 'N/A':
                if loser != 114514:
                    await client.send_message(message.channel,online[loser].display_name+'の勝利です！！')
                else :
                    await client.send_message(message.channel,'引き分けです。')
            else :
                if loser == 0 or loser == 1:
                    await client.send_message(message.channel,'「村人」陣営の勝利です！！')
                else :
                    await client.send_message(message.channel, '「人狼」陣営の勝利です！！')
            for i in range(0,num+2):
                if online[i] != 'N/A':
                    if i == 0 or i == 1:
                        await client.send_message(message.channel,online[i].display_name +'「人狼」投票先：'+online[vote[i]].display_name)
                    elif i == 2:
                        await client.send_message(message.channel,online[i].display_name +'「占い師」投票先：'+online[vote[i]].display_name)
                    elif i == 3:
                        await client.send_message(message.channel,online[i].display_name +'「怪盗」投票先：'+online[vote[i]].display_name)
                    else :
                        await client.send_message(message.channel,online[i].display_name +'「村人」投票先：'+online[vote[i]].display_name)
            for i in range(0,num+2):
                if online[i] == 'N/A':
                    if i == 0 or i == 1:
                        await client.send_message(message.channel,'欠け「人狼」')
                    elif i == 2:
                        await client.send_message(message.channel,'欠け「占い師」')
                    elif i == 3:
                        await client.send_message(message.channel,'欠け「怪盗」')
                    else :
                        await client.send_message(message.channel,'欠け「村人」')
        await client.send_message(message.channel,'＊＊＊＊＊＊＊＊ゲーム終了＊＊＊＊＊＊＊＊')
#Connection and starting up
client.run('Write your token here.')
