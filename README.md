# MK 妹機械人
模仿香港 VTuber「[MK 妹](https://www.youtube.com/channel/UCO62chyehk6pX7OitrnJAUg)」講嘢風格嘅 Discord 機械人，**限 Python 3.3 以上版本**（好似係）。

# 點架起佢？
1. 用 `pip` 裝 `discord`，即係打 `pip install discord`；
2. 去 [Discord 開發者介面](https://discord.com/developers/applications/)開一個新 bot；
3. 去 `Bot` 分頁複製 token 再貼落去 `fake_mkmui.run(呢度)`，*記得係放字串*；
   * 譖氣都要講：*唔好畀人知你個 token！*
4. 就噉開起佢，見到「`機械人個名#號碼`駕到！」即係程式正常運作緊；
5. 去 `OAuth2` 分頁嘅 `URL Generator` 整個邀請連結；
   * `SCOPES` 剔 `bot`
   * `BOT PERMISSIONS` 剔 `Send Messages`
6. 貼落瀏覽器，揀你想佢入嘅伺服器；
7. **娘娘駕到！**

# 點同娘娘傾計？
喺訊息開頭打呢啲觸發詞：
* `$娘娘`
* `$MK妹`；或者
* `$mk妹`

佢就會~~鬧你~~覆你。

留意觸發詞前面*唔應該有任何字符（包括空格），亦唔好係全形嘅* `＄`，唔係嘅話佢連理都唔會理。

如果你有需要喺訊息開頭打觸發詞，但係又唔想佢應你，就要喺 `$` 前面加個反斜線變成 `\$`。

# 要搞掂嘅嘢
* 暫時冇。
