from huepy import cyan, bold

menu_sites = {
	"Social Media": {
		"Facebook",
		"Google",
		"LinkedIn",
		"Twitter",
		"Instagram",
		"Snapchat",
		"FbRobotCaptcha",
		"VK",
		"Github",
	},
	"Others": {
		"StackOverflow",
		"Wordpress",
		"Steam",
	}
}

SF_PROMPT = cyan(" SF > ")

def colorize_option(chave, valor):
	'''
	Based on index type format and print out menu options.
	'''
	if type(chave) == int:
		selector = cyan(' [') + bold(cyan('%s')) + cyan('] ')
		suffix = cyan('%s\n') 
		return selector % chave + suffix % valor
	if type(chave) == str:
		pos = valor.lower().find(chave)
		prefix, radical, suffix = valor.partition(valor[pos])
		if prefix:
			prefix = cyan('%s')
		radical = cyan('[') + bold(cyan('%s' % radical))+ cyan(']')
		return ' %s%s%s\n' % (prefix, radical, suffix)

def build_options(dict_menu):
	'''
	Returns tuple of numbereded options.
	'''
	return enumerate(dict_menu, 1)

def ask_user(prompt: str, options: dict):
	'''
	Print prompt and verifies if the answer is in options.keys
	'''
	while True:
		resp = input(prompt)
		try:
			resp = int(resp)
		except ValueError:
			'''If cannot be converted to int, its a string option.'''
			pass
		if resp in options.keys():
			return options[resp]

def get_option(prompt: str, options: dict):
	'''
	Print out options and prompt user.
	'''
	for k, v in options.items():
		print(colorize_option(k,v))
	return ask_user(prompt, options)

def get_letters(opts: list):
	'''
	Return a tuple of unique letter for each word, to build options 
	for menu.
	'''
	selected = []
	for word in opts:
		ch = word.lower()
		if ch[:1] in selected:
			l = set(ch).difference(set(selected))
			sl = min(ch.index(c) for c in l)
			selected.append(ch[sl])
		else:
			selected.append(ch[:1])
	return zip(selected, opts)

def build_menu(dict_menu: dict, prompt: str=None, numerate: bool=True):
	if not prompt:
		prompt = "\n => "
	numdict = { True: build_options, False: get_letters }
	menu = numdict[numerate](dict_menu)
	resp = get_option(prompt, dict(menu))
	return resp

def main_menu():
	print(cyan('\n Select an option\n'))
	net_menu = build_menu(menu_sites, SF_PROMPT, False)
	return build_menu(menu_sites[net_menu], SF_PROMPT)	