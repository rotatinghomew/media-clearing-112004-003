# 跨平台节目片段收益归属与结算

三方对账采用最小货币单位。片段范围用母带秒数（左闭右开），grant 的份额以万分数表示。日期采用 ISO 日历日；各笔收入使用发生日匹配授权，财务不做换汇。 数据均为合成。

CSV 使用 UTF-8、首行字段名，`-` 表示来源未填；JSON 使用原生布尔、字符串及数字。没有另行给定时，`seq` 只用于还原各条来件的先后，不是业务日期。

## 来源说明

- `assets.csv`：一个平台包可以多次引用同一母带范围；tag 是来源片段编号，不是独立作品。basis_unit 与 weight 是平台自带计量的单位与量；包内另有 meters 时，使用后者核对和分摊。
- `statements.csv`：source 行是正向收入，refund 行通过 reference 追溯原收入。specific 非空时表示金额全部来自该片段。
- `grants.csv`：layer 是收入权利层，每层预算见 layer_share；share 表示该层内的比例。exclusive 为 1 表示该层覆盖时间不能与同优先级另一个排他持有人同时拨付。priority 越大优先级越高。
- `revisions.csv`：withdraw 指明原授权行中撤回的日期、地域、音轨和范围。wire 回执以 transfer 为唯一编号，recover 对应此前确认的 pay 转账。
- `meters.csv`：平台给同包计量的校对结果。source_tag 表示出现于该投放清单；同 package 和 meter 的多行是同一计量的重复引用，量为所指区间总量，在区间内均匀解释。没有统一的计量单位时不可把相异单位混算。

## 数据清单

- `layer_share.json`：配置对象。
- `assets.csv`：`platform`, `package`, `tag`, `master`, `start`, `end`, `audio`, `region`, `basis_unit`, `weight`。
- `meters.csv`：`package`, `source_tag`, `meter`, `master`, `start`, `end`, `audio`, `region`, `unit`, `amount`。
- `statements.csv`：`id`, `at`, `platform`, `package`, `currency`, `minor`, `kind`, `specific`, `reference`。
- `grants.csv`：`id`, `payee`, `master`, `start`, `end`, `audio`, `region`, `layer`, `share`, `exclusive`, `priority`, `from`, `through`。
- `revisions.csv`：`seq`, `kind`, `grant`, `from`, `through`, `start`, `end`, `region`, `audio`。
- `wire.csv`：`seq`, `transfer`, `kind`, `source`, `original`, `payee`, `currency`, `minor`, `grant`, `start`, `end`。

## 补充来源说明

- `clearing_terms.json`：币种清算契约。minor 是整数最小单位。归属、授权层和收款人分配时，各自的同一原款分组按分段理论份额以最大余数分厘；同余按时间、授权编号顺序。相同 original 与区间的旧付款未确认时不可另发新支出。
- `clearing_events.csv`：两期清算回执；accepted 未出账，failed 与 cancelable 分别为无法成功与经确认可撤。net 是整批银行确认值，不分配到明细行。at 单调按来件顺序，actual_at 可早于补报。
- `clearing_lines.csv`：清算所来件索引。范围沿用母带秒和音轨，用途与当前权利说明不同。退款 scope 另由平台给出。

## 本地检查

使用 Python 3.11 标准库，无需安装第三方依赖。构建检查和来源契约测试：

```sh
python3 -m compileall -q tests
python3 -m unittest discover -s tests -v
```
