import discord
import json
import os
import re
import time

from collections import deque
from datetime import datetime, timedelta, timezone
from discord.ext import tasks
from functools import cached_property

from misc.config import validate_time_format_json
from misc.random import flip_coin, random_choice
from misc.string import (
    not_same_width, both_ascii, join_string, normalize_ascii_cjk_spacing
)


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
        final = self.content
        name_list = self.names.copy()
        if not self.no_pronoun:
            name_list.extend(self.name_pronouns)
        
        name_ = random_choice(name_list).get(self.no_measure)
        
        add_suffix = flip_coin()
        
        if self.suffixes and add_suffix:
            suffix = random_choice(self.suffixes)
            final = join_string(final, suffix, both_ascii)
        
        if self.name_at_end and add_suffix and flip_coin():
            final = join_string(final, name_, both_ascii)
                
        elif self.name_at_front:
            final = join_string(name_, final, both_ascii)
        
        if self.emoji_type and flip_coin():
            emoji_type_ = random_choice(self.emoji_type)
            emoji_ = random_choice(self.emoji[emoji_type_])
            final = join_string(final, emoji_, both_ascii)
        
        return final


class Fake_MKMui:
    def __init__(self, settings: dict = dict()):
        if not isinstance(settings, dict):
            settings = dict()
        self.load_settings(settings)
        
        # {user_id: dict}
        # the dictionary (as value) can contain the following keys:
        # - message: str; for the custom message
        # - annoyance: deque; deque of datetime objects
        # - ignore_until: datetime; when to stop ignoring the user
        # - last_modified: datetime
        self.memory = dict()
            
    def load_settings(self, settings: dict = dict()) -> None:
        self.annoyance_limit = settings.get('annoyance_limit', 8)
        
        time_window = settings.get('time_window', dict())
        if validate_time_format_json(time_window):
            self.time_window = timedelta(**time_window)
            
        punishment_duration = settings.get('punishment_duration', dict())
        if validate_time_format_json(punishment_duration):
            self.punishment_duration = timedelta(**punishment_duration)
    
    @property
    def replies(self) -> list[Sentence]:
        return [
            Sentence('OK 898', False, False, [], False, False, ['mock']),
            Sentence('唔想理你', False, False, [], False, False, ['sad', 'mock', 'angry']),
            Sentence('八八冇LU', False, False, [], False, False, ['mock']),
            Sentence('dont ff', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('LAAN', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('收皮', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('食屎', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('死開', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('躝開', True, True, ['啦', 'la'], True, False, ['mock', 'angry']),
            Sentence('比錢我未', True, True, ['啦', 'la'], True, False, ['mock']),
            Sentence('送樓比我未', True, True, ['啦', 'la'], True, False, ['mock']),
            Sentence('送車比我未', True, True, ['啦', 'la'], True, False, ['mock']),
            Sentence('真係好撚恐怖', True, True, ['囉', 'lor'], False, False, ['sad', 'mock']),
            Sentence('真係好撚kam', True, True, ['啊'], False, False, ['mock']),
            Sentence('關我咩事', False, True, ['呢'], True, True, ['mock']),
            Sentence('關你咩事', False, True, ['呢'], True, True, ['mock']),
            Sentence('關你地咩事', False, True, ['呢'], True, True, ['mock']),
            Sentence('瞓啦', False, True, [], True, False, ['mock']),
        ]
        
    @property
    def replies_to_empty(self) -> list[Sentence]:
        return [
            Sentence('??', False, False, [], True, True, []),
            Sentence('jm9', False, False, ['??'], True, True, []),
        ]
        
    @property
    def replies_discord(self) -> list[Sentence]:
        return [
            Sentence(':middle_finger:', False, False, [], False, False, []),
            Sentence(':thumbsdown:', False, False, [], False, False, []),
        ]
        
    @property
    def replies_salutation(self) -> list[Sentence]:
        return [
            Sentence('瞓啦柒頭', False, False, ['zzz'], True, True, ['mock']),
            Sentence('瞓啦染頭', False, False, ['zzz'], True, True, ['mock']),
            Sentence('瞓啦', False, False, ['zzz'], True, False, ['mock']),
        ]
        
    @property
    def replies_greeting(self) -> list[Sentence]:
        return [
            Sentence('閪佬', True, True, [], True, True, ['mock']),
            Sentence('hi', True, True, [], True, True, ['mock']),
        ]
    
    @property
    def replies_parting(self) -> list[Sentence]:
        return [
            Sentence('bye', True, True, [], True, True, ['mock']),
            Sentence('898', True, True, [], True, True, ['mock']),
            Sentence('bibi', True, True, [], True, True, ['mock']),
            Sentence('八八冇LU', False, False, [], False, False, ['mock']),
        ]
        
    @cached_property
    def replies_greeting_final(self) -> list[Sentence]:
        return (
            self.replies_salutation
            + self.replies_greeting
            + self.replies_parting
        )
        
    @cached_property
    def replies_parting_final(self) -> list[Sentence]:
        return (
            self.replies_salutation
            + self.replies_parting
        )
        
    @property
    def replies_gura(self) -> list[Sentence]:
        return [
            Sentence('gura…', False, False, [], True, True, ['sad']),
            Sentence('好掛住gura', False, False, ['…'], True, True, ['sad']),
            Sentence('gura我老婆', False, False, [], True, True, ['love']),
            Sentence('gura喺我隔離', False, False, [], True, True, ['love']),
            Sentence(':shark:', False, False, [], True, True, ['love']),
        ]
        
    @property
    def custom_actions(self) -> dict:
        return {
            'greeting': {
                'regex': r'(^早+(?:$|晨|安|上好|呀|啊|吖|[.,!。，！]))|(^午安$)|(^晚上好$)|(^你好$)|(^hi$)|(^hello$)',
                'action': self.reply_to_greeting,
            },
            'parting': {
                'regex': r'(早(?:抖|唞))|(晚(?:安))|(^8(?:9)?8+$)|(^bye$)|(^(?:bye)?(?:bi)+$)',
                'action': self.reply_to_parting,
            },
            'gura': {
                'regex': r'(gura\b)|(\bgura)',
                'action': self.reply_to_gura,
            },
        }
    
    @property
    def keywords(self) -> list[str]:
        return ['$娘娘', '$牙娘', '$阿娘', '$mk妹']
        
    def acknowledge_user(self, user_id: int):
        if not self.remember(user_id):
            self.memory[user_id] = {
                'message': None,
                'annoyance': deque(),
                'ignore_until': None,
                'last_modified': None,
            }
        self.memory[user_id]['last_modified'] = datetime.now(timezone.utc)
        
    def remember(self, user_id: int) -> bool:
        return user_id in self.memory
    
    def remember_custom_message(
        self,
        user_id: int,
        message: str
    ) -> None:
        self.memory[user_id]['message'] = message
        
    def recall_custom_message(
        self,
        user_id: int
    ) -> bool or None:
        return self.memory[user_id].pop('message', None)
        
    def update_annoyance(self, user_id: int) -> None:
        now = datetime.now(timezone.utc)
        annoyance = self.memory[user_id]['annoyance']
        ignore_until = self.memory[user_id].get('ignore_until', None)
        
        if isinstance(ignore_until, datetime) and not self.is_annoyed(user_id):
            self.unignore(user_id)
        
        # Remove timestamps outside the time window
        while annoyance and now - annoyance[0] > self.time_window:
            annoyance.popleft()
            
        annoyance.append(now)
        
        # Punish users that spammed the bot
        if len(annoyance) > self.annoyance_limit:
            self.ignore(user_id)
            
    def is_annoyed(self, user_id: int) -> bool:
        ignore_until = self.memory[user_id].get('ignore_until', None)
        
        if not isinstance(ignore_until, datetime):
            return False
        
        return datetime.now(timezone.utc) < ignore_until
        
    def ignore(self, user_id: int) -> None:
        now = datetime.now(timezone.utc)
        self.memory[user_id]['ignore_until'] = now + self.punishment_duration
        
    def unignore(self, user_id: int) -> None:
        if 'ignore_until' in self.memory[user_id]:
            del self.memory[user_id]['ignore_until']
        
    def read(self, message: str, keyword_required: bool = True) -> str or None:
        
        # Return the string if keyword check is not needed
        if not keyword_required:
            return normalize_ascii_cjk_spacing(message)
        
        # If not, check if the message starts with a keyword
        for keyword in self.keywords:
            if message.lower().startswith(keyword):
                return normalize_ascii_cjk_spacing(
                    message[len(keyword):].strip()
                )
        
        # Otherwise, return None to ignore the message
        return None
        
    def reply(
        self,
        message: str,
        discord: bool = False,
        user_id: int or None = None
    ) -> str:
        # Return a specific message to any non-string object
        # or empty message
        if not (isinstance(message, str) and message):
            return self.reply_to_empty()
            
        # Return the custom message from memory if exists
        if self.remember(user_id) and 'message' in self.memory[user_id]:
            custom_message = self.recall_custom_message(user_id)
            if custom_message:
                return custom_message
            
        # Return a specific message if it meets a custom condition
        for type_, condition in self.custom_actions.items():
            if re.search(condition.get('regex', ''), message, re.IGNORECASE):
                return condition.get('action', lambda:'')()
                
        # Default behaviour
        return self.reply_generic(discord)

    def reply_generic(self, discord: bool = False) -> str:
        all_replies = self.replies.copy()
        if discord:
            all_replies.extend(self.replies_discord)
        return random_choice(all_replies).get()

    def reply_to_empty(self) -> str:
        return random_choice(self.replies_to_empty).get()
        
    def reply_to_greeting(self) -> str:
        return random_choice(self.replies_greeting_final).get()
        
    def reply_to_parting(self) -> str:
        return random_choice(self.replies_parting_final).get()
    
    def reply_to_gura(self) -> str:
        return random_choice(self.replies_gura).get()


class Fake_MKMui_deploy(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fake_mkmui = Fake_MKMui(settings=kwargs.get('settings', None))
    
    async def on_ready(self):
        print(f'{self.user}駕到！')
    
    async def on_disconnect(self):
        print(f'{self.user}斷線！')
        raise RuntimeError('Disconnected.')
    
    async def on_message(self, message):
        # Ignore messages from the bot itself to prevent loops
        if message.author == self.user:
            return
            
        self.fake_mkmui.acknowledge_user(message.author.id)
        user_id = message.author.id

        # Check if the message is a direct message
        if isinstance(message.channel, discord.DMChannel):
            dm_message = message.content.strip()
            if not dm_message:
                await message.reply(
                    f'屌你係咪唔識打字 7.777',
                    mention_author=False
                )
                return
                
            if dm_message.lower() == '$del':
                if (
                    self.fake_mkmui.remember(user_id)
                    and self.fake_mkmui.memory[user_id].get('message', None)
                ):
                    self.fake_mkmui.recall_custom_message(user_id)
                    await message.reply(
                        f'鏟鳥！下次覆你唔會講呢句嘢！',
                        mention_author=False
                    )
                    return
                await message.reply(
                    f'冇任何資料 7.7',
                    mention_author=False
                )
                return
                
            self.fake_mkmui.remember_custom_message(user_id, message.content)
            await message.reply(f'下次覆你就會講呢句！', mention_author=False)
            return
            
        # Check if the message is a reply
        # If so, keywords are not required in order to trigger the bot
        keyword_required = True
        
        if (
            message.reference
            and isinstance(message.reference.resolved, discord.Message)
        ):
            replied_message = message.reference.resolved
            # Check if the replied-to message was sent by the bot
            if replied_message.author == self.user:
                keyword_required = False
        
        read_content = self.fake_mkmui.read(message.content, keyword_required)
        
        # Check if the bot must react to the message
        if isinstance(read_content, str):
            is_annoyed_before = self.fake_mkmui.is_annoyed(user_id)
            self.fake_mkmui.update_annoyance(user_id)
            is_annoyed_after = self.fake_mkmui.is_annoyed(user_id)
            
            if is_annoyed_before or is_annoyed_after:
                if not is_annoyed_before and is_annoyed_after:
                    until = self.fake_mkmui.memory[user_id]['ignore_until']
                    await message.reply(
                        f'少煩 :(\n到 <t:{int(until.timestamp())}:T> 先理你',
                        mention_author=False
                    )
                return
            
            await message.reply(
                self.fake_mkmui.reply(
                    read_content,
                    discord=True,
                    user_id=user_id,
                ),
                mention_author=False
            )
            return
    
    @tasks.loop(hours=24)
    async def cleanup(self):
        return  # TODO: Reconstruct logic
        now = datetime.now(timezone.utc)
        expired = [user_id for user_id, until in self.ignore_until.items() if now >= until]
        for user_id in expired:
            del self.ignore_until[user_id]
        

if __name__ == '__main__':
    DEBUG = False
    
    if DEBUG:
        fake_mkmui = Fake_MKMui()
        while True:
            content = input('>>')
            read_content = fake_mkmui.read(content)
            if isinstance(read_content, str):
                reply = fake_mkmui.reply(read_content)
                print(reply)
    else:
        while True:
            try:
                intents = discord.Intents.default()
                intents.message_content = True
                
                working_dir = os.path.dirname(os.path.realpath(__file__))
                settings_json = os.path.join(working_dir, 'settings.json')
                with open(settings_json, 'r') as f:
                    settings = json.load(f)
                    
                token = settings.pop('token')
                
                fake_mkmui = Fake_MKMui_deploy(
                    intents=intents,
                    settings=settings
                )
                fake_mkmui.run(token)
            except Exception as e:
                print(f'Error: {e}\nRestarting in 10 seconds.')
                time.sleep(10)
