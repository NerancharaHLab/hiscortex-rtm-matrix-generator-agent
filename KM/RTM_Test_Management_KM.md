# 📘 KM: RTM Multi-Tenant Test Management Workbook

> Knowledge-management handoff doc สำหรับ agent/ทีมที่รับช่วงต่อ
> ไฟล์ต้นทาง: RTM workbook (Excel) · ข้อมูลจริงจาก E2E_TMH-UAT V2.6.0
>
> **เอกสารที่เกี่ยวข้อง:**
> - [qa_methodology_km.md](./qa_methodology_km.md) — QA Responsibility Mapping + Test Intent Classification + Mitigation Strategy
> - [qa_testing_strategy_for_team.md](./qa_testing_strategy_for_team.md) — Testing Pyramid + Phase A/B + Exit Criteria + Defect Tracking + AI TC Generation

---

## 1. วัตถุประสงค์
Workbook นี้คือ Requirements Traceability Matrix (RTM) สำหรับบริหารเทสของระบบ HIS ที่มีลูกค้าหลายโรงพยาบาล ออกแบบให้ traceability ไหลครบสาย Module → Scenario → Test Case → Execution และคำนวณ coverage / execution อัตโนมัติ

---

## 2. โครงสร้างชีต (11 ชีต)

| ชีต | บทบาท | คอลัมน์หลัก / คีย์ |
|---|---|---|
| Dashboard | สรุป coverage & execution รายโมดูล | KPI + ตาราง modules (COUNTIFS) |
| Sites | ทะเบียนลูกค้า (โรงพยาบาล) | Site ID (PK): dev-x (Core กลาง), NUH, SBH, TMH |
| Modules | โมดูลของระบบ | Module ID (PK) MOD-01..n |
| Scenarios | สถานการณ์ทดสอบ (= requirement unit) | Scenario ID (PK) TS001-045, Module (FK), Objective, Related Risk, #TC, Covered? |
| Test Cases | เคสทดสอบ | TC ID (PK) format: `[MOD]-TC[NNN]`, Scenario ID (FK), Module/Scenario (lookup), Test Intent, Case Type, Critical Point, Priority, Applicability, Regression?, Smoke Test? |
| Test Runs | ผลรันต่อรอบ / ต่อ รพ. | Run ID (PK), TC ID (FK), Cycle ID (FK), Site ID, Version, Run Type, Phase, Status |
| Test Cycles | บันทึก build gate ต่อรอบ | Cycle ID (PK), Build Version, Site ID, Gate 1 (Master Data), Gate 2 (Smoke), Gate 3 (Full Auth), Status, Rejected Reason |
| Site_Feature | enablement matrix Site × Module | โมดูลที่แต่ละ รพ.เปิดใช้ (Yes/No) |
| Master Data | คลังค่า dropdown | Severity, Priority, Case Type (Functional / Non-Functional: Security / Non-Functional: Performance / Non-Functional: Compliance), Run Status, Critical Point, Yes/No ฯลฯ |
| Version History | changelog | v1.0 → v1.x |
| QA Mapping | เอกสารหลักการ QA | Dev vs QA responsibility, Test Flow (Happy/Unhappy/Edge/Error) |

---

## 3. ความสัมพันธ์ (เชื่อมด้วย ID)

```
Site ─┐
      └─(Site × Module)─ Module ─< Scenario ─< Test Case ─< Test Run
                                                    ↑
                                            Master Data (dropdown)
```

ทุกชั้นเป็นความสัมพันธ์ 1-ต่อ-หลาย ผูกด้วยคีย์ ID
- ID = input (พิมพ์เอง, สีน้ำเงิน)
- ชื่อ / ความสัมพันธ์ = สูตร (ดึงด้วย XLOOKUP)

---

## 4. กลไกสำคัญ (ทุกอย่าง formula-driven / dynamic)

