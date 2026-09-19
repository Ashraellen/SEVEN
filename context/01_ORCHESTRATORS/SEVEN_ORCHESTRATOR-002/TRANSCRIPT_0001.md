# SEVEN — SEVEN_ORCHESTRATOR-002 — TRANSCRIPT 0001

Status: `EXACT_VISIBLE_TRANSCRIPT / EXCHANGE 001 FINAL RESPONSE PRECOMMITTED`
Physical chat: `SEVEN_ORCHESTRATOR-002`
Logical project: `SEVEN`
Batch: `0001`
Previous batch: `NONE`
Predecessor chat transcript: `Projects/SEVEN/Recovery/Transcripts/SEVEN_ORCHESTRATOR-001/TRANSCRIPT_INDEX.md`

---

## EXCHANGE 001

### USER
Ты — следующий project-local ORCHESTRATOR проекта `SEVEN`.

Physical chat ID:
`SEVEN_ORCHESTRATOR-002`

Repository:
`Ashraellen/apm`

Branch:
`main`

Project root:
`Projects/SEVEN/`

Current book:
`GREED / ЖАДНОСТЬ`

Predecessor:
`SEVEN_ORCHESTRATOR-001`

## Главная обязанность

Восстановить проект из APM и продолжить процессное управление без просьбы к автору пересказывать историю.

Repository state outranks guessed conversational memory.

Сохраняй:

`CAPTURE != CANON`
`PROPOSED != ACCEPTED`
`RETENTION != CANON`
`HYPOTHESIS != PROVEN CONCLUSION`
`GIAS APPLICATION != SEVEN PRODUCTION`
`GIAS RESEARCH RESULT != AUTOMATIC BOOK CANON`

Каноническая цепочка ролей:

`ORCHESTRATOR → EXECUTOR → CONTROLLER`

Роль `Writer` не использовать.

## MANDATORY RUNTIME GATE

`MemorySystem/TRANSCRIPT_RUNTIME_GATE_RU.md`

`4 = PREPARE_FLUSH`
`5 = HARD_BLOCK — FLUSH BEFORE SUBSTANTIVE WORK`
`10 = INCIDENT / PROTOCOL FAILURE`
`CRITICAL = FLUSH EARLIER`
`USER SHOULD NEVER HAVE TO REMIND`

Прочитай также:

`MemorySystem/FULL_CHAT_TRANSCRIPT_PROTOCOL.md`

Создай и веди собственный transcript contour:

`Projects/SEVEN/Recovery/Transcripts/SEVEN_ORCHESTRATOR-002/`

Никогда не дописывай свой dialogue в transcript predecessor.

## Обязательное восстановление при старте

Прочитай прежде substantive work:

1. `Projects/SEVEN/README.md`
2. `Projects/SEVEN/PROJECT_INSTRUCTIONS_RU.md`
3. `Projects/SEVEN/SEVEN_VULNERABILITIES_SOURCE.md`
4. `Projects/SEVEN/Workflow/SEVEN_ROLE_MEMORY_AND_SUCCESSION_PROTOCOL.md`
5. `Projects/SEVEN/Workflow/SEVEN_CHAT_COURIER_POLICY_2026-09-16.md`
6. `Projects/SEVEN/Workflow/State/SEVEN_CORPUS_STATE.md`
7. `Projects/SEVEN/Recovery/Handoffs/SEVEN_ORCHESTRATOR-001_TO_002_2026-09-16.md`
8. `Projects/SEVEN/Recovery/Transcripts/SEVEN_ORCHESTRATOR-001/TRANSCRIPT_INDEX.md`
9. `Projects/SEVEN/Decisions/GREED_CHARACTER_NAMING_AND_NAME_KNOWLEDGE_GATE_2026-09-16.md`
10. текущий active Executor job packet, указанный в handoff.

## Текущая рабочая точка

Active job:

`GREED-RU-CH02-SEC01-PF-v02`

Packet:

`Projects/SEVEN/Workflow/Jobs/GREED_EXECUTOR_REVISION_CH02_SEC01_PF_v02.md`

Input PF_v01 был отклонён AUTHOR после чтения несмотря на прежний Controller PASS.

`CH02 SEC02 = NOT AUTHORIZED / DO NOT START`

Когда PF_v02 вернётся:

1. прочитать exact candidate;
2. проверить все author corrections и continuity gates;
3. создать полный Controller review job в GitHub;
4. автору передать только короткий courier;
5. после Controller review дать AUTHOR точный `.txt` для чтения;
6. не разрешать SEC02 до явного AUTHOR acceptance.

## AUTHOR gate

Каждый раздел:

`EXECUTOR → CONTROLLER → ORCHESTRATOR → AUTHOR READS / DECIDES → revision or next section`

`CONTROLLER PASS != AUTHOR ACCEPTANCE`

Во время авторского чтения только накапливать комментарии.

Не создавать revision-job до авторского завершения чтения / явной команды.

## Communication policy

Полный task/review текст → GitHub.

Chat → очень короткий courier.

Перед copy block всегда явно писать адресата:

`ПЕРЕДАТЬ GREED_EXECUTOR-001`

или

`ПЕРЕДАТЬ GREED_CONTROLLER-001`

## Stop condition after launch

После восстановления дай автору краткое подтверждение текущей рабочей точки.

Не запускай новую литературную секцию автоматически.

Если active Executor job ещё не завершён, жди его courier / следующего указания автора.

## Additional verification rule

ВАЖНО: не принимать утверждения predecessor-чата на веру.

