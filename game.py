
import pygame
import time
import math
import os
import random
import sys


class SpecificKeyConfigScene:
	def __init__(self, action, bg_scene):
		self.bg = bg_scene
		self.foo = pygame.Surface((640, 480)).convert_alpha()
		self.foo.fill((0, 0, 0, 120))
		self.next = self
		self.is_menu = True
		self.raw_input_desired = True
		self.action = action
		
	def ProcessInput(self, raw_input):
		for pygame_event in raw_input:
			if pygame_event.type ==  pygame.KEYUP:
				pygame_key = pygame_event.key
				my_code = self.action
				set_configuration(my_code, pygame_key)
				self.next = NewICScene()
	
	def Update(self, counter):
		pass
	
	def Render(self, screen):
		self.bg.Render(screen)
		screen.blit(self.foo, (0, 0))
		player = self.action[0]
		key = self.action[1:].upper()
		img = render_text("Press the key for " + key + " (Player " + player + ")", 26, (255, 255, 255))
		w = img.get_width()
		h = img.get_height()
		screen.blit(img, (320 - w // 2, 240 - h // 2))
		
		
				

_key_names = {}
keys = filter(lambda x:x.startswith('K_'), dir(pygame))
for key in keys:
	
	exec ('foo = pygame.' + key)
	_key_names[foo] = key[2:].upper()

def get_key_name(pygame_key_code):
	global _key_names
	return _key_names[pygame_key_code]

was_mouse_released_this_frame = False

class ClickButton:
	
	def __init__(self, x, y, config_code):
		self.x = x
		self.y = y
		self.color = (0, 0, 255)
		self.code = config_code
		self.img = self.get_image()
		self.w = self.img.get_width()
		self.h = self.img.get_height()
		
	def hover(self):
		if self.color[2] == 255:
			self.color = (0, 200, 0)
			self.img = self.get_image()
	
	def unhover(self):
		if self.color[1] == 200:
			self.color = (0, 0, 255)
			self.img = self.get_image()
		
	def is_mouse_over(self, mx, my):
		is_over = mx >= self.x and mx <= (self.x + self.w) and (my >= self.y) and (my <= self.y + self.h)
		if is_over:
			self.hover()
		else:
			self.unhover()
		return is_over
		
	def get_image(self):
		
		text = self.get_label()
		img = render_text(text, 16, self.color)
		w = img.get_width()
		h = img.get_height()
		padding = 5
		bg = pygame.Surface((w + padding * 2, h + padding *2))
		bg.fill((255, 255, 255))
		pygame.draw.rect(bg, self.color, pygame.Rect(0, 0, w + padding * 2, h + padding * 2), 1)
		bg.blit(img, (padding, padding))
		return bg
		
	def get_label(self):
		global _new_ic
		display = _new_ic.get(self.code)
		
		if display != None and len(display) > 0: return get_key_name(display[0])
		return "---"
	
	def Render(self, screen):
		screen.blit(self.img, (self.x, self.y))


class NewICScene:
	
	def __init__(self):
		self.next = self
		self.is_menu = True
		self.raw_input_desired = False
		x1 = 200
		x2 = x1 + 150
		y1 = 100
		y2 = y1 + 50
		y3 = y2 + 50
		y4 = y3 + 50
		y5 = y4 + 50
		self.x = [x1, x2]
		self.y = [y1, y2, y3, y4, y5]
		self.buttons = [
			ClickButton(x1, y1, '1up'),
			ClickButton(x1, y2, '1down'),
			ClickButton(x1, y3, '1left'),
			ClickButton(x1, y4, '1right'),
			ClickButton(x1, y5, '1eat'),
			ClickButton(x2, y1, '2up'),
			ClickButton(x2, y2, '2down'),
			ClickButton(x2, y3, '2left'),
			ClickButton(x2, y4, '2right'),
			ClickButton(x2, y5, '2eat')
			]
		
		self.done_button = [
			render_text('Done!', 36, (0, 0, 255)),
			render_text('Done!', 36, (0, 200, 0))
		]
		db = []
		for d in self.done_button:
			nd = pygame.Surface((d.get_width() + 10, d.get_height() + 10))
			nd.fill((255, 255, 255))
			nd.blit(d, (0, nd.get_height() - d.get_height()))
			db.append(nd)
		self.done_button = db
		
	def ProcessInput(self, ignored):
		global was_mouse_released_this_frame
		m = pygame.mouse.get_pos()
		mx = m[0]
		my = m[1]
		for button in self.buttons:
			if button.is_mouse_over(mx, my):
				if was_mouse_released_this_frame:
					self.next = SpecificKeyConfigScene(button.code, self)
					return
		
		
		over_done = mx > 640 - self.done_button[0].get_width() and my < self.done_button[1].get_height()
		if over_done and was_mouse_released_this_frame:
			self.next = MainMenuB()
				
	
	def Update(self, counter):
		pass
	
	def Render(self, screen):
		m = pygame.mouse.get_pos()
		mx = m[0]
		my = m[1]
		
		screen.fill((255, 255, 255))
		
		screen.blit(render_text('Use the mouse to change key configurations', 18, (123, 123, 123)), (5, 5))
		
		for button in self.buttons:
			button.Render(screen)
		
		x = self.x[0] - 100
		screen.blit(render_text('Up',    36, (0, 0, 0)), (x, self.y[0]))
		screen.blit(render_text('Down',  36, (0, 0, 0)), (x, self.y[1]))
		screen.blit(render_text('Left',  36, (0, 0, 0)), (x, self.y[2]))
		screen.blit(render_text('Right', 36, (0, 0, 0)), (x, self.y[3]))
		screen.blit(render_text('Eat',   36, (0, 0, 0)), (x, self.y[4]))
		
		screen.blit(render_text("Player 1", 36, (0, 0, 0)), (self.x[0], self.y[0] - 40))
		screen.blit(render_text("Player 2", 36, (0, 0, 0)), (self.x[1], self.y[0] - 40))
		
		over_done = mx > 640 - self.done_button[0].get_width() and my < self.done_button[1].get_height()
		screen.blit(self.done_button[over_done], (640 - self.done_button[0].get_width(), 0))
		
		msg = render_text(
			"Both configurations for P1 and P2 will control single-player games",
			18,
			(0, 0, 0))
		screen.blit(msg, (320 - msg.get_width() // 2, 480 - 5 - msg.get_height()))
		
		

_new_ic = {
	'1up' : [pygame.K_w],
	'1down' : [pygame.K_s],
	'1left' : [pygame.K_a],
	'1right' : [pygame.K_d],
	'1eat' : [pygame.K_TAB],
	'2up' : [pygame.K_UP],
	'2down' : [pygame.K_DOWN],
	'2left' : [pygame.K_LEFT],
	'2right' : [pygame.K_RIGHT],
	'2eat' : [pygame.K_PERIOD],
	'3up' : [pygame.K_UP],
	'3down' : [pygame.K_DOWN],
	'3left' : [pygame.K_LEFT],
	'3right' : [pygame.K_RIGHT],
	'3eat' : [pygame.K_SPACE, pygame.K_RETURN]
}

def set_configuration(my_new_code, pygame_key):
	global _new_ic
	for key in filter(lambda x:x[0] != '3', _new_ic.keys()):
		while pygame_key in _new_ic[key]:
			_new_ic[key].remove(pygame_key)
	_new_ic[my_new_code] = [pygame_key]
	
	generate_inverse_input_lookup()
	
	
	
_new_ic_i = {}

def generate_inverse_input_lookup():
	global _new_ic, _new_ic_i
	_new_ic_i.clear()
	for key in _new_ic.keys():
		for code in _new_ic[key]:
			v = _new_ic_i.get(code)
			if v == None:
				v = []
				_new_ic_i[code] = v
			v.append(key)

generate_inverse_input_lookup()

def get_players_input(is_menu, raw_input):
	global _new_ic_i, was_mouse_released_this_frame
	
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_F4]:
		if pressed[pygame.K_LALT] or pressed[pygame.K_RALT]:
			quit_attempt()

	if raw_input:
		output = []
		for event in pygame.event.get():
			output.append(event)
			if event.type == pygame.QUIT:
				quit_attempt()
		return output
	
	was_mouse_released_this_frame = False
	
	lookup = _new_ic_i
	output = [[],[],[]]
	for event in pygame.event.get():
		if event.type in (pygame.KEYDOWN, pygame.KEYUP):
			down = pygame.KEYDOWN == event.type
			code = lookup.get(event.key)
			if code != None:
				for c in code:
					
					player_index = int(c[0]) - 1
					
					if is_menu: player_index = 0
					
					output[player_index].append(MyEvent(c[1:], down))
		elif event.type == pygame.MOUSEBUTTONUP:
			was_mouse_released_this_frame = True
		elif event.type == pygame.QUIT:
				quit_attempt()
	return output

_debug_disabled = True
_debug_buffer = []

_theme_list = 'marine element geometry space fruit clothes'.split()
def get_theme_list():
	global _theme_list
	return _theme_list

def debug(line):
	global _debug_buffer
	_debug_buffer.append(render_text(line, 16, (255, 255, 255)))

_stdout_stash = sys.stdout
def hide_output():
	sys.stdout = None

def enable_output():
	global _stdout_stash
	sys.stdout = _stdout_stash

class InputMapping:
	
	def __init__(self, key, name, joystick):
		self.key = key
		self.joystick = joystick
		self.name = name
		self.key_mapping = {
			pygame.K_RETURN : 'start',
			pygame.K_SPACE : 'action'
		}
		
		self.joystick_state = {}
		
		self.joystick_mapping = {}
		self.joystick_scale = 1
		
		
		self.rendered_default = {
			'start' : ("???", "Enter")[self.joystick == None],
			'action' : ("???", "Space")[self.joystick == None],
			'up' : ("???", "Arrow")[self.joystick == None],
			'down' : ("???", "Arrow")[self.joystick == None],
			'left' : ("???", "Arrow")[self.joystick == None],
			'right' : ("???", "Arrow")[self.joystick == None],
			'aim_left' : ("???", "Mouse")[self.joystick == None],
			'aim_right' : ("???", "Mouse")[self.joystick == None],
			'aim_down' : ("???", "Mouse")[self.joystick == None],
			'aim_up' : ("???", "Mouse")[self.joystick == None],
			'trigger' : ('???', "Click")[self.joystick == None]
		}
		self.rendered_keys = {}
		#self.rendered_joystick = {}
		
		self.key_mappingB = {}
		if key == 'rhand_qwerty':
			self.key_mappingB = {
				pygame.K_a : 'left',
				pygame.K_s : 'down',
				pygame.K_d : 'right',
				pygame.K_w : 'up'
			}
			self.rendered_keys = {
				'left' : "A",
				'down' : "S",
				'right' : "D",
				'up' : "W"
			}
		elif key == 'rhand_dvorak':
			self.key_mappingB = {
				pygame.K_a : 'left',
				pygame.K_o : 'down',
				pygame.K_e : 'right',
				pygame.K_COMMA : 'up'
			}
			self.rendered_keys = {
				'left' : "A",
				'down' : "O",
				'right' : "E",
				'up' : "Comma"
			}
		elif key == 'rhand_dvorakleft':
			self.key_mappingB = {
				pygame.K_MINUS : 'left',
				pygame.K_k : 'down',
				pygame.K_c : 'right',
				pygame.K_q : 'up'
			}
			self.rendered_keys = {
				'left' : "Hyphen",
				'down' : "K",
				'right' : "C",
				'up' : "Q"
			}
		elif key == 'rhand_dvorakright':
			self.key_mappingB = {
				pygame.K_7 : 'left',
				pygame.K_8 : 'down',
				pygame.K_z : 'right',
				pygame.K_6 : 'up'
			}
			self.rendered_keys = {
				'left' : "7",
				'down' : "8",
				'right' : "Z",
				'up' : "6"
			}
		else:
			self.key_mappingB = {
				pygame.K_UP : 'up',
				pygame.K_DOWN : 'down',
				pygame.K_LEFT : 'left',
				pygame.K_RIGHT : 'right'
			}
			self.rendered_keys = {
				'left' : 'Arrow',
				'down' : 'Arrow',
				'right' : 'Arrow',
				'up' : 'Arrow'
			}
		for q in self.key_mappingB.keys():
			self.key_mapping[q] = self.key_mappingB[q]
		
		self.inv_mapping = {}
		for key in self.key_mapping.keys():
			value = self.key_mapping[key]
			self.inv_mapping[value] = key
		
	def GetRenderedKey(self, action):
		
		
		if self.joystick != None:
				
			config = self.joystick_mapping.get(action)
			if config == None:
				return '???'
			
			if config[0] == 'hat':
				return 'Hat ' + str(config[1] + 1) + ' (' + config[2] + ')'
			if config[0] == 'axis':
				return 'Axis ' + str(config[1] + 1) + ' (' + config[2] + ')'
			if config[0] == 'button':
				return "Button " + str(config[1] + 1)
		
		name = self.rendered_keys.get(action)
		if name != None:
			return name
		
		name = self.rendered_default.get(action)
		if name != None:
			return name
		
		#debug("AN AWFUL ERROR OCCURED!!!!!!!!!!!!!!!!!!!1 D:")
		return 'error'
		
	def SetJoystickMapping(self, action, type, arg, opt, scale=1):
		name = ''
		if type == 'hat':
			opt = (('L', 'R')[opt[0] > 0], ('U', 'D')[opt[1] > 0])[opt[0] == 0]
			name = "Hat " + str(arg + 1) + ' (' + opt + ')'
		elif type == 'axis':
			opt = ('-','+')[opt]
			name = "Axis " + str(arg + 1) + ' (' + opt + ')'
		elif type == 'button':
			name = "Button " + str(arg + 1)
		else:
			return # what happened?
		#self.rendered_joystick[action] = name
		self.joystick_mapping[action] = (type, arg, opt)
		self.SetMaxJoystickScale(scale)
		
	def SetMaxJoystickScale(self, scale):
		if scale < 0: scale *= -1
		if scale > self.joystick_scale:
			self.joystick_scale = scale
	
	def get_shooting_vector(self):
		return self._get_vector('aim_')
		
	def get_movement_vector(self):
		return self._get_vector('')
		
	def _get_vector(self, prefix):
		dx = 0
		dy = 0
		
		rkey = prefix + 'right'
		lkey = prefix + 'left'
		ukey = prefix + 'up'
		dkey = prefix + 'down'
		
		if self.joystick == None:
			pressed = pygame.key.get_pressed()
			if pressed[self.inv_mapping[lkey]]:
				dx = -1
			elif pressed[self.inv_mapping[rkey]]:
				dx = 1
			if pressed[self.inv_mapping[ukey]]:
				dy = -1
			elif pressed[self.inv_mapping[dkey]]:
				dy = 1
		else:
			left = self.joystick_state.get(str(self.joystick_mapping[lkey]))
			if str(left) == 'True':
				dx = -1
			elif str(left) == 'False':
				dx = 0
			elif left != None:
				dx = -1 * left
			
			if dx == 0:
				right = self.joystick_state.get(str(self.joystick_mapping[rkey]))
				if str(right) == 'True':
					dx = 1
				elif str(right) == 'False':
					dx = 0
				elif right != None:
					dx = right
				
			down = self.joystick_state.get(str(self.joystick_mapping[dkey]))
			if str(down) == 'True':
				dy = 1
			elif str(down) == 'False':
				dy = 0
			elif down != None:
				dy = down
				
			if dy == 0:
				up = self.joystick_state.get(str(self.joystick_mapping[ukey]))
				if str(up) == 'True':
					dy = -1
				elif str(up) == 'False':
					dy = 0
				elif up != None:
					dy = -1 * up
				
			
		return (dx, dy)
	
	def GetEvents(self, pygame_events):
		events = []
		bad_indices = []
		
		#hide_output()
		
		if self.joystick != None:
			for key in self.joystick_mapping.keys():
				config = self.joystick_mapping[key]
				state_key = str(config)
				
				type = config[0]
				n = config[1]
				direction = config[2]
				
				previous = self.joystick_state.get(state_key, False)
				
				if type == 'hat':
					pressed = False
					hat_full_state = self.joystick.get_hat(n)
					if direction == 'L' and hat_full_state[0] == -1:
						pressed = True
					elif direction == 'R' and hat_full_state[0] == 1:
						pressed = True
					elif direction == 'D' and hat_full_state[1] == 1:
						pressed = True
					elif direction == 'U' and hat_full_state[1] == -1:
						pressed = True
					
					if pressed != previous:
						events.append(MyEvent(key, pressed))
						self.joystick_state[state_key] = pressed
				
				elif type == 'button':
					button_state = self.joystick.get_button(n)
					if button_state != previous:
						events.append(MyEvent(key, button_state))
						self.joystick_state[state_key] = button_state
				
				elif type == 'axis':
					state = self.joystick_state.get(state_key)
					axis_state = self.joystick.get_axis(n)
					self.SetMaxJoystickScale(axis_state)
					scale = self.joystick_scale
					new_state = 0
					if direction == '-':
						if axis_state < 0:
							new_state = (0.0 - axis_state) / scale
							if new_state < 0.05:
								new_state = 0
					else:
						if axis_state > 0:
							new_state = (0.0 + axis_state) / scale
							if new_state < 0.05:
								new_state = 0
					
					events.append(MyEvent(key, new_state != 0, new_state))
					self.joystick_state[state_key] = new_state
		
		enable_output()
		
		for event in pygame_events:
			if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				action = self.key_mapping.get(event.key)
				if action != None:
					if self.joystick == None or action in ('start', 'action', 'eat'):
						down = event.type == pygame.KEYDOWN
						events.append(MyEvent(action, down))
						if action in ('action', 'start', 'eat'):
							bad_indices.append(event)
			if self.joystick == None:
				if event.type == pygame.MOUSEBUTTONDOWN:
					events.append(MyEvent('trigger', True))
				elif event.type == pygame.MOUSEBUTTONUP:
					events.append(MyEvent('trigger', False))
				elif event.type == pygame.MOUSEMOTION:
					events.append(MyEvent('aim_left', True, 'mouse'))
			
			if event.type == pygame.QUIT:
				quit_attempt()
		
		for bad in bad_indices:
			pygame_events.remove(bad)
		
		for event in events:
			pass #debug(event.command + ', ' + str(event.down) + ', ' + str(event.magnitude))
		
		return events

_configurations = [
		InputMapping('rhand_qwerty', "Right Hand Qwerty (WASD)", None),
		InputMapping('lhand_qwerty', "Left Hand Qwerty (Arrows)", None),
		InputMapping('rhand_dvorak', "Dvorak (,AOE)", None),
		InputMapping('rhand_dvorakleft', "Left Hand Dvorak (Q-KC)", None),
		InputMapping('rhand_dvorakright', "Right Hand Dvorak (8Z67)", None)
		]

def initialize_input_config_defaults():
	global _configurations, _player1_config, _player2_config
	return
	joysticks = []
	p1s = 0
	p2s = -1
	if os.path.exists('joystick.txt'):
		c = open('joystick.txt', 'rt')
		lines = c.read().split('\n')
		c.close()
		if len(lines) >= 2 and lines[0][0] == '1' and lines[1][0] == '2':
			p1 = lines[0].split(':#')
			p1s = int(p1[1])
			p2 = lines[1].split(':#')
			p2s = int(p2[1])
		lines = lines[2:]
		joysticks = []
		for line in lines:
			p = line.split('%%%%%')
			if len(p) > 1:
				jsname = p[0]
				data = p[1].split('|')
				jsscale = data[0]
				if '.' in jsscale:
					jsscale = float(jsscale)
				else:
					jsscale = int(jsscale)
				jsmapping = {}
				for piece in data[1:]:
					parts = piece.split(',')
					action = parts[0]
					type = parts[1]
					n = int(parts[2])
					arg = str(parts[3])
					if arg == "None": arg = None
					jsmapping[action] = (type, n, arg)
				joysticks.append((jsname, jsscale, jsmapping))
	
	for i in range(pygame.joystick.get_count()):
		joystick = pygame.joystick.Joystick(i)
		joystick.init()
		
		cached_data = None
		if len(joysticks) > i:
			if joysticks[i][0] == joystick.get_name():
				cached_data = joysticks[i]
		
		mapping = InputMapping(None, "Gamepad " + str(i + 1) + ' [' + joystick.get_name() + ']', joystick)
		if cached_data != None:
			mapping.joystick_scale = cached_data[1]
			mapping.joystick_mapping = cached_data[2]
		_configurations.append(mapping)
	
	if p1s != -1 and len(_configurations) > p1s:
		_player1_config = _configurations[p1s]
	else:
		_player1_config = None
		
	if p2s != -1 and len(_configurations) > p2s:
		_player2_config = _configurations[p2s]
	else:
		_player2_config = None
		
	

def get_input_configs():
	global _configurations
	return _configurations

_player1_config = None
_player2_config = None

def get_player_input_source(player_num):
	global _player1_config, _player2_config
	
	if _player1_config == None:
		return get_input_configs()[0]
	
	if player_num == 1:
		return _player1_config
	return _player2_config

def get_all_player_input_sources():
	output = [get_player_input_source(1)]
	p2 = get_player_input_source(2)
	if p2 != None:
		output.append(p2)
	return output

_dim = None

class PressAKeyScene:
	def __init__(self, action, name, parent, input_config):
		self.is_menu = True
		self.next = self
		self.config = input_config
		self.name = name
		self.action = action
		self.menu = parent
		self.raw_input_desired = True
		parent.next = parent
	
	def ProcessInput(self, players_input):
		pass
	
	def Update(self, counter):
		config = self.config
		js = config.joystick
		
		hide_output()
		
		# check buttons
		for i in range(js.get_numbuttons()):
			if js.get_button(i):
				config.SetJoystickMapping(self.action, 'button', i, None)
				self.next = InputConfigScene()
				enable_output()
				return
		
		# check hats
		for i in range(js.get_numhats()):
			hat = js.get_hat(i)
			if hat[0] != 0 or hat[1] != 0:
				config.SetJoystickMapping(self.action, 'hat', i, hat)
				self.next = InputConfigScene()
				enable_output()
				return
		
		# check axes
		for i in range(js.get_numaxes()):
			axis = js.get_axis(i)
			if axis == 0: continue
			config.SetMaxJoystickScale(axis)
			
			is_double = '.' in str(axis)
			if is_double: #presumably between -1.0 and 1.0
				if abs(axis) > 0.1:
					config.SetJoystickMapping(self.action, 'axis', i, axis > 0)
					self.next = InputConfigScene()
					enable_output()
					return
			else: # probably a 16-bit integer
				if abs(axis) > 10000:
					config.SetJoystickMapping(self.action, 'axis', i, axis > 0)
					self.next = InputConfigScene()
					enable_output()
					return
	
		enable_output()
		
	# action, hat, index, (x, y)
	# action, axis, index, ispositive?
	# action, button, index, None
	
	def Render(self, screen):
		global _dim
		self.menu.Render(screen)
		width = screen.get_width()
		height = screen.get_height()
		
		if _dim == None:
			_dim = pygame.Surface((width, height)).convert()
			_dim.fill((0, 0, 0))
			_dim.set_alpha(100)
		screen.blit(_dim, (0, 0))
		image = render_text("Press the joystick key for " + self.name, 36, (255, 255, 255))
		x = (width - image.get_width()) // 2
		y = (height - image.get_height()) // 2
		
		screen.blit(image, (x, y))

class Star:
	
	def __init__(self, distance=0):
		self.angle = random.random() * 3.14159 * 2
		self.distance = distance * 600
	
	def Update(self):
		self.distance += 10
_stars = []
_star_count = 400
for i in range(_star_count):
	_stars.append(Star(random.random()))
	
class InputConfigScene:
	
	def __init__(self):
		global _stars, _star_count
		self.is_menu = True
		self.next = self
		self.raw_input_desired = False
		self.mouse_over = None
		self.divider = 320
		self.render_counter = 0
		self.stars = _stars
		self.star_count = _star_count
	
	def render_background(self, screen):
		screen.fill((0, 0, 0))
		while len(self.stars) < self.star_count:
			self.stars.append(Star())
		
		too_far = []
		for star in self.stars:
			p_dist = ((star.distance / 600.0) ** 4) * 600
			x = int(math.cos(star.angle) * p_dist + 400)
			y = int(math.sin(star.angle) * p_dist + 200)
			
			cv = max(0, min(255, int(255 * (p_dist * 1.3 - 50) / 300.0)))
			c = (cv, cv, cv)
			near = p_dist > 200
			pygame.draw.rect(screen, c, pygame.Rect(x, y, 2 + near, 2 + near))
			star.Update()
			if star.distance > 600:
				too_far.append(star)
		
		for star in too_far:
			self.stars.remove(star)
		
	def ProcessInput(self, players_input):
		global _player1_config, _player2_config
		mouse_pos = pygame.mouse.get_pos()
		mx = mouse_pos[0]
		my = mouse_pos[1]
		
		for events in players_input:
			for event in events:
				if event.command == 'trigger' and event.down and self.mouse_over != None:
					
					if self.mouse_over == 'exit':
						self.next = MainMenuB()
						return
					
					configs = get_input_configs()
					
					player = 1
					if mx > self.divider:
						player = 2
					
					for config in configs + ['ZOMG Hack', None]:
						if self.mouse_over == config:
							if player == 1:
								if _player2_config == config:
									_player2_config = _player1_config
								_player1_config = config
							else:
								if _player1_config == config:
									_player1_config = _player2_config
								_player2_config = config
							
							if _player1_config == 'ZOMG Hack':
								_player1_config = None
							elif _player2_config == "ZOMG Hack":
								_player2_config = None
							return
					
					actions = 'start up down left right aim_left aim_right aim_down aim_up trigger'.split()
					names = 'PAUSE|UP|DOWN|LEFT|RIGHT|AIM LEFT|AIM RIGHT|AIM DOWN|AIM UP|TRIGGER'.split('|')
					for i in range(len(actions)):
						action = actions[i]
						if str(self.mouse_over) == action:
							name = names[i]
							self.next = PressAKeyScene(action, name, self, get_player_input_source(player))
							return

	def Update(self, counter):
		pass
	
	def get_configs(self):
		global _configurations
		return _configurations
	
	def Render(self, screen):
		
		self.render_background(screen)
		
		mouse_pos = pygame.mouse.get_pos()
		mx = mouse_pos[0]
		my = mouse_pos[1]
		
		configs = get_input_configs()
		
		
		self.mouse_over = None
		
		exit_sign = render_text("Done", 36, (128, 128, 128))
		x = screen.get_width() - exit_sign.get_width() - 5
		y = 5
		if mx > x and my < exit_sign.get_height() + y:
			self.mouse_over = 'exit'
			exit_sign = render_text("Done", 36, (255, 255, 0))
		screen.blit(exit_sign, (x, y))
		
		left = 20
		for player in (1, 2):
			config = get_player_input_source(player)
			screen.blit(
				render_text('Player ' + str(player), 36, (255, 255, 255)),
				(left - 10, 10))
			
			y = 50
			font_size = 18
			if player == 2:
				configs = configs + ['ZOMG Hack']
			for tconfig in configs:
				
				color = (128, 128, 128)
				active = False
				if tconfig == config or (tconfig == 'ZOMG Hack' and config == None):
					color = (0, 255, 0)
					active = True
				
				if tconfig == 'ZOMG Hack':
					name = "Not Present"
				else:
					name = tconfig.name
				
				image = render_text(name, font_size, color)
				x = left
				right = x + image.get_width()
				bottom = y + image.get_height()
				
				if mx >= x and mx <= right and my >= y and my <= bottom:
					self.mouse_over = tconfig
					image = render_text(name, font_size, (180, 180, 40))
				
				screen.blit(image, (x, y))
				
				y += 25
			
			y += 30
			
			std_spacing = 22
			disable_debug()
			column = 125
			render_button = self.render_button
			render_button(1, screen, "Pause", left, y, 'start', config, mx, my)
			y += std_spacing - 3
			screen.blit(render_text("Movement", 24, (128, 128, 128)), (left, y))
			y += std_spacing + 5
			render_button(1, screen, "Left", left, y, 'left', config, mx, my)
			render_button(1, screen, "Right", left + column, y, 'right', config, mx, my)
			y += std_spacing
			render_button(1, screen, "Up", left, y, 'up', config, mx, my)
			render_button(1, screen, "Down", left + column, y, 'down', config, mx, my)
			y += std_spacing - 3
			screen.blit(render_text("Weapons", 24, (128, 128, 128)), (left, y))
			y += std_spacing + 5
			render_button(1, screen, "Aim Left", left, y, 'aim_left', config, mx, my)
			render_button(1, screen, "Aim Right", left + column, y, 'aim_right', config, mx, my)
			y += std_spacing
			render_button(1, screen, "Aim Up", left, y, 'aim_up', config, mx, my)
			render_button(1, screen, "Aim Down", left + column, y, 'aim_down', config, mx, my)
			y += std_spacing
			render_button(1, screen, "Trigger", left, y, 'trigger', config, mx, my)
			y += std_spacing
			
			self.divider = left - 10
			left += 300
			
		
		
		
	def render_button(self, player, screen, name, x, y, action, input_config, mx, my):
		if input_config == None: return
		
		customizeable = input_config.joystick != None
		font_size = 18
		caption = render_text(name, font_size, (255, 255, 255))
		screen.blit(caption, (x, y))
		nx = x + caption.get_width() + 5
		key_name = input_config.GetRenderedKey(action)
		color = (128, 128, 255)
		if customizeable:
			color = (255, 128, 0)
		key = render_text(key_name, font_size, color)
		if customizeable and mx >= nx and mx <= nx + key.get_width() and my >= y and my <= y + key.get_height():
			color = (255, 255, 0)
			self.mouse_over = action
			key = render_text(key_name, font_size, color)
		pygame.draw.rect(screen, color, pygame.Rect(nx - 1, y - 1, key.get_width() + 2, key.get_height() + 2), 1)
		screen.blit(key, (nx, y))

		



def disable_debug():
	global _debug_disabled
	_debug_disabled = True

_quit_attempted = False

def is_quit_attempted():
	global _quit_attempted
	return _quit_attempted

def quit_attempt():
	global _quit_attempted
	_quit_attempted = True

_image_library = {}
def get_image(path):
	global _image_library
	
	image = _image_library.get(path)
	if image != None:
		return image
	
	canonical_path = path.replace('\\', '/').lower()
	image = _image_library.get(canonical_path)
	if image != None:
		_image_library[path] = image
		return image
	
	real_path = ('images/' + path).replace('/', os.sep).replace('\\', os.sep).replace(os.sep + os.sep, os.sep).lower()
	image = _image_library.get(real_path)
	if image != None:
		_image_library[path] = image
		return image
	
	image = pygame.image.load(real_path)
	_image_library[path] = image
	
	return image

class MyEvent:
	def __init__(self, key, down, magnitude=1.0):
		self.down = down
		self.up = not down
		self.command = key
		self.magnitude = magnitude

class Alien:
	def __init__(self, playscene, type, stage, x, y):
		self.scene = playscene
		self.type = type
		self.stage = stage
		self.landed = 600
		self.real_x = x + 0.0
		self.real_y = y + 0.0
		self.x = int(x)
		self.expired = False
		self.y = int(y)
		self.counter = 0
		self.is_ship = type.startswith('ship_')
	
	def get_velocity(self):
		if self.is_ship:
			return 0
		
		type = self.type
		if type == 'blob':
			return 2.0
			
	def get_closest_player(self):
		closest_player = None
		closest_d = 999
		for player in self.scene.players:
			dx = player.real_x - self.real_x
			dy = player.real_y - self.real_y
			d = dx * dx + dy * dy
			
			if closest_player == None or closest_d > d:
				closest_player = player
				closest_d = d
		return (closest_player, dx, dy, closest_d ** .5)
			
	def get_direction_vector(self):
		if self.is_ship: return (0, 0)
		
		p = self.get_closest_player()
		player = p[0]
		dx = p[1]
		dy = p[2]
		distance = (dx * dx + dy * dy) ** .5
		v = self.get_velocity()
		if distance < v:
			return (0, 0)
		vx = v * p[1] / distance
		vy = v * p[2] / distance
		return (vx, vy)
		
	def Update(self):
		self.counter += 1
		
		if self.is_ship:
			grounded_for = 4 # seconds
			self.landed -= 5
			lift_off_at = grounded_for * -30 * 5
			if self.landed > 0:
				pass
			elif self.landed > lift_off_at:
				if self.counter % 15 == 0:
					spawn_type = '_'.join(self.type.split('_')[1:])
					self.scene.aliens.append(Alien(self.scene, spawn_type, 1, self.x, self.y + 8))
			else:
				if self.ship_elevation_offset() < -1200:
					self.expired = True
		elif self.type == 'blob':
			v = self.get_direction_vector()
			self.move(v[0], v[1])
		
	
	def ship_elevation_offset(self):
		if self.landed > 0:
			return -1 * self.landed
		if self.landed < -30 * 4 * 5: #on the ground for 4 seconds, 30 fps, counter goes by 5's
			return self.landed + 600
		return 0
	
	def move(self, dx, dy):
		self.real_x += dx
		self.real_y += dy
		self.x = int(self.real_x)
		self.y = int(self.real_y)
	
	def Render(self, screen):
		if self.is_ship:
			y = self.y + self.ship_elevation_offset()
			pygame.draw.ellipse(screen, (0, 0, 0), pygame.Rect(self.x - 20 - 2, y - 10 - 2, 44, 24))
			pygame.draw.ellipse(screen, (128, 128, 128), pygame.Rect(self.x - 20, y - 10, 40, 20))
			
		elif self.type == 'blob':
			pulse_period = 10
			t = self.counter % pulse_period
			t = t - pulse_period // 2
			if t < 0: t *= -1
			left = self.x - t - 3
			right = self.x + t + 3
			width = right - left
			top = self.y - 8 + t
			bottom = self.y + 5
			height = bottom - top
			pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(left, top, width, height))

class Weapon:
	def __init__(self, name):
		self.name = name
		self.init()

	def init(self):
		if self.name == 'shotgun':
			self.cooldown = 10
			self.triggered = True
		elif self.name == 'flamethrower':
			self.cooldown = 5
			self.triggered = False
	
	def make_bullets(self, player, x, y, ang):
		if self.name == 'shotgun':
			return [Bullet(True, player, x, y, ang, self)]
		return []

_weapon_store = {
	'shotgun' : Weapon('shotgun'),
	'flamethrower' : Weapon('flamethrower')
}

def get_weapon(name):
	global _weapon_store
	return _weapon_store[name]

class Player:
	def __init__(self, id, x, y):
		self.ID = id
		self.x = x
		self.y = y
		self.real_x = 0.0 + x
		self.real_y = 0.0 + y
		self.weapon = get_weapon('shotgun')
		self.last_fired = -999
		
	def move(self, dx, dy):
		self.real_x += dx
		self.real_y += dy
		self.x = int(self.real_x)
		self.y = int(self.real_y)
	
	def Render(self, screen, x, y):
		pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(x - 5, y - 5, 10, 10))

class PlayScene:
	
	def __init__(self):
		self.is_menu = False
		self.next = self
		self.players = [Player(1, 0, 0)]
		if get_player_input_source(2) != None:
			self.players.append(Player(2, 10, 0))
		self.bullets = []
		self.aliens = [Alien(self, 'ship_blob', 1, 500, 350)]
		self.counter = 0
		
	def ProcessInput(self, player_inputs):
		self.counter += 1
		for i in range(len(player_inputs)):
			player = self.players[i]
			input_source = get_player_input_source(i + 1)
			for event in player_inputs[i]:
				if event.down and event.command == 'trigger':
					self.fire_one_time_weapon(player)
				if input_source.joystick != None:
					shooting_vector = input_source.get_shooting_vector()
					if shooting_vector[0] != 0 or shooting_vector[1] != 0:
						self.fire_one_time_weapon(player, shooting_vector)
			d = self.get_movement_vector(input_source)
			v = 3
			player.move(d[0] * v, d[1] * v)
		
	def get_movement_vector(self, input_source):
		return input_source.get_movement_vector()
	
	def spawn_aliens(self):
		pass
	
	def Update(self, counter):
		
		self.spawn_aliens()
		
		new_bullets = []
		for bullet in self.bullets:
			bullet.Update()
			if bullet.x < -20 or bullet.x > 660 or bullet.y < -20 or bullet.y > 500:
				pass
			else:
				new_bullets.append(bullet)
		self.bullets = new_bullets
		
		used_bullets = []
		new_aliens = []
		for alien in self.aliens:
			alien.Update()
			dead = False
			used_bullet = None
			for bullet in self.bullets:
				dx = bullet.x - alien.x
				dy = bullet.y - alien.y
				d = dx * dx + dy * dy
				if d < 100:
					used_bullet = bullet
					dead = True
					break
			if used_bullet != None:
				self.bullets.remove(used_bullet)
			if not dead:
				new_aliens.append(alien)
			else:
				pass
				# TODO: play death noise
				# TODO: guts sprite!
		self.aliens = new_aliens
		
	def Render(self, screen):
		screen.fill((0, 100, 0))
		
		for alien in self.aliens:
			alien.Render(screen)
		
		for bullet in self.bullets:
			bullet.Render(screen)
		
		for player in self.players:
			player.Render(screen, player.x, player.y)
		
	
	def fire_one_time_weapon(self, player, vector=None):
		weapon = player.weapon		
		if player.last_fired + weapon.cooldown < self.counter:
			ang = self.get_shooting_angle(player, vector)
			x = player.real_x
			y = player.real_y
			bullets = weapon.make_bullets(player, x, y, ang)
			
			for b in bullets:
				self.bullets.append(b)

	def get_shooting_angle(self, player, vector):
		
		if vector == None:
			target = pygame.mouse.get_pos()
			
			dx = target[0] - player.real_x
			dy = target[1] - player.real_y
		else:
			dx = vector[0]
			dy = vector[1]
		
		while dx == 0 and dy == 0:
			dx = random.random() - .5
			dy = random.random() - .5
		distance = (dx * dx + dy * dy) ** .5
		vx = dx / distance
		vy = dy / distance
		
		return math.atan2(vy, vx)
		
		

class Bullet:
	def __init__(self, friendly, player_origin, x, y, angle, weapon):
		self.is_friendly = friendly
		self.origin = player_origin
		self.real_x = x
		self.real_y = y
		self.x = int(x)
		self.y = int(y)
		self.angle = angle
		v = self.velocity(weapon)
		self.vx = v * math.cos(angle)
		self.vy = v * math.sin(angle)
	
	def velocity(self, weapon):
		#TODO: this
		return 8
	
	def Update(self):
		self.real_x += self.vx
		self.real_y += self.vy
		self.x = int(self.real_x)
		self.y = int(self.real_y)
		
	def Render(self, screen):
		pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 2)

