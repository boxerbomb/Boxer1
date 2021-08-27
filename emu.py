import pygame

print("DO AN OVERHAUL OF THE MEM SYSTEM ITS A JOKE")
SINGLE=False
CLOCKRATE=0.000001 #ms
oldtime=pygame.time.get_ticks()

SCREENSIZE=36

pygame.init()
screen = pygame.display.set_mode((700, 500))

halt = False

deltaFrame=0
UPDATERATE=10

REGA="10101010" #0000 
REGB="00000000" #0001
REGC="00000000" #0010
REGD="00000000" #0011 --This is really a four bit register with 4 leading zeroes
REGH="00000000" #0100
REGL="00000000" #0101
ALUO="00000000" #0111
KEYB="00000000" #1000
REGI="00000000" #1001

#register but not through copy. only through memory write FD
ALUF="00000000" # 0xFD
#IF ALUF="00000000" - Addition Flag if Equal
#IF ALUF="00000001" - Sub Flag if zero/equal
#IF ALUF="00000010" - 

JUMPFLAG=0


PC="0000000100000000"
MAR="0000000000000000"

IR="000000000000"

BUS="0000000000000000"

QRAM=[]
#Upper Limit 00 FF
for i in range(0,255):
    QRAM.append("00000000")
ROM=[]
# Upper Limit 3E FF
for i in range(256,16127):
    ROM.append("000000000000")
RAM=[]
# Upper Limit BF FF
for i in range(16127,49151):
    RAM.append("000000000000")
filepath = 'rom.txt'

with open(filepath) as fp:
   romLines = fp.readlines()

i=0
for item in romLines:
    ROM[i]=item
    i=i+1

def bintoDec(num):
    return int(num,2)

def dectoBin(num,width):
    return format(num,'0'+str(width)+'b')

def readMem(addStr,bit12=False):
    global ROM,RAM,QRAM
    addInt=bintoDec(addStr)
    line=""
    if addInt<pow(2,8)-1:
        line=QRAM[addInt]
    elif addInt<pow(2,14):
        #[4:13] is for when a register tries to read from ROM. it doesnt need the data 
        if bit12==True:
            line=ROM[addInt-pow(2,8)]
        else:
            line=ROM[addInt-pow(2,8)][4:13]
    elif addInt<pow(2,16):
        line=RAM[addInt-pow(2,14)-1]

        #12-bits when reading from ROM and 8-bits when Reading from RAM
        #this doesn't seem like it will be an issue though
    if bit12==False:
        line=to8bit(line)
    return line

def ALUSettings(data):
    global ALUF
    ALUF=data
def writeMem(addStr,data):
    global QRAM,ROM,RAM
    addInt=bintoDec(addStr)

    if addInt<pow(2,8)-3:
        QRAM[addInt]=data[4:]
    elif addInt==pow(2,8)-1:
        writeTerm(data[4:])
    # This is the address that goes to newLine FE
    elif addInt==pow(2,8)-2:
        newTermLine()
    elif addInt==pow(2,8)-3:
        ALUSettings(data[4:])
    elif addInt<pow(2,14):
        ROM[addInt-pow(2,8)]=data
    elif addInt<pow(2,16):
        RAM[addInt-pow(2,14)-1]=data


#Term data is meant to be handled by the arduino not the cpu
termData = [[' ' for i in range(64)] for j in range(64)]
termX=0
termY=0

#Having issues with losing a bit when writing and storing to RAM
def to8bit(anybitstr):
    return dectoBin(bintoDec(anybitstr),8)

    

def writeTerm(data):
    global termX
    global termY
    dataInt=bintoDec(data)
    line="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ+-*/=:_<"
    termData[termX][termY]=line[dataInt]
    termX=termX+1
    if termX>=SCREENSIZE:
        termX=1
        termY=termY+1
        if termY>=SCREENSIZE:
            termY=0
            termX=0
def newTermLine():
    global termX
    global termY
    termX=0
    termY=termY+1



black=(0,0,0)
white=(255,255,255)
font = pygame.font.Font('font.ttf', 30) 

