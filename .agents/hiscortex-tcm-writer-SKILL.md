---
name: hiscortex-tcm-writer
description: Write new test scenarios and test cases into the HIS Cortex Test Case Management workbook's "2. Scenarios" and "1. Master_TCM" sheets, preserving existing formulas, dropdown lists, and data.
---

## เริ่มต้นใช้งาน (สำหรับมนุษย์ที่ส่ง skill นี้ให้ AI หลายตัวทำงานต่อกัน)

ถ้าคุณกำลังทำงานข้าม AI หลายตัว (เช่น เริ่มคุยกับ Ask Linear ใน Linear แล้วส่งต่อให้ Antigravity หรือ Claude ใน Excel หรือ ChatGPT) ทำตามนี้:

1. แปะ skill นี้ทั้งไฟล์ให้ AI ตัวที่คุณกำลังคุยด้วยอ่านก่อนเสมอ (ไม่ต้องอธิบายเพิ่ม AI จะเช็คความสามารถตัวเองเองตามหัวข้อ 0.1)
2. บอก Card ID ของ Linear ticket ที่ต้องการเขียนเทสเคส (เช่น `NUH-1199`) — AI จะดึงรายละเอียดเองถ้ามี connector หรือถามให้คุณ paste ถ้าไม่มี
3. **ถ้า AI ตัวนั้นเขียนไฟล์ Excel โดยตรงไม่ได้ (โหมด B ตามหัวข้อ 0.1)** คุณจะได้ตาราง Markdown/CSV กลับมา — คัดลอกทั้งหมดไปวางในแชทของ AI ตัวถัดไป (เช่น Antigravity หรือ Claude ใน Excel) พร้อมบอกว่า "นำไปเขียนต่อในไฟล์ TCM_HIS_Cortex ตาม skill hiscortex-tcm-writer"
4. AI ตัวถัดไปจะเช็คโหมดตัวเอง (หัวข้อ 0.1) และเขียนไฟล์จริงให้ พร้อมแจ้งผลตรวจสอบกลับมา (หัวข้อ 15)

หมายเหตุ: ไม่จำเป็นต้องอธิบายเพิ่มเติมว่าแต่ละหัวข้อคืออะไร — skill นี้ถูกออกแบบมาให้ AI อ่านแล้วเข้าใจเองทั้งหมดโดยไม่ต้องมีคนอธิบายเพิ่ม

## 0. อ่านก่อนเริ่มงาน (สำหรับ AI ที่ไม่มี context มาก่อนเลย)

นี่คือไฟล์ Excel ชื่อ `TCM_HIS_Cortex` ใช้บริหารจัดการ Test Case ของระบบโรงพยาบาล (HIS/Cortex) งานของคุณคือ **เพิ่ม Test Scenario และ/หรือ Test Case ใหม่** ลงใน 2 ชีตเท่านั้น: `1. Master_TCM` และ `2. Scenarios` โดยห้ามทำให้สูตร, dropdown, หรือข้อมูลเดิมเสียหายแม้แต่เซลล์เดียว อ่าน skill นี้ทั้งหมดก่อนพิมพ์อะไรลงไฟล์ — มันจะบอกทุกอย่างที่คุณต้องรู้ ไม่ต้องเดา

**ขอบเขตงาน (สำคัญที่สุด):** ห้ามแตะ แก้ไข หรือพิมพ์ข้อมูลใน sheet อื่นทั้งหมด (`Dashboard`, `Test_Plan`, `Settings`, `Read Me.`, `3. Test Executed for NUH`, `4. Task Support`) เพราะเป็น dashboard/lookup/สรุปผลอัตโนมัติที่ผูกสูตรมาจาก Master_TCM อยู่แล้ว โดยเฉพาะ `3. Test Executed for NUH` เป็นสูตร FILTER ทั้งชีท จะอัปเดตข้อมูลให้เองอัตโนมัติทันทีที่ Master_TCM ตรงเงื่อนไข (Execution Status = "Ready to Test" และ Run in This Cycle? = "Yes") — ไม่ต้องทำอะไรเพิ่มที่ชีทนั้น **ข้อยกเว้นเดียว:** อนุญาตให้เพิ่มค่า Module ใหม่ลงใน `Settings!D` ได้ เฉพาะกรณีที่ไม่มีค่าใดในลิสต์เดิมเหมาะสมจริงๆ ดูวิธีที่ถูกต้องในหัวข้อ 12.2 — ห้ามแก้ค่าอื่นใดใน Settings นอกจากนี้

### 0.1 เช็ค "โหมดการทำงาน" ของตัวเองก่อนเสมอ (Self-Detection — ทำก่อนพิมพ์อะไรทั้งสิ้น)

Skill นี้ถูกอ่านโดย AI หลายแพลตฟอร์มที่มีความสามารถต่างกัน **ห้ามเดาว่าตัวเองทำอะไรได้ ให้เช็คจากเครื่องมือที่ตัวเองมีจริงก่อนเริ่มงานทุกครั้ง** แล้วเลือก 1 ใน 3 โหมดนี้:

**โหมด C — Live Document Agent (เช่น Claude ใน Excel, Copilot ใน Excel):**
เช็ค: มีเครื่องมืออ่าน/เขียน cell ของ Excel ที่เชื่อมกับไฟล์ที่เปิดอยู่จริงโดยตรงไหม (เช่น get_cell_ranges, set_cell_range, execute_office_js หรือเทียบเท่า)? ถ้าใช่ → คุณอยู่โหมดนี้ เขียนข้อมูลผ่านเครื่องมือเหล่านั้นโดยตรงเท่านั้น **ห้ามพยายามเปิด/เซฟไฟล์ .xlsx เองผ่าน Python/openpyxl เด็ดขาด** เพราะจะสร้างไฟล์สำเนาที่ไม่ sync กับไฟล์จริงที่ผู้ใช้เห็นอยู่ ทำตามหัวข้อ 0-13 ตามปกติ

