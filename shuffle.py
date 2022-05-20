import random
import tkinter
from tkinter import *
from tkinter import ttk
import copy
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np

shufflemode = ['hindu', 'faro', 'deal']

def main():
    global deck,deck_b
    logreset()
    deck=[]
    deck_b=[]
    deck=readdeck(deck)
    deck_b=copy.deepcopy(deck)
    
    paint()

def update_list():#UIのうち、随時更新が必要なものがここの中、更新がOK押すたびなのでshufflleと合体させてもよさそう
    vl1=StringVar(value=list(i[0] for i in deck_b))
    lb1 = Listbox(
        frame1, listvariable=vl1,
        selectmode='multiple',height=len(deck))
    lb1.grid(row=1, column=0)
    
    vl2=StringVar(value=list(i[0] for i in deck))
    lb2 = Listbox(
        frame1, listvariable=vl2, 
        selectmode='multiple',height=len(deck))
    lb2.grid(row=1, column=1)
    
    for i in range(len(deck)):
        lb1.itemconfig(i, background=deck_b[i][2])
        lb2.itemconfig(i, background=deck[i][2])
    
    root.after(100,update_list)
    
def paint():#UI周り
    global frame1,frame2,frame3,frame4,root,num
    root=tkinter.Tk()
    root.title(u"shuffle")
    frame1 = ttk.Frame(root, padding=16)
    frame1.grid(row=1,column=0)
    deck_label=ttk.Label(frame1,text='シャッフル前',padding=(5, 2))
    deck_label.grid(row=0,column=0)
    deck_b_label=ttk.Label(frame1,text='シャッフル後',padding=(5, 2))
    deck_b_label.grid(row=0,column=1)
    
    frame2 = ttk.Frame(root, padding=16)
    frame2.grid(row=0,column=0)
    
    cbv = StringVar()
    cb = ttk.Combobox(
        frame2, textvariable=cbv, 
        values=shufflemode, width=10)
    cb.set(shufflemode[0])

    num=StringVar()
    num_entry=ttk.Entry(frame2,textvariable=num)
    num_entry.grid(row=1,column=1)
    num_entry.insert(0,2)
    shuffle_label=ttk.Label(frame2,text='シャッフルの方法',padding=(5, 2))
    num_label=ttk.Label(frame2,text='数指定',padding=(5, 2))#ディールシャッフルの束の数指定
    button1 = ttk.Button(
        frame2, text='OK', 
        command=lambda: shuffle(cbv.get(),int(num.get())))
    cb.grid(row=1, column=0)
    num_label.grid(row=0,column=1)
    button1.grid(row=1, column=2)
    shuffle_label.grid(row=0,column=0)

    frame3= ttk.Frame(root, padding=16)
    frame3.grid(row=1,column=1)
    dis_label=ttk.Label(frame3,text='カードの移動距離の散布図')
    move_label=ttk.Label(frame3,text='カードの移動を示した折れ線グラフ')
    dis_label.grid(row=0,column=2)
    move_label.grid(row=2,column=2)
    frame4 = ttk.Frame(root, padding=16)
    frame4.grid(row=1,column=2)
    log_label=ttk.Label(frame4,text='シャッフルの記録')
    log_label.grid(row=0,column=0)

    frame5 = ttk.Frame(root, padding=16)
    frame5.grid(row=0,column=1)
    
    update_list()
    root.mainloop()

def movedisfigure(deck):#移動距離のグラフ描画
    x = np.array([])
    y = np.array([])
    for i in deck:      
        y=np.append(y,abs(i[1][-1]-i[1][0]))
        x=np.append(x,abs(i[1][0]))
    fig = Figure()   
    ax = fig.add_subplot(1, 1, 1)           
    ax.scatter(x, y)
    canvas = FigureCanvasTkAgg(fig, frame3)
    canvas.get_tk_widget().grid(row=1,column=2)