screen.fill(white)
REGAtext = font.render("A:"+hex(int(REGA, 2)), False, black)
REGBtext = font.render("B:"+hex(int(REGB, 2)), False, black)
REGCtext = font.render("C:"+hex(int(REGC, 2)), False, black)
REGDtext = font.render("D:"+hex(int(REGD, 2)), False, black)
REGHtext = font.render("H:"+hex(int(REGH, 2)), False, black)
REGLtext = font.render("L:"+hex(int(REGL, 2)), False, black)
ALUFtext = font.render("ALF:"+hex(int(ALUF, 2)), False, black)
ALUOtext = font.render("ALO:"+hex(int(ALUO, 2)), False, black)
KEYBtext = font.render("Key:"+hex(int(KEYB, 2)), False, black)
REGItext = font.render("R_I:"+hex(int(REGI, 2)), False, black)

PCtext = font.render("PC:"+hex(int(PC, 2)), False, black)
IRtext = font.render("IR:"+hex(int(IR, 2)), False, black)


print("Machine Start")
clicked=False
while not halt:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        halt = True

        # Refresh Screen and detect the keyboard pressed this clock
        # FF is a no keys pressed
        clock=False

        screen.fill(white)
        KEYB="11111111"
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_0]: KEYB="00000000"
        if pressed[pygame.K_1]: KEYB="00000001"
        if pressed[pygame.K_2]: KEYB="00000010"
        if pressed[pygame.K_3]: KEYB="00000011"
        if pressed[pygame.K_4]: KEYB="00000100"
        if pressed[pygame.K_5]: KEYB="00000101"
        if pressed[pygame.K_6]: KEYB="00000110"
        if pressed[pygame.K_7]: KEYB="00000111"
        if pressed[pygame.K_8]: KEYB="00001000"
        if pressed[pygame.K_9]: KEYB="00001001"
        if pressed[pygame.K_a]: KEYB="00001010"
        if pressed[pygame.K_b]: KEYB="00001011"
        if pressed[pygame.K_c]: KEYB="00001100"
        if pressed[pygame.K_d]: KEYB="00001101"
        if pressed[pygame.K_e]: KEYB="00001110"
        if pressed[pygame.K_f]: KEYB="00001111"
        if pressed[pygame.K_g]: KEYB="00010000"
        if pressed[pygame.K_h]: KEYB="00010001"
        if pressed[pygame.K_i]: KEYB="00010010"
        if pressed[pygame.K_j]: KEYB="00010011"
        if pressed[pygame.K_k]: KEYB="00010100"
        if pressed[pygame.K_l]: KEYB="00010101"
        if pressed[pygame.K_m]: KEYB="00010110"
        if pressed[pygame.K_n]: KEYB="00010111"
        if pressed[pygame.K_o]: KEYB="00011000"
        if pressed[pygame.K_p]: KEYB="00011001"
        if pressed[pygame.K_q]: KEYB="00011010"
        if pressed[pygame.K_r]: KEYB="00011011"
        if pressed[pygame.K_s]: KEYB="00011100"
        if pressed[pygame.K_t]: KEYB="00011101"
        if pressed[pygame.K_u]: KEYB="00011110"
        if pressed[pygame.K_v]: KEYB="00011111"
        if pressed[pygame.K_w]: KEYB="00100000"
        if pressed[pygame.K_x]: KEYB="00100001"
        if pressed[pygame.K_y]: KEYB="00100010"
        # Add Special Chars
        if pressed[pygame.K_SPACE]: KEYB="00101010"
        if pressed[pygame.K_RETURN]: KEYB="00101011"


        if SINGLE==True:
            if pressed[pygame.K_PERIOD] and clicked==False:
                clock=True
                clicked=True
            if pressed[pygame.K_PERIOD]==0:
                clock=False
                clicked=False
        else:
            newtime=pygame.time.get_ticks()
            if clock==False and abs(newtime-oldtime)>CLOCKRATE/2:
                clock=True
                oldtime=newtime
            if clock==True and abs(newtime-oldtime)>CLOCKRATE/2:
                clock=False
                oldtime=newtime

        # We Now have the updated keybaord info so lets start the emulator!
        if clock==True:
            IR=readMem(PC,True)
            instructOp=IR[0:4]
            instructData=IR[4:12]

            if(ALUF=="00000000"):
                #Add and EQUAL FLAG
                ALUO=dectoBin(bintoDec(REGA)+bintoDec(REGB),8)
                if bintoDec(REGA)==bintoDec(REGB):
                    JUMPFLAG=1
                else:
                    JUMPFLAG=0
            if(ALUF=="00000001"):
                #Subtract and EQUAL FLAG
                ALUO=dectoBin(bintoDec(REGA)-bintoDec(REGB),8)
                if bintoDec(REGA)==bintoDec(REGB):
                    JUMPFLAG=1
                else:
                    JUMPFLAG=0
            if(ALUF=="00000010"):
                #Return Left Half Of REGA
                ALUO="0000"+REGA[:4]
                JUMPFLAG=0
            if(ALUF=="00000011"):
                #Return Right half of REGA
                ALUO="0000"+REGA[4:]
                JUMPFLAG=0
            if(ALUF=="00000100"):
                exit()
                #Add and overflow
                #ALUO=dectoBin(bintoDec(REGA)+bintoDec(REGB),8)
                ALUO=10
                if ALUO>255:
                    JUMPFLAG=1
                else:
                    JUMPFLAG=0



                        #LDA -- Looks like to works so far. I need to test changing H and L
            if instructOp=="0001":
                # Read Memory at HL
                REGA=readMem(REGH+REGL,True)[4:]
                REGD="0000"+readMem(REGH+REGL,True)[:4]
                print("BIGGER DEAL",REGD)

                    #LDB
            elif instructOp=="0011":
                # Set B to the value specified
                REGB=instructData


                    #CPY
            elif instructOp=="0100":
                sourceVal=0
                sourceReg=instructData[0:4]
                destReg=instructData[4:8]
            
                if sourceReg=="0000":
                    sourceVal=REGA
                elif sourceReg=="0001":
                    sourceVal=REGB
                elif sourceReg=="0010":
                    sourceVal=REGC
                elif sourceReg=="0011":
                    sourceVal=REGD
                    print("HIT!!",REGD)
                elif sourceReg=="0100":
                    sourceVal=REGH
                elif sourceReg=="0101":
                    sourceVal=REGL
                elif sourceReg=="0111":
                    sourceVal=ALUO
                elif sourceReg=="1000":
                    #Add get special keycodes
                    sourceVal=KEYB
                else:
                    print("ILLEGAL SOURCE REGISTER")

                if destReg=="0000":
                    REGA=sourceVal
                elif destReg=="0001":
                    REGB=sourceVal
                elif destReg=="0010":
                    REGC=sourceVal
                elif destReg=="0011":
                    REGD=sourceVal
                elif destReg=="0100":
                    REGH=sourceVal
                elif destReg=="0101":
                    REGL=sourceVal
                elif destReg=="0111":
                    ALUO=sourceVal
                elif destReg=="1000":
                    pass
                    # Can not write to keyboard register
                else:
                    print("ILLEGAL destReg REGISTER")

                #LDQ Load A with value at 00000000-<8 bit data aftr>
            elif instructOp=="0010":
                    # Read Memory at 00000000<Instruction Data>
                REGA=readMem("00000000"+instructData)
            elif instructOp=="0000":
                pass
                    #JMP
            elif instructOp=="0101":
                #Force Jump
                if instructData=="11111111":
                    JUMPFLAG=True
                if JUMPFLAG==1:
                    PC=REGH+REGL
                else:
                    pass
                    #STO
            elif instructOp=="0110":
                writeMem(REGH+REGL,REGD[4:]+REGA)
                #STQ
            elif instructOp=="1000":
                # NOT SURE ABOUT REG I HERE> TAKE A LOOK. LOOKS LIKE I MIXED UP IR and REG I and REGD
                writeMem("00000000"+instructData,REGI[4:]+REGA)
            elif instructOp=="1111":
                print("-----------------------------------")
                print("RegA: ",REGA,"(",bintoDec(REGA),")")
                print("RegB: ",REGB,"(",bintoDec(REGB),")")
                print("RegC: ",REGC,"(",bintoDec(REGC),")")
                print("RegH: ",REGH,"(",bintoDec(REGH),")")
                print("RegL: ",REGL,"(",bintoDec(REGL),")")
                print("ALUO: ",ALUO,"(",bintoDec(ALUO),")")
                print("-----------------------------------")
                pause=input("Continue?")
            else:
                print("Invalid Command")

                #Increment the PC counter only if jump isnt used
            if instructOp!="0101" or JUMPFLAG==False:
                PC=dectoBin(bintoDec(PC)+1,16)
            else:
                pass

        font = pygame.font.Font('font.ttf', 30) 
        REGAtext = font.render("A:"+hex(int(REGA, 2)), False, black)
        #REGAtext = font.render("A:"+REGA, False, black)
        REGBtext = font.render("B:"+hex(int(REGB, 2)), False, black)
        REGCtext = font.render("C:"+hex(int(REGC, 2)), False, black)
        REGDtext = font.render("D:"+hex(int(REGD, 2)), False, black)
        REGHtext = font.render("H:"+hex(int(REGH, 2)), False, black)
        REGLtext = font.render("L:"+hex(int(REGL, 2)), False, black)
        ALUFtext = font.render("ALF:"+hex(int(ALUF, 2)), False, black)
        ALUOtext = font.render("ALO:"+hex(int(ALUO, 2)), False, black)
        KEYBtext = font.render("Key:"+hex(int(KEYB, 2)), False, black)
        REGItext = font.render("R_I:"+hex(int(REGI, 2)), False, black)

        PCtext = font.render("PC:"+hex(int(PC, 2)), False, black)

        optext=""
        code=IR[0:4]
        if code=="0000":
            optext="NOP"
        elif code=="0001":
            optext="LDA" 
        elif code=="0010":
            optext="LDQ" 
        elif code=="0011":
            optext="LDB" 
        elif code=="0100":
            optext="CPY" 
        elif code=="0101":
            optext="JMP"
        elif code=="0110":
            optext="STO"
        elif code=="0111":
            optext=="FIXME!!"
        elif code=="1000":
            optext="STQ"
        elif code=="1111":
            optext="HALT"
            pause=input("CONTINUE?")
        else:
            print("NOSUPPORT") 
        IRtext = font.render("IR:"+optext, False, black)
        IRdataText = font.render("Data:"+IR[4:8]+" "+IR[8:13], False, black)
        IRdataHText = font.render("DataH:"+hex(int(IR[4:13], 2)), False, black)
        JMPFText = font.render("JMPF:"+str(JUMPFLAG), False, black)

        
       

        # --------------------------
        # Refresh ALU at end
        # ---------------------------
        screen.blit(REGAtext,(0,0,1,1))
        screen.blit(REGBtext,(0,30,1,1))
        screen.blit(REGCtext,(0,60,1,1))
        screen.blit(REGDtext,(0,90,1,1))
        screen.blit(REGHtext,(0,120,1,1))
        screen.blit(REGLtext,(0,150,1,1))
        screen.blit(ALUFtext,(0,180,1,1))
        screen.blit(ALUOtext,(0,210,1,1))
        screen.blit(KEYBtext,(0,240,1,1))
        screen.blit(REGItext,(0,270,1,1))

        screen.blit(PCtext,(0,300,1,1))
        screen.blit(IRtext,(0,330,1,1))
        screen.blit(IRdataText,(0,360,1,1))
        screen.blit(IRdataHText,(0,390,1,1))
        screen.blit(JMPFText,(0,420,1,1))

        font = pygame.font.Font('font.ttf', 15) 
        for x in range(0,SCREENSIZE):
            for y in range(0,SCREENSIZE):
                drawChar = font.render(termData[x][y], False, black)
                screen.blit(drawChar,(250+12*x,12+15*y,0,0))

        deltaFrame+=1
        if deltaFrame>UPDATERATE:
        	pygame.display.flip()
        	deltaFrame=0