| กลไก | สูตรที่ใช้ | ทำอะไร |
|---|---|---|
| Lookup | XLOOKUP | แปลง ID → ชื่อ (เช่น Test Cases ดึง Module/Scenario Name จาก Scenario ID) |
| Coverage | COUNTIF | นับ #TC ต่อ scenario → Covered? จับ scenario ที่ไม่มีเทส (coverage gap) |
| Execution | COUNTIFS | Dashboard นับ Pass / Fail / Not Run ต่อโมดูล + คำนวณ Exec % |
| Validation | Data Validation list | dropdown อ้าง Master Data / Sites / Modules ทุกช่องค่าควบคุม |

---

## 4.1 TC ID Format — มาตรฐาน Modular ID

### รูปแบบ

```
[MOD]-TC[NNN]

MOD = ตัวย่อโมดูล 3 ตัวอักษร (ตารางด้านล่าง)
NNN = ลำดับ 3 หลัก เริ่มจาก 001 ต่อโมดูล (reset ทุก module)
```

ตัวอย่าง: `APT-TC001`, `REG-TC042`, `OPD-TC277`

### กฎที่ต้องรักษา

1. **Counter reset ต่อ module** — REG เริ่ม 001, OPD เริ่ม 001 แยกกัน ไม่นับต่อกัน
2. **Site ไม่อยู่ใน TC ID** — site ผูกที่ Test Runs ผ่าน Site ID ไม่ใช่ที่ตัว TC
3. **ห้าม recycle ID** — TC ที่ลบออกให้ mark deprecated ห้ามเอา ID นั้นมาใช้ซ้ำ
4. **3 หลักรองรับได้ถึง 999 TC ต่อ module** — เพียงพอสำหรับทุก module ใน HIS

### ตาราง Module Abbreviation

**กลุ่ม Admin / Config (RTM ปัจจุบัน)**

| Module | Abbreviation | TC ปัจจุบัน | สถานะ |
|---|---|---|---|
| Setting | SET | ย้ายจาก TC sequential | ✅ Active |
| Insurance Plan | INS | ย้ายจาก TC sequential | ✅ Active |
| Payor | PAY | ย้ายจาก TC sequential | ✅ Active |
| Permission | PRM | ย้ายจาก TC sequential | ✅ Active |
| Role Permission | RPM | ย้ายจาก TC sequential | ✅ Active |
| Appointment | APT | ย้ายจาก TC sequential | ✅ Active |
| Migration Procedure | MGP | ย้ายจาก TC sequential | ✅ Active |
| Migration Procedure Form | MGF | ย้ายจาก TC sequential | ✅ Active |
| Vital Signs Viewer | VSV | ย้ายจาก TC sequential | ✅ Active |
| Discharge Summary | DCH | ย้ายจาก TC sequential | ✅ Active |

**กลุ่ม Clinical Core — Phase 1 (Cortex ready 100%)**

| Module | Abbreviation | TC พร้อม | สถานะ |
|---|---|---|---|
| Registration | REG | 257 | ✅ เพิ่มได้เลย |
| OPD | OPD | 277 | ✅ เพิ่มได้เลย |
| Claim | CLM | 202 | ✅ เพิ่มได้เลย |
| Pharmacy | PHA | 156 | ✅ เพิ่มได้เลย |
| Lab | LAB | 61 | ✅ เพิ่มได้เลย |
| Imaging | IMG | 7 | ✅ เพิ่มได้เลย |

**กลุ่ม Clinical Core — Phase 2 (รอ Expected Result)**

| Module | Abbreviation | TC ทั้งหมด | ขาด | สถานะ |
|---|---|---|---|---|
| IPD | IPD | 130 | 43 | ⏳ รอ Dev เติม Expected Result |
| Admission Center | AMC | 32 | 3 | ⏳ รอ Dev เติม Expected Result |

**กลุ่ม Clinical Core — Phase 3 (Placeholder)**

| Module | Abbreviation | สถานะ |
|---|---|---|
| EMR | EMR | ⚠️ มีโครง 8 TC แต่ยังไม่มี Expected Result |
| Cashier | CSH | ⚠️ Placeholder ยังไม่มี TC จริง |
| CPOE | CPO | ⚠️ Placeholder |
| Coder | CDR | ⚠️ Placeholder |