def moverecfigure(deck):#移動記録のグラフ描画
    fig = Figure()   
    ax = fig.add_subplot(1, 1, 1)  
    for i in deck:
        x = np.array([])
        y = np.array([])
        tmp=0
        for j in i[1]:
            y=np.append(y,j)
            x=np.append(x,tmp)
            tmp+=1
        line, =ax.plot(x, y)
    ax.invert_yaxis()
    canvas1 = FigureCanvasTkAgg(fig, frame3)
    canvas1.get_tk_widget().grid(row=3,column=2)

def shuffle(v,num):#シャッフルの判別
    global deck_b,deck
    deck_b=copy.deepcopy(deck)
    
    if v==shufflemode[0]:
        deck=randomhindu(deck,num)
    if v==shufflemode[1]:
        deck=randomfaro(deck,num)
    if v==shufflemode[2]:
        deck=deal(deck,num)    
    n=0
    for i in deck:
        n+=1
        i[1].append(n)
    writelog(v,num)
    movedisfigure(deck)
    moverecfigure(deck)
    printlog()
        
def writelog(text,num):#ログの書き込み
    f=open('shufflelog.txt','a',encoding='utf-8')
    f.write(text+':'+str(num)+'\n')
    f.close()

def printlog():#ログの出力
    f=open('shufflelog.txt','r',encoding='utf-8')
    l='log:'
    for i in f:
        l+=i+'→'
    print(l)
    log=ttk.Label(frame4,text=l,padding=(5, 2))
    log.grid(row=2,column=0)
    f.close()

def logreset():#ログのリセット
    f=open('shufflelog.txt','w',encoding='utf-8')
    f.close()

def deal(deck,n):#デッキを何枚の束に分けるかを指定
    t=0
    decknum=len(deck)
    ex_n=int(decknum/n)+1
    dealstack=[[] for i in range(n)]
    for i in range(decknum):
        dealstack[t].append(deck[i])
        t=(t+1)
        if t==n:
            t=0
    deck=[]
    for j in range(len(dealstack)):
        for k in reversed(dealstack[j]):
            deck.append(k)
    
    return deck

def hindu(deck,n):#デッキの配列と上から何枚つかむかを指定
    hindu=[]
    for i in range(n):
        hindu.append(deck[i])
    del deck[:n]
    print(deck)
    for i in hindu:
        deck.append(i)
    print(deck)
    return deck

def faro(deck,n,t):#デッキを二つに分ける際の片方の山の状態を指定,ｔは何番目から差し込むかを指定
    faro=[[] for i in range(2)]
    decknum=len(deck)
    for i in range(n):
        if(deck[i]!=[]):
            faro[0].append(deck[i])
    del deck[:n]
    faro[1]=deck
    deck=[]
    
    for i in range(decknum):
        if(i<t and faro[0]!=[] ):
            deck.append(faro[0].pop(0))
        elif(faro[i%2]!=[]):
            deck.append(faro[i%2].pop(0))
        elif(faro[(i+1)%2]!=[]):
            deck.append(faro[(i+1)%2].pop(0))
        else:
            break
    
    return deck

def readdeck(deck):#デッキリストの読み込み
    f1=open('deck.txt',mode='r',encoding="utf_8")
    num=0
    while True:
        num+=1
        card=f1.readline().replace('\n','')
        if card:
            deck.append([card,[num],'gray'+str(97-num)])
        else:
            f1.close()
            break
    
    return deck  

def randomfaro(deck,n):#nはシャッフルする回数
    t=int(len(deck)/2)
    l=list(range(t-10,t+10))
    for i in range(n):
        tr=random.choice(l)
        deck=faro(deck,tr,random.choice(list(range(1,t))))
    return deck

def randomhindu(deck,n):#nはシャッフルする回数
    t=int(len(deck)/2)
    l=list(range(1,t))
    for i in range(n):        
        deck=hindu(deck,random.choice(l))
    return deck
    
if __name__ == '__main__':
    main()





