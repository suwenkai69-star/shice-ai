# 食策AI Mini V1 — 微信小程序老板版

当前工程建立在 `V0.5.0-R1 Data Foundation` 上，新增原生微信小程序、Schema V3、利润区间估算、截图确认式导入、数据完整度、Top-3 异常、行动闭环、提醒、次日验证与结构化 AI 解释能力。

## 产品入口

小程序固定 4 个 Tab：

- 今天
- 待办
- 上传
- 我的

“问食策AI”是辅助入口，不占 Tab。

## 本地后端

```bash
python -m pip install -r requirements.txt
python run.py
```

默认本机开发地址：`http://127.0.0.1:8765`。

健康检查：`GET /api/health`。

## 小程序开发配置

`miniprogram/project.config.json` 当前使用 `touristappid`，用于开发工程占位。真正微信测试/发布前请替换为自己的测试或正式 AppID。

小程序 Release 配置不会把 localhost 写死到源码。开发时可在小程序存储中配置 API 地址：

- key: `shice_api_base_url`

正式真机环境必须使用 HTTPS，并把域名加入微信公众平台合法 request/uploadFile 域名。

## 必需/可选环境变量

生产微信登录：

```text
WECHAT_APPID
WECHAT_SECRET
MINI_TOKEN_SECRET
```

微信订阅消息：

```text
WECHAT_SUBSCRIBE_TEMPLATE_ID
```

真实截图识别（当前已提供 OpenAI adapter）：

```text
RECOGNITION_PROVIDER=openai
OPENAI_API_KEY=...
OPENAI_RECOGNITION_MODEL=...
```

`MINI_TOKEN_SECRET` 生产环境必须设置成强随机密钥，不应使用开发 fallback。

## 数据可靠性硬规则

1. OCR/视觉识别只生成草稿；用户确认后才正式入库。
2. 营业额没有真实数据，不生成利润结果。
3. 缺失成本可以用本店历史/当地/行业 Benchmark 估算，但必须保留来源并以区间展示。
4. AI 不承担核心财务计算，不允许用语言模型补猜缺失经营数据。
5. 高风险经营动作只给建议和执行材料，不未经用户确认自动操作第三方平台。
6. 对账差异只能表达为“暂时没对上”，不能无证据判断平台少付。

## 自动化验证

```bash
python -m pytest -q
python -m compileall -q .
find miniprogram -name '*.js' -print0 | xargs -0 -n1 node --check
```

本候选版本最新自动化结果：`210 passed / 0 failed`；仍有 2 条继承自旧 FastAPI `on_event` 的 deprecation warnings。

## 尚未完成的正式发布 Gate

自动化通过不等于微信正式上线。还必须完成：

- 真实 AppID
- HTTPS 合法域名
- 微信开发者工具窄屏/普通屏 smoke
- 真机 `wx.login`
- 真机截图/文件上传
- 真机订阅消息授权与实际送达
- 各主流平台真实截图黄金样本识别验证

详见：

- `docs/superpowers/gates/2026-09-02-mini-v1-e2e-checklist.md`
- `docs/superpowers/gates/2026-09-02-mini-v1-final-gate.md`
