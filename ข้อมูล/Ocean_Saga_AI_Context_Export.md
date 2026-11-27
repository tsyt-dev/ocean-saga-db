# Ocean Saga — AI Context & Knowledge Pack (Handoff Export — Updated New ID)

> **คำสั่งสำหรับ AI (เช่น Antigravity / Gemini / Claude / ChatGPT):**
> เอกสารนี้คือไฟล์สรุปบริบทล่าสุดของเกม **Ocean Saga (ID ใหม่ของผู้ใช้)** ให้ใช้ข้อมูล **Real Tier List**, **รายชื่อตัวละคร ID ใหม่ (พร้อมจำนวนดาวและตัวซ้ำ)**, **ทีมหลักแนะนำ**, และ **ฐานข้อมูลในโฟลเดอร์ `OP_Cha`** ด้านล่างเป็นข้อมูลอ้างอิงหลักทันที (ไม่ต้องดึงข้อมูลจากเว็บใหม่)

---

## 1. โครงสร้างไฟล์ในโฟลเดอร์โปรเจกต์ (`ocean-saga-db`)
- **โฟลเดอร์ `ข้อมูล/`:**
  - `characters_en.json` / `characters_en.csv` — ฐานข้อมูลตัวละคร + สกิลต้นฉบับครบ **237 ตัว (815 สกิล)** จาก `https://guragon.com/ocean-saga/characters`
  - `characters_th.json` / `characters_th.csv` — ฐานข้อมูลตัวละคร + สกิล **แปลภาษาไทยครบทั้ง 237 ตัว**
  - `analysis_results.json` — ผลคำนวณคะแนนความน่าปั้น 5 มิติ (เต็ม 100) และ Effective Burst Damage ของทั้ง 237 ตัว
  - `Ocean_Saga_AI_Context_Export.md` & `Ocean_Saga_AI_Context_Export.json` — ไฟล์สรุปบริบทสำหรับนำเข้าให้ AI เครื่องอื่น
- **โฟลเดอร์ `ทีม/`:**
  - `Real_Tier_List.png` — ภาพเทียร์ลิสต์ที่ผู้เล่นในเซิร์ฟเวอร์ใช้กันจริง (แพตช์ `Ace & Sabo` + `Boa Lilith`)
  - `Ocean_Saga_NewID_Team_TH.pdf` & `Ocean_Saga_NewID_Team_TH.png` — แผนทีมหลักแนะนำของ ID ใหม่ (PDF 1 หน้า + รูป PNG)
  - `Ocean_Saga_Tier_List_TH.pdf` — รายงานวิเคราะห์ & Tier List ฉบับเต็ม 237 ตัว (PDF)
- **โฟลเดอร์ `โปรแกรม/`:**
  - `roster_gui.py` — โปรแกรม GUI จัดการตัวละครระดับ SS (เพิ่ม/แก้ไข/ลบ และบันทึกอัปเดตไฟล์อัตโนมัติ)
- **โฟลเดอร์ `อื่นๆ/`:**
  - `Ocean_Saga_AI_AutoSync_HowTo_TH.pdf` — คู่มือการตั้งค่า Auto-Sync
- **ด้านหน้าโฟลเดอร์หลัก (Root):**
  - `เปิดโปรแกรมจัดการตัวละคร_SS.bat` — ดับเบิลคลิกเพื่อเปิดโปรแกรม GUI ได้ทันที
  - `README.md` — คู่มือและลิงก์สำหรับ AI ทั่วโลก


---

## 2. กฎสำคัญในการให้คำแนะนำผู้ใช้
1. **ยึด `Real Tier List` (แพตช์จริงของเซิร์ฟเวอร์) เป็นหลัก:** เว็บ `guragon.com` มีตัวละครแพตช์อนาคต (เช่น `Luffy Reverse`, `Blackbeard Yonko`, `Nami & Robin`, `Zoro King Of Hell`, `Hero Koby`, `Bonney Egghead`) ซึ่งยังไม่เข้าเซิร์ฟเวอร์ปัจจุบัน
2. **รูปแบบทีมมาตรฐาน:** ทีม 6 ตัว แบ่งเป็น **แถวหน้า 2 ตัว / แถวหลัง 4 ตัว**
3. **ภาษาและสไตล์:** ตอบเป็นภาษาไทย กระชับ อ้างอิงค่าสถานะ (ATK/HP/DEF/SPD) และสกิลจริงจาก `characters_th.json`

---

## 3. Real Tier List ฉบับยืนยันถูกต้องแล้ว (71 ตัว + Boa Lilith T0)
- **T0 (ตัวใหม่ล่าสุดนอกภาพ):** `Boa Lilith` *(Vitality / Support)*
- **SSS (3 ตัว):** `Ace & Sabo`, `Luffy Nika`, `Shirahoshi`
- **S (7 ตัว):** `Kaido Hybrid`, `Jinbe Wano`, `Yamato`, `Brook Wano`, `Whitebeard` (หนวดขาว), `Katakuri`, `Luffy Wano`
- **A (14 ตัว):** `Robin Wano`, `Uta`, `Nami N.W`, `Blackbeard` (หนวดดำ), `Usop Wano`, `Chopper N.W`, `Nami Wano`, `Sanji Vinsmoke`, `Reiju`, `Law N.W`, `Zoro Wano`, `Hidden Black Sanji`, `Oden`, `Shanks`
- **B (14 ตัว):** `Rayleigh`, `Bullet`, `Law Wano`, `Usopp N.W`, `Kid Wano`, `Luffy N.W`, `Doflamingo`, `Carina`, `Nekomamushi`, `Big Mom`, `Kin emon`, `Yonko Buggy`, `Robin N.W`, `King`
- **D (33 ตัว):**
  - แถว 1: `Luffy SM`, `Benn Beckman`, `Carrot`, `Queen`, `Mecha Franky`, `Niji`, `Raizo`, `Franky N.W`, `Capone Bege`, `Jack`, `Cracker`
  - แถว 2: `Brook N.W`, `Enel`, `Crocodile`, `Magellan`, `Akainu`, `Mihawk`, `Kaido`, `Inuarashi`, `Hancock`, `Aokiji`, `Luffy BM`
  - แถว 3: `Fujitora`, `Sanji N.W`, `Law`, `Ichiji`, `Ace`, `Zoro N.W`, `Yasopp`, `Marco`, `Sabo`, `Sengoku`, `Kizaru`

