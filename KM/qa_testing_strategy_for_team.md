# QA Testing Strategy — Cortex HIS
### สำหรับนำเสนอทีม Dev / QA / BA

> **วัตถุประสงค์:** กำหนดกรอบการทดสอบร่วมกัน ให้ทุกฝ่ายเข้าใจตรงกันว่า "ใครทำอะไร", "ทำถึงแค่ไหน", และ "ทำไมถึงแบ่งแบบนี้"
> **อ้างอิง:** ISTQB Foundation Level · Risk-Based Testing · มาตรฐาน HIS (HL7 / JCI / MOPH)

---

## 🧩 1. บริบทของทีม — ทำไมต้องกำหนดกรอบนี้

| สถานการณ์ | ผลกระทบถ้าไม่จัดการ |
|---|---|
| Dev มี Unit Test บางส่วน ไม่ครบ 100% | QA กังวล → ลงไปทำ Unit level → งานซ้ำซ้อน → ทำไม่ทัน |
| ทีม QA มีจำนวนน้อย | รัน full test ทุก sprint ไม่ทัน → คุณภาพตกในระยะยาว |
| HIS มี critical patient path | ถ้า miss จุดสำคัญ → ความปลอดภัยผู้ป่วยมีความเสี่ยง |
| หลาย site (NUH / SBH / TMH) | พฤติกรรมต่างกัน ต้องทดสอบแยก config |

> **ข้อสรุปหลัก:** QA ต้องเป็น "นักยุทธศาสตร์" ไม่ใช่ "คนกดปุ่มทุก test"

---

## 🏗️ 2. Testing Pyramid — แบ่งหน้าที่ตาม Layer

```
           ▲
          /E2E\          ← QA เป็นหลัก (น้อยแต่ครอบ real flow จริง)
         /──────\
        / Integrat\      ← Dev + QA ร่วมกัน (contract testing)
       /────────────\
      /  Unit Test   \   ← Dev รับผิดชอบทั้งหมด
     /────────────────\
```

### ข้อตกลงหลัก

> **QA จะไม่ลงไปทำ Unit Test ซ้ำ — แต่ Dev ต้องการันตีว่า Unit Test ครอบ 5 จุดนี้:**

| HIS Critical Point | Unit Test ที่ Dev ต้องครอบ |
|---|---|
| 🔴 Patient Identity | validate HN · ชื่อ-นามสกุลไม่สลับตัวผู้ป่วย |
| 🔴 Drug Safety | allergy check · dosage calculation · ชื่อยาถูกต้อง |
| 🔴 Order Integrity | คำสั่งแพทย์ส่งถึง destination ถูกต้อง |
| 🔴 Financial | คำนวณค่ารักษาถูกต้อง · ไม่มีรายการหาย |
| 🔴 Audit Trail | ทุก action มี log + user + timestamp |

> ถ้า Dev ยืนยันว่า Unit Test ครอบ 5 จุดนี้แล้ว → **QA ไม่ต้อง re-test ชั้นนั้นซ้ำ**

---

## 🎯 3. QA ทดสอบอะไร — แบ่งตาม Phase

### Phase A — UAT (ทำก่อน ช่วง Stabilization)

**เป้าหมาย:** ยืนยันว่าระบบรัน patient journey ครบลูปได้ในทุก site

| ✅ ทำ | ❌ ยังไม่ทำ |
|---|---|
| Happy Path ของทุก workflow หลัก | Edge Case ที่ระบบยังไม่ stable |
| Integration flow ข้ามโมดูล | Non-functional (performance, security) |
| Site-specific config (NUH/SBH/TMH) | Error recovery กรณีระบบล่ม |
| Smoke Test ก่อน full test | Full regression ทุก sprint |

**Patient Journey ที่ต้องครบก่อน:**
```
Registration → OPD → [Lab / Pharmacy] → Cashier
```

### Phase B — Pre Go-Live (ก่อน production)

- Regression full suite
- Non-functional: performance · security · HL7 / สปสช. compliance
- Error Case: network failure · DB timeout · partial payment recovery
- Cross-site scenario: ผู้ป่วยย้าย site

---

## 🔀 4. Decision Flow — "QA ต้องทดสอบไหม?"

