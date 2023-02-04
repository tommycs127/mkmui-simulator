import asyncio
import discord
import random
import time
import unicodedata


class Name(object):
    content = ''
    classifier_single = ''
    classifier_multiple = ''
    
    def __init__(self, content, classifier_single='', classifier_multiple=''):
        self.content = content
        self.classifier_single = classifier_single
        self.classifier_multiple = classifier_multiple
        
    def get(self, no_measure=False):
        if not no_measure:
            if self.classifier_multiple != '' and random.randint(0,1):
                if random.randint(0,1):
                    return '你哋呢' + self.classifier_multiple + self.content
                return self.classifier_multiple + self.content
            
            elif self.classifier_single != '' and random.randint(0,1):
                if random.randint(0,1):
                    return '你呢' + self.classifier_single + self.content
                return self.classifier_single + self.content
            
            return self.content
        return self.content


class Sentence(object):
    content = ''
    prefix = False
    suffix = False
    particle = ''
    no_measure = False
    no_pronoun = False
    names = [
        Name('毒撚', classifier_single='個', classifier_multiple='啲'),
        Name('死毒撚', classifier_single='個', classifier_multiple='啲'),
        Name('柒頭', classifier_single='條', classifier_multiple='啲'),
        Name('on9', classifier_single='條', classifier_multiple='啲'),
        Name('單身狗', classifier_single='隻', classifier_multiple='啲'),
        Name('處男', classifier_single='個', classifier_multiple='啲'),
        Name('青頭仔', classifier_single='個', classifier_multiple='啲'),
        Name('變態佬', classifier_single='個', classifier_multiple='啲'),
        Name('死變態佬', classifier_single='個', classifier_multiple='啲'),
    ]
    name_pronouns = [
        Name('你'),
        Name('你哋'),
    ]
    emoji = ['7.7', '7.777', '：）', '：（']
    
    def __init__(self, content, prefix=False, suffix=False, particle='', no_measure=False, no_pronoun=False):
        self.content = content
        self.prefix = prefix
        self.suffix = suffix
        self.particle = particle
        self.no_measure = no_measure
        self.no_pronoun = no_pronoun
        
    def get(self):
        final_content = self.content
        
        name_list = self.names
        if not self.no_pronoun:
            name_list += self.name_pronouns
            
        name_ = random.choice(name_).get(no_measure=self.no_measure)
        
        if self.suffix and random.randint(0,1):
            if self.particle != '':
                final_content += self.particle
                
            # Add space if it is two half-width characters joining
            half_to_half = unicodedata.east_asian_width(final_content[-1]) != 'F' and unicodedata.east_asian_width(name_[0]) != 'F'
            
            if half_to_half:
                final_content += ' '
                
            final_content += name_
        elif self.prefix:
            # Add space if it is two half-width characters joining
            half_to_half = unicodedata.east_asian_width(final_content[0]) != 'F' and unicodedata.east_asian_width(name_[-1]) != 'F'
            
            final_content += name_
            
            if half_to_half:
                final_content += ' '
            
        if random.randint(0,1):
            final_content += ' ' + random.choice(self.emoji)
        
        return final_content


class Fake_MKMui(discord.Client):
    replies = [
        Sentence('唔想理你'),
        Sentence('dont ff', prefix=True, no_measure=True),
        Sentence('LAAN', prefix=True, suffix=True, particle='啦', no_measure=True),
        Sentence('收皮', prefix=True, suffix=True, particle='啦', no_measure=True),
        Sentence('食屎', prefix=True, suffix=True, particle='啦', no_measure=True),
        Sentence('死開', prefix=True, suffix=True, particle='啦', no_measure=True),
        Sentence('躝開', prefix=True, suffix=True, particle='啦', no_measure=True),
        Sentence('真係好撚恐怖', prefix=True),
        Sentence('關我咩事呢', suffix=True, no_measure=True, no_pronoun=True),
        Sentence('關你咩事呢', suffix=True, no_measure=True, no_pronoun=True),
        Sentence('瞓啦', suffix=True, no_measure=True),
    ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    
    async def on_connect(self):
        print(f'{self.user}駕到！')
        
        
    async def on_disconnect(self):
        print(f'{self.user}斷線！')
        raise RuntimeError('Disconnected.')
        
    
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(('$娘娘', '$MK妹', '$mk妹')):
            reply = random.choice(self.replies).get()
            if random.randint(0,3):
                await message.channel.send(reply)
            else:
                await message.reply(reply)


while True:
    try:
        fake_mkmui = Fake_MKMui(loop=asyncio.new_event_loop())
        fake_mkmui.run('Put your token here la 7.7')
    except Exception as e:
        print(f'Error: {e}\nRestarting in 10 seconds.')
        time.sleep(10)