### Migration Plan สำหรับ TC เดิม (TC001–TC116)

TC ชุดเดิม 74 รายการใช้ sequential ID ไม่มี module prefix — ต้อง re-map เมื่อเปิด Excel:

```
1. เปิดชีต Test Cases ใน workbook
2. ดูว่า TC แต่ละแถวผูกกับ Scenario ID ไหน
3. ดู Scenario ID → Module → ได้ abbreviation
4. rename TC ID จาก TC00X → [MOD]-TC00X
5. อัปเดต Test Runs ให้อ้างอิง TC ID ใหม่
```

---

## 4.2 Critical Point — tag ความเสี่ยง 5 จุดของ Dev

คอลัมน์ **Critical Point** ใน Test Cases ใช้ระบุว่า TC นี้ verify ความถูกต้องของจุดใดที่ Dev ต้องรับผิดชอบที่ Unit Test ระดับล่าง หากพบว่า TC ใน QA ยัง fail ทั้งที่ Dev อ้างว่า Unit Test ผ่านแล้ว → ใช้ column นี้ escalate ได้ทันที

| Critical Point | ความหมายในบริบท HIS | ตัวอย่าง TC ที่ tag |
|---|---|---|
| **Patient Identity** | ข้อมูล HN / ชื่อ-นามสกุลไม่สลับ ไม่ผิดคน | REG-TC001 ลงทะเบียนผู้ป่วยใหม่ |
| **Drug Safety** | allergy check, dosage calculation, ชื่อยาถูกต้อง | PHA-TC001 จ่ายยาตามใบสั่ง |
| **Order Integrity** | คำสั่งแพทย์ส่งถึง destination ถูกต้อง ไม่หาย | OPD-TC010 สั่ง Lab → ไปถึง LAB module |
| **Financial** | คำนวณค่ารักษาถูกต้อง ไม่มีรายการหาย | CSH-TC001 คิดเงินผู้ป่วย |
| **Audit Trail** | ทุก action มี log + user + timestamp | ทุก TC ที่มีการบันทึกข้อมูล |
| **-** | TC นี้ไม่เกี่ยวกับ 5 จุดข้างต้น | Config / UI / report TC ทั่วไป |

> ถ้า Dev ยืนยันว่า Unit Test ครอบ Critical Point ทั้ง 5 แล้ว QA ไม่ต้อง re-test ชั้น unit — แต่ยังต้อง verify ที่ระดับ Integration/E2E ผ่าน TC ที่ tag ไว้

---

## 4.3 Non-Functional Test Case Types

Case Type ใน Master Data รองรับทั้ง Functional และ Non-Functional:

| Case Type | ทดสอบอะไร | ทำใน Phase ไหน |
|---|---|---|
| **Functional** | business flow ทำงานถูกต้องตาม requirement | Phase A + Phase B |
| **Non-Functional: Security** | RBAC · PHI protection · Audit log · session timeout | Phase B |
| **Non-Functional: Performance** | response time ช่วงผู้ป่วยหนาแน่น · concurrent users | Phase B |
| **Non-Functional: Compliance** | HL7 / ICD-10 / สปสช. (NHSO) format ถูกต้อง | Phase B |

> Non-Functional TC จะมี Regression? = Yes แต่ Smoke Test? = No เสมอ เพราะไม่ใช่ critical path สำหรับ sprint ปกติ

---

## 4.4 Test Cycles — Build Gate Sheet

ชีต **Test Cycles** บันทึกว่า build แต่ละรอบผ่าน gate ไหนแล้วก่อน QA จะรัน full suite

### คอลัมน์ใน Test Cycles