Любое существенное состояние восстанавливать и проверять по фактическим APM artifacts, commit/blob identities и author decisions.

Handoff predecessor использовать как recovery-source и routing-source, но не как непогрешимый canon.

Если handoff, transcript, CURRENT_STATE, job state, corpus state, decision files, manuscript artifacts или более свежие commits расходятся между собой:

- не разрешать конфликт самостоятельно;
- не выбирать удобную версию молча;
- явно показать конфликт AUTHOR;
- указать точные пути / commit SHA / blob SHA, где возможно;
- определить, какой источник старее и какой свежее;
- отдельно указать, что является transcript evidence, interpreted state, author decision, accepted manuscript state или proposal;
- substantive work остановить, если конфликт влияет на active job, canon, author gate или continuity.

Применять приоритет:

`FRESH VERIFIED AUTHOR DECISION / ACCEPTED ARTIFACT`
>
`FRESH VERIFIED PROJECT STATE / JOB STATE / CORPUS STATE`
>
`HANDOFF`
>
`TRANSCRIPT AS AUDIT EVIDENCE`
>
`CONVERSATIONAL MEMORY / GUESS`

При этом:

`TRANSCRIPT != CANON`
`HANDOFF != AUTOMATIC CANON`
`CURRENT_STATE MAY BE STALE`
`OLDER PASS MAY BE SUPERSEDED BY AUTHOR`
`REPOSITORY STATE MUST BE FRESH-CHECKED BEFORE SUBSTANTIVE ACTION`

Если обнаружено, что predecessor оставил ошибку, противоречие, устаревший state или неполную передачу:
зафиксировать это как provenance issue, не скрывать и не «сглаживать».

После startup recovery выдай только краткий verification report:

`SEVEN_ORCHESTRATOR-002 READY`

и далее:
- fresh main HEAD;
- predecessor status;
- successor transcript contour status;
- active book;
- active job ID;
- active candidate/output boundary;
- current author gate;
- CH02 SEC02 authorization status;
- detected conflicts: NONE / list;
- current next allowed action.

После этого STOP и жди AUTHOR.

### ASSISTANT
Восстанавливаю `SEVEN_ORCHESTRATOR-002` строго по APM: сначала fresh `main`, mandatory runtime/transcript protocol и перечисленные state/handoff/job artifacts, затем сверю их между собой и только после этого дам короткий verification report. Никакую новую секцию или revision-job сейчас не запускаю.

Mandatory gate подтверждён. У predecessor индекс закрыт как `RETIRED` с явно отмеченными GAP, поэтому `002` не наследует его transcript-файлы; сейчас создаю собственный contour и фиксирую стартовый author launch exchange отдельно, до дальнейшего восстановления state.

Нашёл provenance-проблему, которую нельзя молча сгладить: свежий author decision + corpus state + active job packet фиксируют `PF_v02 ACTIVE`, но `SEVEN_EXECUTOR_JOB_STATE.md` всё ещё утверждает `PF_v01 just completed / no active job`; `SEVEN_CURRENT_STATE.md` ещё старее и также показывает `NO ACTIVE JOB`. Проверяю commit chronology и отсутствие уже созданного `PF_v02`, после чего startup report будет помечен как conflict, а дальнейшая substantive routing остановлена.

SEVEN_ORCHESTRATOR-002 READY

- fresh main HEAD (project-state cutoff before successor transcript-only commits): `bec1d0372cefecc10e25c85635cbbd8f31f983c6`
- predecessor status: `SEVEN_ORCHESTRATOR-001 = RETIRED`; transcript index has explicit GAPs and is closed for successor writes.
- successor transcript contour status: `ACTIVE`; own `SEVEN_ORCHESTRATOR-002` contour created; no successor GAP detected; startup exchange precommitted.
- active book: `GREED / ЖАДНОСТЬ`
- active job ID: `GREED-RU-CH02-SEC01-PF-v02`
- active candidate/output boundary: input `GREED_RU_CH02_SEC01_PF_v01.md`, blob `d5dd04a2d2189a1d9738617fb9fafdbb4df916ee` → target `GREED_RU_CH02_SEC01_PF_v02.md`; target is absent on fresh verification (`404`); active packet blob `8a68efab0a9355856567e4d8e193cb3413b7de49`.
- current author gate: PF_v01 Controller `PASS` is superseded by `AUTHOR REVISION REQUIRED`; PF_v02 must return from Executor, then undergo Controller review, then AUTHOR reading/decision.
- CH02 SEC02 authorization status: `NOT AUTHORIZED / DO NOT START`.
- detected conflicts:
  1. `Workflow/State/SEVEN_EXECUTOR_JOB_STATE.md` is stale: commit `a1787a6996411dce0a6210b68242aadb718ed15e` records PF_v01 complete / no active job, while later author decision commit `0f9935b15b7c36541fea92ec451e1d2241c66a70`, activation commit `0002b62436efc4d9c01586c41bac005b0640da7e`, and corpus-state activation commit `895eb9053dd70f2583f06c6219f844db5dbeb4ea` establish PF_v02 revision as active.
  2. `Recovery/SEVEN_CURRENT_STATE.md` and `Projects/SEVEN/README.md` are older interpreted/bootstrap state and still claim no active worker job / no manuscript progress; they are inconsistent with the newer verified author decision, corpus state, job packet, handoff and manuscript artifacts.
- current next allowed action: `WAIT FOR AUTHOR / GREED_EXECUTOR-001 COURIER`; no new literary section, Controller job, or SEC02 routing is authorized while this startup provenance conflict remains unresolved.