---

## 4. รายชื่อตัวละครของ ID ใหม่ปัจจุบัน (อัปเดต 27 พ.ย. 2026)
- **ระดับ T0:** `Boa Lilith` (**9 ดาว** + ซ้ำ **5 ดาว 1 ตัว** พร้อมขึ้นดาวต่อ!)
- **ระดับ SSS:** `Ace & Sabo` (**6 ดาว** + ซ้ำ **5 ดาว 2 ตัว** พร้อมขึ้นดาวต่อ!)
- **ระดับ S (5 ตัว):** `Jinbe Wano` (6 ดาว +ซ้ำ1), `Kaido Hybrid` (6 ดาว), `Brook Wano` (5 ดาว), `Luffy Wano` (5 ดาว), `Whitebeard / หนวดขาว` (5 ดาว)
- **ระดับ A (3 ตัว):** `Law N.W` (5 ดาว), `Usop Wano` (5 ดาว), `Uta` (5 ดาว)
- **ระดับ B (6 ตัว):** `Carina` (5 ดาว), `Doflamingo` (6 ดาว +ซ้ำ1), `Kid Wano` (6 ดาว +ซ้ำ1), `King` (5 ดาว +ซ้ำ1), `Nekomamushi` (5 ดาว), `Usopp N.W` (5 ดาว)
- **ระดับ D (17 ชนิด / 18 ตัว):** `Aokiji` (5★), `Benn Beckman` (5★), `Burgess` (5★), `Cracker` (5★), `Hancock` (6★), `Ichiji` (5★), `Jack` (5★), `Kaido` (5★), `Kizaru` (5★), `Kuma` (5★ x2), `Magellan` (5★), `Mihawk` (5★), `Queen` (5★), `Sabo` (5★), `Sanji N.W` (5★), `Zoro N.W` (5★), `Carrot` (6★)

---

## 5. ทีมหลักแนะนำของ ID ใหม่ (6 ตัว · หน้า 2 / หลัง 4)
- **แถวหน้า 2 ตัว:**
  1. **หน้า 1: `Jinbe Wano` (5★, S #2)** — แทงก์หลัก DEF 6,216 (+100%, +40% ทุกครั้งที่โดนตี) กาง *Protection* ลดดาเมจตรงทั้งทีม 4 เทิร์น + เทิร์นแรกเพื่อน 70% ไม่โดนเล็งเป้า + ใบ้ Silence 65%
  2. **หน้า 2: `Luffy Wano` (5★, S #7)** — แทงก์รอง HP 1.50M (+50%), ต้นเทิร์นโอกาส 75% กันดาเมจ 2 แอ็กชัน + แจก *Rage Fire* ให้ตัวแบก 2 ตัว (แปะ *Flame* 5% Max HP ลบไม่ได้), เลือดต่ำกว่า 30% เด้ง 300 Rage + กันดาเมจ 5 แอ็กชัน
- **แถวหลัง 4 ตัว (กัน CC 100% ทั้งแถวจาก Boa Lilith):**
  3. **หลัง 1: `Boa Lilith` (6★, T0)** — กัน CC ทั้งแถวหลัง 4 ตัว + เริ่มเกมป่วน *Flower Dance* แถวหน้าศัตรู 2 เทิร์น + ไม้ตายบัฟ ATK ทั้งทีม +40% + *Possessed* ระเบิด 25% Max HP + ฟื้น 75 Rage
  4. **หลัง 2: `Ace & Sabo` (6★ + ซ้ำ 5★, SSS #1)** — เดอะแบก AoE หลัก 3 ฮิตทบต้น + *Soul Burn* ตัด Rage + 4 เทิร์นแรกโดนตีไม่เกิน 10% Max HP
  5. **หลัง 3: `Brook Wano` (5★, S #4)** — ชุบเพื่อน + **แจกอมตะ (Immortal) ทั้งทีม** (ครบ 3 Soul, สูงสุด 3 ครั้ง) + ล้างดีบัฟเทิร์นคู่ + ตีปกติเติม +25 Rage ทั้งทีม + การันตีคริ & แช่แข็งปิด 2 พาสซีฟ (*Enhanced Ice Seal* ลบไม่ได้)
  6. **หลัง 4: `Kaido Hybrid` (5★, S #1)** — ล้างโล่ศัตรูทั้งหมด + ตีปกติแปะ *Divine Power* (ตัดดาเมจเป็น 0) + แปลงร่าง *Dragon God* (SPD +9999)
- **ลำดับการปั้น (1 → 6):** `Ace & Sabo (6★)` → `Boa Lilith (6★)` → `Jinbe Wano` → `Brook Wano` → `Kaido Hybrid` → `Luffy Wano`
- **ตัวสำรองสลับโหมด:** `Whitebeard / หนวดขาว` (5★, S #5) สลับลงแทน `Luffy Wano` ในโหมดตีบอส PvE ที่ต้องการดาเมจ *Shock* 750% ATK ท้ายเทิร์น