| คอลัมน์ | ค่าที่เป็นไปได้ | หมายความว่า |
|---|---|---|
| Cycle ID | CYC-001, CYC-002 ... | ID ของรอบการทดสอบ (PK) |
| Build Version | v2.6.0, v2.6.1 ... | version ของ build ที่รับมา |
| Site ID | TMH / NUH / SBH | รพ.ที่รันรอบนี้ |
| Date | วันที่รับ build | — |
| Gate 1 — Master Data | Pass / Fail | ข้อมูลระบบตั้งต้นครบและถูกต้องไหม |
| Gate 2 — Smoke Test | Pass / Fail / Blocked | critical path ผ่านไหม (Smoke Test? = Yes) |
| Gate 3 — Full Auth | Yes / No | QA อนุมัติให้รัน full suite หรือยัง |
| Status | In Progress / Accepted / Rejected | สถานะรวมของ cycle นี้ |
| Rejected Reason | ข้อความ | เหตุผลถ้า reject build กลับ Dev |

### Flow การใช้งาน

```
Dev ส่ง build
      │
      ▼
QA เปิด Cycle ใหม่ใน Test Cycles (status = In Progress)
      │
      ▼
Gate 1: ตรวจ Master Data (รหัสยา, ตารางเวร, สิทธิ์ผู้ป่วย)
      ├── Fail → Gate 1 = Fail · Status = Rejected · ส่งกลับ Dev
      └── Pass → ไป Gate 2
      │
      ▼
Gate 2: รัน Smoke Test (Smoke Test? = Yes)
      ├── Fail → Gate 2 = Fail · Status = Rejected · ส่งกลับ Dev
      └── Pass → Gate 3 = Yes · Status = Accepted
      │
      ▼
รัน Full Test Suite ตาม Run Type ที่กำหนด
```

### เชื่อม Test Cycles กับ Test Runs

Test Runs มีคอลัมน์ **Cycle ID (FK)** — ทุก run ใน cycle เดียวกันใช้ Cycle ID เดียวกัน ทำให้ filter ได้ว่า "build CYC-003 มีผลรันอะไรบ้าง" และ "reject เพราะ Gate ไหน"

---

## 5. หลักการออกแบบ (design decisions — สำคัญที่สุดสำหรับ KM)

1. ไฟล์เดียว ไม่แยกตามประเภทเทส — E2E / Regression / Functional เป็น attribute (คอลัมน์) ไม่ใช่เหตุผลในการแยกไฟล์ แยกไฟล์เฉพาะเมื่อคนละ product/ทีม หรือไฟล์ใหญ่จนช้า

2. ไม่ duplicate ไฟล์ต่อ version
   - version ของซอฟต์แวร์ → คอลัมน์ใน Test Runs
   - version ของเอกสาร → Version History + auto-history ของแพลตฟอร์ม (SharePoint/OneDrive/Google)
   - duplicate ได้กรณีเดียว: baseline snapshot ตอน release/audit (แช่แข็ง read-only)

3. Multi-tenant = แยก Core ออกจาก Variant — ไม่ก๊อปชุดเทสต่อ รพ. ใช้ enablement matrix (Site × Module) + field Applicability (Core / Site-specific) + Site ID แทน
   - Test Plan ต่อ รพ. = เคสที่ enabled สำหรับ รพ.นั้น AND (Core OR tag ตรง รพ.)

4. ปรับโครงให้ตรงข้อมูลจริง — E2E จริงมีลำดับชั้น Module → Scenario → Test Case (ไม่มีชั้น Feature) จึงลบชั้น Feature/Feature Groups ที่ไม่มีข้อมูลรองรับ และเปลี่ยน Dashboard เป็น coverage รายโมดูล

---

## 6. ข้อมูลปัจจุบัน

- 10 Modules: Setting, Insurance Plan, Payor, Permission, Role Permission, Appointment, Migration Procedure, Migration Procedure Form, Vital Signs Viewer, Discharge Summary
- 45 Scenarios (TS001-TS045)
- 74 Test Cases (TC ID สูงสุด TC116 — ID ไม่ต่อเนื่อง มีบาง ID ที่ถูกลบออกไปแล้ว)
- 74 Test Runs (สถานะ Not Run ทั้งหมด — UAT ยังไม่เริ่มรัน)
- ทุก scenario มีเทสครอบคลุม (ไม่มี coverage gap)
- แหล่งข้อมูล: ไฟล์ E2E_TMH-UAT V2.6.0 (ชีต Test case + Scenario)

