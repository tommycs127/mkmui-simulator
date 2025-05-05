# MK 妹機械人

模仿香港 VTuber「[MK 妹](https://www.youtube.com/channel/UCO62chyehk6pX7OitrnJAUg)」講嘢風格嘅 Discord 機械人，**限 Python 3.8 以上版本**（[Vermin](https://github.com/netromdk/vermin) 話嘅）。

# 點架起佢？

1. 用 `pip` 裝 `discord`，即係打 `pip install discord`；
2. 去 [Discord 開發者介面](https://discord.com/developers/applications/)開一個新 bot；
3. 由 `settings_example.json` 複製一份 `settings.json`，同 `mkmui-simulator.py` 擺埋一齊；
4. 去 `Bot` 分頁複製 token 再貼落去 `settings.json` 入面 `token` 嘅值，*記得係放字串*；
   * 譬如你個 token 係 `u.on99.sau.pei.lah.dllm.mk.mui.no.1.ah.7head`：
   ```jsonc
   {
       "token": "u.on99.sau.pei.lah.dllm.mk.mui.no.1.ah.7head",
       // 下略...
   }
   ```
   * 譖氣都要講：*唔好畀人知你個 token！*
6. 就噉開起佢，見到「`機械人個名#號碼`駕到！」即係程式正常運作緊；
7. 去 `OAuth2` 分頁嘅 `URL Generator` 整個邀請連結；
   * `SCOPES` 剔 `bot`
   * `BOT PERMISSIONS` 剔 `Send Messages`
8. 貼落瀏覽器，揀你想佢入嘅伺服器；
9. **娘娘駕到！**

# 點同娘娘傾計？

喺訊息開頭打呢啲觸發詞：

* `$娘娘`
* `$牙娘`
* `$阿娘`
* `$MK妹`（唔理大細階，撈埋一齊亦得）

又或者覆佢任何一個訊息，佢就會~~鬧你~~覆你。

留意觸發詞前面*唔應該有任何字符（包括空格），亦唔好係全形嘅* `＄`，唔係嘅話佢連理都唔會理。

如果你有需要喺訊息開頭打觸發詞，但係又唔想佢應你，就要喺 `$` 前面加個反斜線變成 `\$`。

# 自肥功能 a.k.a. 洗腦 Play！

呢個機械人畀使用者傳送私人訊息，要求佢喺下次覆你嗰陣講啲乜，成功嘅話會喺私人訊息度覆「下次覆你就會講呢句！」。

如果想取消要求，喺私人訊息度傳送 `$del` 就得。想修改內容嘅話，再次要求就得。

# 懲罰功能

呢個機械人一分鐘內淨係可以傾八次，過咗就會已讀不回一分鐘。

懲罰嘅條件同計時都有得喺 `settings.json` （麻煩自己開一個）度校。

# 要搞掂嘅嘢

* 除咗解 bug 之外暫時冇。
