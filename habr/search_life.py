from tkinter import Tk, Canvas, Button, Frame, BOTH, NORMAL, HIDDEN

def refresh(): #функция обновления картинки
	for i in range(field_height):
		for j in range(field_width):
			k = 0
			for i_shift in range(-1, 2):
				for j_shift in range(-1, 2):
					print(addr(i + i_shift, j + j_shift))
					if (canvas.gettags(cell_matrix[addr(i + i_shift, j + j_shift)])[0] == 'vis' and (i_shift != 0 or j_shift != 0)):
						k += 1
			current_tag = canvas.gettags(cell_matrix[addr(i, j)])[0]
			#в зависимости от числа соседей устанавливаем значение клетки
			if k == 3:
				canvas.itemconfig(cell_matrix[addr(i, j)], tags=(current_tag, 'to_vis'))
			if k == 4:
				canvas.itemconfig(cell_matrix[addr(i, j)], tags=(current_tag, 'to_hid'))
			if k == 2 and canvas.gettags(cell_matrix[addr(i, j)])[0] == 'vis':            
				canvas.itemconfig(cell_matrix[addr(i, j)], tags=(current_tag, 'to_vis'))

def repaint(): #перерисовываем поле
	for i in range(field_height):
		for j in range(field_width):			            
			if (canvas.gettags(cell_matrix[addr(i, j)])[1] == 'to_hid'):
				canvas.itemconfig(cell_matrix[addr(i, j)], state=HIDDEN, tags=('hid','0'))
			if (canvas.gettags(cell_matrix[addr(i, j)])[1] == 'to_vis'):
				canvas.itemconfig(cell_matrix[addr(i, j)], state=NORMAL, tags=('vis','0'))

def step():	      
	refresh()
	repaint()

def clear():
	for i in range(field_height):
		for j in range(field_width):
			canvas.itemconfig(cell_matrix[addr(i, j)], state=HIDDEN, tags=('hid','0'))

def draw_a(e):
	ii = int((e.y - 3)/cell_size)
	jj = int((e.x - 3)/cell_size)
	canvas.itemconfig(cell_matrix[addr(ii, jj)], state=NORMAL, tags='vis')

#эта функция преобразует двумерную координату в простой адрес нашего одномерного массива
def addr(ii,jj):
	if(ii < 0 or jj < 0 or ii >= field_height or jj >= field_width):
		return len(cell_matrix) - 1
	else:
		return ii*int((win_width/cell_size)) + jj

#----------MAIN----------------#
root = Tk() #создаем окно

win_width = 350 #ширина и высота окна
win_height = 370
config_string = '{0}x{1}'.format(win_width, win_height + 32) 

root.geometry(config_string) 
cell_size = 20 #размер ячейки
canvas = Canvas(root, height=win_height) #создаем дочку окна на которой будем рисовать
canvas.pack(fill=BOTH) #упаковщик в tkinter

field_height = int(win_height / cell_size) #размеры поля в клетках
field_width = int(win_width / cell_size)
print(field_width, field_height)

cell_matrix = [] #массив для клеток
print(len(cell_matrix))
for i in range(field_height):
	for j in range(field_width):
		#создаем экземпляры клеток и делаем их скрытыми
		square = canvas.create_rectangle(2 + cell_size*j, 2 + cell_size*i, cell_size + cell_size*j - 2, cell_size + cell_size*i - 2, fill="green")
		canvas.itemconfig(square, state=HIDDEN, tags=('hid', '0'))
		cell_matrix.append(square)

#создаем фиктивный элемент на все поле, как бы по всюду и вне поля
fict_square = canvas.create_rectangle(0,0,0,0, state=HIDDEN, tags=('hid','0'))
cell_matrix.append(fict_square)

#создаем фрейм по хранению кнопок
frame = Frame(root)
btn1 = Button(frame, text='Eval', command = step)
btn2 = Button(frame, text='Clear', command = clear)
btn1.pack(side='left') #пакуем кнопки
btn2.pack(side='right')
frame.pack(side='bottom') #пакуем фрейм

canvas.bind('<B1-Motion>', draw_a) #привязывваем событие нажатия кнопки на canvas к функции draw_a
canvas.bind('<ButtonPress>', draw_a) 

root.mainloop() #стандартный цикл запуска графического окна