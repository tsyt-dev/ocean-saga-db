# Ocean Saga — Character Database & AI Knowledge Pack

ฐานข้อมูลตัวละคร สกิลแปลภาษาไทย (`237 ตัวละคร / 815 สกิล`), Real Tier List และแผนจัดทีมเกม **Ocean Saga** สำหรับใช้งานร่วมกับ AI (เช่น Antigravity, Gemini, Claude, ChatGPT) จากทุกเครื่อง

---

## ลิงก์ฐานข้อมูลสำหรับให้ AI อ่านโดยตรง (Raw URLs)

ส่งลิงก์ด้านล่างให้ AI บนเครื่องใดก็ได้เพื่อโหลดบริบทและฐานข้อมูลทันที:

- **ไฟล์บริบทหลัก (AI Context + ตัวละคร ID ปัจจุบัน + Real Tier List + แผนทีม):**
  `https://raw.githubusercontent.com/tsyt-dev/ocean-saga-db/main/ข้อมูล/Ocean_Saga_AI_Context_Export.md`
- **ไฟล์บริบทแบบ JSON:**
  `https://raw.githubusercontent.com/tsyt-dev/ocean-saga-db/main/ข้อมูล/Ocean_Saga_AI_Context_Export.json`
- **ฐานข้อมูลตัวละคร + สกิลแปลไทยทั้งหมด (237 ตัว):**
  `https://raw.githubusercontent.com/tsyt-dev/ocean-saga-db/main/ข้อมูล/characters_th.json`
- **ผลคำนวณคะแนนและดาเมจทั้งหมด:**
  `https://raw.githubusercontent.com/tsyt-dev/ocean-saga-db/main/ข้อมูล/analysis_results.json`

### ตัวอย่างคำสั่งเวลาเปิดแชท AI บนเครื่องอื่น
> *"อ่านข้อมูลจาก `https://raw.githubusercontent.com/tsyt-dev/ocean-saga-db/main/ข้อมูล/Ocean_Saga_AI_Context_Export.md` และใช้เป็นฐานข้อมูลหลักในการช่วยจัดทีม Ocean Saga ให้หน่อย"*

---

## หมวดหมู่ไฟล์ในคลังข้อมูลนี้

### 📁 ด้านหน้าโฟลเดอร์ (Root)
- `เปิดโปรแกรมจัดการตัวละคร_SS.bat` — **ตัวรันโปรแกรม GUI หลัก** (ดับเบิลคลิกเปิดโปรแกรมทันทีบน Windows)
- `README.md` — เอกสารแนะนำและการใช้งาน

### 📁 หมวด `ข้อมูล/`
| ไฟล์ | รายละเอียด |
| :--- | :--- |
| `Ocean_Saga_AI_Context_Export.md` | สรุปบริบทหลัก, ตัวละคร ID ปัจจุบัน, Real Tier List, ทีมแนะนำ (ไฟล์หลักสำหรับ AI) |
| `Ocean_Saga_AI_Context_Export.json` | ข้อมูลชุดเดียวกันในรูปแบบ JSON |
| `characters_th.json` / `.csv` | ฐานข้อมูลตัวละคร + สกิลแปลภาษาไทยครบ 237 ตัว |
| `characters_en.json` / `.csv` | ฐานข้อมูลต้นฉบับภาษาอังกฤษจาก `guragon.com/ocean-saga/characters` |
| `analysis_results.json` | ผลคำนวณคะแนนความน่าปั้น 5 มิติ และ Effective Burst Damage |

### 📁 หมวด `โปรแกรม/`
| ไฟล์ | รายละเอียด |
| :--- | :--- |
| `roster_gui.py` | ซอร์สโค้ดโปรแกรม GUI จัดการตัวละครระดับ SS (เพิ่ม/แก้ไข/ลบ/บันทึก/Git Push) |

### 📁 หมวด `ทีม/`
| ไฟล์ | รายละเอียด |
| :--- | :--- |
| `Real_Tier_List.png` | ภาพ Real Tier List แพตช์ปัจจุบันของเซิร์ฟเวอร์ |
| `Ocean_Saga_NewID_Team_TH.pdf` / `.png` | แผนทีมหลักแนะนำของ ID ปัจจุบัน (PDF 1 หน้า + รูป PNG) |
| `Ocean_Saga_Tier_List_TH.pdf` | รายงานวิเคราะห์ & Tier List ฉบับเต็ม 237 ตัว |

### 📁 หมวด `อื่นๆ/`
| ไฟล์ | รายละเอียด |
| :--- | :--- |
| `Ocean_Saga_AI_AutoSync_HowTo_TH.pdf` | คู่มือและคำแนะนำการตั้งค่า Auto-Sync |

---

## การใช้งานโปรแกรมจัดการตัวละครระดับ SS (GUI)
สามารถเปิดโปรแกรมได้ง่ายๆ:
1. **ดับเบิลคลิกที่ไฟล์หน้าโฟลเดอร์:** `เปิดโปรแกรมจัดการตัวละคร_SS.bat`
2. **หรือรันคำสั่ง Terminal:** `python โปรแกรม\roster_gui.py`

### ฟังก์ชันหลักของโปรแกรม:
- **กรองเฉพาะระดับ SS (122 ตัว):** เลือกตัวละครจาก Dropdown ที่คัดเฉพาะระดับ SS มาให้ ไม่ต้องค้นหาจาก 237 ตัว
- **เพิ่ม / แก้ไข / ลบ:** ปรับจำนวนดาว (5★ - 15★), จำนวนตัว, ตัวซ้ำ 5★ สำหรับอัปดาว และใส่หมายเหตุได้
- **บันทึกอัตโนมัติ (Auto-Save):** เมื่อเพิ่ม, แก้ไข หรือลบตัวละคร ระบบจะบันทึกอัปเดตไฟล์ `ข้อมูล/Ocean_Saga_AI_Context_Export.json` และ `.md` ในเครื่องทันทีโดยไม่ต้องกดปุ่มบันทึก
- **ปุ่มอัปเดต Git ทั้งโฟลเดอร์ (Push):** กดปุ่มเดียวเพื่อ Commit & Push ไฟล์ทั้งหมดในโฟลเดอร์ขึ้น GitHub ให้ทุกเครื่องและ AI ได้ข้อมูลตรงกันทันที
- **ปุ่มดึงข้อมูล Git (Pull & Replace All):** แทนที่ไฟล์ในเครื่องทั้งโฟลเดอร์ด้วยข้อมูลล่าสุดจาก GitHub ทันที พร้อมระบบยืนยันความปลอดภัยก่อนแทนที่