def get_marquee_x(counter, i):
	return i * 110 - counter * 3
	
def draw_marquee(screen, counter, y):
	i = 0
	items = get_random_items()
	
	while True:
		x = get_marquee_x(counter, i)
		while x < -200:
			i += 1
			x = get_marquee_x(counter, i)
			
		if x > 641:
			break
		item = items[i % len(items)]
		screen.blit(get_image('items_large/' + item + '.png'), (x, y))
		i += 1
		
class TitleScene:
	
	def __init__(self):
		self.is_menu = True
		self.next = self
		self.counter = 0
		self.raw_input_desired = False
		self.game_counter = 0
	def ProcessInput(self, player_inputs):
		for events in player_inputs:
			for event in events:
				if event.down:
					if event.command == 'eat':
						self.next = TransToMenuFromTitleScene()
				
				
	
	def Update(self, counter):
		self.game_counter = counter
	
	def Render(self, screen):
		self.counter += 1
		#screen.blit(get_image('title.png'), (0, 0))
		screen.fill((255, 255, 255))
		title = render_text("Shape Shifter", 72, (0, 0, 0))
		screen.blit(title, (320 - title.get_width() // 2, 30))
		c = int(min(255, max(0, abs((self.counter % 30) - 15) * 255 // 15)))
		pressEnter = render_text("Press ENTER. Or SPACE. Whichever.", 18, (c, c, c))
		screen.blit(pressEnter, (320 - pressEnter.get_width() // 2, 30 +  title.get_height() + 20))
		
		draw_marquee(screen, self.game_counter, 200)


_sounds = {}
def play_sound(file):
	global _sounds
	
	if _sounds.get(file) == None:
		
		path = 'sounds' + os.sep + file + '.wav'
		_sounds[file] = pygame.mixer.Sound(path)
		
	_sounds[file].play()
	

class TransToMenuFromTitleScene:
	def __init__(self):
		self.is_menu = True
		self.next = self
		self.y = 200
		self.raw_input_desired = False
		self.game_counter = 0
		play_sound('change')
		
	def ProcessInput(self, ignored):
		pass
	
	def Update(self, counter):
		self.game_counter = counter
		self.y += 8
		if self.y == 360:
			self.next = MainMenuB()
	
	def Render(self, screen):
		screen.fill((255, 255, 255))
		draw_marquee(screen, self.game_counter, self.y)

class MainMenuScene:
	
	def __init__(self):
		self.raw_input_desired = False
		self.is_menu = True
		self.next = self
		spacing = 60
		self.items = {
			'play' : ("Play Game", 10, 10),
			'config' : ("Configure Input", 10, 10 + spacing),
			'credits' : ("Credits", 400, 300),
			'classic' : ("The Classic", 400, 300 + spacing),
			'exit' : ("Quit", 400, 300 + spacing * 2)
		}
		self.mouse_over = None
		
	def ProcessInput(self, player_inputs):
		for events in player_inputs:
			for event in events:
				if event.command == 'trigger' and event.down:
					mouse_over = self.mouse_over
					if mouse_over != None:
						if mouse_over == 'play':
							self.next = PuzzlePlayScene(1, False)
						elif mouse_over == 'exit':
							self.next = None
						elif mouse_over == 'config':
							self.next = InputConfigScene()
						elif mouse_over == 'credits':
							self.next = CreditsScene()
						elif mouse_over == 'classic':
							self.next = ClassicScene()
	
	def Update(self, counter):
		pass

	def Render(self, screen):
		screen.blit(get_image('main_menu.png'), (0, 0))
		mouse_pos = pygame.mouse.get_pos()
		mx = mouse_pos[0]
		my = mouse_pos[1]
		self.mouse_over = None
		font_size = 48
		items = self.items
		for key in items.keys():
			item = items[key]
			text = item[0]
			x = item[1]
			y = item[2]
			text_img = render_text(text, font_size, (255, 255, 255))
			r = x + text_img.get_width()
			b = y + text_img.get_height()
			if mx <= r and mx >= x and my >= y and my <= b:
				self.mouse_over = key
				text_img = render_text(text, font_size, (255, 255, 0))
			
			screen.blit(text_img, (x, y))
			
		
		


_fonts = {}
_text_cache = {}
def render_text(text, size, color):
	global _fonts, _text_cache
	
	tkey = text + ':' + str(size) + str(color)
	image = _text_cache.get(tkey)
	if image != None:
		return image
	
	key = str(size)
	font = _fonts.get(key)
	if font == None:
		font = pygame.font.SysFont('foo', size)
		_fonts[key] = font
	
	image = font.render(text, True, color)
	_text_cache[tkey] = image
	
	return image


def save_input_config():
	global _configurations
	return
	lines = []
	for player in (1, 2):
		input = get_player_input_source(player)
		if input in _configurations:
			lines.append(str(player) + ':#' + str(_configurations.index(input)))
		else:
			lines.append(str(player) + ':#-1')
	for config in _configurations:
		if config.joystick != None:
			save = config.joystick.get_name() + "%%%%%"
			save += str(config.joystick_scale)
			for action in config.joystick_mapping.keys():
				save += '|'
				save += action
				c = config.joystick_mapping[action]
				save += ',' + ','.join(map(str, c))
			lines.append(save)
	output = '\n'.join(lines)
	c = open('joystick.txt', 'wt')
	c.write(output)
	c.close()

class ActiveItem:
	def __init__(self, theme, player):
		self.player = player
		#self.x = x
		#self.y = y
		self.theme = theme
		
	def Render(self, screen):
		colors = {
			'r' : 'red',
			'o' : 'orange',
			'y' : 'yellow',
			'g' : 'green',
			'b' : 'blue',
			'i' : 'purple'
		}
		
		if self.player.color in 'roygbi':
			image = get_image('images_large/' + self.theme + '_' + colors[self.player.color] + '.png')
			screen.blit(image, (self.x, self.y))

_race_winner_is = None

class PuzzlePlayScene:
	def __init__(self, mode):
		p = []
		default_width = 10
		self.raw_input_desired = False
		default_height = 18
		self.active_items = []
		#width, height, filled_rows, players, should_fall
		self.mode = mode
		if mode == '1player_clear':
			p = [PuzzlerInstance(default_width, default_height, 12, 1, False)]
			
			self.active_items.append(ActiveItem(p[0].theme, p[0].eaters[0]))
		elif mode == '1player_survival':
			p = [PuzzlerInstance(default_width, default_height, 6, 1, True)]
		elif mode == '2player_coop':
			p = [PuzzlerInstance(default_width + 4, default_height, 8, 2, True)]
		elif mode == '2player_vs':
			p = [PuzzlerInstance(default_width, default_height, 8, 1, True),
				 PuzzlerInstance(default_width, default_height, 8, 1, True)]
		elif mode == '2player_race':
			p = [PuzzlerInstance(default_width * 5 // 2 + 4, default_height * 2 // 3, default_height * 2 // 3, 2, False)]
			p[0].eaters[0].x = 0
			p[0].eaters[0].y = p[0].rows // 2
			p[0].eaters[1].x = p[0].cols - 1
			p[0].eaters[1].y = p[0].rows // 2
			
			r = 2
			for eater in p[0].eaters:
				x = eater.x
				y = eater.y
				
				for tx in range(x - r, x + r + 1):
					for ty in range(y - r, y + r + 1):
						if tx >= 0 and tx < p[0].cols:
							p[0].grid[tx][ty] = None
			x = p[0].cols // 2
			y = p[0].rows // 2
			p[0].grid[x][y] = 'x'
		else:
			print("A catastrophic error has occured. Barracade doors and windows. Hoard iodine. Hide under desk. Cover head. ")
			
		self.next = self
		self.is_menu = False
		self.puzzles = p
		self.winner_index = -1
		
	def ProcessInput(self, player_inputs):
		if len(self.puzzles) == 1:
			self.puzzles[0].ProcessInput(player_inputs)
		else:
			for i in range(len(self.puzzles)):
				self.puzzles[i].ProcessInput([player_inputs[i]])
	
	def Update(self, counter):
		global _race_winner_is
		winner_index = -1
		has_winner = False
		i = 0
		for p in self.puzzles:
			p.Update()
			if str(p.win) != "False":
				has_winner = True
				
				if str(p.win) == "True":
					winner_index = i
				else:
					winner_index = int(p.win)
				
				if len(self.puzzles) == 1 and len(self.puzzles[0].eaters) == 2:
					if self.mode.find('race') != -1:
						if 0 == _race_winner_is:
							i =0
						else: i = 1
							
						self.next = ResultScreen(self, "Player " + str(i + 1))
						play_sound('win')
					else:
						self.next = ResultScreen(self, "You Win!", True, True)
						play_sound('win')
				else:
					self.next = ResultScreen(self, "Player " + str(i + 1))
					play_sound('win')
			elif str(p.lose) != "False":
				
				has_winner = True
				if len(self.puzzles) == 1:
					self.next = ResultScreen(self, "CRASH!", False)
					play_sound('lose')
				elif len(self.puzzles) > 0:
					winner_index = 1 - i # OMGHAX
					if str(p.lose) != "True":
						winner_index = 1 - int(p.lose)
					self.next = ResultScreen(self, "Player " + str(winner_index + 1))
					play_sound('win')
				
			i += 1
	
	def get_eater_anim_color(self, eater):
		
		cs = []
		for colors in (eater.last_color, eater.color):
			if eater.color == 'w':
				color = (180, 180, 180)
			elif eater.color == 'x':
				color = (60, 60, 60)
			else:
				color = get_color_lookup()[eater.color]
			cs.append(color)
		
		if eater.since_last_eat < 14:
			a = cs[0]
			b = cs[1]
			p = eater.since_last_eat / 14.0
			ap = 1.0 - p
			
			t = (
				max(0, min(255, int(p * a[0] + ap * b[0]))),
				max(0, min(255, int(p * a[1] + ap * b[1]))),
				max(0, min(255, int(p * a[2] + ap * b[2])))
				)
			
			return (t, p)
		#TODO: animate transition
		return (color, 1.0)
	def RenderEater(self, win_mode, screen, x, y, eater):
		
		color = self.get_eater_anim_color(eater)
		pygame.draw.rect(screen, color[0], pygame.Rect(x, y, 99, 99))
		
		
		eater_counter = eater.since_last_eat
		shifts = (1, 2, 3, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2)
		
		if win_mode != None:
			if win_mode == True:
				screen.blit(get_image('muncher/happy.png'), (x, y))
			else:
				screen.blit(get_image('muncher/dead.png'), (x, y))
			return
			
		if eater_counter < len(shifts):
			
			i = shifts[eater_counter]
			screen.blit(get_image('muncher/shift_'+str(i)+'.png'), (x, y))
		else:
			norms = (1, 2, 3, 4, 5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2)
			norm_i = norms[(eater.counter // 2)% len(norms)]
			screen.blit(get_image('muncher/norm_'+str(norm_i)+'.png'), (x, y))
		
	def Render(self, screen, win_mode=None):
		screen.fill((255, 255, 255))
		puzzle_screens = []
		for p in self.puzzles:
			puzzle_screens.append(p.Render())
		
		coords = self.get_board_coords(puzzle_screens)
		
		i = 0
		for p in puzzle_screens:
			screen.blit(p, coords[i])
			i += 1
		
		
		if self.mode in ('1player_survival', '1player_clear') :
			if win_mode == True: win_mode = 1
			self.RenderEater(win_mode, screen, coords[0][0] - 110, coords[0][1], self.puzzles[0].eaters[0])
		elif self.mode == '2player_vs':
			if win_mode != None:
				self.RenderEater(win_mode == 1, screen, coords[0][0] - 110, coords[0][1], self.puzzles[0].eaters[0])
				self.RenderEater(win_mode == 2, screen, coords[1][0] + puzzle_screens[1].get_width() + 10, coords[1][1] + puzzle_screens[1].get_height() - 100, self.puzzles[1].eaters[0])
			else:
				self.RenderEater(None, screen, coords[0][0] - 110, coords[0][1], self.puzzles[0].eaters[0])
				self.RenderEater(None, screen, coords[1][0] + puzzle_screens[0].get_width() + 10, coords[1][1] + puzzle_screens[1].get_height() - 100, self.puzzles[1].eaters[0])
		elif self.mode == '2player_coop':
			if win_mode != None:
				if str(win_mode) != 'False':
					win_mode = True
			self.RenderEater(win_mode, screen, coords[0][0] - 110, coords[0][1], self.puzzles[0].eaters[0])
			self.RenderEater(win_mode, screen, coords[0][0] + puzzle_screens[0].get_width() + 10, coords[0][1] + puzzle_screens[0].get_height() - 100, self.puzzles[0].eaters[1])
		elif self.mode == '2player_race':
			if win_mode != None:
				self.RenderEater(win_mode == 1, screen, coords[0][0], coords[0][1] - 110, self.puzzles[0].eaters[0])
				self.RenderEater(win_mode == 2, screen, coords[0][0] + puzzle_screens[0].get_width() - 110, coords[0][1] + puzzle_screens[0].get_height() + 10, self.puzzles[0].eaters[1])
			else:
				self.RenderEater(None, screen, coords[0][0], coords[0][1] - 110, self.puzzles[0].eaters[0])
				self.RenderEater(None, screen, coords[0][0] + puzzle_screens[0].get_width() - 110, coords[0][1] + puzzle_screens[0].get_height() + 10, self.puzzles[0].eaters[1])
		
	def get_board_coords(self, puzzle_screens):
		
		count = len(puzzle_screens)
		width = puzzle_screens[0].get_width()
		height = puzzle_screens[0].get_height()
		
		space = 640 - width * count
		space = space // (count + 1)
		
		
		output = []
		
		i = 0
		for p in puzzle_screens:
			output.append( (space * (i + 1) + i * width, (480 - height) // 2))
			i += 1
			
		if self.mode == '2player_vs':
			output[0] = (output[0][0] + 33, output[0][1])
			output[1] = (output[1][0] - 33, output[1][1])
		
		return output
class Eater:
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color
		self.last_color = color
		self.direction = 'up'
		self.counter = 0
		self.since_last_eat = 99999
	
	def do_changing_color(self):
		self.since_last_eat = 0
	
	def render(self, screen, cell_width):
		self.since_last_eat += 1
		self.counter += 1
		cx = int((self.x + .5) * cell_width)
		cy = int((self.y + .5) * cell_width)
		radius = cell_width // 2
		ang_offset = 3.14159 * -.5 # up
		if self.direction == 'down': ang_offset += 3.14159
		elif self.direction == 'left': ang_offset += 3.14159 * 3 / 2
		elif self.direction == 'right': ang_offset += 3.14159 / 2
		
		if self.color == 'x':
			c = min(255, max(0, abs((self.counter % 50) - 25) * 255 // 25))
			color = (c, c, c)
		else:
			color = get_color_lookup()[self.color]
		
		x = math.cos(ang_offset + 0) * radius / 4 + cx
		y = math.sin(ang_offset + 0) * radius / 4 + cy
		points = [(int(x), int(y))]
		
		i = 0
		begin = 0.25 * 3.14159
		end = 1.75 * 3.14159 
		while i <= 12:
			ang = (begin * i + end * (12 - i)) / 12
			points.append((
				int(math.cos(ang + ang_offset) * radius + cx),
				int(math.sin(ang + ang_offset) * radius + cy)
				))
			i += 1
		pygame.draw.polygon(screen, color, points)
		pygame.draw.polygon(screen, (0, 0, 0), points, 2)

_colors = {
			'w' : (255, 255, 255),
			'r' : (255, 0, 0),
			'o' : (255, 128, 0),
			'y' : (255, 255, 0),
			'g' : (0, 200, 60),
			'b' : (0, 80, 255),
			'i' : (160, 0, 160)
		}
def get_color_lookup():
	global _colors
	return _colors

_random_items= None
def get_random_items():
	global _random_items
	if _random_items == None:
		themes = get_theme_list()
		output = []
		for theme in themes:
			for color in 'red green blue yellow orange purple'.split():
				output.append(theme + '_' + color)
		
		random.shuffle(output)
		_random_items = output
	return _random_items


def make_grid(w, h, defaultValue=None):
	cols = []
	x = 0
	while x < w:
		col = []
		y = 0
		while y < h:
			col.append(defaultValue)
			y += 1
		x += 1
		cols.append(col)
	return cols

class ResultScreen:
	
	def __init__(self, bg, winner_name, is_win=True, blarg = False):
		self.bg = bg
		self.next = self
		self.winner = (1, 2)[winner_name.find('2') != -1] # OMG HAX
		if blarg:
			self.text = winner_name
		else:
			self.text= winner_name + " Wins!"
		if not is_win:
			self.text = "CRASH!"
		self.can_leave = False
		self.is_menu = True
		self.counter = 0
		self.raw_input_desired = False
		self.text_color = (255, 255, 0)
		if not is_win: self.text_color = (0, 0, 0)
		self.overlay = pygame.Surface((640, 480)).convert_alpha()
		c = (0, 0, 0, 100)
		if not is_win:
			c = (255, 0, 0, 100)
		pygame.draw.rect(self.overlay, c, pygame.Rect(0, 0, 640, 480))
		
	def ProcessInput(self, player_input):
		if self.can_leave:
			for events in player_input:
				for event in events:
					if event.down and event.command == 'eat':
						self.next = MainMenuB()
	
	def Update(self, counter):
		self.counter += 1
		if self.counter > 60:
			self.can_leave = True
		
	def Render(self, screen):
		status = self.winner
		if self.text == 'CRASH!':
			status = False
		self.bg.Render(screen, status)
		screen.blit(self.overlay, (0, 0))
		text = render_text(self.text, 72, self.text_color)
		screen.blit(text, (320 - text.get_width() // 2, 240 - text.get_height() // 2))

class PuzzlerInstance:
	
	def __init__(self, width, height, filled_rows, players, should_fall):
		self.theme = random.choice(get_theme_list())
		self.raw_input_desired = False
		self.next = None
		self.tile_cache = {
			'r': get_image('items_small/' + self.theme + '_red.png'),
			'o': get_image('items_small/' + self.theme + '_orange.png'),
			'y': get_image('items_small/' + self.theme + '_yellow.png'),
			'g': get_image('items_small/' + self.theme + '_green.png'),
			'b': get_image('items_small/' + self.theme + '_blue.png'),
			'i': get_image('items_small/' + self.theme + '_purple.png')
		}
		rows = filled_rows
		self.eaters = []
		self.win = False
		self.lose = False
		startX = width // 2 - (players * 2 - 1) // 2
		for i in range(players):
			self.eaters.append(Eater(startX + 2 * i, 15, 'r'))
		self.game_counter = 0
		self.pixel_width = 20
		self.should_fall = should_fall
		self.rows = height
		self.cols = width
		self.grid = make_grid(self.cols, self.rows)
		self.screen = pygame.Surface((self.pixel_width * self.cols, self.pixel_width * self.rows))
		self.screen = self.screen.convert_alpha()
		colors = 'r o y g b i'.split()
		self.totals = {}
		for c in colors:
			self.totals[c] = 0
		for y in range(rows):
			for x in range(self.cols):
				c = random.choice(colors)
				self.totals[c] += 1
				self.grid[x][y] = c
		self.last_fall = 0

	def try_nibble(self, player_index):
		global _race_winner_is
		eater = self.eaters[player_index]
		x = eater.x
		y = eater.y
		tx = x
		ty = y
		d = eater.direction
		if d == 'up':
			ty -= 1
		elif d == 'down':
			ty += 1
		elif d == 'left':
			tx -= 1
		elif d == 'right':
			tx += 1
		
		if tx >= 0 and tx < self.cols and ty >= 0 and ty < self.rows:
			color = self.grid[tx][ty]
			
			if color != None:
				your_color = eater.color
				
				if color == your_color:
					self.spill_alg(tx, ty)
					play_sound('change')
				elif color == 'x':
					your_color = 'x'
					_race_winner_is = player_index
					self.grid[tx][ty] = None
					self.win = player_index
				else:
					self.grid[tx][ty] = your_color
					eater.last_color = your_color
					eater.color = color
					eater.do_changing_color()
					self.totals[your_color] += 1
					self.totals[color] -= 1
					play_sound('click')
		colors_left = []
		for c in filter(lambda x:self.totals[x] > 0, self.totals.keys()):
			colors_left.append(c)
		for eater in self.eaters:
			if not eater.color in colors_left:
				eater.color = 'w' if len(colors_left) == 0 else random.choice(colors_left)
				
				if eater.color == 'w':
					self.win = True

	def spill_alg(self, tx, ty):
		queue = [(tx, ty)]
		color = self.grid[tx][ty]
		while len(queue) > 0:
			item = queue[0]
			queue = queue[1:]
			x = item[0]
			y = item[1]
			if self.grid[x][y] != None:
				self.grid[x][y] = None
				self.totals[color] -= 1
				for n in ((-1, 0), (1, 0), (0, -1), (0, 1)):
					tx = x + n[0]
					ty = y + n[1]
					if tx >= 0 and tx < self.cols and ty >= 0 and ty < self.rows:
						if self.grid[tx][ty] == color:
							queue.append((tx, ty))

	
	def ProcessInput(self, player_inputs):
		
		if len(self.eaters) == 1 and len(player_inputs) > 1:
			down = {}
			up = {}
			t = []
			for players in player_inputs:
				for event in players:
					a = event.command
					d = event.down
					if d:
						if down.get(a) == None:
							down[a] = True
							t.append(MyEvent(a, d))
					else:
						if up.get(a) == None:
							up[a] = True
							t.append(MyEvent(a, d))
			player_inputs = [t]
						
			#player_inputs = [player_inputs[0] + player_inputs[1] + player_inputs]
		
		for i in range(len(self.eaters)):
			eater = self.eaters[i]
			x = eater.x
			y = eater.y
			dx = 0
			dy = 0
			for event in player_inputs[i]:
				if event.down:
					if event.command == 'up':
						dy = -1
						eater.direction = 'up'
					elif event.command== 'down':
						dy = 1
						eater.direction = 'down'
					elif event.command == 'left':
						dx = -1
						eater.direction = 'left'
					elif event.command == 'right':
						dx = 1
						eater.direction = 'right'
					elif event.command in ('action', 'eat', 'trigger'):
						self.try_nibble(i)
			
			if dx != 0 or dy != 0:
				nx = dx + x
				ny = dy + y
				
				# try move x
				if nx < 0 or nx >= self.cols:
					pass 
					# TODO: thunk noise
				else:
					if self.grid[nx][y] == None:
						x = nx
				
				# try move y
				if ny < 0 or ny >= self.rows:
					pass
					# TODO: thunk noise
				else:
					if self.grid[x][ny] == None:
						y = ny
				
				eater.x = x
				eater.y = y
				
		
	def resynch_counter(self):
		self.totals = {}
		for t in 'r o y g b i'.split():
			self.totals[t] = 0
		x = 0
		width = self.cols
		height = self.rows
		while x < width:
			y = 0
			while y < height:
				c = self.grid[x][y]
				if c != None:
					self.totals[c] += 1
				y += 1
			x += 1
	def Update(self):
		self.game_counter += 1
		if self.should_fall:
			diff = self.game_counter - self.last_fall
			# TODO: make it speed up with time
			max_diff = 30 * 10
			if diff > max_diff:
				self.do_fall()
	
	def do_fall(self):
		self.last_fall = self.game_counter
		crash = False
		for eater in self.eaters:
			eater.y += 1
			if eater.y >= self.rows:
				eater.y -= 1
				if self.grid[eater.x][eater.y] != None:
					crash = True
					self.lose = True
		x = 0
		width = self.cols

		while x < width:
			col = self.grid[x]
			if col[-1] != None:
				crash = True
				self.lose = True
				break
			x += 1
		
		colors = []
		for c in self.totals.keys():
			if self.totals[c] != 0:
				colors.append(c)
		
		
		if not crash and len(colors) > 0:
			x = 0
			while x < width:
				col = self.grid[x]
				c = random.choice(colors)
				self.totals[c] += 1
				self.grid[x] = [c] + col[:-1]
				x += 1
		
		
			
	def Render(self):
		
		width = self.cols
		height = self.rows
		screen = self.screen
		pw = self.pixel_width
		screen.fill((0, 0, 0, 128))
		colors = get_color_lookup()
		x = 0
		while x < width:
			y = 0
			while y < height:
				
				v = self.grid[x][y]
				if v != None:
					color = colors.get(v, None)
					if v == 'x':
						c = min(255, max(0, abs((self.game_counter % 50) - 25) * 255 // 25))
						color = (c, c, c)
					if color != None:
						if v in 'roygbi':
							screen.blit(self.tile_cache[v], (x * pw, y * pw))
								
						else:
							pygame.draw.circle(screen, color, (x * pw + pw // 2, y * pw + pw // 2), pw // 2)
				
				y += 1
			x += 1
		
		for eater in self.eaters:
			eater.render(screen, pw)
		return screen

class CreditsScene:
	def __init__(self):
		self.next = self
		self.is_menu = True
		self.raw_input_desired = False
		
	def Update(self, counter):
		pass
	
	def ProcessInput(self, player_inputs):
		for events in player_inputs:
			for event in events:
				if event.down and event.command in ('start', 'action', 'eat', 'trigger'):
					self.next = MainMenuB()
	
	def Render(self,screen):
		screen.fill((255, 255, 255))
		img = render_text('Blake did EVERYTHING!', 72, (0, 0, 0))
		screen.blit(img, (320 - img.get_width() // 2, 240 - img.get_height() // 2))
	
class TutorialScene:
	def __init__(self):
		self.raw_input_desired = False
		self.next = self
		self.is_menu = True
		self.page = 0
		self.total_pages = 6
		self.pages = map(get_image, map(
			lambda x: 'tutorials/page' + str(x) + '.jpg',
			range(1, self.total_pages + 1)))
		f = []
		for page in self.pages:
			f.append(page)
		
		self.pages = f
	
	def Update(self, counter):
		pass
	
	def ProcessInput(self, player_inputs):
		for events in player_inputs:
			for event in events:
				if event.down and event.command in ('start', 'action', 'eat', 'trigger'):
					self.page += 1
					if self.page >= self.total_pages:
						self.next = MainMenuB()
						self.page -= 1
	
	def Render(self,screen):
		screen.blit(self.pages[self.page], (0, 0))
	
	

class MainMenuB:
	def __init__(self):
		self.raw_input_desired = False
		self.next = self
		self.is_menu = True
		self.cursor = 'configure_input'
		self.last_1p_mode = '1player_survival'
		self.last_2p_mode = '2player_coop'
	
	def GoToNextScene(self, key):
		if key == 'configure_input':
			self.next = NewICScene()
		elif key == 'tutorial':
			self.next = TutorialScene()
		elif key == 'credits':
			self.next = CreditsScene()
		else:
			self.next = PuzzlePlayScene(key)
		play_sound('change')
	
	def ProcessInput(self, player_inputs):
		
		dx = 0
		dy = 0
		
		for events in player_inputs:
			for event in events:
				if event.down:
					if event.command == 'up':
						dy = -1
					elif event.command == 'down':
						dy = 1
					elif event.command == 'left':
						dx = -1
					elif event.command == 'right':
						dx = 1
					elif event.command == 'eat':
						self.GoToNextScene(self.cursor)
		
		pc = self.cursor
		if self.cursor == 'configure_input':
			if dy == 1:
				self.cursor = 'tutorial'
		elif self.cursor == 'tutorial':
			if dy == -1:
				self.cursor = 'configure_input'
			elif dy == 1:
				self.cursor = self.last_1p_mode
		elif self.cursor == '1player_survival':
			if dx == 1:
				self.cursor = '1player_clear'
				self.last_1p_mode = self.cursor
			elif dy == -1:
				self.cursor = 'tutorial'
			elif dy == 1:
				self.cursor = self.last_2p_mode
		elif self.cursor == '1player_clear':
			if dx == -1:
				self.cursor = '1player_survival'
				self.last_1p_mode = self.cursor
			elif dy == -1:
				self.cursor = 'tutorial'
			elif dy == 1:
				self.cursor = self.last_2p_mode
		elif self.cursor.startswith('2player_'):
			if dy == -1:
				self.cursor = self.last_1p_mode
			elif dy == 1:
				self.cursor = 'credits'
			elif dx != 0:
				if self.cursor == '2player_coop':
					if dx == 1:
						self.cursor = '2player_vs'
						self.last_2p_mode = self.cursor
				elif self.cursor == '2player_race':
					if dx == -1:
						self.cursor = '2player_vs'
						self.last_2p_mode = self.cursor
				elif self.cursor == '2player_vs':
					if dx == 1:
						self.cursor = '2player_race'
					elif dx == -1:
						self.cursor = '2player_coop'
					self.last_2p_mode = self.cursor
		elif self.cursor == 'credits':
			if dy == -1:
				self.cursor = self.last_2p_mode
			
		if self.cursor != pc:
			play_sound('click')
	def Update(self, counter):
		self.counter = counter
	
	def Render(self, screen):
		screen.fill((255, 255, 255))
		counter = self.counter
		
		left = 100
		
		# configure input
		y = 50
		img = render_text('Configure Input', 24, self.GetTextColor('configure_input', counter))
		screen.blit(img, (left, y))
		if self.cursor == 'configure_input':
			self.RenderCursor(left - 30, y, counter, screen)
		
		# tutorial
		y += 50
		img = render_text("Tutorialification", 24, self.GetTextColor('tutorial', counter))
		screen.blit(img, (left, y))
		if self.cursor == 'tutorial':
			self.RenderCursor(left - 30, y, counter, screen)
		
		# 1 player
		y += 50
		img = render_text("Single Player Modes", 24, (0, 0, 0))
		screen.blit(img, (left, y))
		
		# 1 player - survival
		y += 30
		img = render_text("Survival Mode", 36, self.GetTextColor('1player_survival', counter))
		screen.blit(img, (left + 50, y))
		if self.cursor == '1player_survival':
			self.RenderCursor(left + 50 - 30, y, counter, screen)
		
		# 1 player - clear
		img = render_text("Clear Mode", 36, self.GetTextColor('1player_clear', counter))
		screen.blit(img, (left + 300, y))
		if self.cursor == '1player_clear':
			self.RenderCursor(left + 300 - 30, y, counter, screen)
		
		# 2 player
		y += 50
		img = render_text("Two Player Modes", 24, (0, 0, 0))
		screen.blit(img, (left, y))
		
		# 2 player - Co-op
		y += 30
		img = render_text("Co-op", 36, self.GetTextColor('2player_coop', counter))
		screen.blit(img, (left + 50, y))
		if self.cursor == '2player_coop':
			self.RenderCursor(left + 50 - 30, y, counter, screen)
		
		# 2 player - Vs
		img = render_text("Versus", 36, self.GetTextColor('2player_vs', counter))
		screen.blit(img, (left + 200, y))
		if self.cursor == '2player_vs':
			self.RenderCursor(left + 200 - 30, y, counter, screen)
		
		# 2 player - Race
		img = render_text("Race", 36, self.GetTextColor('2player_race', counter))
		screen.blit(img, (left + 370, y))
		if self.cursor == '2player_race':
			self.RenderCursor(left + 370 - 30, y, counter, screen)
		
		# Credits
		y += 50
		img = render_text("Credits", 24, self.GetTextColor('credits', counter))
		screen.blit(img, (left, y))
		if self.cursor == 'credits':
			self.RenderCursor(left - 30, y, counter, screen)
		
		
		draw_marquee(screen, self.counter, 360)
		
	def RenderCursor(self, x, y, counter, screen):
		pygame.draw.rect(screen, self.GetTextColor(self.cursor, counter), pygame.Rect(x, y, 20, 20))
		
	def GetTextColor(self, key, counter):
		
		if key != self.cursor:
			return (0, 0, 0)
			
		p = min(1.0, max(0, abs((counter % 30) - 15) / 15.0))
		
		c = (255, 255, 255)
		if key == 'configure_input':
			c = (0, 128, 255)
		elif key == 'tutorial':
			c = (255, 220, 0)
		elif key.startswith('1player_'):
			c = (255, 0, 0)
		elif key.startswith('2player_'):
			c = (0, 255, 0)
		elif key == 'credits':
			c = (255, 0, 255)
		r = int(c[0] * p)
		g = int(c[1] * p)
		b = int(c[2] * p)
		
		return (r, g, b)
def main():
	global _debug_buffer, _debug_disabled
	
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	initialize_input_config_defaults()
	
	
	debug_screen = pygame.Surface((640, 480)).convert()
	debug_screen.fill((0, 0, 0))
	debug_screen.set_alpha(80)
	
	scene = TitleScene()
	counter = 0
	fps = 30.0
	
	while scene != None:
		
		start = time.time()
		
		events = get_players_input(scene.is_menu, scene.raw_input_desired)
		scene.ProcessInput(events)
		scene.Update(counter)
		scene.Render(screen)
		
		if not _debug_disabled and len(_debug_buffer) != 0:
			y = 0
			debug_screen.fill((0, 0, 0))
			for line in _debug_buffer[::-1]:
				debug_screen.blit(line, (5, y + 5))
				y += line.get_height() + 5
			screen.blit(debug_screen, (0, 0))
		
		pygame.display.flip()
		
		scene = scene.next
		
		if is_quit_attempted():
			scene = None
		
		counter += 1
		
		end = time.time()
		
		diff = end - start
		delay = 1.0 / fps - diff
		if delay > 0:
			time.sleep(delay)
	
	save_input_config()

main()