**โหมด A — Local File Agent (เช่น Antigravity หรือ coding agent อื่นที่มีสิทธิ์เข้าถึง filesystem):**
เช็ค: มีสิทธิ์รันโค้ด (Python/bash) ที่เปิด/เซฟไฟล์ .xlsx บนดิสก์ได้จริง แต่ไม่มีการเชื่อมต่อกับ Excel ที่เปิดอยู่แบบ live? ถ้าใช่ → คุณอยู่โหมดนี้ ทำตาม "Execution Strategy" (openpyxl script) ด้านล่างสุดของ skill นี้ **เพิ่มเติมจากที่เขียนไว้เดิม: ต้อง unhide แถวที่เขียนด้วย (`ws.row_dimensions[n].hidden = False`)** เพราะแถวว่างที่เตรียมไว้ล่วงหน้าถูกซ่อนอยู่ (ดูหัวข้อ 4 กฎเหล็กเรื่องแถวว่าง)

**โหมด B — Cloud/No-Write Agent (เช่น Ask Linear, ChatGPT ทั่วไป, Slack bot):**
เช็ค: ไม่มีทั้งสองอย่างข้างต้น (ไม่มี Office.js bridge และไม่มี filesystem access)? ถ้าใช่ → คุณอยู่โหมดนี้ ทำตามหัวข้อ 11 (สร้าง CSV/Markdown table ส่งต่อ ห้ามบอกว่าเขียนเสร็จแล้ว)

**กฎป้องกันข้อมูลชนกัน (สำคัญที่สุดเมื่อมีหลาย agent ทำงานร่วมกัน):** ห้ามให้โหมด A และโหมด C แก้ไฟล์เวอร์ชันเดียวกันพร้อมกันโดยไม่ sync กัน ถ้าใช้ทั้งคู่ในงานเดียวกัน ต้องถามผู้ใช้ก่อนเสมอว่าใครคือ "ต้นทางข้อมูลจริง (source of truth)" ณ ตอนนั้น แล้วให้อีกฝ่ายรอ/sync ใหม่หลังมีการเขียนเสร็จ ไม่ใช่เขียนพร้อมกัน

## 1. ศัพท์ที่ต้องรู้ (Glossary)

- **Card ID**: เลข ticket จาก Linear เช่น `NUH-802` (ไม่มีคำนำหน้า TS-/TC-) — เป็นตัวเชื่อมทุกอย่างเข้าด้วยกัน
- **Scenario ID**: รหัสของ "เรื่อง/ฟีเจอร์" ที่จะทดสอบ 1 เรื่อง = 1 แถวใน sheet `2. Scenarios` รูปแบบ `TS-{CardID}` เช่น `TS-NUH-802`
- **TC ID**: รหัสของ "เทสเคสย่อย" หนึ่งกรณีทดสอบ = 1 แถวใน sheet `1. Master_TCM` รูปแบบ `TC-{CardID}-{ลำดับ 3 หลัก}` เช่น `TC-NUH-802-001` — หลาย TC ID ผูกกับ 1 Scenario ID เดียวกันได้ (สอบหลายกรณีในฟีเจอร์เดียว)
- **Feature**: ข้อความสรุปสั้นๆ ต่อท้ายด้วยชื่อ Module คำนวณเองจากสูตร ไม่ต้องพิมพ์
- **BDD**: รูปแบบ Given/When/Then สำหรับอธิบายเงื่อนไข-การกระทำ-ผลลัพธ์

## 2. Workbook map (โครงสร้างไฟล์ทั้งหมด)

- **"1. Master_TCM"** — Excel Table ชื่อ `Master_TCM`, คอลัมน์ A:Y หนึ่งแถว = หนึ่งเทสเคส
- **"2. Scenarios"** — Excel Table ชื่อ `Scenarios`, คอลัมน์ A:H หนึ่งแถว = หนึ่ง scenario/feature (พ่อแม่ของเทสเคส)
- **"Settings"** — ลิสต์ค่าที่ dropdown ทุกตัวดึงมาใช้ (ห้ามแก้)
- **"3. Test Executed for NUH"** — auto จาก FILTER ของ Master_TCM ห้ามพิมพ์ตรงนี้
- **Dashboard, Test_Plan, Read Me., 4. Task Support** — อ้างอิง/รายงานเท่านั้น ห้ามแตะสำหรับงานนี้

## 3. "2. Scenarios" — columns (Table `Scenarios`, A:H)

| Col | Field         | Type                                                                                                                                                                                                                | Notes                                                                                                                                                 |
| --- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| A   | Scenario ID   | free text                                                                                                                                                                                                           | Format `TS-{CardID}` e.g. `TS-NUH-802`. Must be unique. **เช็คก่อนเสมอว่า Card ID นี้มี Scenario ID อยู่แล้วหรือยัง ถ้ามีให้ใช้ตัวเดิม ห้ามสร้างซ้ำ** |
| B   | Scenario Name | free text                                                                                                                                                                                                           | Short feature/story name, ภาษาอังกฤษหรือไทยก็ได้ ให้สอดคล้องกับของเดิมในชีท                                                                           |
| C   | Module        | free text (no dropdown, but MUST match a value from Settings!D: Pharmacy, Billing, EMR, Lab, Patient, Register, Triage, CPOE, Insurance, Appointment, Cashier, Claim, Report, Security, Audit, Admission, Document) |
| D   | Case Type     | free text (match Settings!M: Happy, Unhappy, Edge, Error)                                                                                                                                                           |
| E   | Objective     | free text — ประโยคเดียวสรุปว่าเทสเรื่องนี้เพื่อยืนยันอะไร                                                                                                                                                           |
| F   | Priority      | free text (match Settings!A: Critical, High, Medium, Low)                                                                                                                                                           |
| G   | Related Risk  | free text — ความเสี่ยง/ผลกระทบถ้าฟีเจอร์นี้พัง                                                                                                                                                                      |
| H   | Card ID       | free text                                                                                                                                                                                                           | Bare ticket ref, e.g. `NUH-802` (no `TS-`/`TC-` prefix) — this is the suffix used to build Scenario ID and TC IDs                                     |

No formulas live in this table. No pre-built blank rows exist beyond the last data row — **add new rows as real new table rows** (so banding/formatting stays correct), don't just type into cells past the table boundary.

## 4. "1. Master_TCM" — columns (Table `Master_TCM`, A:Y)

