import discord
import random
import re
import time
import unicodedata


class Name:
    def __init__(self, content, classifier_single=None, classifier_multiple=None):
        self.content = content
        self.classifier_single = classifier_single
        self.classifier_multiple = classifier_multiple
        self.random_generator = random.Random()

    def flip_coin(self):
        return self.random_generator.randint(0, 1) == 1

    def get(self, no_measure):
        if not no_measure:
            if self.classifier_multiple and self.flip_coin():
                if self.flip_coin():
                    return '你哋呢' + self.classifier_multiple + self.content
                else:
                    return self.classifier_multiple + self.content
            elif self.classifier_single and self.flip_coin():
                return '你呢' + self.classifier_single + self.content
        return self.content


class Sentence:
    def __init__(self, content, prefix, suffix, particle, no_measure, no_pronoun, no_emoji):
        self.content = content
        self.prefix = prefix
        self.suffix = suffix
        self.particle = particle
        self.no_measure = no_measure
        self.no_pronoun = no_pronoun
        self.no_emoji = no_emoji
        self.names = [
            Name('毒撚', '個', '啲'),
            Name('死毒撚', '個', '啲'),
            Name('柒頭', '條', '啲'),
            Name('on9', '條', '啲'),
            Name('單身狗', '隻', '啲'),
            Name('處男', '個', '啲'),
            Name('青頭仔', '個', '啲'),
            Name('變態佬', '個', '啲'),
            Name('死變態佬', '個', '啲')
        ]
        self.name_pronouns = [Name('你'), Name('你哋')]
        self.emoji = ['7.7', '7.777', ':)', ':(', '</3', r'\\./', 'T^T']
        self.random_generator = random.Random()

    def flip_coin(self):
        return self.random_generator.randint(0, 1) == 1

    def is_half_to_half(self, s1, s2):
        return unicodedata.east_asian_width(s1[-1]) != 'W' and unicodedata.east_asian_width(s2[0]) != 'W'

    def get(self):
        final_content = self.content
        name_list = self.names.copy()
        if not self.no_pronoun:
            name_list.extend(self.name_pronouns)

        index = self.random_generator.randint(0, len(name_list) - 1)
        name_ = name_list[index].get(self.no_measure)

        if self.suffix and self.flip_coin():
            if self.particle:
                final_content += self.particle

            if self.is_half_to_half(final_content, name_):
                final_content += ' '

            final_content += name_
        elif self.prefix:
            final_content = name_

            if self.is_half_to_half(name_, final_content):
                final_content += ' '

            final_content += self.content

        if not self.no_emoji and self.flip_coin():
            index = self.random_generator.randint(0, len(self.emoji) - 1)
            emoji_ = self.emoji[index]

            if self.is_half_to_half(final_content, emoji_):
                final_content += ' '

            final_content += emoji_

        return final_content