```
มี feature ใหม่ / แก้โค้ด
        │
        ▼
  Dev มี Unit Test ไหม? ──── ใช่ + ครอบ critical path ──► QA ทำแค่ Integration
        │ ไม่มี / ไม่ครอบ
        ▼
  กระทบ patient safety / financial? ──── ใช่ ──► Smoke Test ทันที (P0)
        │ ไม่กระทบ
        ▼
  QA ทำ Spot Check เท่านั้น
```

---

## ⚖️ 5. Risk Matrix — เลือกสิ่งที่ควรทำก่อน

> **Risk = โอกาสเกิดขึ้น × ความรุนแรงถ้าเกิด**
> **Impact สูง (HIS)** = กระทบผู้ป่วยโดยตรง หรือ กระทบการเงิน / สิทธิ์รักษา

|  | Impact ต่ำ | Impact สูง |
|---|---|---|
| **Risk สูง** | เก็บไว้ทำ Phase B | ✅ ทำก่อน P0/P1 |
| **Risk ต่ำ** | Skip / Dev รับ | ⚡ Spot Check |

---

## 📋 6. Regression Strategy ตาม Sprint Type

| Trigger | รัน Test อะไร | เวลาโดยประมาณ |
|---|---|---|
| Sprint ปกติ | Smoke Test — 20% TC (critical path) | ~2–3 ชั่วโมง |
| Pre-release | Full Regression — 100% TC | ~1–2 วัน |
| Post-hotfix | Targeted — เฉพาะ area ที่แก้ + adjacent | ~1–4 ชั่วโมง |
| New site onboard | Full E2E + site config verification | ~2–3 วัน |

---

## 📝 7. วิธีเขียน Test Case ที่แนะนำ — Scenario-first

### ❌ แบบเดิม (Step-by-step — เขียนช้า อ่านยาก)
```
Step 1: เปิดหน้า Registration
Step 2: กรอก HN
Step 3: กดค้นหา
...
```

### ✅ แบบที่แนะนำ (Scenario-based — เร็วกว่า 3–5 เท่า)
```
Given  ผู้ป่วย walk-in ไม่มีนัด
When   เจ้าหน้าที่ลงทะเบียนครบถ้วน
Then   ระบบออก HN และส่งเข้าคิว OPD ได้
And    ข้อมูลปรากฏครบใน OPD Module
```

> Dev อ่านเข้าใจด้วย → ลด back-and-forth ระหว่างทีม → เขียน TC ได้เร็วขึ้น

---

## 🤝 8. ข้อตกลงที่ QA ขอจากแต่ละฝ่าย

### ขอจาก **Dev**
- [ ] ยืนยันว่า Unit Test ครอบ 5 critical path ก่อน deliver build
- [ ] แจ้งล่วงหน้าถ้า feature มีการเปลี่ยน flow (ไม่ใช่แค่ bug fix)
- [ ] ทำ API contract test ก่อนส่ง QA — เพื่อแยกว่าบั๊กอยู่ที่ API หรือ UI

### ขอจาก **BA**
- [ ] AC (Acceptance Criteria) ต้องระบุด้วยว่า "รพ.ไหน" ที่ใช้ feature นี้
- [ ] ถ้ามี site-specific flow ให้ระบุใน ticket ชัดเจน
- [ ] เมื่อ requirement เปลี่ยน แจ้ง QA ก่อน sprint start

### **QA** รับปากว่าจะทำ
- [ ] ไม่ block sprint ด้วย edge case ที่ไม่ใช่ critical
- [ ] ส่ง Smoke Test result ภายใน 1 วันหลังรับ build
- [ ] แยก P0 bug (ต้อง fix ทันที) กับ P2–P3 (fix ตามแผน) ให้ชัดเจน
- [ ] รักษา Test Intents ให้ครบ 4 แบบ แต่ทำ Grade A ก่อน (Happy + Unhappy)

---

## 📊 9. Mapping กับ RTM Workbook (v1.6)

> Workbook ปัจจุบันมี **11 ชีต** รองรับ strategy นี้ครบแล้ว — ดูรายละเอียดโครงสร้างเต็มใน [RTM_Test_Management_KM.md](./RTM_Test_Management_KM.md)

### โครงสร้างที่รองรับ Strategy