| Col | Field              | Type                                                                                                                                                                                                                                                                                                                                |
| --- | ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A   | TC ID              | free text — format `TC-{CardID}-{seq}` e.g. `TC-NUH-802-001`. Sequence is per Scenario ID group, zero-padded to 3 digits, continuing the existing max for that scenario (start at 001 for a brand-new scenario, never reuse or skip numbers).                                                                                       |
| B   | Scenario ID        | **DROPDOWN** (`=ScenarioIDList`, sourced from `2. Scenarios!A`). Must exactly match an existing row in the Scenarios table — add the scenario there FIRST if it doesn't exist yet.                                                                                                                                                  |
| C   | Module             | **DROPDOWN** (`=ModuleList` → Settings!D) — must match the Module of the parent Scenario.                                                                                                                                                                                                                                           |
| D   | Feature            | **FORMULA — ห้ามพิมพ์เด็ดขาด.** `="IPD - "&[@Module]`. มีอยู่แล้วทุกแถวรวมถึงแถวว่าง จะคำนวณเองทันทีที่กรอก Module (C)                                                                                                                                                                                                              |
| E   | Priority           | **DROPDOWN** (`=PriorityList` → Settings!A: Critical/High/Medium/Low)                                                                                                                                                                                                                                                               |
| F   | Test Case Name     | free text — **ต้องตามรูปแบบในหัวข้อ 6 ด้านล่าง** ห้ามตั้งชื่อกว้างเกินไป                                                                                                                                                                                                                                                            |
| G   | Pre-conditions     | free text — เงื่อนไขก่อนเริ่มทดสอบ                                                                                                                                                                                                                                                                                                  |
| H   | Test Steps         | free text, ลำดับเลข `1. 2. 3.` คั่นด้วยขึ้นบรรทัดใหม่ (\n) ในเซลล์เดียว                                                                                                                                                                                                                                                             |
| I   | Test Data          | free text — ใส่ "-" ถ้าไม่มีข้อมูลทดสอบเฉพาะ                                                                                                                                                                                                                                                                                        |
| J   | BDD                | free text, Given/When/Then — ใส่ "-" หรือเว้นว่างได้ถ้าไม่จำเป็น                                                                                                                                                                                                                                                                    |
| K   | Expected Result    | free text — ผลลัพธ์ที่คาดหวัง ระบุให้ตรวจสอบได้จริง ไม่คลุมเครือ                                                                                                                                                                                                                                                                    |
| L   | Test Level         | **DROPDOWN** (`=TestLevelList` → Settings!K: Unit/Integration/System/Acceptance)                                                                                                                                                                                                                                                    |
| M   | Test Type          | **DROPDOWN** (`=TestTypeList` → Settings!L: Functional/UI-UX/Security/Performance/Interoperability/Compliance)                                                                                                                                                                                                                      |
| N   | Case Type          | **DROPDOWN** (`=CaseTypeList` → Settings!M: Happy/Unhappy/Edge/Error) — ควรสอดคล้องกับ Case Type ของ Scenario แม่                                                                                                                                                                                                                   |
| O   | Create By          | **DROPDOWN** (`=MemberList` → Settings!I: Neran/Matt/Tar/Aof/June/Jame). กรอกช่องนี้จะ trigger สูตร P ให้ stamp วันที่อัตโนมัติ                                                                                                                                                                                                     |
| P   | Create Date        | **FORMULA — ห้ามพิมพ์เด็ดขาด.** `=IF(O<>"",IF(OR(P="",P=0),NOW(),P),"")` — stamp NOW() อัตโนมัติทันทีที่ O มีค่า                                                                                                                                                                                                                    |
| Q   | Review By          | **DROPDOWN** (`=MemberList`) — ปล่อยว่างได้ถ้ายังไม่มีคนรีวิว                                                                                                                                                                                                                                                                       |
| R   | Review Date        | **FORMULA — ห้ามพิมพ์เด็ดขาด.** สูตรรูปแบบเดียวกับ P ทุกประการ แค่ผูกกับ Q แทน `=IF(Q<>"",IF(OR(R="",R=0),NOW(),R),"")` — **นี่คือสูตร ไม่ใช่ช่องว่างเปล่าๆ** แม้ Q จะยังว่างอยู่ก็ตาม                                                                                                                                              |
| S   | Approval By        | **DROPDOWN** (`=MemberList`) — ปล่อยว่างได้ถ้ายังไม่มีคนอนุมัติ                                                                                                                                                                                                                                                                     |
| T   | Approval Date      | **FORMULA — ห้ามพิมพ์เด็ดขาด.** สูตรรูปแบบเดียวกับ P ผูกกับ S แทน `=IF(S<>"",IF(OR(T="",T=0),NOW(),T),"")` — **นี่คือสูตร ไม่ใช่ช่องว่างเปล่าๆ**                                                                                                                                                                                    |
| U   | Execution Status   | **DROPDOWN** (`=ExecutionStatusList` → Settings!G: Draft/Ready for Review/Ready to Test/Not Test). **ค่าเริ่มต้นของเทสเคสใหม่ทุกแถวคือ `Draft` เสมอ ไม่ต้องถามผู้ใช้ซ้ำ** — ใช้ค่าอื่นเฉพาะเมื่อผู้ใช้ระบุสถานะมาชัดเจนในคำสั่งเท่านั้น (ค่านี้จะดึงแถวไปโผล่ในชีท 3 อัตโนมัติก็ต่อเมื่อเป็น `Ready to Test` และ X เป็น `Yes` ด้วย) |
| V   | Cards Requirment   | free text — URL ของ Linear issue เช่น `https://linear.app/cortexcloud/issue/NUH-802/...`                                                                                                                                                                                                                                            |
| W   | Requirment Detail  | free text — สรุปสั้นๆ ของ ticket เช่น `[Module] คำอธิบาย` หรือ `[Bug][Module]คำอธิบาย`                                                                                                                                                                                                                                              |
| X   | Run in This Cycle? | **DROPDOWN** (`=RunInCycleList` → Settings!H: Yes/No)                                                                                                                                                                                                                                                                               |
| Y   | Remark             | free text, optional                                                                                                                                                                                                                                                                                                                 |

### ⚠️ กฎเหล็กเรื่องสูตร — ห้ามพิมพ์ทับคอลัมน์ D, P, R, T เด็ดขาด

