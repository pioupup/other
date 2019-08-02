

import requests
import re
from tkinter import *
from tkinter import filedialog

fail = 'Ничего не найдено!'

def run():   
	database=[] # Заводим пустой список для хранения адресов
	headers = { # Заголовок чтоб сервер считал нас клиентом
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
	}

	url=url_value.get()
	try:
		page=requests.get(url,headers=headers)
	except:
		url="http://"+url
		page=requests.get(url,headers=headers)
            
	page=str(page.text)
	urls=re.findall('<a href="([^"]+)">',page)
	urls.insert(0,url)

	for k in range(len(urls)):
		page=requests.get(urls[k],headers=headers)
		page=str(page.text)
		if var.get()==0:
			emails=re.findall('\w+@\w+.\w+',page)

		if var.get()==1:
			emails=re.findall('\w+@gmail.com',page)

		if var.get()==2:
			emails=re.findall('\w+@yandex.ru',page)

		if var.get()==3:
			emails=re.findall('\w+@mail.ru',page)

		for i in range(len(emails)):
			if emails[i] in database:
				pass
			else:
				email.insert(END, emails[i]+'\n')
				database.append(emails[i])

	if len(emails)==0:
		email.insert(END, fail)

def save():
	fn = filedialog.SaveAs(filetypes = [('*.txt', '.txt')]).show()
	if fn == '':
		return
	if not fn.endswith(".txt"):
		fn+=".txt"
	open(fn, 'wt').write(email.get('1.0', 'end'))

def clear1():
	url_value.delete(0,"end")

def clear2():
	email.delete(1.0,END)

root=Tk()
root.geometry("400x250")
root.resizable(width=False, height=False)
__version__="0.1.0"
root.title("MailParser "+__version__+" By Pirnazar")