| Sheet / Column | รองรับ Strategy ข้อไหน | หมายเหตุ |
|---|---|---|
| **Test Cases › TC ID** `[MOD]-TC[NNN]` | Section 6 Regression Strategy | filter by module ได้ทันที เช่น `APT-TC*` |
| **Test Cases › Test Intent** | Section 3 Phase A/B | Happy/Unhappy/Edge/Error |
| **Test Cases › Regression? + Smoke Test?** | Section 6 Sprint Type | กรองเคสตาม trigger ได้ทันที |
| **Test Cases › Applicability** | Section 1 Multi-site | Core รันทุก site / Site-specific เฉพาะ site |
| **Test Cases › Critical Point** | Section 2 Critical Points | tag 5 จุดที่ Dev ต้องรับผิดชอบ |
| **Test Cases › Case Type** | Section 3 Phase B | Functional / Non-Functional: Security / Performance / Compliance |
| **Test Runs › Run Type + Phase** | Section 3 Phase A/B | UAT-A / UAT-B / Smoke / Regression / Hotfix / New-Site |
| **Test Runs › Cycle ID** | Section 9.1 Build Gate | ผูกทุก run กับ build cycle |
| **Test Cycles** (ชีตใหม่) | Section 4 Mitigation Gate | Gate 1→2→3 ก่อนรัน full suite |
| **Site_Feature** | Section 1 Multi-site | เพิ่ม site ใหม่ได้โดยไม่ต้องแก้สูตร |
| **Master Data** | ทุก section | dropdown ป้องกัน typo ที่ทำให้ COUNTIF พัง |

### 9.1 Build Gate — ก่อนรัน Test ทุกครั้ง

```
Dev ส่ง build → QA เปิด Cycle ใหม่ใน Test Cycles
        │
        ▼
Gate 1: Master Data ครบไหม?
  Fail → reject build → Dev แก้ก่อน
        │ Pass
        ▼
Gate 2: Smoke Test (Smoke Test? = Yes) ผ่านไหม?
  Fail → reject build → Dev แก้ก่อน
        │ Pass
        ▼
Gate 3: อนุมัติรัน Full Suite
```

### 9.2 Filter Recipe ตาม Sprint Type

| Trigger | Filter บน Test Cases | ชีต Test Runs: Run Type |
|---|---|---|
| Sprint ปกติ | `Smoke Test? = Yes` | Smoke |
| Pre-release | `Regression? = Yes` | Regression |
| Post-hotfix | `Module = [ที่แก้]` | Hotfix |
| New site | Site_Feature → Core → Site-specific | New-Site |
| UAT Phase A | `Test Intent = Happy / Unhappy` | UAT · Phase = A |
| UAT Phase B | `Test Intent = Edge / Error` | UAT · Phase = B |

---

## 🏁 10. Exit Criteria — "เมื่อไหร่ถือว่าทดสอบเสร็จ"

> Entry Criteria = ก่อนเริ่มรัน (Build Gate) | Exit Criteria = เมื่อไหร่จะหยุดรัน

### Phase A — UAT Stabilization

| เงื่อนไข | เกณฑ์ |
|---|---|
| Pass rate | Happy + Unhappy TC ≥ **95%** ต่อ site |
| P0 bug | **= 0** (ไม่มี P0 เปิดอยู่) |
| P1 bug | ≤ 3 และมี workaround ชัดเจน |
| Coverage | ทุก Scenario มีผลรันอย่างน้อย 1 ครั้ง |

### Phase B — Pre Go-Live

| เงื่อนไข | เกณฑ์ |
|---|---|
| Pass rate (Functional) | ≥ **95%** ทุก module |
| Pass rate (Non-Functional) | ≥ **80%** (Security + Compliance ต้องผ่านทุกเคส) |
| P0 + P1 bug | **= 0** |
| P2 bug | มี plan ปิดภายใน 1 sprint หลัง go-live |
| Regression | Full suite ผ่านอย่างน้อย 1 รอบในทุก site |

### Regression Sprint

| เงื่อนไข | เกณฑ์ |
|---|---|
| Pass rate | ≥ **95%** |
| P0 bug | **= 0** |
| Delta จาก sprint ก่อน | ไม่มี test ที่เคย Pass แล้วกลาย Fail (regression) |

---

## 🐛 11. Defect Tracking — bug ไปไหน ทำอะไรต่อ

### นิยาม Priority

