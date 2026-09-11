# 食策AI V0.5.0-R1 — Data Integrity Fix

这是 **食策AI V0.5.0 Data Foundation** 的数据完整性修订版。

R1 不进入 V0.5.1，不做 UI 大改、不重构 AI、不开发税务/BOM/库存/平台自动抓取；只修复 V0.5.0 复审中确认的数据安全与兼容问题。

## 启动

```bash
python run.py
```

浏览器打开：`http://127.0.0.1:8765`

## V0.4 / V0.5.0 原能力仍保留

- FastAPI 后端 + SQLite 持久化
- `/api/state` 等旧接口
- 经营概览 / 经营诊断 / 商品分析 / AI经营建议 / AI营销 / 数据中心 / 设置
- CSV / JSON 上传
- Demo 流程
- localStorage fallback
- Schema V2：渠道销售、结算、平台费用、到账、导入批次、Raw Row、对账匹配

## R1 修复重点

### 1. 修正版文件不再静默擦除旧数据

如果同一条销售/结算/到账记录已经包含较完整字段，而后续修正版缺少已有字段，R1 **不会自动把缺失字段写成 NULL，也不会做混合来源合并**。

处理方式：

> 字段不完整 → 拒绝本次更新 → 保留原记录 → 提示上传完整记录。

这是刻意采用的保守策略，避免一条记录的不同字段来自不同 Import Batch，破坏可追溯性。

### 2. 结算周期费用不再伪造成某一天费用

由 `settlements` 拆出的 `platform_fees.business_date` 默认保持 `NULL`。

结算周期为 8/1–8/7 时，不再把整周佣金错误记到 8/7。

### 3. 渠道一致性加强

如果 API 指定 `MEITUAN_DELIVERY`，文件行却写 `DOUYIN_LOCAL`：

> 直接拒绝该行，不再产生“批次是美团、数据是抖音”的冲突记录。

手工对账也禁止跨渠道匹配。

### 4. 空文件/坏文件可审计

- 空 CSV → FAILED
- JSON 解析失败 → FAILED
- 仍然创建 `import_batch`
- API 返回明确 400
- 不再出现“0 行但 COMPLETED”

### 5. 中文真实文件兼容

CSV / JSON 文本读取增加：

- UTF-8 / UTF-8 BOM
- GB18030

日期支持常见非补零格式，例如：

- `2026/8/7`
- `2026-8-7`

统一标准化为 `2026-08-07`。

### 6. Migration 备份修复

V0.4 → Schema V2 真正发生升级前：

- `shice_ai_v04_backup.db` 会刷新为**本次升级前**数据库
- 同时新增时间戳备份，避免只留下过期旧备份

### 7. 全量备份 / 清空 / 恢复一致

服务端模式下：

- `GET /api/backup`：导出完整 JSON 备份，包含可检查的 V2 数据摘要与 SQLite 快照
- `POST /api/reset`：清空当前门店 legacy + V2 经营/导入数据
- `POST /api/restore`：校验后原子恢复完整数据库

恢复前会另外保存 `pre_restore` 安全备份。

### 8. 收入口径和结算口径分离

`calculate_channel_net_revenue()` 不再直接复用 `calculate_expected_settlement()`。

经营收入与平台应结算正式视为不同概念。

### 9. store type 双字段同步

旧字段 `stores.type` 与 Schema V2 `stores.store_type` 在保存设置时同步更新，避免旧页面和新数据层看到不同门店类型。

## 数据追溯原则

仍保持：

`Normalized Record → Raw Import Row → Import Batch → Original File Metadata`

R1 为保护这条链路，**不自动执行缺字段 merge update**。

## 测试

最终以交付目录运行：

```bash
python -m pytest -q
```

详见：

- `V0.5.0-R1_GATE_REVIEW.md`
- `V0.5.0-R1_FINAL_VERIFICATION.txt`

## 当前明确边界

R1 仍不提供：

- 美团/抖音/京东专用 parser
- 平台 API / RPA 自动抓取
- 渠道对账中心 UI
- 概率/智能对账匹配
- BOM / 库存 / 税务 / 发票
- GPT / 云端大模型接入
- 缺字段记录的字段级 provenance merge（因此当前选择安全拒绝）

下一版本仍需单独定义并审核，不自动进入 V0.5.1。