ทั้ง 4 คอลัมน์นี้มีสูตรอยู่แล้วทุกแถวของตาราง (ตรวจสอบแล้วถึงแถว 476 ในไฟล์นี้ และจะขยายเพิ่มถ้าตารางโตขึ้น) พิมพ์ค่าทับแม้แถวเดียวจะทำลายการคำนวณอัตโนมัติของแถวนั้นถาวร **ข้อผิดพลาดที่พบบ่อยที่สุดคือเข้าใจผิดว่า R (Review Date) และ T (Approval Date) เป็นช่องว่างธรรมดา — ไม่ใช่ ทั้งคู่เป็นสูตร auto-timestamp เหมือน P ทุกประการ**

### ⚠️ กฎเหล็กเรื่องแถวว่าง — แถว 92 เป็นต้นไปถูก "ซ่อน" ไว้ ไม่ใช่แค่ว่างเฉยๆ

ยืนยันด้วย Office.js แล้วว่าแถวตั้งแต่แถว 92 ของ Master_TCM เป็นต้นไป (หลังแถวข้อมูลจริงแถวสุดท้าย) ถูกตั้งค่า `rowHidden = true` ไว้ล่วงหน้าทั้งหมด และมีสูตร D/P/R/T พร้อมฟอร์แมตแถบสีสลับอยู่แล้ว — นี่คือพื้นที่ที่ตั้งใจซ่อนไว้สำหรับรอเพิ่มข้อมูล **การพิมพ์ค่าลงแถวที่ซ่อนอยู่จะสำเร็จแต่ผู้ใช้จะมองไม่เห็นแถวใหม่จนกว่าจะ unhide** ทุกครั้งที่เขียนแถวใหม่ต้อง unhide แถวนั้นด้วย (`row.getEntireRow().rowHidden = false`) ก่อนรายงานว่าเสร็จงาน — ห้ามเดาตำแหน่งแถว ต้องอ่านแถวจริงก่อนเขียนทุกครั้ง

## 5. Dropdown Lists ทั้งหมด (จาก sheet Settings — ห้ามใช้ค่านอกลิสต์นี้ สะกด/ตัวพิมพ์ใหญ่เล็กต้องตรงเป๊ะ)

- Priority: Critical, High, Medium, Low
- Module: Pharmacy, Billing, EMR, Lab, Patient, Register, Triage, CPOE, Insurance, Appointment, Cashier, Claim, Report, Security, Audit, Admission, Document
- Tester/Member (Create/Review/Approval By): Neran, Matt, Tar, Aof, June, Jame
- Execution Status: Draft, Ready for Review, Ready to Test, Not Test
- Run in This Cycle?: Yes, No
- Test Level: Unit, Integration, System, Acceptance
- Test Type: Functional, UI/UX, Security, Performance, Interoperability, Compliance
- Case Type: Happy, Unhappy, Edge, Error

## 6. รูปแบบการตั้งชื่อ Test Case Name (คอลัมน์ F) — ต้องสื่อ 2 อย่างในประโยคเดียว

Pattern: `[ตรวจสอบ/ทดสอบ] + [สิ่งที่ตรวจสอบ] + [เงื่อนไข/กรณีที่ทดสอบ]`

(1) **สิ่งที่ตรวจสอบ** — verb + object เช่น "ตรวจสอบการคำนวณ...", "ตรวจสอบการแสดงผล...", "ทดสอบการบันทึก..."
(2) **เงื่อนไข/กรณีที่ทดสอบ** — สถานการณ์เฉพาะของเคสนั้น เช่น "เมื่อ...", "กรณีที่...", "ในกรณี..."

ตัวอย่างจริงจากไฟล์นี้ (แถว TC-NUH-802-001 ถึง 003):

- "สร้าง Admit Order พร้อม Preferred Bed - ตรวจสอบการสร้าง Bed Reservation Priority 1 อัตโนมัติในหน้าผู้ป่วยเตรียมเข้า"
- "สร้าง Admit Order โดยไม่ระบุ Preferred Bed - คอลัมน์ลำดับเตียงต้องไม่แสดงเป็นค่าว่างเปล่า"
- "แก้ไข Admit Order เปลี่ยน Preferred Bed"

ตัวอย่างที่ดีอื่นๆ (สื่อทั้ง "อะไร" และ "กรณีไหน"):

- ตรวจสอบการคำนวณส่วนลดถูกต้อง กรณีอัตราลดหย่อน 30%
- ตรวจสอบการแสดงข้อความ Empty State กรณีไม่มีข้อมูลลดหย่อนในช่วงเวลาที่เลือก
- ตรวจสอบการ Export Excel กรณีมีข้อมูลมากกว่า 1,000 แถว

ตัวอย่างที่ไม่ควรทำ (กว้างเกินไป ไม่ระบุกรณี): "ทดสอบรายงาน", "ตรวจสอบการทำงานของระบบ", "ทดสอบ Export"

หลักการนี้ควรสอดคล้องกับ **Case Type (คอลัมน์ N)** ด้วย เช่นถ้า Case Type = Error ชื่อเคสควรระบุ input ผิดปกติ/เงื่อนไขล้มเหลวชัดเจน (เช่น "ตรวจสอบระบบแจ้งเตือนกรณีกรอกอัตราลดหย่อนเป็นค่าติดลบ")

### สไตล์การเขียนคอลัมน์อื่นๆ ให้ตรงของเดิม (ตัวอย่างจริงจากไฟล์)

- **Test Steps (H)**: เลขลำดับ + ขึ้นบรรทัดใหม่ในเซลล์เดียว เช่น `"1. เข้าหน้า Admission Center > แท็บ 'ผู้ป่วยเตรียมเข้า'\n2. กดสร้าง Admit Order ใหม่...\n3. บันทึกข้อมูล\n4. ตรวจสอบแถวผู้ป่วยในตาราง..."`
- **Test Data (I)**: ระบุ key:value สั้นๆ เช่น `"Preferred Bed: 'S-02', Ward: 'NUH_Ward_test'"` หรือ `"-"` ถ้าไม่มี
- **BDD (J)**: `"Given ผู้ใช้อยู่หน้าสร้าง Admit Order\nWhen เลือก Preferred Bed เป็นเตียง S-02...แล้วกด Save\nThen ระบบสร้าง Admit Order สำเร็จ..."`
- **Expected Result (K)**: อธิบายผลลัพธ์แบบเจาะจง ตรวจสอบได้จริง บางแถวใช้ bullet ด้วย `-` นำหน้าแต่ละบรรทัดถ้ามีหลายเงื่อนไข

