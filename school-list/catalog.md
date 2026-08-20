# 选校库

文件名形态：`school-navigator-catalog-*.sqlite`。来源 Terra School Navigator。只含学校/项目/课程，不含学生名单。

路径每次现找，不要写死盘符或某天的文件名。用户给了链接用用户的；否则 `scripts/resolve_paths.py` 找最新一份。只读打开。不要写库，不要把库上传到网上。

表结构以打开的那份为准。常见是：

| 表 | 用途 |
|---|---|
| `schools` | 校名、国家、城市、排名、官网 |
| `programs` | 项目名、学院、学位、介绍、要求、官网 |
| `courses` | 项目下课程中英文名 |
| `meta` | `dumped_at_utc`、计数。先读这个 |

`schools.country_code` 常见：`US` / `GB` / `OTHER`。港新澳加欧中多半在 `OTHER`，要用校名或城市再筛。

`programs.degree_types_json`：本科以 `BA` `BS` `BSc` `BEng` 为主的话，硕士选校不要只靠库。

## 查询

```bash
python scripts/query_catalog.py --db "<这次解析到的sqlite>" --q "computer science" --q "计算机" --country US --degree ug --limit 40
```

| 参数 | 说明 |
|---|---|
| `--country` | `US` `GB` `OTHER` `HK` `SG` `AU` `CN` `CA` `all`。HK/SG/AU/CN/CA 在 `OTHER` 里用城市/校名滤 |
| `--degree` | `ug` `grad` `all` |
| `--q` | 可重复。匹配项目中英文名、学院、简介、要求 |
| `--city` | 可选 |
| `--json` | 打 JSON；默认是人看的表 |

要某项目课程：

```bash
python scripts/query_catalog.py --db "<sqlite>" --courses "<program_id>"
```

国家、学位、关键词按学生情况改。同一所学校至少两套 `--q`：高（真正想学的）和低（更好进的相邻口）。例如物理/工程可以再查 applied physics、engineering physics、statistics、information science，不要只查最热的那个名。

## 怎么用查询结果

- 当候选池，不是终榜。终榜按 [strategy.md](strategy.md) 来：好看、好申、匹配；同校一高一低。
- 同一 `school_id` 下把能当「高」和能当「低」的项目都留下来，交给浏览器去核转专业和招生规模。
- `official_url` 必须再用浏览器打开核对。
- 库没有的学校可以补，在名单里写「库外，来源：官网/论坛」。