| Priority | นิยาม | ตัวอย่างใน HIS | Action |
|---|---|---|---|
| **P0 — Critical** | ระบบ crash / data loss / ผู้ป่วยได้รับอันตราย | HN สลับ · ยาผิดคน · บิลหาย | block sprint ทันที · Dev fix ก่อนออก build ใหม่ |
| **P1 — High** | feature หลักพังแต่ไม่ crash · workaround ยาก | นัดหมายบันทึกไม่ได้ · Lab order ไม่ส่ง | fix ใน sprint นี้ · QA re-test ก่อน release |
| **P2 — Medium** | feature รอง / UI ผิด / workaround ได้ | ปุ่มแสดงผิดที่ · เลขลำดับข้ามไป | log ใน backlog · fix sprint ถัดไป |
| **P3 — Low** | cosmetic / nice-to-have | สีปุ่มไม่ตรง · tooltip ผิด | fix เมื่อมีเวลา |

### กระบวนการ

```
QA เจอ bug ระหว่างรัน TC
        │
        ▼
บันทึกใน Linear: ชื่อ bug + P0/P1/P2/P3 + TC ID อ้างอิง + screenshot
        │
        ▼
P0/P1 → notify Dev ทันที (Slack/comment ใน Linear)
P2/P3 → log และ continue รัน TC ต่อ
        │
        ▼
Dev fix → ส่ง build ใหม่ → QA เปิด Cycle ใหม่
        │
        ▼
QA re-test เฉพาะ TC ที่ fail (Hotfix run type)
อัปเดต Status ใน Test Runs → Passed / Still Failing
```

### การเชื่อม Bug กับ RTM

- ทุก bug ต้องมี **TC ID อ้างอิง** ใน Linear description เช่น `APT-TC003`
- ถ้า bug ไม่มี TC รองรับ → QA สร้าง TC ใหม่ก่อน log bug (ป้องกัน gap ใน RTM)
- เมื่อ bug ปิด Dev ต้องระบุ build version ที่แก้ → QA อัปเดต Test Runs ใน Cycle ใหม่

---

## 🤖 12. AI-Assisted TC Generation — วิธีใช้ AI เขียน TC

> QA น้อย + AI ช่วย = เขียน TC เร็วขึ้น 3–5 เท่า · QA ทำหน้าที่ review + clinical judgment

### Input ที่ต้องให้ AI

```
1. Module: [ชื่อ module และ abbreviation เช่น Appointment (APT)]
2. Scenario: [Objective ของ scenario เช่น "สร้างนัดหมายใหม่สำหรับผู้ป่วยที่มีข้อมูลในระบบ"]
3. AC (Given/When/Then):
   Given  [precondition]
   When   [action]
   Then   [expected outcome]
4. Test Intents ที่ต้องการ: Happy / Unhappy / Edge / Error (ระบุหรือขอครบ 4)
5. Critical Point (ถ้ามี): Patient Identity / Drug Safety / Order Integrity / Financial / Audit Trail
```

### Output ที่ได้จาก AI

AI จะ generate ตารางพร้อม paste เข้า Excel:

| TC ID | Scenario | Test Intent | Title | Precondition | Steps | Expected Result | Priority | Critical Point | Regression? | Smoke Test? |

### สิ่งที่ QA ต้อง Review ก่อน Merge

- [ ] Steps ตรงกับหน้าจอจริงของระบบ (ชื่อปุ่ม / เมนู / URL)
- [ ] Expected Result ครอบ integration effect ด้วย (ไม่ใช่แค่ UI แสดงผล)
- [ ] Precondition ระบุ data setup ที่ต้องทำก่อนรัน
- [ ] Smoke Test? = Yes เฉพาะ TC ที่เป็น critical path จริงๆ (ไม่ใช่ทุก Happy TC)
- [ ] Critical Point tag ถูกต้อง หรือ `-` ถ้าไม่เกี่ยว

### ตัวอย่างที่สร้างแล้ว

- [generated_tc_APT.md](../docs/generated_tc/generated_tc_APT.md) — Appointment module 10 TC ครบ 4 intents

---

> **จัดทำโดย:** QA Team | **อัปเดตล่าสุด:** 2026-06-27
> **เอกสารที่เกี่ยวข้อง:**
> - [qa_methodology_km.md](./qa_methodology_km.md) — QA Responsibility Mapping + Test Intent Classification
> - [RTM_Test_Management_KM.md](./RTM_Test_Management_KM.md) — โครงสร้าง workbook + filter recipe + TC ID format
