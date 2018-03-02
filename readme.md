### changelog:
已完成登录，房间页面，实时消息传递接口

### next：
1. 设计玩家对象，用于保存玩家的相关状态等信息，以及可进行的操作
2. 接口设计，`{action:"action", user:"user", content:"content", error:"ok", time:"time"}`
3. 前端用户设计，`{name:"username", staus:"ready|leave|wait", pai:"poker", mark:"mark"}`
4. 扑克背面设计，back
5. 牌局进行状态的保存和改变
6. 还缺少总牌局计分、结束，结算功能
7. 中途进的无法参与本局游戏
8. 样式有待完善