icon="iVBORw0KGgoAAAANSUhEUgAAAEAAAAAxCAYAAABqF6+6AAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAfDSURBVGhD7VppTFRXFMbYJWpasdo1/eEWo8bGiOyi1CrFRtrGtJqmGqst1PCjLE03RUSUgiJgTJuGamm1Vq2KFlu1Sm0DgrKIoKDgBsimSIVBZ2Nm3nD6ncd74wBiZ4ZZMPEmX+6b9+6555zvnnvuu/eNm9uj0i8GnoT0OMAfCJAwFfWofvU6wIWfhX0rgO3AH8BBYIcZ9kj3M1EnAj4D3B+LzXseLVOAbCANCAJG9iH9BO5PAT6RCGKS3rBY0wBsGA6bCoCvgOE22Pc6ZI4Au4HnbJB3mcggaP5ZCumX7WAFR8R5gHPGgC+c4E4AyXa21BP9VT0MUyILRsbb2Xm5uwm4qASYjAFZEmDVjw62zFuaDu4O1mN192xYIfC41ZLWC3wBkW3WizlW4ji6n+FYFd16z8EvJn1AFF6udmPNm5SweHFKfHJySlxcnN0Rv359SlxCQsrK8RPCB7u5vcU6B4T3kiHen4WGLqPDx4jaFOSwcr2eDsTEVkuOH0M91tUkPAMD/mYjQqOjw0ijJWFvJhlrr9uXA0Eg/dHjRDebKfOv7DLJaV5tol1NwHwYkMFGLF+6NFz0Wquljl/2kFBTax8S4LwOzhsuVor9Ze7fLxPwKtTudDUBK2HAlyIBy5d3EYDSqdFQx65fyVjf0C8SOvV60h05RoJZRGVmZsoE8O7xMICU4LwCh7rp2wLVC3sSIJKg05FmUxoJ1TU2kcDOa9K3mUZe7sSMAH7l/h3gDZfTCuzotm3/DppD7keAsaGR9Dl5pDt0mAynCshQfoEMFfcgVFwkGfJ9QX5eUkr67BNkKC4hfUFRNwLNCGC1vGO0x37DYgJhDBNvKkzAm72mgNEozlsyCAiFThIuXyXh6jWgWsI1Ml6rJiN+M7ru455UC5VV1KnoWk2YRKGu3kSCqwnoydQ3uLGgJwHGC5foav5RqtI20eW7dVSta6Ebxjt0y6ikdtKTEe7kt1dQjqKcTt+5RKBJLBWaOrFuJRVdUd/oyicqNekOHxWJ5NKDgEPQ/aLFw+eAhmvQZ1Q3AnR6Ev48Qc0draTQq0gn6OiGpoX0RgPd1rbSdVUzrnXUoL5FSoOaLt2pIYVOxa5SvbpZdFKpV1Kzts006obyCjKUne8i4N4q4A69nAT5IMVl5V1o5mlgWgaNRSXUWVtHtwx3SGXoEI2uUTaKdVtHG9WobpLGoKFGzb/Ss3pq1SlFAhpBChcViGvRKkwE8OjzasB1ZlaWvArwsRkfpbm0vATtfNzlFhoR8XGnop2M/+SKhrdobosEdHYaqbK9Bu4RKToUVAcn7+ruUrWySWxXq2ygNikCmtQt9ycAdwUkVbp4iQ5km16EPoXaWJd6Lyn/DfXE6KSvl1DRGWQtg+iEmrpGn4uStKZrnXTVQQa6oq+jYnUVlWmrxbvtpDG1O6uupPKO2ntRwFf1TXRg8xY+HeLCo89nBC4v78GCzbEeXgvObf1BKCktFUpKSoSC4kKh6EyxeH26uECsi/Gb78t1ftEpIbcwT8hD3bPdSdw/WZgvnIEcPxNRVCTsXvBODvRNGTtuXE1GRsZkl3sPA/jNKBepmM/4RwO8QXEYcGY+cvCgQTsjIyNp48aNWuw8N4SHh49wNRFvwwA+wXVG8fXx8WHnad26dZScnMx13dq1az9yhvIH6eAPHascbMSIUaNG1a9evVp0HqNPa9asoYSEBJGQ+Pj4UzExMa/JNoSEhDj1a9NQKObvAEscRMKQoUOHlnDop6amio4zAeZISkoSyQAR28PCwmZ7e3vfnDFjxveBgYEvOMimXt3yslgO2DscecNTOGzYsIj09PT34WCdFPq9iMBUoLS0NFq0aBFNnz6dAgICyM/PrwVERIGIx5xBBH/F4UzNn8K6bRxsVM5HbueAZbI8osAdjiZhGmg59NlpORI4AqKiosjLy4sQAcT5AgTIRJSBCHHv4ujCKwNvlXMBTpC2lDEQSgfygPt+C0AumIRo2JeYmEgc/kwC54bg4GDy8PAQnTeHv78/gQBG1qxZs16xxShrZfwgsBfgTQt/HR79Px08jec84t8CfNQWaYnC2NjYYDhezLkBc5+mTZvWy3lzIpgERIUedSqmhVMSJb+3bwSyAH5z3ApsAJIkcLTwKS9vbn4CPgCGWOK8WZtBiIZVQUFB5Onp+UACmAxfX195WjQhT/Bplj2mq0Umj5dGeankKDvLp0oc5k9Z1EMfjaZOnfr5zJkzRed6hn9fv+X8gOlRDNng/uh3uSxGcjIc2cFznWEpCdxOlkG9D9Niosud6Y8BICIQI3tSmutWESHJaEBEIohw748dLpdFSC8DEbX8LmDNtJDzA0i4DkI+dLkj/TFg7ty5w+FEAohQ8+haMy04P7AMiMgHZjvrRao//vYpiyiYAGf22JofOIqYBIcY58xOQUIQHCmUXpEtiggpoZ7F1LB2aXama9bpAhEr4FijJfmBCUA+eSj+o2QVC3PmzBkJ5zZhruv6yg/SqrBL7hgvTE79FGeVQ7Y2RnKbAiIOSgnPNC14NQBUeG76+gQCHu53hAeRhDCfDyJK5WkhJb4YcxkQ4PLjN1sH2iK5hQsXDobjESCiHaPfNG/ePP7rn6mAAKecKVhkrCMbIRrGAB49dThz0+RI/2zu+xEBWAX+AztunxXD/JLRAAAAAElFTkSuQmCC"
img = PhotoImage(data=icon)
root.tk.call('wm', 'iconphoto', root._w, img)

var=IntVar()
var.set(0)

text_1=Label(text="URL:")
text_1.place(x=10,y=10)

text_2=Label(text="Filters:")
text_2.place(x=325,y=40)

url_value=Entry(width=30)
url_value.place(x=50,y=10)

run=Button(text="Run",height=1,command=run)
run.place(x=245,y=10)

email=Text(wrap=NONE, font="Courier 9", width=43, height=13)
email.place(x=15,y=42)

save_btn=Button(text="Save",command=save)
save_btn.place(x=285,y=10)

clear_url=Button(text="Clear",command=clear1)
clear_url.place(x=325,y=10)

clear_text=Button(text="Clear",command=clear2)
clear_text.place(x=325,y=145)

All=Radiobutton(text="All",variable=var,value=0)
All.place(x=325,y=60)

Gmail=Radiobutton(text="Gmail",variable=var,value=1)
Gmail.place(x=325,y=80)

Yandex=Radiobutton(text="Yandex",variable=var,value=2)
Yandex.place(x=325,y=100)

Mail_ru=Radiobutton(text="Mail.ru",variable=var,value=3)
Mail_ru.place(x=325,y=120)

root.mainloop()