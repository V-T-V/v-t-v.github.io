# 经纬 · 古籍数字人文六站门户

> [v-t-v.github.io](https://v-t-v.github.io/) —— 经纬系列的用户根页。

六座同构古籍数字人文站的总入口：同一套方法论（抓取管线 → 结构化数据 →
舆图/循读/检索 → lint·断言 → 论文 PDF），六种空间范式。

| 站 | 书 | 范式 | 线上 |
|---|---|---|---|
| 方舆经纬 | 读史方舆纪要（明·顾祖禹） | 点织版图 | [fangyu-jingwei](https://v-t-v.github.io/fangyu-jingwei/) |
| 水道经纬 | 水经注（北魏·郦道元） | 线溯江河 | [shuidao-jingwei](https://v-t-v.github.io/shuidao-jingwei/) |
| 霞客经纬 | 徐霞客游记（明·徐弘祖） | 线+时序 | [xiake-jingwei](https://v-t-v.github.io/xiake-jingwei/) |
| 伽蓝经纬 | 洛阳伽蓝记（北魏·杨衒之） | 城市尺度 | [qielan-jingwei](https://v-t-v.github.io/qielan-jingwei/) |
| 元和经纬 | 元和郡县图志（唐·李吉甫） | 点列州县 | [yuanhe-jingwei](https://v-t-v.github.io/yuanhe-jingwei/) |
| 寰宇经纬 | 太平寰宇记（宋·乐史） | 点总寰宇 | [huanyu-jingwei](https://v-t-v.github.io/huanyu-jingwei/) |
| 汉志经纬 | 汉书·地理志（汉·班固） | 点起纵贯 | [hanzhi-jingwei](https://v-t-v.github.io/hanzhi-jingwei/) |
| 梦华经纬 | 东京梦华录（北宋·孟元老） | 城忆汴京 | [menghua-jingwei](https://v-t-v.github.io/menghua-jingwei/) |

方法论沉淀：[docs/METHOD.md](docs/METHOD.md)——数据纪律 / 前端架构 / 十层验证兵器谱（每层对应一种被歼灭的假绿）/ 多 agent 会战组织 / 开新站 checklist。

站际互查桥（数字各出自各站 `docs/stats.json`）：

- 霞客 → 方舆：300 锚点匹配 175 府县
- 伽蓝 ↔ 水经注：谷/洛水注命中 21 名物 57 次
- 元和(唐) ↔ 寰宇(宋)：同名 192 州
- 寰宇(宋) → 方舆(明)：对应 169 府

各站之间以相对兄弟路径（`../<repo>/`）互链，在 github.io 项目页间原生可达。

## 本地开发

另有一份本地门户（相对路径版，适合同根服务）位于系列工作区根
`D:\W_A_W\index.html`——在本目录执行 `python -m http.server` 后，
六站与站际深链一页漫游。
