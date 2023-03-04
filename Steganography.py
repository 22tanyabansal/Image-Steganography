# Python program implementing Image Steganography
from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
from PIL import Image
textBg="light cyan"
root = Tk()
root.geometry("400x150")
def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd
def modPix(pix, data):

	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]
def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1
def encode(data,img,new_img_name,message,win):
    try:
        image = Image.open(img, 'r')
    except:
        message.config(text="File not found")
    if (len(data) == 0):
        message.config(text="Data is empty")
    else:
        newimg = image.copy()
        encode_enc(newimg, data)
        newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
        message.config(text="Encrypted Successfully")
def showImage(img):
    try:
        imag = Image.open(img)
        imag.show()
    except:
        showI = Toplevel(root)
        showI.geometry("400x100")
        showI.title(" Fatal Error")
        l = Label(showI,text = "File not found Error",font=("Helvetica" ,14),pady=5)
        l.pack()
def decode(img,win,message,Display1):
 try:
    message.config(text="Successfully Decrypted")
    image = Image.open(img, 'r')
    data = ''
    imgdata = iter(image.getdata())
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if(pixels[-1] % 2 != 0):
            Display1.pack_forget();
            message.config(text="Successfully Decrypted")
            outPut = Label(win,text = "Data Found: "+data,font=("Times New Roman",16),pady=10,padx=5)    
            outPut.pack()
            return
 except:
    message.config(text="File not found")
def Take_input(inputtxt):
    INPUT = inputtxt.get()
    print(INPUT)
    if(INPUT == "120"):
        inputtxt.config(state='disabled',bg='light gray')
        x.config(text = "Success ",foreground="green")
        create()
    else:
        x.config(text = "Wrong input!!Try again ",foreground="red")
def open_file(ImageName):
   file = filedialog.askopenfile(mode='r', filetypes=[('Images', '*.png')])
   if file:
    ImageName.delete(0,"end")
    ImageName.insert(0, file.name)
      
def Take_text_and_filename(win,choice,l,Display,x):  
    win.geometry("400x250") 
    INPUT = choice.get()
    if(INPUT == "1"):
        win.geometry("400x500")
        x.config(text="Selected-Encryptor module",foreground="green")
        l.pack_forget()
        choice.pack_forget()
        Display.pack_forget()
        l1 = Label(win,text = "Enter the text to be encrypted ",font=("Helvetica" ,14),pady=3)
        plainText = Entry(win,bg = textBg)
        l2 = Label(win,text = "Enter image to be encrypted ",font=("Helvetica" ,14),pady=3)
        lside = Label(win,text = "(with extention)",font=("Arial" ,10),pady=5)
        ImageName = Entry(win,bg = textBg)
        l3 = Label(win,text = "Enter output filename",font=("Helvetica" ,14),pady=3)
        lside1 = Label(win,text = "(with extention)",font=("Arial" ,10),pady=5)
        OutputImageName = Entry(win,bg = textBg)
        message=Label(win,text = "",foreground="red")
        Display1 = Button(win, height = 2,
                    width = 20,
                    text ="Encrypt",
                    command = lambda:encode(plainText.get(),ImageName.get(),OutputImageName.get(),message,win))
        ViewImage = Button(win, height = 2,
                    width = 20,
                    text ="ViewImage",
                    command = lambda:showImage(ImageName.get()))
        label = Label(win, text="Click the Button to browse the Files", font=('Georgia 8'))
        b=ttk.Button(win, text="Browse", command=open_file(ImageName))
        l1.pack()
        plainText.pack()
        l2.pack()
        lside.pack()
        ImageName.pack()
        l3.pack()
        lside1.pack()
        OutputImageName.pack()
        label.pack()
        b.pack()
        message.pack()
        Display1.pack(side=RIGHT)
        ViewImage.pack(side=LEFT)
        
    elif(INPUT == "2"):
        x.config(text = "Selected-Decryptor module",foreground="green")
        l.pack_forget()
        choice.pack_forget()
        Display.pack_forget()
        l1 = Label(win,text = "Enter the file name ",font=("Helvetica" ,14),pady=3)
        lside = Label(win,text = "(with extention)",font=("Arial" ,10),pady=5)
        OutputImageName1 = Entry(win,bg = textBg)
        message=Label(win,text = "",foreground="red")
        Display1 = Button(win, height = 2,
                    width = 20,bd=4,
                    text ="DECODE",font =("Courier", 12),
                    command = lambda:decode(OutputImageName1.get(),win,message,Display1))
        label = Label(win, text="Click the Button to browse the Files", font=('Georgia 8'))
        b=ttk.Button(win, text="Browse", command=open_file(OutputImageName1))
        l1.pack()
        lside.pack()
        OutputImageName1.pack()
        label.pack()
        b.pack()
        message.pack()
        Display1.pack()
    else:
        x.config(text = "Wrong Input!!!Try again ",foreground="red")
def create():
    win = Toplevel(root)
    win.geometry("400x150")
    win.title(" Encryptor Decryptor- by EliteCoders")
    l = Label(win,text = "Enter choice 1 for encryption, 2 for decryption",font=("Helvetica" ,14),pady=5)
    x = Label(win,text = "")
    choice = Entry(win,font =("Courier", 12),bg = textBg)
    Display = Button(win, height = 2,
                 width = 20,
                 text ="Next",pady=3,bd=3,
                 command = lambda:Take_text_and_filename(win,choice,l,Display,x))
    l.pack()
    choice.pack()
    x.pack()
    Display.pack()

root.title(" Enter key ")
l = Label(text = "To access this module, Enter the key ",font=("Times New Roman",16),pady=10)
inputtxt = Entry(root,bg = textBg,font =("Courier", 14))
x = Label(text = "")
Display = Button(root, height = 2,
                width = 20,
                text ="Check",bd=4,
                command = lambda:Take_input(inputtxt))
l.pack()
inputtxt.pack()
x.pack()
Display.pack(side=BOTTOM)
mainloop()