## 7. Step-by-step workflow

1. **Read before writing.** อ่านตาราง `Scenarios` ทั้งหมด และอ่าน `Master_TCM` อย่างน้อยคอลัมน์ A:C บวกแถวท้ายๆ เพื่อหา: Scenario ID ที่มีอยู่แล้ว, เลขลำดับ TC ID สูงสุดต่อ Scenario, และแถวว่างแถวแรก (คอลัมน์ A ว่าง + คอลัมน์ D มีสูตร Feature อยู่แล้ว + ตรวจสอบว่า `rowHidden = true`)
2. **Scenario ใหม่?** เพิ่มแถวใน `Scenarios` ก่อน (เป็นแถวตารางจริง) — เช็ค Card ID ซ้ำก่อนเสมอ ใช้ค่า Module/Case Type/Priority ที่ตรงกับ Settings เท่านั้น
3. **Scenario เดิม?** ใช้ Scenario ID และ Card ID เดิมตามที่สะกดไว้ใน `Scenarios!A` เป๊ะๆ
4. คำนวณเลขลำดับ TC ID ถัดไปต่อกลุ่ม Scenario ID (max ที่มีอยู่ + 1, เติมศูนย์ 3 หลัก, เริ่ม 001 ถ้าเป็น Scenario ใหม่)
5. หาแถวเป้าหมายใน `Master_TCM`: ถ้ามีแถวว่างที่ซ่อนอยู่ (unhide ก่อนเขียนหรือหลังเขียนก็ได้ แต่ต้อง unhide ก่อนรายงานเสร็จ) ให้เขียนลงแถวนั้น ถ้าตารางเต็มไม่มีแถวว่างเหลือ ให้เพิ่มแถวผ่าน Table API เพื่อให้สูตร/ฟอร์แมตขยายอัตโนมัติ
6. เขียนเฉพาะ A, B, C, E, F, G, H, I, J(ไม่บังคับ), K, L, M, N, O, Q(ไม่บังคับ), S(ไม่บังคับ), U, V, W, X, Y — ห้ามแตะ D, P, R, T
7. ทุกคอลัมน์ dropdown (B, C, E, L, M, N, O, Q, S, U, X) ใช้ค่าจากลิสต์ในหัวข้อ 5 เท่านั้น สะกด/ตัวพิมพ์ใหญ่เล็กต้องตรงเป๊ะ
8. ตั้งชื่อ Test Case Name (F) ตาม pattern หัวข้อ 6 และเขียนคอลัมน์ H/I/J/K ให้สไตล์ตรงกับตัวอย่างจริงในหัวข้อ 6
9. **ห้าม** เขียนทับ/สลับ/ลบแถวที่มีข้อมูลอยู่แล้ว และห้ามแตะ sheet อื่นนอกจาก Scenarios/Master_TCM

## 8. ตัวอย่างจบครบ (Worked Example)

สมมติได้รับ Card ID ใหม่ `NUH-9999` ("ปรับปรุงหน้าค้นหาผู้ป่วยให้รองรับการค้นหาด้วยเลขบัตรประชาชน") และต้องการ 2 เทสเคส:

**ใน `2. Scenarios` เพิ่มแถวใหม่:**
| Scenario ID | Scenario Name | Module | Case Type | Objective | Priority | Related Risk | Card ID |
|---|---|---|---|---|---|---|---|
| TS-NUH-9999 | Patient search by national ID | Patient | Happy | Verify patient search supports national ID lookup | High | Search returns wrong patient or no results | NUH-9999 |

**ใน `1. Master_TCM` เพิ่ม 2 แถว (unhide แถวที่ใช้ด้วย):**
| TC ID | Scenario ID | Module | Priority | Test Case Name | ... | Test Level | Test Type | Case Type | Create By | ... | Execution Status | ... | Run in This Cycle? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-NUH-9999-001 | TS-NUH-9999 | Patient | High | ตรวจสอบการค้นหาผู้ป่วยด้วยเลขบัตรประชาชน กรณีกรอกเลข 13 หลักถูกต้อง | ... | System | Functional | Happy | Neran | ... | Draft | ... | Yes |
| TC-NUH-9999-002 | TS-NUH-9999 | Patient | Medium | ตรวจสอบระบบแจ้งเตือน กรณีกรอกเลขบัตรประชาชนไม่ครบ 13 หลัก | ... | System | Functional | Error | Neran | ... | Draft | ... | Yes |

(คอลัมน์ D, P, R, T ไม่ต้องใส่ในตารางนี้เพราะเป็นสูตรที่มีอยู่แล้ว — จะคำนวณเองทันทีที่กรอก Module/Create By)

## 9. กฎเหล็ก (ห้ามละเมิดเด็ดขาด — สรุปรวม)

1. ห้ามพิมพ์ทับคอลัมน์ D, P, R, T — ทั้งหมดเป็นสูตร auto-calc แม้จะดูเหมือนว่างก็ตาม
2. ห้ามแตะ sheet ใดๆ นอกจาก Master_TCM และ Scenarios (ดูข้อ 0)
3. แถวว่างของ Master_TCM (แถว 92 เป็นต้นไป) ถูกซ่อนไว้ ต้อง unhide แถวที่เขียนก่อนรายงานว่าเสร็จ ห้ามเดาตำแหน่งแถว ต้องอ่านจริงก่อนเขียน
4. ค่าทุกคอลัมน์ dropdown ต้องเลือกจาก Settings เท่านั้น (หัวข้อ 5)
5. Scenario ID / Card ID ต้องเช็คซ้ำก่อนสร้างใหม่เสมอ
6. TC ID ต้องเรียงลำดับต่อเนื่องไม่ซ้ำกันภายใน Scenario เดียวกัน
7. Test Case Name ต้องระบุทั้ง "สิ่งที่ตรวจสอบ" และ "เงื่อนไข/กรณีที่ทดสอบ" ตาม pattern หัวข้อ 6 ห้ามตั้งชื่อกว้างเกินไป
8. **เขียนต่อเสมอ ห้าม overwrite แถวเดิมเด็ดขาด ไม่ว่ากรณีใด — นี่คือคำตอบตายตัว ไม่ต้องถามผู้ใช้ซ้ำทุกครั้งว่าจะเขียนทับหรือเขียนต่อ** เทสเคสใหม่ = แถวใหม่เสมอ (แถวซ่อนที่ว่างอยู่ หรือแถวตารางใหม่ถ้าตารางเต็ม) เหตุผล: P/R/T เป็นสูตร auto-timestamp ที่จะเสียหายถาวรถ้าทับแถวเดิม และ TC ID/แถวซ่อนถูกออกแบบมาแบบ additive อยู่แล้ว ถ้าเทสเคสเดิมล้าสมัยจริง ให้เปลี่ยน Execution Status เป็น `Not Test` หรือระบุใน Remark แทนการทับ/ลบ
9. Execution Status (U) ของเทสเคสใหม่ default เป็น `Draft` เสมอ ไม่ต้องถามผู้ใช้ซ้ำ เปลี่ยนเป็นค่าอื่นเฉพาะเมื่อผู้ใช้ระบุมาชัดเจน

