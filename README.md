WRO-2026-Future-Engineers-GZU-team-2
WRO 2026 Future Engineers — Official Technical Documentation
 1. Project Overview & Team Metadata
Team Name:GZU TEAM2
Category: World Robot Olympiad (WRO) Future Engineers 2026
NANES:CHARLOME T MAMIRE ,TATENDA L JEGEDESHE, PETRONELLA MOYO
Age Division or Senior (19–22)]
Affiliation:** GZU UNIVERSITY

---

 2. Vehicle Design & Hardware Architecture
Our Autonomous Mobile Robot (AMR) is designed in accordance with the official WRO Future Engineers dimensional, mechanical, and safety specifications[cite: 6].

Mechanical Conversion & Chassis Specifications
Base Platform:Modified ACEBOTT QD003 chassis platform.
Dimensions:Fits strictly within the maximum allowed boundary of 300{ mm} \X200X mm} X300\{ mm}[cite: 6].
Weight:** Under the $1.5\text{ kg}$ maximum mass limit[cite: 6].
Steering System:** Front-wheel rack-and-pinion/steering linkage controlled by a single proportional servo motor[cite: 6].
* **Drive System:** Single rear axle driven by standard DC gear motors[cite: 6].
* **Compliance Note:** The original 4-wheel independent Mecanum/holonomic drive system has been completely removed to meet the strict single-steering-actuator and single-drive-axle requirement[cite: 6]. No differential drive mechanisms are utilized[cite: 6].

 Electronics & Computing Stack
* **Primary Processor:** ESP32 / Microcontroller board for low-level motor drivers and servo pulse width modulation (PWM).
* **Vision Processor:** Integrated AI Camera / Vision Module for real-time object tracking and lane identification.
* **Sensors:** Ultrasonic / Distance sensors for emergency stopping and obstacle clearance verification.
* **Power Supply:** Rechargeable onboard battery pack compliant with standard voltage limits.

---

## 3. Computer Vision & Software Strategy
The vehicle relies on computer vision algorithms paired with closed-loop steering feedback to navigate the challenge arena autonomously.
