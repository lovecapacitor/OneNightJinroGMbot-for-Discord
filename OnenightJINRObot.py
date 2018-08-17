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
        sendmsg = 'none'
        if message.author.display_name == 'かなむら':
            num = 0 #number of members
            online=[] #online member
            for member in client.get_all_members():        
                print(member.display_name)
                print(member.status)
                if str(member.status)=='online':
                    if member.display_name != 'OneNightJinroGM':
                        num = num + 1
                        online.append(member)
            sendmsg = str(num)+'人オンライン'
            sendmsg += '\n'
            #await client.send_message(message.channel,str(num)+'人オンライン')
    #for debug
            for t in online:
                print(t.display_name)
            #add 2 N/A
            online.append('N/A')
            online.append('N/A')
            if num < 3:
                sendmsg +=  '人が少なすぎます（３～６人用です）。'
                await client.send_message(message.channel,sendmsg)
            elif num > 6:
                sendmsg +=  '人が多すぎます（３～６人用です）。'
                await client.send_message(message.channel, sendmsg)
            else :
            #assignment w:0,1 f:2 t:3 v:others
                sendmsg+='人狼2名、占い師1名、怪盗1名、村人'+str(num-2)+'名です。ランダムに２枚抜けます。'+'\n********ゲーム開始********'
                await client.send_message(message.channel,sendmsg)
                sendmsg=''
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
                            await client.send_message(online[2], 'あなたは「占い師」です。\nしばらくお待ちください')
                        elif i == 3:
                            await client.send_message(online[3], 'あなたは「怪盗」です。\nしばらくお待ちください')
                        else :
                            await client.send_message(online[i], 'あなたは「村人」です。\n夜があけるのを待ってください')
              #process of fortune teller and thief
                for i in range(2,4):
                    if online[i]!='N/A':
                        if i == 2:
                            for j in client.get_all_members():
                                if str(j.status) == 'online':
                                    if j.display_name != 'OneNightJinroGM':
                                        sendmsg+=j.display_name+'\n'
                            flag = True
                            await client.send_message(online[2], sendmsg+'誰を占いますか？（名前を入力してください）')
                            while(flag):
                                telling = await client.wait_for_message(author=online[2])
                                for k in range(0,num+2):
                                    if online[k] !='N/A':
                                        if telling.content == online[k].display_name:
                                            if k == 0 or k == 1:
                                                await client.send_message(online[2],online[k].display_name+'は「人狼」です。\n夜があけるのを待ってください')
                                            elif k == 2:
                                                await client.send_message(online[2],online[k].display_name+'は「占い師」です。\n夜があけるのを待ってください')
                                            elif k == 3:
                                                await client.send_message(online[2],online[k].display_name+'は「怪盗」です。\n夜があけるのを待ってください')
                                            else :
                                                await client.send_message(online[2],online[k].display_name+'は「村人」です。\n夜があけるのを待ってください')
                                            flag = False
                                if flag == True:
                                    await client.send_message(online[2],'入力が不正です。\n誰を占いますか？（名前を入力してください）')
                        if i == 3:
                            if sendmsg == '':
                                for j in client.get_all_members():
                                    if str(j.status) == 'online':
                                        if j.display_name != 'OneNightJinroGM':
                                            sendmsg += j.display_name+'\n'
                            flag = True
                            change = 3
                            await client.send_message(online[3],sendmsg+ '誰と入れ替わりますか？（名前を入力してください）')
                            sendmsg=''
                            while(flag):
                                telling = await client.wait_for_message(author=online[3])
                                for k in range(0,num+2):
                                    if online[k] !='N/A':
                                        if telling.content == online[k].display_name:
                                            if k == 0 or k == 1:
                                                await client.send_message(online[3],online[k].display_name+'は「人狼」でした。\n今はあなたが「人狼」です。\n夜があけるのを待ってください。')
                                                change = k
                                            elif k == 2:
                                                await client.send_message(online[3],online[k].display_name+'は「占い師」でした。\n今はあなたが「占い師」です。\n夜があけるのを待ってください。')
                                                change = k
                                            elif k == 3:
                                                await client.send_message(online[3],'あなたは交換をしませんでした。\n夜があけるのを待ってください。')
                                            else :
                                                await client.send_message(online[3],online[k].display_name+'は「村人」でした。\n今はあなたが「村人」です。\n夜があけるのを待ってください。')
                                                change = k
                                            flag = False
                                if flag == True:
                                    await client.send_message(online[3],'入力が不正です。\n誰と入れ替わりますか？（名前を入力してください）')
                            online[change],online[3]=online[3],online[change]    
                    elif online[i] == 'N/A':
                            await asyncio.sleep(30+30*random.randrange(2))
                #daytime
                await asyncio.sleep(5)
                await client.send_message(message.channel,'夜が明けました。\n議論時間は5分です。(全員の/skip で投票に移ります)')
                agreement = [0,0,0,0,0,0,0,0,0]
                skipflag = False
                for tim in range(0,5):
                    await client.send_message(message.channel,'残り'+str(5-tim)+'分です。')
                    for l in range(0,600):
                        skip = await client.wait_for_message(timeout=0.1)
                        if str(skip) != 'None':
                            if skip.content == '/skip':
                               for m in range(0,num+2):
                                   if online[m] != 'N/A' and skip.author == online[m] and agreement[m] == 0:
                                        agreement[m] = 1
                                        await client.send_message(message.channel,online[m].display_name+'がスキップに同意しました。\n現在'+str(num)+'人中'+str(sum(agreement))+'人が同意。')
                                        if sum(agreement) == num:
                                               skipflag = True
                        if skipflag:
                            break
                    if skipflag:
                        break
                await client.send_message(message.channel,'日が暮れました。投票の時間です。\nランダムな順序でDMにて投票を行います。しばらくお待ち下さい。')
                #vote
                vote=[0,0,0,0,0,0,0,0,0] #vote[from]=to
                #randomize
                temp=[]
                for i in range(0,num+2):
                    temp.append(i)
                random.shuffle(temp)
                print(temp)
                for i in range(0,num+2):
                    if online[temp[i]]!='N/A':
                        if sendmsg == '':
                            for j in client.get_all_members():
                                if str(j.status) == 'online':
                                    if j.display_name != 'OneNightJinroGM':
                                        sendmsg += j.display_name+'\n'
                        flag = True
                        await client.send_message(online[temp[i]], sendmsg+'誰に投票しますか？（名前を入力してください）')
                        while(flag):
                            telling = await client.wait_for_message(author=online[temp[i]])
                            for k in range(0,num+2):
                                if online[k] !='N/A':
                                    if telling.content == online[k].display_name:
                                        vote[temp[i]]=k
                                        await client.send_message(online[temp[i]],online[k].display_name+'に投票しました。\nしばらくお待ちください。')    
                                        flag = False
                            if flag == True:
                                await client.send_message(online[temp[i]],'入力が不正です。\n誰に投票しますか？（名前を入力してください）')
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
                sendmsg ='投票が終わりました。\n'
                if loser != 114514:
                    sendmsg += online[loser].display_name+'が処刑されました！！\n'
                else :
                    sendmsg += '誰も処刑されませんでした。\n'
                if online[0] == 'N/A' and online[1] == 'N/A':
                    if loser != 114514:
                        await client.send_message(message.channel,sendmsg+online[loser].display_name+'の勝利です！！')
                    else :
                        await client.send_message(message.channel,sendmsg+'引き分けです。')
                else :
                    if loser == 0 or loser == 1:
                        await client.send_message(message.channel,sendmsg+'「村人」陣営の勝利です！！')
                    else :
                        await client.send_message(message.channel, sendmsg+'「人狼」陣営の勝利です！！')
                sendmsg = ''
                for i in range(0,num+2):
                    if online[i] != 'N/A':
                        if i == 0 or i == 1:
                            sendmsg += online[i].display_name +'「人狼」投票先：'+online[vote[i]].display_name+'\n'
                        elif i == 2:
                            sendmsg += online[i].display_name +'「占い師」投票先：'+online[vote[i]].display_name+'\n'
                        elif i == 3:
                            sendmsg += online[i].display_name +'「怪盗」投票先：'+online[vote[i]].display_name+'\n'
                        else :
                            sendmsg += online[i].display_name +'「村人」投票先：'+online[vote[i]].display_name+'\n'
                for i in range(0,num+2):
                    if online[i] == 'N/A':
                        if i == 0 or i == 1:
                            sendmsg += '欠け「人狼」\n'
                        elif i == 2:
                            sendmsg += '欠け「占い師」\n'
                        elif i == 3:
                            sendmsg += '欠け「怪盗」\n'
                        else :
                            sendmsg += '欠け「村人」\n'
                await client.send_message(message.channel,sendmsg)
            await client.send_message(message.channel,'＊＊＊＊＊＊＊＊ゲーム終了＊＊＊＊＊＊＊＊')
#Connection and starting up
client.run('Write your token here')
