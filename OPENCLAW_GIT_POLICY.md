# OPENCLAW_GIT_POLICY.md

Карта того, что из окружения OpenClaw стоит хранить в репозитории workspace.

## Держать в этом репозитории

### 1. Живой workspace

Это основной слой, который и должен жить в `openclaw-alex`:

- `AGENTS.md`
- `SOUL.md`
- `IDENTITY.md`
- `USER.md`
- `TOOLS.md`
- `HEARTBEAT.md`
- `README.md`
- `MEMORY.md`
- `memory/`
- `state/` — только если мы сами начнём хранить там полезное переносимое состояние
- `skills/` — наши собственные skill'ы
- `scripts/`, `references/`, `assets/` — если это наши рабочие материалы внутри workspace

### 2. Выборочное служебное состояние

Сейчас разумно хранить:

- `.openclaw/workspace-state.json`

Это небольшой и понятный файл, который описывает состояние инициализации workspace.

## Обычно не держать в этом репозитории

### 1. Установленный OpenClaw как software

Не тащить сюда содержимое:

- `~/.npm-global/lib/node_modules/openclaw/skills/`
- `~/.npm-global/lib/node_modules/openclaw/docs/`
- другие файлы установленного пакета OpenClaw

Почему:
- это upstream, а не наш проект
- оно обновляется отдельно через установку/апдейт OpenClaw
- копирование этого в workspace создаст шум, дублирование и конфликты при обновлениях

### 2. Глобальные runtime-данные OpenClaw

Обычно не коммитить:

- `~/.openclaw/credentials/`
- `~/.openclaw/identity/`
- `~/.openclaw/devices/`
- `~/.openclaw/logs/`
- `~/.openclaw/tasks/`
- `~/.openclaw/telegram/`
- `~/.openclaw/qqbot/`
- `~/.openclaw/agents/`
- `~/.openclaw/memory/main.sqlite`
- `~/.openclaw/exec-approvals.json`
- `~/.openclaw/update-check.json`

Почему:
- там секреты, идентификаторы устройства, pairing-данные, логи, SQLite-базы и runtime-хвосты
- это либо чувствительные данные, либо локальная операционная механика
- это плохо переносится и почти всегда только засоряет репозиторий

### 3. Конфиги инстанса, только если не решили отдельно

Файлы вроде:

- `~/.openclaw/openclaw.json`
- `~/.openclaw/openclaw.json.bak*`

по умолчанию не держим в этом workspace-репозитории, потому что там могут быть приватные настройки и инстанс-специфика.

Если захочется версионировать конфигурацию, лучше сделать одно из двух:
- хранить отдельный очищенный шаблон, например `config/openclaw.example.json`
- или вести отдельный приватный infra/config-репозиторий

## Что делать со skill'ами

### Встроенные skill'ы OpenClaw

Не копировать в репозиторий workspace.

Примеры встроенных skill'ов на этой машине:
- `weather`
- `healthcheck`
- `node-connect`
- `taskflow`
- `skill-creator`
- и многие другие из `~/.npm-global/lib/node_modules/openclaw/skills/`

Они уже доступны как часть установленного OpenClaw.

### Наши skill'ы

Если делаем свои skill'ы, хранить их прямо в workspace. Для удобства держать в `skills/INDEX.md` короткий индекс того, что уже есть.

Например:

```text
skills/
  alex-workspace/
    SKILL.md
    references/
    scripts/
```

Это и надо коммитить.

## Практическое правило

Если файл отвечает хотя бы на один вопрос ниже, он обычно подходит для git:
- Это часть моей личности, памяти или рабочего процесса?
- Это мы сами написали или осознанно кастомизировали?
- Это полезно перенести на другую машину или восстановить после сбоя?

Если файл отвечает хотя бы на один вопрос ниже, его обычно не надо коммитить:
- Это секрет, токен, ключ, pairing-данные или device identity?
- Это лог, кэш, SQLite, очередь задач, offset или runtime-state?
- Это часть установленного OpenClaw, а не нашего workspace?