class Fake_MKMui:
    def __init__(self):
        self.replies = [
            Sentence('OK 898', False, False, '', False, False, True),
            Sentence('唔想理你', False, False, '', False, False, False),
            Sentence('八八冇LU', False, False, '', False, False, False),
            Sentence('dont ff', True, False, 'la', True, False, False),
            Sentence('LAAN', True, True, '啦', True, False, True),
            Sentence('收皮', True, True, '啦', True, False, False),
            Sentence('食屎', True, True, '啦', True, False, False),
            Sentence('死開', True, True, '啦', True, False, False),
            Sentence('躝開', True, True, '啦', True, False, False),
            Sentence('畀錢我先', True, True, '啦', True, False, False),
            Sentence('真係好撚恐怖', True, False, '', False, False, False),
            Sentence('真係好撚kam', True, False, '', False, False, False),
            Sentence('關我咩事呢', False, True, '', True, True, False),
            Sentence('關你咩事呢', False, True, '', True, True, False),
            Sentence('關你哋咩事呢', False, True, '', True, True, False),
            Sentence('瞓啦', False, True, '', True, False, False)
        ]
        self.replies_to_empty = [
            Sentence('??', False, False, '', True, True, True),
            Sentence('jm9', False, False, '??', True, True, False),
        ]
        self.replies_discord = [
            Sentence(':middle_finger:', False, False, '', False, False, True),
            Sentence(':thumbsdown:', False, False, '', False, False, True)
        ]
        self.replies_greeting = [
            Sentence('瞓啦柒頭', False, False, '', True, True, False),
            Sentence('瞓啦染頭', False, False, '', True, True, False),
            Sentence('瞓啦', False, True, '', True, False, False),
        ]
        self.replies_greeting_hi = [
            Sentence('閪佬', False, True, '', True, True, False),
            Sentence('hi', False, True, '', True, True, False),
        ]
        self.replies_greeting_bye = [
            Sentence('898', False, False, '', True, True, False),
            Sentence('bibi', True, True, '', True, True, False),
        ]
        self.random_generator = random.Random()
    
    @property
    def keywords(self):
        return ['$娘娘', '$牙娘', '$阿娘', '$mk妹']
        
    def read(self, input_string):
        for keyword in self.keywords:
            if input_string.lower().startswith(keyword):
                return input_string[len(keyword):].strip()
        return None  # Not triggered
        
    def __pick(self, L):
        return L[self.random_generator.randint(0, len(L) - 1)].get()

    def reply(self, discord):
        all_replies = self.replies.copy()
        if discord:
            all_replies.extend(self.replies_discord)
        return self.__pick(all_replies)

    def reply_to_empty(self):
        return self.__pick(self.replies_to_empty)
        
    def reply_to_greeting(self, type_=''):
        replies_greeting = self.replies_greeting.copy()
        if type_ == 'hi':
            replies_greeting.extend(self.replies_greeting_hi)
        elif type_ == 'bye':
            replies_greeting.extend(self.replies_greeting_bye)
        return self.__pick(replies_greeting)


class Fake_MKMui_deploy(discord.Client):
    def __init__(self, *args, **kwargs):
        self.fake_mkmui = Fake_MKMui()
        self.memory = dict()
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'{self.user}駕到！')
        
    
    async def on_disconnect(self):
        print(f'{self.user}斷線！')
        raise RuntimeError('Disconnected.')
        
    
    async def on_message(self, message):
        if message.author == self.user:
            return

        if isinstance(message.channel, discord.DMChannel):
            content = message.content.strip()
            if content:
                if content == '$del':
                    if user in self.memory:
                        del self.memory[user]
                        await message.reply(f'del 鳥！下次覆你唔會講呢句嘢！', mention_author=False)
                    else:
                        await message.reply(f'冇任何資料 7.7', mention_author=False)
                else:
                    self.memory[message.author] = message.content
                    await message.reply(f'下次覆你就會講呢句！', mention_author=False)
            else:
                await message.reply(f'屌你係咪唔識打字 7.777', mention_author=False)
            return

        read_content = self.fake_mkmui.read(message.content)
        if read_content is None:
            return

        if read_content:
            if message.author in self.memory:
                await message.reply(self.memory.pop(message.author), mention_author=False)
            else:
                greeting_hi_match = re.search(r'(早(?:晨|安|上好))|(^午安$)|(^好$)|(晚上好$)|(^hi$)|(^hello$)', read_content, re.IGNORECASE)
                greeting_bye_match = re.search(r'(早(?:抖|唞))|(晚(?:安))|(^8(?:9)?8+$)', read_content)
                if greeting_hi_match:
                    await message.reply(self.fake_mkmui.reply_to_greeting(type_='hi'), mention_author=False)
                elif greeting_bye_match:
                    await message.reply(self.fake_mkmui.reply_to_greeting(type_='bye'), mention_author=False)
                else:
                    await message.reply(self.fake_mkmui.reply(True), mention_author=False)
        else:
            await message.reply(self.fake_mkmui.reply_to_empty(), mention_author=False)
        

if __name__ == '__main__':
    DEBUG = False
    token = 'Put your token here la 7.7'
    
    if DEBUG:
        fake_mkmui = Fake_MKMui()
        while True:
            print(fake_mkmui.reply())
            input('Press ENTER to continue; Press Ctrl+C to stop')
    else:
        while True:
            try:
                intents = discord.Intents.default()
                intents.message_content = True
                
                fake_mkmui = Fake_MKMui_deploy(intents=intents)
                fake_mkmui.run(token)
            except Exception as e:
                print(f'Error: {e}\nRestarting in 10 seconds.')
                time.sleep(10)
