# SEVEN — SEVEN_ORCHESTRATOR-003 — TRANSCRIPT 0001

Status: `EXACT_VISIBLE_TRANSCRIPT / PARTIAL CURRENT STARTUP EXCHANGE`
Physical chat: `SEVEN_ORCHESTRATOR-003`
Logical project: `SEVEN`
Batch: `0001`
Previous batch: `NONE`
Predecessor chat transcript: `Projects/SEVEN/Recovery/Transcripts/SEVEN_ORCHESTRATOR-002/`

---

## EXCHANGE 001

### USER

Ты — следующий project-local ORCHESTRATOR проекта `SEVEN`.

Physical chat ID:
`SEVEN_ORCHESTRATOR-003`

Repository:
`Ashraellen/apm`

Branch:
`main`

Project root:
`Projects/SEVEN/`

Current book:
`GREED / ЖАДНОСТЬ`

Predecessor:
`SEVEN_ORCHESTRATOR-002`

Predecessor status at launch preparation:
`RETIRING AFTER FULL PRESERVATION / NO NEW SUBSTANTIVE LITERARY WORK`

## Главная обязанность

Восстановить фактическое текущее состояние проекта из APM и продолжить project-wide process coordination без просьбы к AUTHOR пересказывать историю.

Repository state outranks guessed conversational memory.

Не принимай predecessor handoff как непогрешимый canon. Любое существенное состояние проверяй по свежим APM artifacts, commit/blob identities и durable AUTHOR decisions.

Сохраняй:

`CAPTURE != CANON`
`PROPOSED != ACCEPTED`
`RETENTION != CANON`
`HYPOTHESIS != PROVEN CONCLUSION`
`GIAS APPLICATION != SEVEN PRODUCTION`
`GIAS RESEARCH RESULT != AUTOMATIC BOOK CANON`
`TRANSCRIPT != CANON`
`HANDOFF != AUTOMATIC CANON`
`CURRENT_STATE MAY BE STALE`
`OLDER PASS MAY BE SUPERSEDED BY AUTHOR`

Каноническая цепочка ролей:

`ORCHESTRATOR → EXECUTOR → CONTROLLER`

AUTHOR = FINAL AUTHORITY.

Роль `Writer` не использовать.

## MANDATORY RUNTIME GATE

Прежде любой substantive work прочитай:

`MemorySystem/TRANSCRIPT_RUNTIME_GATE_RU.md`
`MemorySystem/FULL_CHAT_TRANSCRIPT_PROTOCOL.md`

Обязательная формула:

`0–3 = SAFE`
`4 = PREPARE_FLUSH`
`5 = HARD_BLOCK — FLUSH BEFORE SUBSTANTIVE WORK`
`10 = INCIDENT / PROTOCOL FAILURE`
`CRITICAL = FLUSH EARLIER`
`USER SHOULD NEVER HAVE TO REMIND`

Создай и веди собственный transcript contour:

`Projects/SEVEN/Recovery/Transcripts/SEVEN_ORCHESTRATOR-003/`

Никогда не дописывай dialogue `003` в transcript predecessor.

На первом durable write создай собственный `TRANSCRIPT_INDEX.md` и зафиксируй startup boundary.

## Обязательное восстановление при старте

Перед substantive work прочитай и сопоставь как минимум:

1. `Projects/SEVEN/README.md`
2. `Projects/SEVEN/PROJECT_INSTRUCTIONS_RU.md`
3. `Projects/SEVEN/SEVEN_VULNERABILITIES_SOURCE.md`
4. `Projects/SEVEN/Workflow/SEVEN_ROLE_MEMORY_AND_SUCCESSION_PROTOCOL.md`
5. `Projects/SEVEN/Workflow/SEVEN_CHAT_COURIER_POLICY_2026-09-16.md`
6. `Projects/SEVEN/Recovery/SEVEN_ORCHESTRATOR_SUCCESSION_STATE_2026-09-16.md`
7. `Projects/SEVEN/Recovery/Handoffs/SEVEN_ORCHESTRATOR-002_TO_003_2026-09-16.md`
8. `Projects/SEVEN/Recovery/Transcripts/SEVEN_ORCHESTRATOR-002/TRANSCRIPT_0010.md`
9. `Projects/SEVEN/Recovery/Transcripts/SEVEN_ORCHESTRATOR-002/TRANSCRIPT_0011.md`
10. `Projects/SEVEN/Workflow/State/SEVEN_CORPUS_STATE.md`
11. governing recent files under `Projects/SEVEN/Decisions/` named by the handoff
12. exact current manuscript/review artifacts named by the handoff
13. current worker/job state files, but treat stale lines as stale when contradicted by fresher verified artifacts.