> **หมายเหตุ scope:** workbook ชุดนี้ครอบเฉพาะ Admin/Config modules ของ TMH — Clinical core (OPD / Lab / Pharmacy / Billing / IPD) อยู่ในไฟล์แยก `(TMH) Cortex-TestCase.xlsx` ซึ่งมี 1,139 TC แยกต่างหาก ทั้งสองชุดไม่ได้แทนกัน

---

## 7. วิธีใช้งาน / ขยายต่อ

| งาน | ทำอย่างไร |
|---|---|
| เพิ่มเคสทดสอบ | กรอกแถวใหม่ในชีต Test Cases (สูตร lookup/coverage รองรับถึง ~แถว 200–2000) |
| บันทึกผลรัน UAT | อัปเดตคอลัมน์ Status ใน Test Runs (Pass/Fail/Blocked) → Dashboard คำนวณเอง |
| เพิ่มโรงพยาบาล | เพิ่มแถวใน Sites + ตั้ง enablement ใน Site_Feature |
| เพิ่มโมดูล/สถานการณ์ | เพิ่มใน Modules / Scenarios (ผูก Module ID) |
| บันทึกการเปลี่ยนแปลง | เพิ่มแถวใน Version History |

---

## 7.1 คอลัมน์ควบคุมการรัน (Run Control Columns)

คอลัมน์ใน Test Cases ที่ใช้กรองเคสให้ตรงกับงานแต่ละประเภท:

| คอลัมน์ | ค่าที่เป็นไปได้ | หมายความว่า |
|---|---|---|
| **Test Intent** | Happy / Unhappy / Edge / Error | ประเภทของสถานการณ์ที่ทดสอบ |
| **Applicability** | Core / Site-specific | Core = รันทุก รพ. / Site-specific = ระบุ รพ.ที่เกี่ยวข้อง |
| **Regression?** | Yes / No | Yes = เคสนี้อยู่ใน regression suite (รันซ้ำทุก release) |
| **Smoke Test?** | Yes / No | Yes = เคสนี้อยู่ใน critical path smoke (subset ของ Regression) |

> **กฎที่ต้องรักษา:** ถ้า Smoke Test? = Yes → Regression? ต้องเป็น Yes เสมอ เพราะ smoke ⊂ regression
> ถ้า Regression? = No → เคสนั้นรันเฉพาะ UAT ครั้งแรกเท่านั้น (เช่น migration test ที่ทำครั้งเดียว)

คอลัมน์ **Run Type** และ **Phase** ใน Test Runs บันทึกว่า execution นั้นเป็นส่วนของงานประเภทไหนและอยู่ในช่วงไหน:

| Run Type | Phase | เมื่อไหร่ |
|---|---|---|
| UAT | A | UAT Phase A — ยืนยัน Happy + Unhappy flow ว่าใช้งานได้ (stabilization) |
| UAT | B | UAT Phase B — ทดสอบ Edge + Error ก่อน go-live จริง |
| Smoke | - | รันตอนรับ build ใหม่ทุก sprint |
| Regression | - | รันรอบ pre-release ครบทุก regression TC |
| Hotfix | - | รันเฉพาะ area ที่แก้ + adjacent module |
| New-Site | - | รันรอบ onboard รพ.ใหม่ |

> **Phase = `-`** หมายถึง run นั้นไม่ใช่ UAT จึงไม่มีการแบ่ง Phase A/B

---

## 7.2 Filter Recipe — ทำอะไร เมื่อเจอสถานการณ์ไหน

> ใช้ Excel Filter บนชีต **Test Cases** ตามสถานการณ์ด้านล่าง
> แต่ละ recipe บอกว่า **เจอสถานการณ์แบบไหน → กรองอะไร → ได้ผลลัพธ์อะไร**

---

### 🟡 สถานการณ์ที่ 1 — รับ Build ใหม่ทุก Sprint (Smoke Test)

**เมื่อไหร่:** Dev ส่ง build มาให้ QA ทุก sprint (ปกติทุก 1–2 สัปดาห์)