## 10. คำเตือนด้านเทคนิค

ไฟล์นี้อาจเปิดผ่าน Excel Online/SharePoint และมีอาการค้าง/ตอบสนองช้าเป็นระยะ (คาดจากสูตร NOW() จำนวนมาก + iterative calculation) แนะนำตรวจสอบผลลัพธ์หลังพิมพ์ทุกครั้งด้วยการอ่านค่ากลับ (ไม่ใช่เดาจาก tool ส่งกลับว่าสำเร็จ) เพื่อป้องกันตัวอักษรตกหล่นหรือเขียนผิดแถว

## 11. ถ้า AI ที่อ่าน skill นี้ ไม่มีสิทธิ์เขียนไฟล์ Excel โดยตรง (เช่น Ask Linear, ChatGPT, หรือ AI บนแพลตฟอร์มอื่น)

สำคัญมาก: **skill นี้ถูกอ่านโดย AI หลายแพลตฟอร์ม ไม่ใช่ AI ทุกตัวมีสิทธิ์เขียนลงไฟล์ Excel ที่เปิดอยู่จริงๆ ได้** เช่น AI ที่อยู่ใน Linear (Ask Linear), Slack bot, หรือ chat AI ทั่วไป — AI เหล่านี้มีเฉพาะความสามารถอ่าน/สร้างข้อความ ไม่มี Office.js หรือสิทธิ์เขียนไฟล์ Excel ที่เปิดอยู่จริง อาการที่พบบ่อยคือ AI จะสร้างไฟล์ CSV แยกออกมาแทน ซึ่งไม่ใช่การเขียนลงไฟล์จริง ต้องมีคน/AI อีกตัวนำเข้ามาอีกที

**วิธีเช็คว่าตัวเองมีสิทธิ์เขียนไฟล์หรือไม่:** ถ้าไม่มีเครื่องมือสำหรับอ่าน/เขียน cell ของ Excel โดยตรง (เช่น get_cell_ranges, set_cell_range, execute_office_js หรือเทียบเคียง) ให้สันนิษฐานทันทีว่าตัวเองอยู่ในกลุ่มนี้ **ห้ามบอกผู้ใช้ว่า "เพิ่มเทสเคสให้แล้ว" ถ้ายังไม่ได้เขียนลงไฟล์จริง** — ให้ทำตามขั้นตอนด้านล่างแทน

**ขั้นตอนสำหรับ AI ที่เขียนไฟล์ Excel โดยตรงไม่ได้:**

1. ทำงานทุกขั้นตอนเหมือนเดิม (เช็ค Card ID ซ้ำ/สร้าง Scenario ID ใหม่ถ้าจำเป็น, คำนวณเลขลำดับ TC ID ต่อ, เลือกค่า dropdown จากหัวข้อ 5, ตั้งชื่อตามหัวข้อ 6, default Execution Status = `Draft`) — เพียงแต่สร้างเป็นชุดข้อมูลแทนการเขียนลง cell จริง
2. **สร้างผลลัพธ์เป็น 2 ตาราง ในรูปแบบ Markdown table (แนะนำ — copy-paste ระหว่างแชทอ่านง่ายกว่า) หรือ CSV ก็ได้ โดยใช้หัวคอลัมน์ตรงกับคอลัมน์จริงในไฟล์เป๊ะๆ**:
   - ไฟล์/ตาราง `Scenarios` (ถ้ามี scenario ใหม่): header = `Scenario ID, Scenario Name, Module, Case Type, Objective, Priority, Related Risk, Card ID`
   - ไฟล์/ตาราง `Master_TCM` (เทสเคสใหม่): header = `TC ID, Scenario ID, Module, Priority, Test Case Name, Pre-conditions, Test Steps, Test Data, BDD, Expected Result, Test Level, Test Type, Case Type, Create By, Execution Status, Cards Requirment, Requirment Detail, Run in This Cycle?, Remark` — **ห้ามใส่คอลัมน์ Feature/Create Date/Review By/Review Date/Approval By/Approval Date เด็ดขาด** (เป็นสูตรหรือเว้นว่างให้คนที่นำเข้าจริงเป็นคนตัดสินเอง)
3. ปิดท้ายคำตอบ/ไฟล์ด้วยข้อความแจ้งเตือนชัดเจนเสมอ 1 ประโยค เช่น: "ข้อมูลนี้ยังไม่ถูกเขียนลงไฟล์ Excel จริง กรุณานำไฟล์นี้ไปให้ Claude ใน Excel (ที่เชื่อมต่อกับไฟล์ TCM_HIS_Cortex โดยตรง) เพื่อนำเข้าและตรวจสอบก่อนบันทึกจริง"
4. ห้ามสรุปว่า "เพิ่มเทสเคสเรียบร้อยแล้ว" หรือ "อัปเดตไฟล์แล้ว" หากยังไม่มีหลักฐานยืนยันว่าเขียนลง cell จริง

หมายเหตุ: เหตุผลที่ห้ามใส่คอลัมน์สูตร (Feature/Create Date/Review Date/Approval Date) ในไฟล์ส่งต่อ เพราะเมื่อ Claude ใน Excel นำเข้าข้อมูลจริง สูตรเหล่านี้มีอยู่แล้วในไฟล์จริงและจะคำนวณเองอัตโนมัติ หาก AI ต้นทางใส่ค่าเหล่านี้มาใน CSV จะทำให้สับสนกับสูตรที่มีอยู่จริงเมื่อ import

