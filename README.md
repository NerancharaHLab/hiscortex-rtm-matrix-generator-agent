# HIS Cortex RTM Matrix Generator Agent

เครื่องมือและตัวเอเจนต์ในการเชื่อมโยง รวบรวมข้อมูล และนำเข้าชุดทดสอบ (Test Scenarios & Test Cases) จากแพลตฟอร์ม Linear บอร์ดเข้าสู่ตารางบริหารจัดการของ Excel (`TCM_HIS_Cortex_*.xlsx`) ตามมาตรฐานโรงพยาบาล TMH/NUH/SBH

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

```text
hiscortex-rtm-matrix-generator-agent/
├── .agents/                               # คลังคู่มือหลักสำหรับสั่งงานเอเจนต์
│   ├── AGENTS.md                          # กติกากลางการออกแบบเทสเคสของระบบ HIS/Cortex
│   ├── hiscortex-asklinear-generator-SKILL.md # คู่มือสำหรับสั่งการ Ask Linear (Cloud AI)
│   └── hiscortex-tcm-writer-SKILL.md      # คู่มือสำหรับตรวจรับและเขียนข้อมูลลง Excel (Local AI)
├── scripts/                               # คลังสคริปต์รันระบบ
│   ├── fetch_linear.py                    # สคริปต์ดึงบริบทการ์ดและประวัติคุยจาก Linear API
│   └── import_tcm.py                      # สคริปต์นำเข้าข้อมูลจาก Markdown สู่ Excel ประจำไซต์
├── .env.example                           # แม่แบบไฟล์คอนฟิก
└── README.md                              # คู่มือนี้
```

---

## ⚙️ การตั้งค่าก่อนใช้งาน (Configuration)

1. คัดลอกและสร้างไฟล์ `.env` ที่ root ของโฟลเดอร์นี้:
   ```bash
   cp .env.example .env
   ```
2. ป้อนค่าตัวแปรในไฟล์ `.env`:
   * **`LINEAR_API_TOKEN`**: Personal API Token ของคุณที่ได้จาก Linear (เมนู Settings > API)
   * **`CURRENT_SITE`**: กำหนดไซต์งานปัจจุบันที่คุณต้องการทำงานด้วย (รองรับ: `NUH`, `TMH`, `SBH`)
     * *สคริปต์จะค้นหาและทำงานกับไฟล์ Excel ของไซต์นั้นๆ อัตโนมัติ (เช่น `TCM_HIS_Cortex_v1.0.0_NUH.xlsx` ในเวิร์กสเปซ)*

---

## 🚀 ขั้นตอนการนำเข้าเทสเคส (Workflow Guide)

กระบวนการส่งมอบงานแบ่งออกเป็น 2 ขั้นตอนง่ายๆ:

### ขั้นตอนที่ 1: วิเคราะห์และสร้างโครงเทสเคสด้วย Ask Linear (ฝั่ง Cloud)
1. ส่งคู่มือคัดลอกทั้งหมดในไฟล์ [**`hiscortex-asklinear-generator-SKILL.md`**](.agents/hiscortex-asklinear-generator-SKILL.md) ให้กับ **Ask Linear** (Linear AI บนระบบคลาวด์)
2. Ask Linear จะประมวลผลรายละเอียดการ์ด บันทึกคอมเมนต์ของ Dev และเจอตารางเทสเคส **หุ้มในกล่อง Markdown Code Block**
3. คัดลอกตารางข้อความนั้นมาวางในคอมพิวเตอร์ของคุณ โดยเซฟไว้ในชื่อไฟล์การ์ด เช่น `workbooks/md from linear/NUH-1199-test-cases.md`

### ขั้นตอนที่ 2: รันสคริปต์เพื่อกรอก Excel และอ้างอิงย้อนกลับ Linear (ฝั่ง Local)
รันสคริปต์ผ่าน Terminal ในโฟลเดอร์โครงการ:

```bash
# รูปแบบ: python3 scripts/import_tcm.py <Markdown-File-Path>
python3 scripts/import_tcm.py ../workbooks/md\ from\ linear/NUH-1199-test-cases.md
```

**สิ่งที่สคริปต์ทำงานให้โดยอัตโนมัติ:**
1. **อ่านคอนฟิกไซต์:** อ่านตัวแปร `CURRENT_SITE` จาก `.env` เพื่อค้นหาไฟล์ Excel ของไซต์นั้นอัตโนมัติ
2. **ทำความสะอาดข้อมูลเก่า:** ดึง ID ตั๋ว (เช่น `NUH-1199`) และลบรายการ Scenarios/Test Cases เดิมของตั๋วใบนั้นออกจากไฟล์ Excel เพื่อไม่ให้ข้อมูลเกะกะหรือทับซ้อนซ้ำสอง
3. **กรอกข้อมูลใหม่พร้อมสูตร:** กรอกข้อมูลScenarios ย่อย และ Test Cases ทั้งหมดต่อท้ายตารางหลัก ปลดซ่อนแถวที่เขียน และปกป้องสูตร Excel ทั้งหมดไม่ให้เสียหาย
4. **โพสต์คอมเมนต์สะกิด Linear บอร์ด:** เชื่อมต่อกับ Linear API เพื่อเข้าไปสร้าง Comment ในการ์ด Linear ใบนั้น เพื่อบอกทุกคนว่า: **"ชุดเทสเคสนี้ถูกเก็บไว้ในไฟล์ Excel ชื่ออะไร และอยู่แถวที่เท่าไหร่"**

---

## 📦 การติดตั้งไลบรารีที่จำเป็น (Dependencies)

สคริปต์รันด้วยภาษา Python 3 และต้องการไลบรารี `openpyxl` ในการควบคุม Excel:

```bash
pip install openpyxl
```
*(ไม่ต้องติดตั้ง dotenv เนื่องจากสคริปต์มีระบบแกะไฟล์ .env ในตัวแล้ว)*