**เป้าหมาย:** ตรวจว่า flow หลักของระบบยังทำงานได้อยู่ ก่อนจะรันเทสอื่นต่อ ถ้า smoke fail แปลว่า build ยังไม่พร้อม → ส่งกลับ Dev ได้เลย ไม่ต้องเสียเวลารันต่อ

**กรองชีต Test Cases:**
```
Smoke Test? = Yes
```

**ผลลัพธ์:** ได้ชุดเคส ~20% ที่ครอบ critical path — ใช้เวลาประมาณ 2–3 ชั่วโมง

---

### 🔴 สถานการณ์ที่ 2 — ก่อน Release ขึ้น Production (Full Regression)

**เมื่อไหร่:** ก่อนปล่อย version ใหม่สู่ production ทุกครั้ง ไม่ว่าจะเป็น major หรือ minor release

**เป้าหมาย:** ยืนยันว่าทุก feature ที่เคยทำงานได้ ยังทำงานได้เหมือนเดิมหลังจากมีการแก้โค้ด ป้องกัน regression (สิ่งที่เคยดีแล้วกลับพัง)

**กรองชีต Test Cases:**
```
Regression? = Yes
```
จากนั้นแยก execution ตาม Site ใน Test Runs เพื่อให้รู้ว่าแต่ละ รพ. ผ่านหรือไม่

**ผลลัพธ์:** ได้ชุดเคสครบ regression suite — ใช้เวลาประมาณ 1–2 วัน

---

### 🟠 สถานการณ์ที่ 3 — Dev แก้ Bug แล้วส่งมาให้ตรวจ (Hotfix)

**เมื่อไหร่:** Dev แก้ bug เฉพาะจุดแล้วส่ง build กลับมา ไม่ใช่ release ใหม่ทั้งหมด

**เป้าหมาย:** ตรวจว่าสิ่งที่แก้ทำงานถูกต้อง และการแก้ครั้งนี้ไม่ได้ทำให้โมดูลข้างเคียงพังไปด้วย

**กรองชีต Test Cases:**
```
Step 1 → Module = [โมดูลที่แก้]           ← ตรวจตรงจุดที่แก้
Step 2 → Module = [โมดูลที่รับข้อมูลต่อ]   ← ตรวจโมดูลที่อาจกระทบ
```

ตัวอย่าง: Dev แก้ Appointment → ตรวจ Appointment + Vital Signs Viewer (ที่ดึงข้อมูลนัดมาแสดง)

**ผลลัพธ์:** ได้เคสเฉพาะ area ที่กระทบ — ใช้เวลาประมาณ 1–4 ชั่วโมง

---

### 🟣 สถานการณ์ที่ 4 — Onboard โรงพยาบาลใหม่

**เมื่อไหร่:** มี รพ.ลูกค้าใหม่เข้ามา ต้องทดสอบว่าระบบทำงานได้ในสภาพแวดล้อมของ รพ.นั้น

**เป้าหมาย:** ยืนยัน config ของ รพ.ใหม่ถูกต้อง และ flow ที่ รพ.นั้น enable ไว้ทำงานได้จริง

**ขั้นตอน:**
```
Step 1 → ชีต Site_Feature: ดูว่า รพ.ใหม่ enable Module ไหนบ้าง (Yes/No)
Step 2 → Test Cases → Filter: Applicability = Core
          รันก่อน — เป็นเคสที่ทุก รพ.ต้องผ่านเหมือนกัน
Step 3 → Test Cases → Filter: Applicability = Site-specific + tag ตรง รพ.นั้น
          รันต่อ — เป็นเคสเฉพาะของ รพ.นั้น
```

**ผลลัพธ์:** ได้ชุดเคสที่ครอบทั้ง core + site-specific — ใช้เวลาประมาณ 2–3 วัน

---

### 🔵 สถานการณ์ที่ 5 — UAT รอบแรก Phase A (ช่วง Stabilization)

**เมื่อไหร่:** ช่วงเริ่มต้น UAT ที่ระบบยังไม่ stable — โฟกัสให้ผ่าน flow หลักก่อน

