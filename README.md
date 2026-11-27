# Ocean Saga — Character Database & AI Knowledge Pack

ฐานข้อมูลตัวละคร สกิลแปลภาษาไทย (`237 ตัวละคร / 815 สกิล`), Real Tier List และแผนจัดทีมเกม **Ocean Saga** สำหรับใช้งานร่วมกับ AI (เช่น Antigravity, Gemini, Claude, ChatGPT) จากทุกเครื่อง

---

## ลิงก์ฐานข้อมูลสำหรับให้ AI อ่านโดยตรง (Raw URLs)

ส่งลิงก์ด้านล่างให้ AI บนเครื่องใดก็ได้เพื่อโหลดบริบทและฐานข้อมูลทันที:

- **ไฟล์บริบทหลัก (AI Context + ตัวละคร ID ปัจจุบัน + Real Tier List + แผนทีม):**
  `https://raw.githubusercontent.com/tsyt-dev/ocean-saga-db/main/Ocean_Saga_AI_Context_Export.md`
- **ไฟล์บริบทแบบ JSON:**
  `https://raw.githubusercontent.com/tsyt-dev/ocean-saga-db/main/Ocean_Saga_AI_Context_Export.json`
- **ฐานข้อมูลตัวละคร + สกิลแปลไทยทั้งหมด (237 ตัว):**
  `https://raw.githubusercontent.com/tsyt-dev/ocean-saga-db/main/characters_th.json`
- **ผลคำนวณคะแนนและดาเมจทั้งหมด:**
  `https://raw.githubusercontent.com/tsyt-dev/ocean-saga-db/main/analysis_results.json`

### ตัวอย่างคำสั่งเวลาเปิดแชท AI บนเครื่องอื่น
> *"อ่านข้อมูลจาก `https://raw.githubusercontent.com/tsyt-dev/ocean-saga-db/main/Ocean_Saga_AI_Context_Export.md` และใช้เป็นฐานข้อมูลหลักในการช่วยจัดทีม Ocean Saga ให้หน่อย"*

---

## รายการไฟล์ในคลังข้อมูลนี้
| ไฟล์ | รายละเอียด |
| :--- | :--- |
| `Ocean_Saga_AI_Context_Export.md` | สรุปบริบทหลัก, ตัวละคร ID ปัจจุบัน, Real Tier List, ทีมแนะนำ (แนะนำให้อัปเดตไฟล์นี้เมื่อได้ตัวใหม่) |
| `Ocean_Saga_AI_Context_Export.json` | ข้อมูลชุดเดียวกันในรูปแบบ JSON |
| `characters_th.json` / `.csv` | ข้อมูลตัวละคร + สกิลแปลภาษาไทยครบ 237 ตัว |
| `characters_en.json` / `.csv` | ข้อมูลต้นฉบับภาษาอังกฤษจาก `guragon.com/ocean-saga/characters` |
| `analysis_results.json` | ผลคำนวณคะแนนความน่าปั้น 5 มิติ และ Effective Burst Damage |
| `Real_Tier_List.png` | ภาพ Real Tier List แพตช์ปัจจุบันของเซิร์ฟเวอร์ |
| `Ocean_Saga_NewID_Team_TH.pdf` / `.png` | แผนทีมหลักแนะนำของ ID ปัจจุบัน (PDF 1 หน้า + รูป PNG) |
| `Ocean_Saga_Tier_List_TH.pdf` | รายงานวิเคราะห์ & Tier List ฉบับเต็ม 237 ตัว |