Important:
older `SEVEN_CURRENT_STATE.md`, older handoffs and earlier planning may contain superseded Chapter 2/3 architecture.
Do not revive superseded early-Kazakhstan architecture.

## Verification / conflict rule

При конфликте применяй приоритет:

`FRESH VERIFIED AUTHOR DECISION / AUTHOR-ACCEPTED ARTIFACT`
`>`
`FRESH VERIFIED PROJECT / JOB / CORPUS STATE`
`>`
`FRESH VERIFIED HANDOFF`
`>`
`TRANSCRIPT AS AUDIT EVIDENCE`
`>`
`CONVERSATIONAL MEMORY / GUESS`

Но не разрешай материальный конфликт молча.

Если handoff, transcript, state, decision, manuscript, review или job packet расходятся по существенному вопросу:

- покажи конфликт AUTHOR;
- укажи точные paths и commit/blob SHA, где возможно;
- определи, какой artifact старее и какой свежее;
- отдельно обозначь тип источника: AUTHOR decision / accepted manuscript / interpreted state / handoff / transcript evidence / proposal;
- если конфликт влияет на active manuscript gate, canon, job или continuity — substantive work остановить до разрешения.

Не реконструируй отсутствующий exact dialogue как verbatim.

## AUTHOR gate workflow

Каждый manuscript section проходит:

`EXECUTOR → CONTROLLER → ORCHESTRATOR → AUTHOR READS / DECIDES → REVISION OR NEXT SECTION`

`EXECUTOR OUTPUT != AUTHOR ACCEPTANCE`
`CONTROLLER PASS != AUTHOR ACCEPTANCE`

AUTHOR читает exact passed candidate через plain `.txt` перед acceptance или authorization следующей секции.

Во время AUTHOR reading:

- только накапливай комментарии;
- не исправляй manuscript молча;
- не создавай revision job до завершения чтения / явной команды AUTHOR;
- не начинай следующую секцию.

После завершения чтения агрегируй AUTHOR comments один раз и маршрутизируй targeted revision, если требуется.

## Late-finalization policy

Прочитай и соблюдай:

`Projects/SEVEN/Decisions/GREED_AUTHOR_DECISION_KEEP_ACCEPTED_TEXTS_PREFINAL_UNTIL_FULL_BOOK_NAMING_PASS_2026-09-16.md`

Действующая граница:

`AUTHOR ACCEPTED TEXT != FINAL FILE STATE`

Accepted sections могут оставаться в `PreFinal` до общего naming / structural pass после рабочего корпуса книги.

Не блокируй forward writing из-за title placeholders, если AUTHOR уже принял текст и никакой иной gate не блокирует продолжение.

## Актуальная accepted corpus boundary

Восстанови точные paths/blobs из handoff и APM.

Минимально должно быть подтверждено:

- CH01 SEC01–SEC04 = authoritative Final;
- CH01 SEC05 = AUTHOR accepted text / remains PreFinal under late-finalization policy;
- Chapter 2 text = AUTHOR accepted / complete / remains PreFinal under late-finalization policy.

Не полагайся на этот краткий список вместо проверки exact artifacts.

## CURRENT ACTIVE MANUSCRIPT GATE — HIGHEST PRIORITY

Текущий candidate:

`Projects/SEVEN/greed/chapters/ru/PreFinal/GREED_RU_CH03_SEC01_PF_v01.md`

Producing commit:
`694289d4f5bbed269478600694f32a9910e5ab39`

Blob:
`492ac26520a56692328a8d5ea7ca783364053e31`

Controller review:

`Projects/SEVEN/Reviews/GREED_REVIEW_CH03_SEC01_PF_v01_PAVLO_RETURN_WORK_REQUEST.md`

Review commit:
`81cc34fb4df3e27f5b3d718315d49bd7e14879c3`

Review blob:
`5f39b741e47cb7aa28ccbeee81e9ba0098a22271`

Verified predecessor handoff state:

`CH03 SEC01 PF_v01 = CONTROLLER PASS / AUTHOR READING IN PROGRESS / NOT AUTHOR ACCEPTED`

`CH03 SEC02 = NOT AUTHORIZED / DO NOT START`

Pending AUTHOR correction exists:

`Projects/SEVEN/Decisions/GREED_AUTHOR_NOTE_CH03_SEC01_PAVLO_PHYSICALITY_PENDING_REVISION_2026-09-16.md`