## 12. วิเคราะห์ข้อมูลจาก Linear Card อัตโนมัติ + ขั้นตอนเพิ่ม Module ใหม่ใน Settings

### 12.1 เมื่อ AI มีข้อมูล Linear ticket/card (จาก connector หรือจากข้อความที่ผู้ใช้วาง)

**อย่าถามผู้ใช้ซ้ำในสิ่งที่วิเคราะห์จาก card ได้เอง** ให้ดึง/อนุมานค่าต่อไปนี้จาก title/description/labels/priority ของ ticket โดยอัตโนมัติ แล้วค่อยถามผู้ใช้เฉพาะส่วนที่คนเท่านั้นที่รู้ได้:

- **Card ID**: ดึงจาก identifier ของ ticket โดยตรง (เช่น `NUH-802`)
- **Scenario Name**: สรุปจาก title ของ ticket
- **Module**: วิเคราะห์จาก title/description/team/label แล้วจับคู่กับค่าที่ใกล้เคียงที่สุดในลิสต์ของหัวข้อ 5 ก่อนเสมอ 17 ค่า: Pharmacy, Billing, EMR, Lab, Patient, Register, Triage, CPOE, Insurance, Appointment, Cashier, Claim, Report, Security, Audit, Admission, Document (เช่น ticket เกี่ยวกับ "Admit Order/Bed Reservation" → `Admission`, "Invoice/ค่ารักษา" → `Billing`)
- **Priority**: map จาก priority ของ Linear (Urgent/High/Medium/Low/No priority) เป็นค่าใน Settings!A (Urgent→Critical, High→High, Medium→Medium, Low/No priority→Low)
- **Objective**: สรุปจาก description ของ ticket เป็น 1 ประโยค
- **Related Risk**: อนุมานจากผลกระทบ/ความเสี่ยงที่กล่าวถึงใน ticket ถ้ามี
- **Case Type**: ticket ประเภท Bug มักต้องการเทสเคส Error/Unhappy เพิ่มจาก Happy path, ticket ประเภท Feature เน้น Happy เป็นหลัก

**สิ่งที่ห้ามเดาจาก card ต้องถามผู้ใช้เสมอ:** Test Steps, Test Data, Expected Result และเนื้อหาเชิงทดสอบจริง — สิ่งเหล่านี้เดาไม่ได้เสี่ยงเกินไป และควรให้คนยืนยันก่อนเสมอ

### 12.2 ถ้าวิเคราะห์แล้วไม่มี Module ที่เข้ากันเลยในลิสต์ — ข้อยกเว้นเดียวที่อนุญาตให้แก้ Settings ได้

โครงสร้างจริง: `Settings!D1` = หัวข้อ "Module", `Settings!D2:D18` = รายการ 17 ค่าปัจจุบัน ไม่มีแถวว่างคั่นกลาง เชื่อมต่อกับ named range `ModuleList = OFFSET(Settings!$D$2,0,0,COUNTA(Settings!$D$2:$D$1000),1)` ซึ่งนับจำนวนเซลล์ที่มีค่าติดกันจาก D2 ลงมา ดังนั้นการเพิ่มค่าใหม่ต่อท้ายแบบติดกัน (ไม่เว้นแถว) จะถูกนับเข้า dropdown โดยอัตโนมัติ

**ขั้นตอน:**

1. เช็คก่อนเสมอว่าความหมาย/เนื้อหาของ module ที่วิเคราะห์ได้ ไม่เข้ากับ 17 ค่าที่มีอยู่แล้วจริงๆ (ลองเทียบคำพ้อง/คำใกล้เคียงก่อน)
2. อ่าน `Settings!D2:D1000` หาแถวว่างแรกเหนือค่าที่มีอยู่จริง (ปัจจุบันคือ D19) — ห้ามเดาเลขแถว ต้องอ่านจริงเสมอเพราะอาจมีคนเพิ่มค่าใหม่ไปก่อนแล้ว
3. พิมพ์ค่า module ใหม่ลงในแถวถัดไปทันที ห้ามเว้นแถว ห้ามเรียงลำดับใหม่/แทรกแถว ห้ามแก้ค่า D1 (หัวข้อ) หรือคอลัมน์อื่นใน Settings
4. ตรวจสอบหลังเขียนว่า dropdown `ModuleList` ของ Master_TCM/Scenarios แสดงค่าใหม่นี้แล้ว (เป็นผลอัตโนมัติจากสูตร OFFSET+COUNTA ไม่ต้องแก้ชื่อ named range เอง)
5. **แจ้งผู้ใช้เสมอว่าเพิ่ม Module ใหม่** (เช่น "เพิ่ม Module '<ชื่อ>' ลงใน Settings เนื่องจากไม่มีค่าใกล้เคียงในลิสต์เดิม") ห้ามเพิ่มเงียบๆ — นี่คือข้อยกเว้นเดียวที่อนุญาตให้แก้ Settings ห้ามนำไปใช้แก้ค่าอื่นใน Settings โดยเด็ดขาด

## 14. Dual-Agent Cross-Check & Verification Flow (เมื่อรับ draft จาก Ask Linear หรือ AI ตัวอื่น)

ใช้ workflow นี้เมื่อคุณ (โหมด A หรือ C ตามหัวข้อ 0.1) ได้รับ test case ร่างจาก AI อื่นที่ทำงานในโหมด B (เช่น Ask Linear) เพื่อเพิ่มความครอบคลุมและคุณภาพก่อนเขียนลงไฟล์จริง:

