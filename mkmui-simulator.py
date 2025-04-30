import discord
import random
import re
import time
import unicodedata

from collections import deque, defaultdict
from datetime import datetime, timedelta, timezone
from discord.ext import tasks


def not_same_width(s1: str, s2: str) -> bool:
    _ = unicodedata.east_asian_width
    return _(s1[-1]) != _(s2[0])

def both_ascii(s1: str, s2: str) -> bool:
    _ = unicodedata.east_asian_width
    # Ref for east_asian_width's results:
    # https://www.unicode.org/reports/tr44/#Validation_of_Enumerated
    mathces = ('F', 'W', 'A')
    return _(s1[-1]) not in mathces and _(s2[0]) not in mathces

def join_string(s1: str, s2: str, condition=both_ascii) -> str:
    return s1 + ' ' + s2 if condition(s1, s2) else s1 + s2

def normalize_ascii_cjk_spacing(string: str) -> str:
    if not string:
        return string
    
    normalized_string = string[0]
    for idx in range(1, len(string)):
        normalized_string = join_string(
            normalized_string, string[idx], not_same_width
        )
    return normalized_string
    
def flip_coin() -> int:
    return random.randint(0, 1)
    
def random_choice(list_: list) -> object:
    return random.choice(list_)


class Name:
    def __init__(
        self,
        content: str,
        classifier_single: str or None = None,
        classifier_multiple: str or None = None,
    ):
        self.content = content
        self.classifier_single = classifier_single
        self.classifier_multiple = classifier_multiple

    def get(self, no_measure: bool) -> str:
        """Get name optionally prefixed by a classifier."""
        if no_measure:
            return self.content
            
        if self.classifier_multiple and flip_coin():
            if flip_coin():
                return '你地呢' + self.classifier_multiple + self.content
            return self.classifier_multiple + self.content
        elif self.classifier_single and flip_coin():
            return '你呢' + self.classifier_single + self.content
            
        return self.content


class Sentence:
    def __init__(
        self,
        content: str,
        name_at_front: bool,
        name_at_end: bool,
        suffixes: list[str],
        no_measure: bool,
        no_pronoun: bool,
        emoji_type: list[str],
    ):
        self.content = content
        self.name_at_front = name_at_front
        self.name_at_end = name_at_end
        self.suffixes = suffixes
        self.no_measure = no_measure
        self.no_pronoun = no_pronoun
        self.emoji_type = emoji_type
        
        self.names = [
            Name('毒撚', '個', '啲'),
            Name('死毒撚', '個', '啲'),
            Name('柒頭', '條', '啲'),
            Name('on9', '條', '啲'),
            Name('on9仔', '條', '啲'),
            Name('單身狗', '隻', '啲'),
            Name('處男', '個', '啲'),
            Name('青頭仔', '個', '啲'),
            Name('死青頭仔', '個', '啲'),
            Name('變態佬', '個', '啲'),
            Name('死變態佬', '個', '啲')
        ]
        
        self.name_pronouns = [
            Name('你'),
            Name('你地')
        ]
        
        self.emoji = {
            'sad': [':(', 'T^T', 'qq', '</3',],
            'mock': ['7.7', '7.777', ':)',],
            'angry': [r'\\./',],
            'love': ['<3'],
        }

    def get(self) -> str:
        final_content = self.content
        name_list = self.names.copy()
        if not self.no_pronoun:
            name_list.extend(self.name_pronouns)
        
        name_ = random_choice(name_list).get(self.no_measure)
        
        add_suffix = flip_coin()
        
        if self.suffixes and add_suffix:
            suffix = random_choice(self.suffixes)
            final_content = join_string(final_content, suffix, both_ascii)
        
        if self.name_at_end and add_suffix and flip_coin():
            final_content = join_string(final_content, name_, both_ascii)
                
        elif self.name_at_front:
            final_content = join_string(name_, final_content, both_ascii)
        
        if self.emoji_type and flip_coin():
            emoji_type_ = random_choice(self.emoji_type)
            emoji_ = random_choice(self.emoji[emoji_type_])
            final_content = join_string(final_content, emoji_, both_ascii)
        
        return final_content