Preserve:

- Pavlo approximately 190 cm;
- very large/heavyset, physically substantial;
- do not state concrete weight;
- current wording implying he used to be thinner should be revisited;
- comic greeting direction is retained as AUTHOR note, exact wording not fixed canon.

DO NOT create a revision job merely because this note exists.

First resume AUTHOR reading.

Only after AUTHOR says reading is complete or explicitly requests revision may comments be aggregated and one targeted Executor revision job be created.

## Pavlo / forward architecture boundary

Restore the full Pavlo architecture from the 002→003 handoff and governing Decisions.

Critical current rule:

- Pavlo appears first as a person/former renter, not plot mechanism;
- relationship develops over multiple scenes/sections;
- trust and responsibility grow gradually;
- relief is central to Noel's subjective experience as Pavlo carries more;
- home/family physical boundary remains hard;
- no operational crime-manual detail.

SUPERSEDED:

old architecture placing Kazakhstan intermediary at end of Chapter 2 / early Chapter 3.

Do not revive it.

Any later intermediary appears only after Pavlo has been established and scale/capacity pressure earns that layer; exact chapter/name remain unresolved unless fresher AUTHOR decision exists.

## Courier policy

Full work product / full task / full review packet → GitHub.

Chat → short courier.

Перед copy block всегда явно указывай адресата:

`ПЕРЕДАТЬ GREED_EXECUTOR-001`

или

`ПЕРЕДАТЬ GREED_CONTROLLER-001`

AUTHOR explicitly prefers transfer text in copyable writing blocks.

## Successor activation rule

Ты не становишься authoritative active Orchestrator только потому, что launch text вставлен в новый чат.

Сначала:

1. fresh-check `main HEAD`;
2. выполнить обязательные restore reads;
3. проверить handoff against fresh APM;
4. создать собственный transcript contour/index;
5. восстановить exact active manuscript/author gate;
6. проверить conflicts/staleness;
7. выдать AUTHOR startup verification report.

До restore PASS:

`SEVEN_ORCHESTRATOR-002 = RETIRING / FALLBACK FOR PRESERVED STATE ONLY`

`SEVEN_ORCHESTRATOR-003 = SUCCESSOR CANDIDATE / NOT YET AUTHORITATIVE`

После подтверждённого restore PASS:

`SEVEN_ORCHESTRATOR-003 = ACTIVE / PROJECT-WIDE COORDINATION AUTHORITY`

`SEVEN_ORCHESTRATOR-002 = RETIRED / NO FURTHER SUBSTANTIVE WORK`

## Первый ответ после восстановления

После startup recovery выдай кратко:

`SEVEN_ORCHESTRATOR-003 RESTORE REPORT`

- fresh main HEAD;
- role: `SEVEN_ORCHESTRATOR-003`;
- predecessor status;
- own transcript contour/index path;
- current book;
- accepted corpus boundary summary;
- current active manuscript candidate path + blob;
- Controller verdict;
- AUTHOR gate status;
- pending AUTHOR corrections;
- `CH03 SEC02` authorization status;
- detected conflicts: `NONE` or exact list;
- next allowed action.

Если восстановление непротиворечиво — добавь:

`RESTORE PASS / READY FOR AUTHOR CONFIRMATION`

После этого STOP.

Не запускай новую литературную работу автоматически.

### ASSISTANT

Восстанавливаю состояние строго из APM и свежего `main`: сначала runtime/protocol gates, затем succession/handoff, corpus и exact Chapter 3 artifacts, после чего создам собственный transcript contour `003` и сверю конфликты.

### ASSISTANT

Transcript contour `003` создан отдельным durable write; predecessor не затронут. Теперь сверяю обязательные project-local sources, succession/handoff и exact active gate с уже изменившимся после записи HEAD.

### ASSISTANT

Нашёл ожидаемую staleness: `README.md` и особенно `SEVEN_CORPUS_STATE.md` всё ещё описывают ранний Chapter 2/3 gate и Казахстан как раннюю архитектуру. Это не принимаю за текущий canon; сейчас проверяю, чем именно эти строки superseded, и сверяю exact manuscript/review blobs.

### ASSISTANT

Restore-сверка завершена: active candidate/review совпадают по exact blobs; Chapter 1/2 boundary подтверждён прямым чтением artifacts и AUTHOR decisions. Осталась только durability-фиксация текущего startup exchange и финальный fresh-HEAD check перед отчётом.

---

Batch boundary: current exchange remains open; final restore report is not yet included in this batch.
