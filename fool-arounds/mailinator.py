from pymailinator.wrapper import Inbox
import time
api_key = '31299e973389e4445288424670ec307d36'

if __name__ == '__main__':
	inbox = Inbox(api_key)
	attempts = 0
	while True:
		try:
			box = inbox.get(mailbox='gerry_dropbox6')
			first = box[0]
			break
		except IndexError:
			attempts += 1
			if attempts == 30:
				raise Exception('timeout_dude')
			else:
				time.sleep(10)
				pass
	first.get_message()
	body = first.body

	import pdb
	pdb.set_trace()