class Fake_MKMui:
    def __init__(self):
        self.replies = [
            Sentence('OK 898', False, False, [], False, False, ['mock']),
            Sentence('唔想理你', False, False, [], False, False, ['sad', 'mock', 'angry']),
            Sentence('八八冇LU', False, False, [], False, False, ['mock']),
            Sentence('dont ff', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('LAAN', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('收皮', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('食屎', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('死開', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('躝開', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('比錢我先', True, True, ['啦', 'la'], True, False, ['mock']),
            Sentence('送樓比我先', True, True, ['啦', 'la'], True, False, ['mock']),
            Sentence('送車比我先', True, True, ['啦', 'la'], True, False, ['mock']),
            Sentence('真係好撚恐怖', True, True, ['囉', 'lor'], False, False, ['sad', 'mock']),
            Sentence('真係好撚kam', True, True, ['啊'], False, False, ['mock']),
            Sentence('關我咩事', False, True, ['呢'], True, True, ['mock']),
            Sentence('關你咩事', False, True, ['呢'], True, True, ['mock']),
            Sentence('關你地咩事', False, True, ['呢'], True, True, ['mock']),
            Sentence('瞓啦', False, True, [], True, False, ['mock']),
        ]
        
        self.replies_to_empty = [
            Sentence('??', False, False, [], True, True, []),
            Sentence('jm9', False, False, ['??'], True, True, []),
        ]
        
        self.replies_discord = [
            Sentence(':middle_finger:', False, False, [], False, False, []),
            Sentence(':thumbsdown:', False, False, [], False, False, []),
        ]
        
        self.replies_greeting = [
            Sentence('瞓啦柒頭', False, False, ['zzz'], True, True, ['mock']),
            Sentence('瞓啦染頭', False, False, ['zzz'], True, True, ['mock']),
            Sentence('瞓啦', False, False, ['zzz'], True, False, ['mock']),
        ]
        
        self.replies_greeting_bye = [
            Sentence('bye', True, True, [], True, True, ['mock']),
            Sentence('898', True, True, [], True, True, ['mock']),
            Sentence('bibi', True, True, [], True, True, ['mock']),
            Sentence('八八冇LU', False, False, [], False, False, ['mock']),
        ]
        
        self.replies_greeting_hi = [
            Sentence('閪佬', True, True, [], True, True, ['mock']),
            Sentence('hi', True, True, [], True, True, ['mock']),
        ] + self.replies_greeting_bye
        
        self.replies_gura = [
            Sentence('gura…', False, False, [], True, True, ['sad']),
            Sentence('好掛住gura', False, False, ['…'], True, True, ['sad']),
            Sentence('gura我老婆', False, False, [], True, True, ['love']),
            Sentence('gura喺我隔離', False, False, [], True, True, ['love']),
            Sentence(':shark:', False, False, [], True, True, ['love']),
        ]
        
        self.random_generator = random.Random()
    
    @property
    def keywords(self) -> list[str]:
        return ['$娘娘', '$牙娘', '$阿娘', '$mk妹']
        
    def read(self, message: str, keyword_required: bool = True) -> str or None:
        input_string = message.content
        
        # Return the string if keyword check is not needed
        if not keyword_required:
            return normalize_ascii_cjk_spacing(input_string)
        
        # If not, check if the message starts with a keyword
        for keyword in self.keywords:
            if input_string.lower().startswith(keyword):
                return normalize_ascii_cjk_spacing(
                    input_string[len(keyword):].strip()
                )
        
        # Otherwise, return None to ignore the message
        return None

    def reply(self, discord: bool = False) -> str:
        all_replies = self.replies.copy()
        if discord:
            all_replies.extend(self.replies_discord)
        return random_choice(all_replies).get()

    def reply_to_empty(self) -> str:
        return random_choice(self.replies_to_empty).get()
        
    def reply_to_greeting(self, type_: str = '') -> str:
        replies_greeting = self.replies_greeting.copy()
        if type_ == 'hi':
            replies_greeting.extend(self.replies_greeting_hi)
        elif type_ == 'bye':
            replies_greeting.extend(self.replies_greeting_bye)
        return random_choice(replies_greeting).get()
    
    def reply_to_gura(self) -> str:
        return random_choice(self.replies_gura).get()


class Fake_MKMui_deploy(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fake_mkmui = Fake_MKMui()
        self.memory = dict()
        
        # Settings
        
        default_settings = {
            'trigger_limit': 8,  # max number of triggers
            'time_window': timedelta(minutes=1),  # time window size
            'punishment_duration': timedelta(minutes=1),
        }
        
        # Fill the blanks in received settings using default values
        settings = kwargs.get('settings') or dict()
        for key, default_value in default_settings.items():
            if key not in settings or settings[key] is None:
                settings[key] = default_value
        
        self.trigger_limit = settings.get('trigger_limit')
        self.time_window = settings.get('time_window')
        self.punishment_duration = settings.get('time_window')
        
        # {user_id: deque of datetime objects}
        self.trigger_history = defaultdict(deque)
        
        # {user_id: datetime}
        self.ignore_until = dict()
    
    async def on_ready(self):
        print(f'{self.user}駕到！')
    
    async def on_disconnect(self):
        print(f'{self.user}斷線！')
        raise RuntimeError('Disconnected.')
    
    async def on_message(self, message):
        keyword_required = True
        
        # Ignore messages from the bot itself to prevent loops
        if message.author == self.user:
            return

        # Check if the message is a direct message
        if isinstance(message.channel, discord.DMChannel):
            content = message.content.strip()
            if not content:
                await message.reply(f'屌你係咪唔識打字 7.777', mention_author=False)
                return
                
            if content.lower() == '$del':
                if message.author in self.memory:
                    del self.memory[message.author]
                    await message.reply(f'鏟鳥！下次覆你唔會講呢句嘢！', mention_author=False)
                    return
                await message.reply(f'冇任何資料 7.7', mention_author=False)
                return
                
            self.memory[message.author] = message.content
            await message.reply(f'下次覆你就會講呢句！', mention_author=False)    
            return
            
        # Check if the message is a reply
        if message.reference and isinstance(message.reference.resolved, discord.Message):
            replied_message = message.reference.resolved
            # Check if the replied-to message was sent by the bot
            if replied_message.author == self.user:
                keyword_required = False
        
        await self.trigger(message, keyword_required)
    
    async def trigger(self, message, keyword_required):
        now = datetime.now(timezone.utc)
        user_id = message.author.id
        history = self.trigger_history[user_id]
        
        # Ignore users who are in punishment period
        if user_id in self.ignore_until:
            if now < self.ignore_until[user_id]:
                return  # silently ignore
            del self.ignore_until[user_id]  # remove expired punishment
        
        # Remove timestamps outside the time window
        while history and now - history[0] > self.time_window:
            history.popleft()
            
        # Punish users that spammed the bot
        if len(history) >= self.trigger_limit:
            self.ignore_until[user_id] = now + self.punishment_duration
            await message.reply(f'少煩 :(\n到 <t:{int(self.ignore_until[user_id].timestamp())}:T> 先理你', mention_author=False)
            return
        
        history.append(now)
        await self.react_to_message(message, keyword_required)
    
    async def react_to_message(self, message, keyword_required):
        read_content = self.fake_mkmui.read(message, keyword_required)
        
        # Do nothing if the content is not a string
        if not isinstance(read_content, str):
            return
        
        # Return a message to any empty message
        if not read_content:
            await message.reply(self.fake_mkmui.reply_to_empty(), mention_author=False)
            return
        
        # Return the custom message if it exists
        if message.author in self.memory:
            await message.reply(self.memory.pop(message.author), mention_author=False)
            return
        
        # Default behaviour        
        greeting_hi_match = re.search(r'(^早+(?:晨|安|上好|呀|啊|吖)?($|[,!，！]))|(^午安$)|(^晚上好$)|(^你好$)|(^hi$)|(^hello$)', read_content, re.IGNORECASE)
        greeting_bye_match = re.search(r'(早(?:抖|唞))|(晚(?:安))|(^8(?:9)?8+$)|(^bye$)|(^(?:bye)?(?:bi)+$)', read_content)
        greeting_gura_match = re.search(r'(gura\b)|(\bgura)', read_content, re.IGNORECASE)
        if greeting_hi_match:
            await message.reply(self.fake_mkmui.reply_to_greeting(type_='hi'), mention_author=False)
        elif greeting_bye_match:
            await message.reply(self.fake_mkmui.reply_to_greeting(type_='bye'), mention_author=False)
        elif greeting_gura_match:
            await message.reply(self.fake_mkmui.reply_to_gura(), mention_author=False)
        else:
            await message.reply(self.fake_mkmui.reply(discord=True), mention_author=False)
    
    @tasks.loop(hours=24)
    async def cleanup(self):
        now = datetime.now(timezone.utc)
        expired = [user_id for user_id, until in self.ignore_until.items() if now >= until]
        for user_id in expired:
            del self.ignore_until[user_id]
        

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