1. **อ่าน draft ที่ส่งต่อมา** (Markdown/CSV ตามรูปแบบหัวข้อ 11)
2. **ดึงบริบทจริงจาก Linear:** ถ้ามี Linear API/connector ให้ดึง description, Acceptance Criteria (AC), และ**คอมเมนต์ล่าสุด**ของ Card ID นั้น ถ้าไม่มีให้ขอผู้ใช้ paste มาให้แทน
3. **กฎแก้ข้อขัดแย้ง:** ถ้า AC เดิมจาก BA ขัดแย้งกับสิ่งที่ Dev คอมเมนต์ไว้ (เช่น เปลี่ยน logic ระหว่างทำ) **ให้ยึดตามคอมเมนต์ของ Dev เป็นหลัก** เพราะสะท้อนโค้ดจริงที่จะถูกทดสอบ
4. **วิเคราะห์ช่องว่าง (QA Gap Analysis)** เทียบ draft กับ AC/คอมเมนต์:
   - ครอบคลุม Happy Path ครบไหม
   - มีเคส Unhappy/Error (invalid input, validation, recovery) ไหม — Ask Linear มักพลาดจุดนี้
   - มีเคส Security/RBAC (role ที่ไม่ควรเข้าถึงได้ถูกกันไหม) ไหม
5. **เสนอเคสเพิ่มเติมที่ขาด** ให้ผู้ใช้ดูก่อนเสมอ อย่าเขียนเคสที่คุณเพิ่มเองลงไฟล์ทันทีโดยไม่ผ่านการอนุมัติ
6. หลังผู้ใช้อนุมัติ ให้รวม draft เดิม + เคสที่เพิ่มเข้าไป แล้วทำตาม workflow ปกติ (หัวข้อ 7) เพื่อเขียนลงไฟล์ตามโหมดของตัวเอง (หัวข้อ 0.1)

## 15. Verification (do this before reporting done)

- Re-read the newly written rows in both sheets.
- Confirm column D in each new Master_TCM row shows `"IPD - " & Module` (formula intact, not a literal string).
- Confirm P/R/T still show as formulas (check via cell formulas, not just displayed value) — if O/Q/S got a value, P/R/T should now show a real timestamp; if O/Q/S are blank, P/R/T should show blank/empty string, never a hardcoded date.
- Confirm every dropdown-backed cell's value appears in its source list (Settings/Scenarios) — if not, the cell will look empty in the dropdown even though a value is typed, which is a silent error worth flagging.
- Confirm the Scenario ID used in each new Master_TCM row exists as a row in `Scenarios!A`.
- Confirm the rows you wrote into are no longer hidden (`rowHidden = false`).
- Confirm no pre-existing row (above/outside the rows you targeted) was altered.
- If a new Module was added to Settings, confirm it appears exactly once, directly below the prior last entry, with no blank rows before it.

**Done when:** every new scenario has exactly one row in `Scenarios`, every new test case has exactly one row in `Master_TCM` with a valid Scenario ID link, all dropdown columns contain only listed values, D/P/R/T are still live formulas, the written rows are visible (unhidden), and a re-read of the written ranges confirms all of the above.

## 16. Execution Strategy สำหรับโหมด A (Local File Agent — openpyxl)

หัวข้อนี้ใช้เฉพาะ agent ที่เช็คตัวเองตามหัวข้อ 0.1 แล้วว่าอยู่ใน **โหมด A** (เช่น Antigravity หรือ coding agent อื่นที่มีสิทธิ์เข้าถึง filesystem แต่ไม่มี Office.js bridge เชื่อมกับ Excel ที่เปิดอยู่จริง)

เนื่องจาก AI กลุ่มนี้ไม่มีเครื่องมือเขียนไฟล์ Excel (binary) โดยตรง **ต้องเขียนและรันสคริปต์ Python ชั่วคราวโดยใช้ไลบรารี `openpyxl`**

**แนวทาง:**

1. โหลดไฟล์ด้วย `load_workbook(path, data_only=False)` เสมอ — `data_only=False` สำคัญมาก ป้องกันสูตรเดิมถูกแทนที่ด้วยค่า hardcode ตอนเซฟ
2. หาแถวว่างที่ถูกต้อง: สแกนจากแถว 2 ของ `1. Master_TCM` ลงมา หาแถวแรกที่คอลัมน์ A (TC ID) ว่างแต่คอลัมน์ D ยังมีสูตรอยู่
3. **ต้อง unhide แถวที่เขียนด้วยเสมอ** (`ws.row_dimensions[n].hidden = False`) — แถวว่างที่เตรียมไว้ล่วงหน้าถูกซ่อนไว้ (ดูหัวข้อ 4 กฎเหล็กเรื่องแถวว่าง) ถ้าไม่ unhide ผู้ใช้จะมองไม่เห็นแถวใหม่แม้เขียนสำเร็จแล้ว
4. ถ้าต้องเพิ่มแถวใหม่เพราะไม่มีแถวว่างเหลือ ต้องขยาย range ของ Excel Table ด้วย (เช่น `ws.tables["Master_TCM"].ref = f"A1:Y{new_max_row}"`) เพื่อให้ฟอร์แมต/คุณสมบัติตารางขยายถูกต้อง
5. คัดลอกสูตรสำหรับคอลัมน์ D, P, R, T จากแถวก่อนหน้า แทนการพิมพ์ค่า literal ถ้าต้องสร้างแถวใหม่:
   - D: `="IPD - " & C{row}`
   - P: `=IF(O{row}<>"",IF(OR(P{row}="",P{row}=0),NOW(),P{row}),"")`
   - R: `=IF(Q{row}<>"",IF(OR(R{row}="",R{row}=0),NOW(),R{row}),"")`
   - T: `=IF(S{row}<>"",IF(OR(T{row}="",T{row}=0),NOW(),T{row}),"")`
6. เซฟไฟล์กลับที่ path เดิมด้วย `wb.save(path)`

**ตัวอย่างโครงสคริปต์:**

````python
import openpyxl

wb = openpyxl.load_workbook("./TCM_HIS_Cortex_v1.0.0.xlsx", data_only=False)
ws_master = wb["1. Master_TCM"]
ws_scenarios = wb["2. Scenarios"]

# (logic: หา first blank row ที่มีสูตร D อยู่แล้ว, unhide แถวนั้น,
#  เขียนค่าลง A,B,C,E,F,G,H,I,J,K,L,M,N,O,U,V,W,X,Y ตามหัวข้อ 4,
#  ห้ามแตะ D,P,R,T โดยเด็ดขาด)

wb.save("./TCM_HIS_Cortex_v1.0.0.xlsx")
print("Excel workbook successfully updated!")
Copy everything from the first `---` line to the last closing ``` and paste it directly to Antigravity's chat as your opening instruction.
````