**เป้าหมาย:** ยืนยันว่าเส้นทางการใช้งานหลักของโรงพยาบาล (patient journey) ทำงานครบลูป ยังไม่ต้องสนใจ edge case

**กรองชีต Test Cases:**
```
Test Intent = Happy  →  flow ปกติที่ใช้งานทุกวัน
Test Intent = Unhappy → flow แยกที่มีธุรกิจรองรับ (เช่น walk-in, partial payment)
```

**บันทึก Test Runs:** Run Type = `UAT` · Phase = `A`

**ผลลัพธ์:** ได้เคสที่บอกว่าระบบ "ใช้งานได้จริง" หรือยัง ก่อนนำขึ้น production

---

### ⚫ สถานการณ์ที่ 6 — UAT Phase B (ก่อน Go-Live จริง)

**เมื่อไหร่:** Phase A ผ่านแล้ว ระบบ stable — ทดสอบความแข็งแกร่งของระบบก่อนเปิดใช้จริง

**เป้าหมาย:** ตรวจว่าระบบรับมือกับกรณีผิดปกติและระบบล่มได้ โดยไม่ทำให้ข้อมูลคนไข้เสียหาย

**กรองชีต Test Cases:**
```
Test Intent = Edge   → เงื่อนไขสุดขั้ว เช่น เด็กแรกเกิด 0 วัน, บิล 0 บาท, ชื่อยาว
Test Intent = Error  → ระบบล่มกลางคัน เช่น network หลุดขณะบันทึก, DB timeout
```

**บันทึก Test Runs:** Run Type = `UAT` · Phase = `B`

**ผลลัพธ์:** ได้ความมั่นใจว่าระบบปลอดภัยพอสำหรับการใช้งานกับผู้ป่วยจริง

ข้อจำกัด / คำแนะนำ: ถ้าข้อมูลโตหลักพันเคส หรือมีหลายคนรันพร้อมกัน แนะนำแปลงชีตเป็น Excel Table (ให้สูตรขยายเอง) หรือย้ายไป test management tool (TestRail / Jira+Xray / Azure DevOps Test Plans) ที่ทำ versioning + RTM + execution history ให้ native — spreadsheet เหมาะกับช่วงเริ่มต้นเท่านั้น

---

## 8. Changelog

| Version | สิ่งที่ทำ |
|---|---|
| v1.0 | สร้างโครง RTM multi-tenant (10 ชีต) + ข้อมูลตัวอย่าง |
| v1.1 | แทนที่ รพ.ตัวอย่างด้วยรายชื่อจริง: dev-x, NUH, SBH, TMH |
| v1.2 | นำเข้าข้อมูลจริง E2E_TMH-UAT V2.6.0 (10 Modules / 45 Scenarios / 74 Test Cases / 74 Test Runs); ลบชั้น Feature; Site_Feature → Site × Module; Dashboard เป็น coverage รายโมดูล |
| v1.3 | เพิ่มคอลัมน์ Test Intent / Applicability / Regression? / Smoke Test? ใน Test Cases และ Run Type ใน Test Runs; เพิ่ม Section 7.1–7.2 filter recipe ตามงานแต่ละประเภท |
| v1.4 | เพิ่มคอลัมน์ Phase ใน Test Runs (A/B/-); แก้ Section 6 ระบุว่า TC ID ไม่ต่อเนื่อง (74 TC สูงสุด TC116); เพิ่ม note แยก scope workbook นี้ออกจาก Cortex-TestCase.xlsx |
| v1.5 | กำหนด TC ID format มาตรฐาน `[MOD]-TC[NNN]`; เพิ่ม Section 4.1 module abbreviation table ครบ 20 modules (Admin/Config + Clinical); เพิ่ม migration plan สำหรับ TC เดิม |
| v1.6 | เพิ่มชีตที่ 11 (Test Cycles); เพิ่มคอลัมน์ Critical Point ใน Test Cases + Section 4.2; เพิ่ม Non-Functional Case Types ใน Master Data + Section 4.3; เพิ่ม Section 4.4 อธิบาย Build Gate flow และโครงสร้าง Test Cycles sheet |
